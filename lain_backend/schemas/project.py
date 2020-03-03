from pydantic import BaseModel, Field
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)


class ProjectCreate(ProjectBase):
    pass


class ProjectIn(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=128)


class ProjectUpdateIn(ProjectUpdate):
    pass


class Project(ProjectBase):
    id: int


class ProjectInnerFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=128)


class ProjectOuterFilter(BaseModel):
    pass


class ProjectFilter(ProjectInnerFilter, ProjectOuterFilter):
    pass
