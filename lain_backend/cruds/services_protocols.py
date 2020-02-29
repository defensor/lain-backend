__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import services_protocols as model


async def create(db: Database, service_id: int, protocol_id: int) -> None:
    await db.execute(model.insert().values(protocol_id=protocol_id, service_id=service_id))

    return


async def update(db: Database, protocol_ids: List[int], service_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.service_id == service_id, not_(model.c.protocol_id.in_(protocol_ids)),)
        )
    )

    for pid in protocol_ids:
        if not await db.execute(
            model.exists().where(
                and_(model.c.service_id == service_id, model.c.protocol_id == pid,)
            )
        ):
            await db.execute(model.insert().values(service_id=service_id, protocol_id=pid))

    return


async def get_all(
    db: Database, protocol_id: Optional[int] = None, service_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if protocol_id is not None:
        return await db.fetch_all(model.select().where(model.c.protocol_id == protocol_id))
    elif service_id is not None:
        return await db.fetch_all(model.select().where(model.c.service_id == service_id))
    else:
        return await db.fetch_all(model.select().where())
