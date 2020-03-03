from pydantic import BaseModel, Field
from typing import Optional, List


class DomainBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    description: Optional[str] = None
    type_id: Optional[int] = None


class DomainCreate(DomainBase):
    pass


class DomainIn(DomainBase):
    host_ids: Optional[List[int]] = None


class DomainUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    description: Optional[str] = None
    type_id: Optional[int] = None


class DomainUpdateIn(DomainUpdate):
    host_ids: Optional[List[int]] = None


class Domain(DomainBase):
    id: int


class DomainInnerFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    type_id: Optional[int] = None


class DomainOuterFilter(BaseModel):
    host_id: Optional[int] = None


class DomainFilter(DomainInnerFilter, DomainOuterFilter):
    pass
