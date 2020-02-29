from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata


services_protocols = Table(
    "services_protocols",
    metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE")),
    Column("protocol_id", Integer, ForeignKey("protocols.id", ondelete="CASCADE")),
)
