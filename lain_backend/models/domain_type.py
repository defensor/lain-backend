from sqlalchemy import Table, Column, Integer, String

from lain_backend.database import metadata

DomainType = Table(
    "domain_types",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(8), unique=True),
)
