from sqlalchemy import Table, Column, Integer, String

from lain.database import metadata

ContactType = Table(
    "contact_types",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(32), unique=True),
)
