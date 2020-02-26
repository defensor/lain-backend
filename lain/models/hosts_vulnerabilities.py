from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata


hosts_vulnerabilities = Table(
    "hosts_vulnerabilities",
    metadata,
    Column("host_id", Integer, ForeignKey("hosts.id", ondelete="CASCADE")),
    Column(
        "vulnerability_id",
        Integer,
        ForeignKey("vulnerabilities.id", ondelete="CASCADE"),
    ),
)
