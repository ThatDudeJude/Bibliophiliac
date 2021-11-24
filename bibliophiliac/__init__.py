from flask import Flask
# from flask_session import Session
import os

from flask import render_template, redirect, url_for



def create_app(testing=False, production=False):
    """"The application factory that creates the app instance"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    if testing:
        app.config.from_object('config.TestingConfig')
    elif production:
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

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
    app.add_url_rule('/', endpoint='index')

    from .views import search
    app.register_blueprint(search.bp)
    app.add_url_rule('/', endpoint='index')    

    @app.route('/')
    def index():
        return redirect(url_for('books.search'))


    return app