import re

from flask import render_template, request
from datetime import datetime
from app import app, db
from models import StreetCleaning, Location

@app.route('/')
def index():
    # note: change street > st, avenue > ave, Boulevard > blvd, lane > ln, court > ct,
    # drive > dr, terrace > ter, tunnel > tunl
    # potential problem strees: mission bay blvd nor/sou, the embarcadero
    current_location = Location.query.filter_by(isCurrent=True).first()
    street_num = int(current_location.streetNumber)
    street_name = current_location.streetName

    street_abbr_dict = {
        'street': 'St',
        'avenue': 'Ave',
        'boulevard': 'Blvd',
        'lane': 'Ln',
        'court': 'Ct',
        'drive': 'Dr',
        'terrave': 'Ter',
        'tunnel': 'Tunl'
    }

    # convert street generics to abbreviations from dict
    # http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
    pattern = re.compile(r'\b(' + '|'.join(street_abbr_dict.keys()) + r')\b')
    street_name = pattern.sub(lambda x: street_abbr_dict[x.group()], street_name.lower()).upper()

    street_cleanings = StreetCleaning.query.filter_by(streetname=street_name).all()

    relevant_cleanings = []
    for street_cleaning in street_cleanings:
        # if street_num odd -> left side of street, even -> right
        # left and right cleanings denoted in cnnrightle column
        if street_num % 2 == 0:
            if (street_num > int(street_cleaning.rt_fadd) and street_num < int(street_cleaning.rt_toadd)
                and street_cleaning.cnnrightle == 'R'):
                relevant_cleanings.append(street_cleaning)
        else:
            if (street_num > int(street_cleaning.lf_fadd) and street_num < int(street_cleaning.lf_toadd)
                and street_cleaning.cnnrightle == 'L'):
                relevant_cleanings.append(street_cleaning)

    print relevant_cleanings
    return render_template('index.html',
                            current_location=current_location,
                            cleanings=relevant_cleanings,
                            )

@app.route('/new-location', methods=['POST'])
def submit_location():
    # remove previous location
    previous_location = Location.query.filter_by(isCurrent=True).first()
    previous_location.isCurrent=False

    # submit new location
    form = request.form
    street_num = form.get('streetNum')
    street_name = form.get('streetName')
    new_location = Location(isCurrent=True, streetNumber=street_num, streetName=street_name)
    new_location.time = datetime.utcnow()
    db.session.add(new_location)
    db.session.commit()

    #TODO what to return here?
    return 'success'

@app.route('/park')
def park():
    return render_template('new_location.html')
