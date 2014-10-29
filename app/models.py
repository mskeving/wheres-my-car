from app import db

class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    isCurrent = db.Column(db.Boolean)
    streetNumber = db.Column(db.Integer)
    streetName = db.Column(db.String(50))

class StreetCleaning(db.Model):
    __tablename__ = "streetCleaning"

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(10))
    side = db.Column(db.Integer)
    fromhour = db.Column(db.Integer)
    tohour = db.Column(db.Integer)
    holidays = db.Column(db.Boolean)
    week1ofmon = db.Column(db.Boolean)
    week2ofmon = db.Column(db.Boolean)
    week3ofmon = db.Column(db.Boolean)
    week4ofmon = db.Column(db.Boolean)
    week5ofmon = db.Column(db.Boolean)
    street_min = db.Column(db.Integer)
    street_max = db.Column(db.Integer)
    streetname = db.Column(db.String(50))
