from pydantic import BaseModel, Field
from typing import Optional, List


class CredentialBase(BaseModel):
    login: Optional[str] = Field(None, max_length=64)
    password: Optional[str] = Field(None, max_length=128)
    key: Optional[str] = Field(None, max_length=512)
    description: Optional[str] = None


class CredentialCreate(CredentialBase):
    pass


class CredentialIn(CredentialBase):
    service_ids: Optional[List[int]] = None


class CredentialUpdate(BaseModel):
    login: Optional[str] = Field(None, max_length=64)
    password: Optional[str] = Field(None, max_length=128)
    key: Optional[str] = Field(None, max_length=512)
    description: Optional[str] = None


class CredentialUpdateIn(CredentialUpdate):
    service_ids: Optional[List[int]] = None


class Credential(CredentialBase):
    id: int


class CredentialInnerFilter(BaseModel):
    login: Optional[str] = Field(None, max_length=64)
    password: Optional[str] = Field(None, max_length=128)
    key: Optional[str] = Field(None, max_length=512)


class CredentialOuterFilter(BaseModel):
    service_id: Optional[int] = None


class CredentialFilter(CredentialInnerFilter, CredentialOuterFilter):
    pass
