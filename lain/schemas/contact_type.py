from pydantic import BaseModel, Field
from typing import Optional


class ContactTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)


class ContactTypeCreate(ContactTypeBase):
    pass


class ContactTypeIn(ContactTypeBase):
    pass


class ContactTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=32)


class ContactTypeUpdateIn(ContactTypeUpdate):
    pass


class ContactType(BaseModel):
    id: int
