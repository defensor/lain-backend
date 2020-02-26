from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata


services_credentials = Table(
    "services_credentials",
    metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE")),
    Column("credential_id", Integer, ForeignKey("credentials.id", ondelete="CASCADE")),
)
