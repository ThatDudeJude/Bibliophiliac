from flask import Flask

import os
import logging
from logging.handlers import RotatingFileHandler
from environs import Env
from flask import redirect, url_for
from flask.logging import default_handler

env = Env()
env.read_env()


def create_app(testing=False, production=False):
    """ "The application factory"""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile("config.py")

    if testing:
        app.config.from_object("bibliophiliac.config.TestingConfig")
    elif production:
        app.config.from_object("bibliophiliac.config.ProductionConfig")
    else:
        app.config.from_object("bibliophiliac.config.DevelopmentConfig")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config["LOG_WITH_GUNICORN"]:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler(
            'instance/bibliophiliac.log', 
            maxBytes=16384,
            backupCount=20
        )
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    app.logger.removeHandler(default_handler)
    app.logger.info('Starting the Bibliophiliac App ...')

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
