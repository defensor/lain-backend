from lain_backend.database import metadata
from sqlalchemy import Column, ForeignKey, Integer, String, Table

Service = Table(
    "services",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("port", Integer),
    Column("state", String(16)),
    Column("proto3", String(8)),
    Column("proto7", String(32), nullable=True),
    Column("version", String(64), nullable=True),
    Column("description", String(512), nullable=True),
    Column("host_id", Integer, ForeignKey("hosts.id", ondelete="CASCADE")),
)
