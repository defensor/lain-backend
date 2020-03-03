__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Contact as model
from lain_backend.schemas import (
    ContactCreate,
    ContactIn,
    ContactUpdate,
    ContactUpdateIn,
    ContactFilter,
    ContactInnerFilter,
    ContactOuterFilter,
)
from lain_backend.cruds import organizations_contacts, peoples_contacts


async def create(db: Database, contact: ContactIn) -> Optional[Mapping[Any, Any]]:
    contact_create = ContactCreate(**contact.dict())

    contact_id = await db.execute(model.insert().values(**contact_create.dict()))

    if contact.organization_ids is not None:
        for oid in contact.organization_ids:
            await organizations_contacts.create(db=db, organization_id=oid, contact_id=contact_id)

    if contact.people_ids is not None:
        for pid in contact.people_ids:
            await peoples_contacts.create(db=db, people_id=pid, contact_id=contact_id)

    return await get(db=db, contact_id=contact_id)


async def get(db: Database, contact_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == contact_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[ContactFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, contact_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == contact_id))

    return


async def update(
    db: Database, contact: ContactUpdateIn, contact_id: int
) -> Optional[Mapping[Any, Any]]:
    contact_update = ContactUpdate(**contact.dict())

    if contact_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**contact_update.dict(exclude_none=True)})
            .where(model.c.id == contact_id)
        )

    if contact.organization_ids is not None:
        await organizations_contacts.update(
            db=db, organization_ids=contact.organization_ids, contact_id=contact_id
        )

    if contact.people_ids is not None:
        await peoples_contacts.update(db=db, people_ids=contact.people_ids, contact_id=contact_id)

    return await get(db=db, contact_id=contact_id)


async def check(db: Database, contact_id: int) -> bool:
    return (await get(db=db, contact_id=contact_id)) is not None


def _compile_filter(filter: ContactFilter) -> str:
    iFilter = ContactInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = ContactOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "contact_id"

    relations = {
        "organization_id": "organizations_contacts",
        "people_id": "peoples_contacts",
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
