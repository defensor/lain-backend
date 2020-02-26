from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata

organizations_buildings = Table(
    "organizations_buildings ",
    metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("building_id", Integer, ForeignKey("buildings.id", ondelete="CASCADE")),
)
