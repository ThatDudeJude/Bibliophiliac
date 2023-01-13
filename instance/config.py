from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
BOOKS_API_KEY = env.str("BOOKS_API_KEY")
DATABASE_URL = env.str("DATABASE_URL")
SESSION_PERMANENT = env.bool("SESSION_PERMANENT", default=False)
