import os

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'hello'

class Development(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/parking'

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
