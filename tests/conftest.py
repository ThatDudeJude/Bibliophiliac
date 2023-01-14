from bibliophiliac import create_app
from bibliophiliac.views.database import initialize_database, access_database
from sqlalchemy import text
import pytest


@pytest.fixture(scope="function")
def app():
    """Create a test app instance and context"""
    app = create_app(testing=True)
    print(app.config)

    with app.app_context():
        initialize_database(testing=True)
        db = access_database()
        file = open(app.config["TEST_DB_FILE"])
        test_sql = text(file.read())
        db.execute(test_sql)
        yield app

    db.execute(
        "DROP TABLE IF EXISTS reviews;DROP TABLE IF EXISTS books;DROP TABLE IF EXISTS users;"
    )
    db.commit()
    db.close()


@pytest.fixture(scope="function")
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Create client to test commands"""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def config(app):
    "Access app config"
    return app.config


class MOCKUSER(object):
    """Define a user-client object that logs in and out during tests"""

    def __init__(self, client):
        self.mock_test_client = client
        self.mock_test_client.post(
            "/register", data={"username": "test two", "password": "1234"}
        )

    def login(self, username="test client", password="1234"):
        return self.mock_test_client.post(
            "/login", data={"username": username, "password": password}
        )

    def register(self, username, password):
        return self.mock_test_client.post(
            "/register", data={"username": username, "password": password}
        )

    def logout(self):
        return self.mock_test_client.get("/logout")


@pytest.fixture(scope="function")
def authenticate(client):
    """Lets test client log in and log out"""
    return MOCKUSER(client)
