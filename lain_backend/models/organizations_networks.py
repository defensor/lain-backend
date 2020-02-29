from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata

organizations_networks = Table(
    "organizations_networks",
    metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("network_id", Integer, ForeignKey("networks.id", ondelete="CASCADE")),
)
