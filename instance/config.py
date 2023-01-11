from environs import Env

env = Env()
env.read_env()

DEBUG= env.bool("DEBUG")
SECRET_KEY = env.str("SECRET_KEY")
BOOKS_API_KEY = env.str("BOOKS_API_KEY")
DATABASE_URL=env.str("DATABASE_URL")
# DATABASE_URL="postgresql://aibzdsyfyztare:053c8a31cc2b6860e8e0de0eeed90fed4906595fb6cd703b8a57bc74ef0bc510@ec2-23-21-229-200.compute-1.amazonaws.com:5432/d8im2d1d2orr32"
SESSION_PERMANENT=env.bool("SESSION_PERMANENT")
# MAX_CONTENT_LENGTH = 7 * 1000 * 1000
# SESSSION_TYPE='filesystem'