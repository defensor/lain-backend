from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from lain_backend.database import metadata

Contact = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("value", String(32)),
    Column("description", Text, nullable=True),
    Column(
        "type_id",
        Integer,
        ForeignKey("contact_types.id", ondelete="SET NULL"),
        nullable=True,
    ),
)
