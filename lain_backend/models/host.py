from lain_backend.database import metadata
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy_utils import IPAddressType

Host = Table(
    "hosts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("addr", IPAddressType),
    Column("os", String, nullable=True),
    Column("description", String(512), nullable=True),
)
