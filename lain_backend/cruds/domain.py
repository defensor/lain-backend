__all__ = ["create", "get", "get_all", "update", "delete", "exist", "exist_name"]

from typing import List, Optional
from databases import Database

from lain_backend.models import Domain as model
from lain_backend.schemas import (
    Domain,
    DomainCreate,
    DomainUpdate,
)
from lain_backend.cruds import hosts_domains


async def create(db: Database, domain: DomainCreate) -> Optional[Domain]:
    domain_id = await db.execute(model.insert().values(**domain.dict()))

    return await get(db=db, domain_id=domain_id)


async def get(db: Database, domain_id: int) -> Optional[Domain]:
    domain = await db.fetch_one(model.select().where(model.c.id == domain_id))

    if domain is not None:
        return Domain(**domain)
    else:
        return None


async def get_all(db: Database, skip: int = 0, limit: int = 100,) -> List[Domain]:
    domains = await db.fetch_all(model.select().offset(skip).limit(limit))

    return [Domain(**domain) for domain in domains]


async def delete(db: Database, domain_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == domain_id))


async def update(
    db: Database, domain: DomainUpdate, domain_id: int
) -> Optional[Domain]:
    await db.execute(
        model.update()
        .values({**domain.dict(exclude_none=True)})
        .where(model.c.id == domain_id)
    )

    return await get(db=db, domain_id=domain_id)


async def exist(db: Database, domain_id: int) -> bool:
    return (await get(db=db, domain_id=domain_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
