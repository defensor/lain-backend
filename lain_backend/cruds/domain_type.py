__all__ = ["create", "get", "get_all", "update", "delete", "exist", "exist_name"]

from typing import List, Optional
from databases import Database

from lain_backend.models import DomainType as model
from lain_backend.schemas import (
    DomainType,
    DomainTypeCreate,
    DomainTypeUpdate,
)


async def create(db: Database, domain_type: DomainTypeCreate) -> Optional[DomainType]:
    domain_type_id = await db.execute(model.insert().values(**domain_type.dict()))
    return await get(db=db, domain_type_id=domain_type_id)


async def get(db: Database, domain_type_id: int) -> Optional[DomainType]:
    domain_type = await db.fetch_one(model.select().where(model.c.id == domain_type_id))

    if domain_type is not None:
        return DomainType(**domain_type)
    else:
        return None


async def get_all(db: Database, skip: int = 0, limit: int = 100,) -> List[DomainType]:
    domain_types = await db.fetch_all(model.select().offset(skip).limit(limit))

    return [DomainType(**domain_type) for domain_type in domain_types]


async def delete(db: Database, domain_type_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == domain_type_id))


async def update(
    db: Database, domain_type: DomainTypeUpdate, domain_type_id: int
) -> Optional[DomainType]:
    await db.execute(
        model.update()
        .values({**domain_type.dict(exclude_none=True)})
        .where(model.c.id == domain_type_id)
    )

    return await get(db=db, domain_type_id=domain_type_id)


async def exist(db: Database, domain_type_id: int) -> bool:
    return (await get(db=db, domain_type_id=domain_type_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
