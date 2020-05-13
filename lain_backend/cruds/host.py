from typing import List, Optional
from databases import Database

from lain_backend.models import Host as model
from lain_backend.schemas import (
    Host,
    HostCreate,
    HostUpdate,
)


async def create(db: Database, host: HostCreate) -> Optional[Host]:
    host_id = await db.execute(model.insert().values(**host.dict()))

    return await get(db=db, host_id=host_id)


async def get(db: Database, host_id: int) -> Optional[Host]:
    host = await db.fetch_one(model.select().where(model.c.id == host_id))

    if host is not None:
        return Host(**host)
    else:
        return None


async def list(
    db: Database, skip: int = 0, limit: int = 100, organization_id: Optional[int] = None
) -> List[Host]:
    if organization_id is None:
        hosts = await db.fetch_all(model.select().offset(skip).limit(limit))
    else:
        hosts = await db.fetch_all(
            model.select()
            .where(model.c.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )

    return [Host(**host) for host in hosts]


async def delete(db: Database, host_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == host_id))


async def update(db: Database, host: HostUpdate, host_id: int) -> Optional[Host]:
    await db.execute(
        model.update()
        .values({**host.dict(exclude_none=True)})
        .where(model.c.id == host_id)
    )

    return await get(db=db, host_id=host_id)


async def exist(db: Database, host_id: int) -> bool:
    return (await get(db=db, host_id=host_id)) is not None


async def exist_name(db: Database, ip: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.ip == ip))) is not None
