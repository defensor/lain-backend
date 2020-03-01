from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from lain_backend.database import metadata

Organization = Table(
    "organizations",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(64), unique=True),
    Column("description", Text, nullable=True),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="CASCADE")),
)
