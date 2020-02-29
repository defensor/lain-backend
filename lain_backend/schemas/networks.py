from pydantic import BaseModel, Field
from typing import Optional, List


class NetworkBase(BaseModel):
    addr: str = Field(
        ...,
        regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\/([1-9]|[1-2][0-9]|3[0-1])$",
    )
    name: str = Field(..., min_length=2, max_length=32)
    description: Optional[str] = None


class NetworkCreate(NetworkBase):
    pass


class NetworkIn(NetworkBase):
    organization_ids: Optional[List[int]] = None


class NetworkUpdate(BaseModel):
    addr: Optional[str] = Field(
        None,
        regex="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\/([1-9]|[1-2][0-9]|3[0-1])$",
    )
    name: Optional[str] = Field(None, min_length=2, max_length=32)
    description: Optional[str] = None


class NetworkUpdateIn(NetworkUpdate):
    organization_ids: Optional[List[int]] = None


class Network(BaseModel):
    id: int
