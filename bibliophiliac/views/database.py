from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask.globals import g, current_app, session

# from flask_session import Session
from flask.cli import with_appcontext
from sqlalchemy import text
import click, csv, os, glob, shutil

basedir = os.path.abspath(os.path.dirname(__name__))

def update_URI_scheme(url):
    return url.replace("postgres://", "postgresql://", 1)


def access_database():
    """Access database connection to database in g within scoped request context.
    Otherwise create a connection and store it in g for new requests.
    """
    if "db" not in g:
        engine = create_engine(update_URI_scheme(current_app.config["DATABASE_URL"]), pool_pre_ping=True, pool_recycle=600)
        db = scoped_session(sessionmaker(bind=engine))
        g.db = db

    return g.db


def initialize_database(testing=False):
    """Initialize database with the file schema.sql
    and import book information to the books table.
    """

    engine = create_engine(update_URI_scheme(current_app.config["DATABASE_URL"]))
    engine.execute(
        "DROP TABLE IF EXISTS reviews; DROP TABLE IF EXISTS books; DROP TABLE IF EXISTS users"
    )
    file = open(current_app.config["INITIALIZE_DB_FILE"])
    sql_query = text(file.read())
    engine.execute(sql_query)

    if testing:
        books_information = open(
            os.path.join(basedir, current_app.config["BOOKS_CSV"]), "r"
        )
    else:
        books_information = current_app.open_resource(
            current_app.config["BOOKS_CSV"], "r"
        )
    reader = csv.reader(books_information)
    next(reader)  # skip first row
    for isbn, title, author, year in reader:
        sql_query = (
            f"INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)"
        )
        engine.execute(sql_query, (isbn, title, author, year))

    # Delete existing avatar profiles

    avatar_images = glob.glob(
        os.path.join(basedir + current_app.config["AVATARS_FOLDER"], "*")
    )
    for file in avatar_images:
        os.remove(file)
    original = basedir + current_app.config["DEFAULT_AVATAR_IMAGE"]
    destination = basedir + current_app.config["AVATARS_FOLDER"] + "/default_avatar.png"
    shutil.copyfile(original, destination)

    if testing:
        original = basedir + current_app.config["DEFAULT_AVATAR_IMAGE"]
        destination = (
            basedir + current_app.config["AVATARS_FOLDER"] + "/test client.png"
        )
        shutil.copyfile(original, destination)


def close_db(e=None):
    """Close access to database during request-response cleanup"""
    if "db" in g:
        g.pop("db")


@click.command("initialize-database")
@with_appcontext
def init_dbase_cmd():
    initialize_database()
    click.echo("DATABASE INITIALIZED")
