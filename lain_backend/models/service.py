from sqlalchemy import Table, Column, Integer, String, Text

from lain_backend.database import metadata

Service = Table(
    "services",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("port", Integer),
    Column("name", String(64)),
    Column("version", String(64), nullable=True),
    Column("description", Text, nullable=True),
)
