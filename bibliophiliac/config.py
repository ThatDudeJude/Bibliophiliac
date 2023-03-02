from environs import Env

env = Env()
env.read_env()


class Config(object):
    TESTING = False
    DEBUG = False
    INITIALIZE_DB_FILE = "./bibliophiliac/schema.sql"
    BOOKS_CSV = "books.csv"
    AVATARS_FOLDER = "/bibliophiliac/static/imgs/avatars"
    DEFAULT_AVATAR_IMAGE = "/bibliophiliac/static/imgs/default_avatar.png"
    LOG_WITH_GUNICORN = False

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    LOG_WITH_GUNICORN = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = env.str("TEST_DATABASE_URL")
    TEST_DB_FILE = "./tests/dbase_test.sql"
    BOOKS_CSV = "tests/test_books.csv"
    AVATARS_FOLDER = "/tests/profile_avatars/avatars"
    DEFAULT_AVATAR_IMAGE = "/tests/profile_avatars/test_default_avatar.png"
    DEFAULT_TEST_PROFILE_IMAGE_CHANGE = "/tests/test_image.jpg"
