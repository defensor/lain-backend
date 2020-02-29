__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Protocol as model
from lain_backend.schemas import (
    ProtocolCreate,
    ProtocolIn,
    ProtocolUpdate,
    ProtocolUpdateIn,
)


async def create(db: Database, protocol: ProtocolIn) -> Optional[Mapping[Any, Any]]:
    protocol_create = ProtocolCreate(**protocol.dict())

    protocol_id = await db.execute(model.insert().values(**protocol_create.dict()))

    return await get(db=db, protocol_id=protocol_id)


async def get(db: Database, protocol_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == protocol_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100
) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, protocol_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == protocol_id))

    return


async def update(
    db: Database, protocol: ProtocolUpdateIn, protocol_id: int
) -> Optional[Mapping[Any, Any]]:
    protocol_update = ProtocolUpdate(**protocol.dict())

    await db.execute(
        model.update()
        .values({**protocol_update.dict(exclude_none=True)})
        .where(model.c.id == protocol_id)
    )

    return await get(db=db, protocol_id=protocol_id)


async def check(db: Database, protocol_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == protocol_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
