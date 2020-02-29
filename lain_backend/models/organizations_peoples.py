from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata

organizations_peoples = Table(
    "organizations_peoples",
    metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("people_id", Integer, ForeignKey("peoples.id", ondelete="CASCADE")),
)
