from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata

organizations_contacts = Table(
    "organizations_contacts",
    metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="CASCADE")),
)
