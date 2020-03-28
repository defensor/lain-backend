from pydantic import BaseModel


class HostDomain(BaseModel):
    host_id: int
    domain_id: int
