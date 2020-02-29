from environs import Env

env = Env()
env.read_env()

ENV = env.str("ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URL = env.str(
    "DATABASE_URL", default="postgresql://lain_user:P%40ssw0rd@localhost:5432/lain_db"
)
