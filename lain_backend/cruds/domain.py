__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Domain as model
from lain_backend.schemas import (
    DomainCreate,
    DomainIn,
    DomainUpdate,
    DomainUpdateIn,
)


async def create(db: Database, domain: DomainIn) -> Optional[Mapping[Any, Any]]:
    domain_create = DomainCreate(**domain.dict())

    domain_id = await db.execute(model.insert().values(**domain_create.dict()))

    return await get(db=db, domain_id=domain_id)


async def get(db: Database, domain_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == domain_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100
) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, domain_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == domain_id))

    return


async def update(
    db: Database, domain: DomainUpdateIn, domain_id: int
) -> Optional[Mapping[Any, Any]]:
    domain_update = DomainUpdate(**domain.dict())

    await db.execute(
        model.update()
        .values({**domain_update.dict(exclude_none=True)})
        .where(model.c.id == domain_id)
    )

    return await get(db=db, domain_id=domain_id)


async def check(db: Database, domain_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == domain_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
