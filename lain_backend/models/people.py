from sqlalchemy import Table, Column, Integer, String, Text

from lain_backend.database import metadata

People = Table(
    "peoples",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("firstname", String(16), nullable=True),
    Column("surname", String(16), nullable=True),
    Column("patronymic", String(16), nullable=True),
    Column("position", String(32), nullable=True),
    Column("description", Text, nullable=True),
)
