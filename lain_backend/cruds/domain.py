from typing import List, Optional

from databases import Database
from lain_backend.cruds import hosts_domains
from lain_backend.models import Domain as model
from lain_backend.schemas.domain import Domain, DomainCreate, DomainUpdate


async def create(db: Database, domain: DomainCreate) -> Optional[Domain]:
    domain_id = await db.execute(model.insert().values(**domain.dict()))

    return await get(db=db, domain_id=domain_id)


async def get(db: Database, domain_id: int) -> Optional[Domain]:
    domain = await db.fetch_one(model.select().where(model.c.id == domain_id))

    if domain is not None:
        return Domain(**domain)
    else:
        return None


async def list(
    db: Database, skip: int = 0, limit: int = 100, host_id: Optional[int] = None
) -> List[Domain]:
    if host_id is None:
        domains = await db.fetch_all(model.select().offset(skip).limit(limit))
    else:
        ids = [
            host_domain.domain_id
            for host_domain in await hosts_domains.list(db=db, host_id=host_id)
        ]
        domains = await db.fetch_all(
            model.select().where(model.c.id.in_(ids)).offset(skip).limit(limit)
        )

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
