from pydantic import BaseModel, Field
from typing import Optional


class HostBase(BaseModel):
    addr: str = Field(
        ...,
        regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
    )
    os: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = None
    network_id: int


class HostCreate(HostBase):
    pass


class HostIn(HostBase):
    pass


class HostUpdate(BaseModel):
    addr: Optional[str] = Field(
        None,
        regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
    )
    os: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = None
    network_id: Optional[int] = None


class HostUpdateIn(HostUpdate):
    pass


class Host(BaseModel):
    id: int
