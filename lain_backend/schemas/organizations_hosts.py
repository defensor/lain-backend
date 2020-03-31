from pydantic import BaseModel


class OrganizationHost(BaseModel):
    organization_id: int
    host_id: int
