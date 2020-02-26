from pydantic import BaseModel, Field
from typing import Optional, List


class PeopleBase(BaseModel):
    firstname: Optional[str] = Field(None, min_length=2, max_length=16)
    surname: Optional[str] = Field(None, min_length=2, max_length=16)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=16)
    position: Optional[str] = Field(None, min_len=2, max_length=32)
    description: Optional[str] = None


class PeopleCreate(PeopleBase):
    pass


class PeopleIn(PeopleBase):
    organization_ids: List[int]


class PeopleUpdate(BaseModel):
    firstname: Optional[str] = Field(None, min_length=2, max_length=16)
    surname: Optional[str] = Field(None, min_length=2, max_length=16)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=16)
    position: Optional[str] = Field(None, min_len=2, max_length=32)
    description: Optional[str] = None


class PeopleUpdateIn(PeopleUpdate):
    organization_ids: List[int] = []


class People(BaseModel):
    id: int
