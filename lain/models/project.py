from sqlalchemy import Table, Column, Integer, String

from lain.database import metadata

Project = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(128), unique=True),
)
