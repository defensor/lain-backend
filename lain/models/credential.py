from sqlalchemy import Table, Column, Integer, String, Text

from lain.database import metadata

Credential = Table(
    "credentials",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("login", String(64), nullable=True),
    Column("password", String(128), nullable=True),
    Column("key", String(512), nullable=True),
    Column("description", Text, nullable=True),
)
