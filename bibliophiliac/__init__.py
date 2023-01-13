from flask import Flask

# from flask_session import Session
import os
from environs import Env
from flask import redirect, url_for

env = Env()
env.read_env()


def create_app(testing=False, production=False):
    """ "The application factory"""

    app = Flask(__name__)
    app.config["SECRET_KEY"] = env.str("SECRET_KEY")
    app.config["DATABASE_URL"] = env.str("DATABASE_URL")
    app.config["SESSION_PERMANENT"] = env.bool("SESSION_PERMANENT", default=False)
    app.config["BOOKS_API_KEY"] = env.str("BOOKS_API_KEY")

    if testing:
        app.config.from_object("config.TestingConfig")
    elif production:
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Session(app)

    from .views import database

    app.cli.add_command(database.init_dbase_cmd)
    app.teardown_appcontext(database.close_db)

    from .views import authentication

    app.register_blueprint(authentication.bp)
    app.add_url_rule("/", endpoint="index")

    from .views import search_and_reviews

    app.register_blueprint(search_and_reviews.bp)
    app.add_url_rule("/", endpoint="index")

    from .views import profiles

    app.register_blueprint(profiles.bp)
    app.add_url_rule("/", endpoint="index")

    @app.route("/")
    def index():
        return redirect(url_for("books.search_for_book"))

    return app
