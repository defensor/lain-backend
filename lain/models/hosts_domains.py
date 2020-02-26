from sqlalchemy import Table, Column, Integer, ForeignKey

from lain.database import metadata

hosts_domains = Table(
    "hosts_domains",
    metadata,
    Column("host_id", Integer, ForeignKey("hosts.id", ondelete="CASCADE")),
    Column("domain_id", Integer, ForeignKey("domains.id", ondelete="CASCADE")),
)
