from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask.globals import g, current_app, session
# from flask_session import Session
from flask.cli import with_appcontext
from sqlalchemy import text
import click, csv



def access_database():
    """Access database connection to database in g within scoped request context.
        Otherwise create a connection and store it in g for new requests.
    """
    if 'db' not in g:
        engine = create_engine(current_app.config["DATABASE_URL"])
        db = scoped_session(sessionmaker(bind=engine))
        g.db = db

    return g.db

def initialize_database():
    """Initialize database with the file schema.sql
        and import book information to the books table.
    """

    engine = create_engine(current_app.config["DATABASE_URL"])
    engine.execute("DROP TABLE IF EXISTS reviews; DROP TABLE IF EXISTS books; DROP TABLE IF EXISTS users")
    file = open(current_app.config["INITIALIZE_DB_FILE"])
    sql_query = text(file.read())
    engine.execute(sql_query)

    books_information = current_app.open_resource(current_app.config['BOOKS_CSV'], 'r')
    reader = csv.reader(books_information)
    next(reader)  # skip first row
    for isbn, title, author, year in reader:
        sql_query = f"INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)"
        engine.execute(sql_query, (isbn, title, author, year))


    
def close_db(e=None):
    """Close access to database during request-response cleanup"""
    if 'db' in g:
        g.pop('db')                

@click.command("initialize-database")
@with_appcontext
def init_dbase_cmd():
    initialize_database()
    click.echo('DATABASE INITIALIZED')

        