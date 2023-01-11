from flask import Flask
# from flask_session import Session
import os

from flask import redirect, url_for



def create_app(testing=False, production=False):
    """"The application factory"""
    if not production:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_pyfile("config.py")
    else:
        app = Flask(__name__)        
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
        app.config['SESSION_PERMANENT'] = os.getenv('SESSION_PERMANENT')
        app.config['BOOKS_API_KEY'] = os.getenv('BOOKS_API_KEY')
    
    if testing:
        app.config.from_object('config.TestingConfig')
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

    from .views import search_and_reviews
    app.register_blueprint(search_and_reviews.bp)
    app.add_url_rule('/', endpoint='index')    

    from .views import profiles
    app.register_blueprint(profiles.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def index():
        return redirect(url_for('books.search_for_book'))


    return app