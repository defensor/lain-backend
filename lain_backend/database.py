import databases
import sqlalchemy

from lain_backend.config import SQLALCHEMY_DATABASE_URL

metadata = sqlalchemy.MetaData()

database = databases.Database(SQLALCHEMY_DATABASE_URL)
