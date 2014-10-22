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
    cnn = db.Column(db.Integer)
    weekday = db.Column(db.String(10))
    blockside = db.Column(db.String(10))
    blocksweep = db.Column(db.String(10))
    cnnrightle = db.Column(db.String(10))
    corridor = db.Column(db.String(50))
    fromhour = db.Column(db.Integer)
    tohour = db.Column(db.Integer)
    holidays = db.Column(db.Boolean)
    week1ofmon = db.Column(db.Boolean)
    week2ofmon = db.Column(db.Boolean)
    week3ofmon = db.Column(db.Boolean)
    week4ofmon = db.Column(db.Boolean)
    week5ofmon = db.Column(db.Boolean)
    lf_fadd = db.Column(db.String(10))
    lf_toadd = db.Column(db.String(10))
    rt_toadd = db.Column(db.String(10))
    rt_fadd = db.Column(db.String(10))
    streetname = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    nhood = db.Column(db.String(50))
    district = db.Column(db.String(50))
