from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata

peoples_vulnerabilities = Table(
    "peoples_vulnerabilities",
    metadata,
    Column("people_id", Integer, ForeignKey("peoples.id", ondelete="CASCADE")),
    Column(
        "vulnerability_id",
        Integer,
        ForeignKey("vulnerabilities.id", ondelete="CASCADE"),
    ),
)
