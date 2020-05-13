from typing import List, Optional
from databases import Database
from sqlalchemy import and_

from lain_backend.models import Service as model
from lain_backend.schemas import (
    Service,
    ServiceCreate,
    ServiceUpdate,
)


async def create(db: Database, service: ServiceCreate) -> Optional[Service]:
    service_id = await db.execute(model.insert().values(**service.dict()))

    return await get(db=db, service_id=service_id)


async def get(db: Database, service_id: int) -> Optional[Service]:
    service = await db.fetch_one(model.select().where(model.c.id == service_id))

    if service is not None:
        return Service(**service)
    else:
        return None


async def list(
    db: Database, skip: int = 0, limit: int = 100, host_id: Optional[int] = None
) -> List[Service]:
    if host_id is None:
        services = await db.fetch_all(model.select().offset(skip).limit(limit))
    else:
        services = await db.fetch_all(
            model.select.where(model.c.host_id == host_id).offset(skip).limit(limit)
        )

    return [Service(**service) for service in services]


async def delete(db: Database, service_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == service_id))


async def update(
    db: Database, service: ServiceUpdate, service_id: int
) -> Optional[Service]:
    await db.execute(
        model.update()
        .values({**service.dict(exclude_none=True)})
        .where(model.c.id == service_id)
    )

    return await get(db=db, service_id=service_id)


async def exist(db: Database, service_id: int) -> bool:
    return (await get(db=db, service_id=service_id)) is not None
