from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata

peoples_contacts = Table(
    "peoples_contacts",
    metadata,
    Column("people_id", Integer, ForeignKey("peoples.id", ondelete="CASCADE")),
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="CASCADE")),
)
