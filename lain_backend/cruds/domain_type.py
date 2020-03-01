__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import DomainType as model
from lain_backend.schemas import (
    DomainTypeCreate,
    DomainTypeIn,
    DomainTypeUpdate,
    DomainTypeUpdateIn,
)


async def create(db: Database, domain_type: DomainTypeIn) -> Optional[Mapping[Any, Any]]:
    domain_type_create = DomainTypeCreate(**domain_type.dict())

    domain_type_id = await db.execute(model.insert().values(**domain_type_create.dict()))

    return await get(db=db, domain_type_id=domain_type_id)


async def get(db: Database, domain_type_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == domain_type_id))


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, domain_type_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == domain_type_id))

    return


async def update(
    db: Database, domain_type: DomainTypeUpdateIn, domain_type_id: int
) -> Optional[Mapping[Any, Any]]:
    domain_type_update = DomainTypeUpdate(**domain_type.dict())

    await db.execute(
        model.update()
        .values({**domain_type_update.dict(exclude_none=True)})
        .where(model.c.id == domain_type_id)
    )

    return await get(db=db, domain_type_id=domain_type_id)


async def check(db: Database, domain_type_id: int) -> bool:
    return (await get(db=db, domain_type_id=domain_type_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
