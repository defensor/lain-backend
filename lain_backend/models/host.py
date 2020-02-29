from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from lain_backend.database import metadata

Host = Table(
    "hosts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("addr", String(15)),
    Column("os", String(32), nullable=True),
    Column("description", Text, nullable=True),
    Column("network_id", Integer, ForeignKey("networks.id", ondelete="CASCADE")),
)
