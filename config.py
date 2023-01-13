from environs import Env

from instance.config import DEBUG

env = Env()
env.read_env()


class Config(object):
    TESTING = False
    DEBUG = False
    INITIALIZE_DB_FILE = "./bibliophiliac/schema.sql"
    BOOKS_CSV = "books.csv"
    AVATARS_FOLDER = "/bibliophiliac/static/imgs/avatars"
    DEFAULT_AVATAR_IMAGE = "/bibliophiliac/static/imgs/default_avatar.png"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = env.str("TEST_DATABASE_URL")
    TEST_DB_FILE = "./tests/dbase_test.sql"
    BOOKS_CSV = "tests/test_books.csv"
