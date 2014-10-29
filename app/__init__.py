from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder='static/templates')
db = SQLAlchemy()

def create_app(config):
    app.config.from_object('config.flask.' + config)
    db.init_app(app)
    return app

def create_db(app):
    from app.models import Location, StreetCleaning

    db.init_app(app)
    db.drop_all()
    db.create_all()

    # add default first location when setting up db
    location = Location(isCurrent=True, streetNumber=531, streetName='FILLMORE ST')
    location.time = datetime.utcnow()
    db.session.add(location)

    # add street cleaning data
    from app.data import populate
    populate.add_street_cleaning_data()
    populate.prune_data()

    db.session.commit

from app import models, views
