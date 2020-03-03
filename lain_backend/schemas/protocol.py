from pydantic import BaseModel, Field
from typing import Optional


class ProtocolBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=32)


class ProtocolCreate(ProtocolBase):
    pass


class ProtocolIn(ProtocolBase):
    pass


class ProtocolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=32)


class ProtocolUpdateIn(ProtocolUpdate):
    pass


class Protocol(ProtocolBase):
    id: int


class ProtocolInnerFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=32)


class ProtocolOuterFilter(BaseModel):
    service_id: Optional[int] = None


class ProtocolFilter(ProtocolInnerFilter, ProtocolOuterFilter):
    pass
