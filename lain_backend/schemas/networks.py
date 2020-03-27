from pydantic import BaseModel, Field, IPvAnyNetwork
from typing import Optional


class NetworkBase(BaseModel):
    addr: IPvAnyNetwork
    name: str = Field(..., min_length=2, max_length=32)
    description: Optional[str] = Field(..., max_length=512)


class NetworkCreate(NetworkBase):
    pass


class NetworkIn(NetworkBase):
    pass


class NetworkUpdate(BaseModel):
    addr: Optional[IPvAnyNetwork] = None
    name: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = Field(None, max_length=512)


class NetworkUpdateIn(NetworkUpdate):
    pass


class Network(NetworkBase):
    id: int


class NetworkInnerFilter(BaseModel):
    addr: Optional[IPvAnyNetwork] = None
    name: Optional[str] = Field(None, min_length=2, max_length=32)


class NetworkOuterFilter(BaseModel):
    organization_id: Optional[int] = None
    vulnerability_id: Optional[int] = None


class NetworkFilter(NetworkInnerFilter, NetworkOuterFilter):
    pass
