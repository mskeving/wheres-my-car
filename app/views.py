import re

from flask import render_template, request
from datetime import datetime
from app import app, db
from models import StreetCleaning, Location

@app.route('/')
def index():
    current_location = Location.query.filter_by(isCurrent=True).first()
    street_num = int(current_location.streetNumber)
    street_name = current_location.streetName

    street_cleanings = StreetCleaning.query.filter_by(streetname=street_name).all()

    relevant_cleanings = []
    for street_cleaning in street_cleanings:
        # if street_num odd -> left side of street, even -> right
        # even numbered addresses on 0 side, odd addresses on 1
        if street_num % 2 == 0:
            if (street_num >= street_cleaning.street_min and street_num <= street_cleaning.street_max
                and street_cleaning.side == 0):
                relevant_cleanings.append(street_cleaning)
        else:
            if (street_num >= street_cleaning.street_min and street_num <= street_cleaning.street_max
                and street_cleaning.side == 1):
                relevant_cleanings.append(street_cleaning)

    return render_template('index.html',
                            current_location=current_location,
                            cleanings=relevant_cleanings,
                            )

@app.route('/park')
def park():
    return render_template('new_location.html')

@app.route('/new-location', methods=['POST'])
def submit_location():
    # Get address
    street_num = request.form.get('streetNum')
    street_name = request.form.get('streetName')

    # Format Address
    street_num, street_name = format_address(street_num, street_name)

    # Remove previous location and submit new
    previous_location = Location.query.filter_by(isCurrent=True).first()
    previous_location.isCurrent=False

    new_location = Location(isCurrent=True, streetNumber=street_num, streetName=street_name)
    new_location.time = datetime.utcnow()
    db.session.add(new_location)
    db.session.commit()

    return 'success'

def format_address(street_num, street_name):
    # change street > st etc. potential problem strees: mission bay blvd nor/sou, the embarcadero
    # street_num to numeric. Not 901-933 or 531A

    street_abbr_dict = {
        'street': 'st',
        'avenue': 'ave',
        'boulevard': 'blvd',
        'lane': 'ln',
        'court': 'ct',
        'drive': 'dr',
        'terrave': 'ter',
        'tunnel': 'tunl'
    }

    # convert street generics to abbreviations from dict
    # http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
    pattern = re.compile(r'\b(' + '|'.join(street_abbr_dict.keys()) + r')\b')
    street_name = pattern.sub(lambda x: street_abbr_dict[x.group()], street_name.lower()).upper()

    # http://stackoverflow.com/questions/13518874/python-regex-get-end-digits-from-a-string
    street_num = re.match('.*?([0-9]+)', street_num).group(0)

    return street_num, street_name
