__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Host as model
from lain_backend.schemas import (
    HostCreate,
    HostIn,
    HostUpdate,
    HostUpdateIn,
)


async def create(db: Database, host: HostIn) -> Optional[Mapping[Any, Any]]:
    host_create = HostCreate(**host.dict())

    host_id = await db.execute(model.insert().values(**host_create.dict()))

    return await get(db=db, host_id=host_id)


async def get(db: Database, host_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == host_id))


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, host_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == host_id))

    return


async def update(db: Database, host: HostUpdateIn, host_id: int) -> Optional[Mapping[Any, Any]]:
    host_update = HostUpdate(**host.dict())

    await db.execute(
        model.update().values({**host_update.dict(exclude_none=True)}).where(model.c.id == host_id)
    )

    return await get(db=db, host_id=host_id)


async def check(db: Database, host_id: int) -> bool:
    return (await get(db=db, host_id=host_id)) is not None


async def exists(db: Database, ip: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.ip == ip))) is not None
