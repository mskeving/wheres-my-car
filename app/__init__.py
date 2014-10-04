from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/parking' 
db = SQLAlchemy(app)

from app import model, views
