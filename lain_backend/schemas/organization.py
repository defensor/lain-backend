from pydantic import BaseModel, Field
from typing import Optional


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    description: Optional[str] = Field(None, max_length=512)
    project_id: int


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationIn(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    description: Optional[str] = Field(None, max_length=512)


class OrganizationUpdateIn(OrganizationUpdate):
    pass


class Organization(OrganizationBase):
    id: int
