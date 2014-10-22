import os
from app import create_app, create_db
from flask.ext.script import Manager

manager = Manager(create_app, with_default_commands=True)
manager.add_option('-x', '--xconfig', dest='config', default='Development')

@manager.command
def initdb(env='Development'):
    # Note: calling this will drop everything in db
    # on production: heroku run python manage.py initdb -e Production
    app = create_app(env)
    create_db(app)

if __name__ == '__main__':
    manager.run()
