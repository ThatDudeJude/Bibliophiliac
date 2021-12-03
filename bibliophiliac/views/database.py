from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask.globals import g, current_app, session
# from flask_session import Session
from flask.cli import with_appcontext
from sqlalchemy import text
import click, csv



def access_database():
    """Access scoped connection to database stored in g.
        If not unavailable, create a connection and store it in g.
    """
    if 'db' not in g:
        engine = create_engine(current_app.config["DATABASE_URL"])
        db = scoped_session(sessionmaker(bind=engine))
        g.db = db

    return g.db

def initialize_database():
    """Initialize database using the file schema.sql"""

    engine = create_engine(current_app.config["DATABASE_URL"])
    file = open(current_app.config["INIT_DB_FILE"])
    sql = text(file.read())
    engine.execute(sql)

    books = current_app.open_resource(current_app.config['BOOKS_CSV'], 'r')
    reader = csv.reader(books)
    next(reader)
    for isbn, title, author, year in reader:
        sql = f"INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)"
        engine.execute(sql, (isbn, title, author, year))



    
def close_db(e=None):
    """Close access to database during request response cleanup"""
    if 'db' in g:
        g.pop('db')                

@click.command("initialize-database")
@with_appcontext
def init_dbase_cmd():
    initialize_database()
    click.echo('DATABASE INITIALIZED')

        