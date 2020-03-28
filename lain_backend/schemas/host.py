from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Optional


class HostBase(BaseModel):
    addr: IPvAnyAddress
    os: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = Field(None, max_length=512)
    network_id: int


class HostCreate(HostBase):
    pass


class HostIn(HostBase):
    pass


class HostUpdate(BaseModel):
    addr: Optional[IPvAnyAddress] = None
    os: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = Field(None, max_length=512)


class HostUpdateIn(HostUpdate):
    pass


class Host(HostBase):
    id: int
