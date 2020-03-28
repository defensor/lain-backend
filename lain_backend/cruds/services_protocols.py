__all__ = ["create", "delete", "get_all", "exist"]

from typing import List, Optional
from databases import Database
from sqlalchemy import and_

from lain_backend.models import services_protocols as model
from lain_backend.schemas import ServiceProtocol


async def create(db: Database, service_id: int, protocol_id: int) -> None:
    await db.execute(
        model.insert().values(protocol_id=protocol_id, service_id=service_id)
    )


async def delete(db: Database, service_id: int, protocol_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.protocol_id == protocol_id, model.c.service_id == service_id)
        )
    )


async def get_all(
    db: Database, protocol_id: Optional[int] = None, service_id: Optional[int] = None
) -> List[ServiceProtocol]:
    if protocol_id is not None:
        services_protocols = await db.fetch_all(
            model.select().where(model.c.protocol_id == protocol_id)
        )
    elif service_id is not None:
        services_protocols = await db.fetch_all(
            model.select().where(model.c.service_id == service_id)
        )
    else:
        services_protocols = await db.fetch_all(model.select().where())

    return [
        ServiceProtocol(**service_protocol) for service_protocol in services_protocols
    ]


async def exist(db: Database, protocol_id: int, service_id: int) -> bool:
    return (
        db.fetch_one(
            model.select().where(
                and_(
                    model.c.protocol_id == protocol_id, model.c.service_id == service_id
                )
            )
        )
    ) is not None
