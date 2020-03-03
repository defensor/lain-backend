from pydantic import BaseModel, Field
from typing import Optional, List


class ServiceBase(BaseModel):
    port: int = Field(..., ge=0, le=65535)
    name: str = Field(..., min_length=3, max_length=64)
    version: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = None
    host_id: int


class ServiceCreate(ServiceBase):
    pass


class ServiceIn(ServiceBase):
    protocol_ids: Optional[List[int]] = None


class ServiceUpdate(BaseModel):
    port: Optional[int] = Field(None, ge=0, le=65535)
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    version: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = None
    host_id: Optional[int] = None


class ServiceUpdateIn(ServiceUpdate):
    protocol_ids: Optional[List[int]] = None


class Service(ServiceBase):
    id: int


class ServiceInnerFilter(BaseModel):
    port: Optional[int] = Field(None, ge=0, le=65535)
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    version: Optional[str] = Field(None, max_length=64)
    host_id: Optional[int] = None


class ServiceOuterFilter(BaseModel):
    protocol_id: Optional[int] = None
    vulnerability_id: Optional[int] = None
    credential_id: Optional[int] = None


class ServiceFilter(ServiceInnerFilter, ServiceOuterFilter):
    pass
