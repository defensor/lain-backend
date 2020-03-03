__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Organization as model
from lain_backend.schemas import (
    OrganizationCreate,
    OrganizationIn,
    OrganizationUpdate,
    OrganizationUpdateIn,
    OrganizationFilter,
    OrganizationInnerFilter,
    OrganizationOuterFilter,
)


async def create(db: Database, organization: OrganizationIn) -> Optional[Mapping[Any, Any]]:
    organization_create = OrganizationCreate(**organization.dict())

    organization_id = await db.execute(model.insert().values(**organization_create.dict()))

    return await get(db=db, organization_id=organization_id)


async def get(db: Database, organization_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == organization_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[OrganizationFilter] = None,
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, organization_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == organization_id))

    return


async def update(
    db: Database, organization: OrganizationUpdateIn, organization_id: int
) -> Optional[Mapping[Any, Any]]:
    organization_update = OrganizationUpdate(**organization.dict())

    if organization_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**organization_update.dict(exclude_none=True)})
            .where(model.c.id == organization_id)
        )

    return await get(db=db, organization_id=organization_id)


async def check(db: Database, organization_id: int) -> bool:
    return (await get(db=db, organization_id=organization_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None


def _compile_filter(filter: OrganizationFilter) -> str:
    iFilter = OrganizationInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = OrganizationOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "organization_id"

    relations = {
        "network_id": "organizations_networks",
        "people_id": "organizations_peoples",
        "building_id": "organizations_buildings",
        "contact_id": "organizations_contacts",
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
