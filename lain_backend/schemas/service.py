from typing import Optional

from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    port: int = Field(..., ge=0, le=65535)
    state: str = Field(..., min_length=1, max_length=16)
    proto3: str = Field(..., min_length=1, max_length=8)
    proto7: Optional[str] = Field(None, max_length=32)
    version: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = Field(None, max_length=512)


class ServiceOut(ServiceBase):
    pass


class ServiceCreate(ServiceBase):
    host_id: Optional[int] = None


class ServiceIn(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    port: Optional[int] = Field(None, ge=0, le=65535)
    proto3: str = Field(None, min_length=1, max_length=8)
    proto7: str = Field(None, min_length=1, max_length=32)
    version: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = Field(None, max_length=512)


class ServiceUpdateIn(ServiceUpdate):
    pass


class Service(ServiceBase):
    id: int
    host_id: int
