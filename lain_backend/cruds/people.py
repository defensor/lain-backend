__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import People as model
from lain_backend.schemas import (
    PeopleCreate,
    PeopleIn,
    PeopleUpdate,
    PeopleUpdateIn,
    PeopleFilter,
    PeopleInnerFilter,
    PeopleOuterFilter,
)
from lain_backend.cruds import organizations_peoples


async def create(db: Database, people: PeopleIn) -> Optional[Mapping[Any, Any]]:
    people_create = PeopleCreate(**people.dict())

    people_id = await db.execute(model.insert().values(**people_create.dict()))

    if people.organization_ids is not None:
        for oid in people.organization_ids:
            await organizations_peoples.create(db=db, organization_id=oid, people_id=people_id)

    return await get(db=db, people_id=people_id)


async def get(db: Database, people_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == people_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[PeopleFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, people_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == people_id))

    return


async def update(
    db: Database, people: PeopleUpdateIn, people_id: int
) -> Optional[Mapping[Any, Any]]:
    people_update = PeopleUpdate(**people.dict())

    if people_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**people_update.dict(exclude_none=True)})
            .where(model.c.id == people_id)
        )

    if people.organization_ids is not None:
        await organizations_peoples.update(
            db=db, organization_ids=people.organization_ids, people_id=people_id
        )

    return await get(db=db, people_id=people_id)


async def check(db: Database, people_id: int) -> bool:
    return (await get(db=db, people_id=people_id)) is not None


def _compile_filter(filter: PeopleFilter) -> str:
    iFilter = PeopleInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = PeopleOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "people_id"

    relations = {
        "organization_id": "organizations_peoples",
        "vulnerability_id": "peoples_vulnerabilities",
        "contact_id": "peoples_contacts",
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
