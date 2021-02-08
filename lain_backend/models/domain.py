from sqlalchemy import Table, Column, Integer, String

from lain_backend.database import metadata

Domain = Table(
    "domains",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(64), unique=True),
    Column("description", String(512), nullable=True),
    Column("record", String(32)),
)
