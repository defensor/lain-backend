from pydantic import BaseModel


class ServiceProtocol(BaseModel):
    service_id: int
    protocol_id: int
