from pydantic import BaseModel, Field
from typing import Optional


class DomainTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=8)


class DomainTypeCreate(DomainTypeBase):
    pass


class DomainTypeIn(DomainTypeBase):
    pass


class DomainTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=8)


class DomainTypeUpdateIn(DomainTypeUpdate):
    pass


class DomainType(DomainTypeBase):
    id: int


class DomainTypeInnerFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=8)


class DomainTypeOuterFilter(BaseModel):
    pass


class DomainTypeFilter(DomainTypeInnerFilter, DomainTypeOuterFilter):
    pass
