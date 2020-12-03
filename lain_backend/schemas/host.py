from typing import Optional

from pydantic import BaseModel, Field, IPvAnyAddress


class HostBase(BaseModel):
    addr: IPvAnyAddress
    os: Optional[str] = None
    description: Optional[str] = Field(None, max_length=512)


class HostOut(HostBase):
    pass


class HostCreate(HostBase):
    pass


class HostIn(HostBase):
    pass


class HostUpdate(BaseModel):
    addr: Optional[IPvAnyAddress] = None
    os: Optional[str] = None
    description: Optional[str] = Field(None, max_length=512)


class HostUpdateIn(HostUpdate):
    pass


class Host(HostBase):
    id: int
