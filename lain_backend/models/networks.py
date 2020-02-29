from sqlalchemy import Table, Column, Integer, String, Text

from lain_backend.database import metadata

Network = Table(
    "networks",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("addr", String(18)),
    Column("name", String(32)),
    Column("description", Text, nullable=True),
)
