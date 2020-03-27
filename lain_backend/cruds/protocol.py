__all__ = ["create", "get", "get_all", "update", "delete", "exist", "exist_name"]

from typing import List, Optional
from databases import Database

from lain_backend.models import Protocol as model
from lain_backend.schemas import (
    Protocol,
    ProtocolCreate,
    ProtocolUpdate,
)


async def create(db: Database, protocol: ProtocolCreate) -> Optional[Protocol]:
    protocol_id = await db.execute(model.insert().values(**protocol.dict()))

    return await get(db=db, protocol_id=protocol_id)


async def get(db: Database, protocol_id: int) -> Optional[Protocol]:
    protocol = await db.fetch_one(model.select().where(model.c.id == protocol_id))

    if protocol is not None:
        return Protocol(**protocol)
    else:
        return None


async def get_all(db: Database, skip: int = 0, limit: int = 100,) -> List[Protocol]:
    protocols = await db.fetch_all(model.select().offset(skip).limit(limit))

    return [Protocol(**protocol) for protocol in protocols]


async def delete(db: Database, protocol_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == protocol_id))


async def update(
    db: Database, protocol: ProtocolUpdate, protocol_id: int
) -> Optional[Protocol]:
    await db.execute(
        model.update()
        .values({**protocol.dict(exclude_none=True)})
        .where(model.c.id == protocol_id)
    )

    return await get(db=db, protocol_id=protocol_id)


async def exist(db: Database, protocol_id: int) -> bool:
    return (await get(db=db, protocol_id=protocol_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
