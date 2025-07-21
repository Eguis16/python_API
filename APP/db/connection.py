import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instruccion

# Conexión a la base de datos
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host =current_app.config['DB_HOST'],
            user =current_app.config['DB_USER'],
            password =current_app.config['DB_PASSWORD'],
            db =current_app.config['DB'],
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

# Cierre de base de datos
def Close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for i in instruccion:
        c.execute(i)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_commit():
    init_db()
    click.echo('Base de datos iniciada')

def init_app(app):
    app.teardown_appcontext(Close_db)
    app.cli.add_command(init_db_commit)