from pydantic import BaseModel, Field
from typing import Optional


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    description: Optional[str] = None
    project_id: int


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationIn(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    description: Optional[str] = None
    project_id: Optional[int] = None


class OrganizationUpdateIn(OrganizationUpdate):
    pass


class Organization(OrganizationBase):
    id: int


class OrganizationInnerFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=64)
    project_id: Optional[int] = None


class OrganizationOuterFilter(BaseModel):
    network_id: Optional[int] = None
    people_id: Optional[int] = None
    building_id: Optional[int] = None
    contact_id: Optional[int] = None


class OrganizationFilter(OrganizationInnerFilter, OrganizationOuterFilter):
    pass
