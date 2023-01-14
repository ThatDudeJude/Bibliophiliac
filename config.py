from environs import Env

from instance.config import DEBUG

env = Env()
env.read_env()


class Config(object):
    DEBUG = env.bool("DEBUG", default=False)
    SECRET_KEY = env.str("SECRET_KEY")
    BOOKS_API_KEY = env.str("BOOKS_API_KEY")
    DATABASE_URL = env.str("DATABASE_URL")
    SESSION_PERMANENT = env.bool("SESSION_PERMANENT", default=False)
    TESTING = False
    DEBUG = False
    INITIALIZE_DB_FILE = "./bibliophiliac/schema.sql"
    BOOKS_CSV = "books.csv"
    AVATARS_FOLDER = "/bibliophiliac/static/imgs/avatars"
    DEFAULT_AVATAR_IMAGE = "/bibliophiliac/static/imgs/default_avatar.png"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = env.str("TEST_DATABASE_URL")
    TEST_DB_FILE = "./tests/dbase_test.sql"
    BOOKS_CSV = "tests/test_books.csv"
    AVATARS_FOLDER = "/tests/profile_avatars/avatars"
    DEFAULT_AVATAR_IMAGE = "/tests/profile_avatars/test_default_avatar.png"
    DEFAULT_TEST_PROFILE_IMAGE_CHANGE = "/tests/test_image.jpg"
