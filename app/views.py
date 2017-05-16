import re, json

from sqlalchemy import and_
from flask import render_template, request
from datetime import datetime
from app import app, db
from models import StreetCleaning, Location

@app.route('/')
def index():
    current_location = Location.query.filter_by(isCurrent=True).first()
    street_num = int(current_location.streetNumber)
    street_name = current_location.streetName

    return render_template('index.html',
                            current_location=current_location,
                            cleanings=get_cleanings(street_num, street_name),
                            )

@app.route('/lookup', methods=['POST'])
def lookup():
    street_num, street_name = format_address(request.form.get('streetNum'),
        request.form.get('streetName'))

    cleanings = get_cleanings(street_num, street_name)

    content = "<div class='cleaning-content'>"
    if len(cleanings) > 0:
        for c in cleanings:
            content += "<div class='cleaning'>" \
                + c.weekday + ' ' + str(c.fromhour) + ' - ' + str(c.tohour) \
                + "</div>"
    else:
        content += "<div class='cleaning'>No Cleaning Found</div>"
    content += "</div>"

    return json.dumps(content)

@app.route('/new-location', methods=['POST'])
def submit_location():
    """
    Endpoint to update current location of car. Once
    location is updated, returns list of street cleanings
    for that location.
    """
    street_num = request.form.get('streetNum')
    street_name = request.form.get('streetName')

    # Add new current location
    street_num, street_name = format_address(street_num, street_name)
    db.session.add(Location(isCurrent=True,
                            streetNumber=street_num,
                            streetName=street_name,
                            time=datetime.utcnow()))

    # Remove previous location
    previous_location = Location.query.filter_by(isCurrent=True).first()
    previous_location.isCurrent = False
    db.session.add(previous_location)

    db.session.commit()

    # Get street cleaning schedule for new location
    cleaning_list = []
    for cleaning in get_cleanings(street_num, street_name):
        cleaning_list.append({
            'weekday': cleaning.weekday,
            'fromhour': cleaning.fromhour,
            'tohour': cleaning.tohour
        })
    return json.dumps(cleaning_list)

def get_cleanings(street_num, street_name):
    return StreetCleaning.query.filter(
        and_(StreetCleaning.streetname==street_name,
        StreetCleaning.street_min<=street_num,
        StreetCleaning.street_max>=street_num,
        StreetCleaning.side==street_num%2)
    ).all()

def format_address(street_num, street_name):
    # change street > st etc. potential problem streets: mission bay blvd nor/sou, the embarcadero
    # street_num to numeric. Not 901-933 or 531A

    street_abbr_dict = {
        'street': 'st',
        'avenue': 'ave',
        'boulevard': 'blvd',
        'lane': 'ln',
        'court': 'ct',
        'drive': 'dr',
        'terrace': 'ter',
        'tunnel': 'tunl'
    }

    # convert street generics to abbreviations from dict
    # http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
    pattern = re.compile(r'\b(' + '|'.join(street_abbr_dict.keys()) + r')\b')
    street_name = pattern.sub(lambda x: street_abbr_dict[x.group()], street_name.lower()).upper()

    # http://stackoverflow.com/questions/13518874/python-regex-get-end-digits-from-a-string
    street_num = int(re.match('.*?([0-9]+)', street_num).group(0))

    return street_num, street_name
