from pydantic import BaseModel, Field
from typing import Optional, List


class BuildingBase(BaseModel):
    addr: str = Field(..., min_length=3, max_length=64)
    name: str = Field(..., min_length=2, max_length=32)
    description: Optional[str] = None


class BuildingCreate(BuildingBase):
    pass


class BuildingIn(BuildingBase):
    organization_ids: List[int]


class BuildingUpdate(BaseModel):
    addr: Optional[str] = Field(None, min_length=3, max_length=64)
    name: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = None


class BuildingUpdateIn(BuildingUpdate):
    organization_ids: List[int] = []


class Building(BaseModel):
    id: int
