from sqlalchemy import Table, Column, Integer, ForeignKey

from lain_backend.database import metadata


services_vulnerabilities = Table(
    "services_vulnerabilities",
    metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE")),
    Column(
        "vulnerability_id",
        Integer,
        ForeignKey("vulnerabilities.id", ondelete="CASCADE"),
    ),
)
