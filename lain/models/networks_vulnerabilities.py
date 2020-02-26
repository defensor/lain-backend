from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata

networks_vulnerabilities = Table(
    "networks_vulnerabilities",
    metadata,
    Column("network_id", Integer, ForeignKey("networks.id", ondelete="CASCADE")),
    Column(
        "vulnerability_id",
        Integer,
        ForeignKey("vulnerabilities.id", ondelete="CASCADE"),
    ),
)
