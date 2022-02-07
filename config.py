from instance.config import BOOKS_CSV


class Config(object):
    TESTING=False 
    DEBUG=False 
    INITIALIZE_DB_FILE='/bibliophiliac/schema.sql'

class ProductionConfig(Config):
    pass 

class DevelopmentConfig(Config):
    DEBUG=True

class TestingConfig(Config):
    TESTING=True 
    DEBUG=True 
    DATABASE_URL="postgresql:///test_bibliophiliac"
    TEST_DB_FILE='/tests/dbase_test.sql'
    BOOKS_CSV='/tests/test_books.csv'