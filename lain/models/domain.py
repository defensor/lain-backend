from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from lain.database import metadata

Domain = Table(
    "domains",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(64), unique=True),
    Column("description", Text, nullable=True),
    Column(
        "type_id",
        Integer,
        ForeignKey("domain_types.id", ondelete="SET NULL"),
        nullable=True,
    ),
)
