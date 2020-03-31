from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata

organizations_hosts = Table(
    "organizations_hosts",
    metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("host_id", Integer, ForeignKey("hosts.id", ondelete="CASCADE")),
)
