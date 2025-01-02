import _mysql_connector
from flask import current_app, g
import click
from flask.cli import with_appcontext
from .schema import Instructions

def get_db():
    if 'db' not in g:
        g.db = _mysql_connector.connect(
            host = current_app.config['DB_HOST'],
            user= current_app.config['DB_USER'],
            password = current_app.config['DB_PASSWORD'],
            database = current_app.config['DB']
        )
        g.c = g.db.Cursor(dictionary=True)
    
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)

