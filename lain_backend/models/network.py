from sqlalchemy import Table, Column, Integer, String
from sqlalchemy_utils import IPAddressType

from lain_backend.database import metadata

Network = Table(
    "networks",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("addr", IPAddressType),
    Column("name", String(32)),
    Column("description", String(512), nullable=True),
)
