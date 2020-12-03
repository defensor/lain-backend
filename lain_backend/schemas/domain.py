from typing import Optional

from pydantic import BaseModel, Field


class DomainBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    record: str = Field("A", min_length=1, max_length=32)
    description: Optional[str] = None


class DomainOut(DomainBase):
    pass


class DomainCreate(DomainBase):
    pass


class DomainIn(DomainBase):
    pass


class DomainUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    record: Optional[str] = Field(None, min_length=1, max_length=32)
    description: Optional[str] = None


class DomainUpdateIn(DomainUpdate):
    pass


class Domain(DomainBase):
    id: int
