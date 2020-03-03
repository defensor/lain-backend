from pydantic import BaseModel, Field
from typing import Optional, List


class ContactBase(BaseModel):
    value: str = Field(..., min_length=4, max_length=32)
    description: Optional[str] = None
    type_id: Optional[int] = None


class ContactCreate(ContactBase):
    pass


class ContactIn(ContactBase):
    organization_ids: Optional[List[int]] = None
    people_ids: Optional[List[int]] = None


class ContactUpdate(BaseModel):
    value: Optional[str] = Field(None, min_length=4, max_length=32)
    description: Optional[str] = None
    type_id: Optional[int] = None


class ContactUpdateIn(ContactUpdate):
    organization_ids: Optional[List[int]] = None
    people_ids: Optional[List[int]] = None


class Contact(ContactBase):
    id: int


class ContactInnerFilter(BaseModel):
    value: Optional[str] = Field(None, min_length=4, max_length=32)
    type_id: Optional[int] = None


class ContactOuterFilter(BaseModel):
    organization_id: Optional[int] = None
    people_id: Optional[int] = None


class ContactFilter(ContactInnerFilter, ContactOuterFilter):
    pass
