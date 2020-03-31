from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy_utils import IPAddressType

from lain_backend.database import metadata

Host = Table(
    "hosts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("addr", IPAddressType),
    Column("os", String(32), nullable=True),
    Column("description", String(512), nullable=True),
)
