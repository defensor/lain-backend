from pydantic import BaseModel


class OrganizationNetwork(BaseModel):
    organization_id: int
    network_id: int
