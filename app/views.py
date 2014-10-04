from flask import render_template, request
from app import app, db
from model import StreetCleaning, Location

@app.route('/')
def index():
    current_location = Location.query.filter_by(isCurrent=True).first()
    street_num = current_location.streetNumber
    street_cleanings = StreetCleaning.query.filter_by(streetname=current_location.streetName).all()

    relevant_cleanings = []
    for street_cleaning in street_cleanings:
        # if street_num odd -> left side of street, even -> right
        if street_num % 2 == 0:
            if street_num > int(street_cleaning.rt_fadd) and street_num < int(street_cleaning.rt_toadd):
                relevant_cleanings.append(street_cleaning)
        else:
            if street_num > int(street_cleaning.lf_fadd) and street_num < int(street_cleaning.lf_toadd):
                relevant_cleanings.append(street_cleaning)

    return render_template('index.html',
                            current_location=current_location,
                            cleanings=relevant_cleanings,
                            )

@app.route('/new-location', methods=['POST'])
def submit_location():
    # remove previous location
    previous_location = Location.query.filter_by(isCurrent=True).first()
    previous_location.isCurrent=False
    db.session.commit()

    # submit new location
    form = request.form
    street_num = form.get('streetNum')
    street_name = form.get('streetName')
    new_location = Location(isCurrent=True, streetNumber=street_num, streetName=street_name)
    db.session.add(new_location)
    db.session.commit()

    #TODO what to return here?
    return 'success'

@app.route('/park')
def park():
    return render_template('new_location.html')
