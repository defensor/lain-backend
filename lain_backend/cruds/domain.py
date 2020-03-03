__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Domain as model
from lain_backend.schemas import (
    DomainCreate,
    DomainIn,
    DomainUpdate,
    DomainUpdateIn,
    DomainFilter,
    DomainInnerFilter,
    DomainOuterFilter,
)
from lain_backend.cruds import hosts_domains


async def create(db: Database, domain: DomainIn) -> Optional[Mapping[Any, Any]]:
    domain_create = DomainCreate(**domain.dict())

    domain_id = await db.execute(model.insert().values(**domain_create.dict()))

    if domain.host_ids is not None:
        for hid in domain.host_ids:
            await hosts_domains.create(db=db, host_id=hid, domain_id=domain_id)

    return await get(db=db, domain_id=domain_id)


async def get(db: Database, domain_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == domain_id))


async def get_all(
    db: Database,
    skip: int = 0,
    limit: int = 100,
    domain_type_id: int = None,
    filter: Optional[DomainFilter] = None,
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, domain_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == domain_id))

    return


async def update(
    db: Database, domain: DomainUpdateIn, domain_id: int
) -> Optional[Mapping[Any, Any]]:
    domain_update = DomainUpdate(**domain.dict())

    if domain_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**domain_update.dict(exclude_none=True)})
            .where(model.c.id == domain_id)
        )

    if domain.host_ids is not None:
        await hosts_domains.update(db=db, host_ids=domain.host_ids, domain_id=domain_id)

    return await get(db=db, domain_id=domain_id)


async def check(db: Database, domain_id: int) -> bool:
    return (await get(db=db, domain_id=domain_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None


def _compile_filter(filter: DomainFilter) -> str:
    iFilter = DomainInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = DomainOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "domain_id"

    relations = {
        "host_id": "hosts_domains",
    }

    statement = (
        " AND ".join(
            [
                f"{table_name}.{key} = '{iFilter[key]}'"
                if isinstance(iFilter[key], str)
                else f"{table_name}.{key} = {iFilter[key]}"
                for key in iFilter
            ]
            + [
                f"{table_name}.id = {relations[key]}.{ref_name} AND {relations[key]}.{key} = {oFilter[key]}"
                for key in oFilter
            ]
        )
        or "TRUE"
    )

    sources = ", ".join([table_name] + [relations[key] for key in oFilter])

    query = f"SELECT * FROM {sources} WHERE {statement} LIMIT :limit OFFSET :offset"
    return query
