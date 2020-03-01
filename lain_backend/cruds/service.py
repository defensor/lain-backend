__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Service as model
from lain_backend.schemas import (
    ServiceCreate,
    ServiceIn,
    ServiceUpdate,
    ServiceUpdateIn,
)
from lain_backend.cruds import services_protocols


async def create(db: Database, service: ServiceIn) -> Optional[Mapping[Any, Any]]:
    service_create = ServiceCreate(**service.dict())

    service_id = await db.execute(model.insert().values(**service_create.dict()))

    return await get(db=db, service_id=service_id)


async def get(db: Database, service_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == service_id))


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, service_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == service_id))

    return


async def update(
    db: Database, service: ServiceUpdateIn, service_id: int
) -> Optional[Mapping[Any, Any]]:
    service_update = ServiceUpdate(**service.dict())

    await db.execute(
        model.update()
        .values({**service_update.dict(exclude_none=True)})
        .where(model.c.id == service_id)
    )

    return await get(db=db, service_id=service_id)


async def check(db: Database, service_id: int) -> bool:
    return (await get(db=db, service_id=service_id)) is not None

