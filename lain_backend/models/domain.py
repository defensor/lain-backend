from sqlalchemy import Table, Column, Integer, String, ForeignKey

from lain_backend.database import metadata

Domain = Table(
    "domains",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(64), unique=True),
    Column("description", String(512), nullable=True),
    Column(
        "type_id",
        Integer,
        ForeignKey("domain_types.id", ondelete="SET NULL"),
        nullable=True,
    ),
)
