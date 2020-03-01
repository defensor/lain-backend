__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Organization as model
from lain_backend.schemas import (
    OrganizationCreate,
    OrganizationIn,
    OrganizationUpdate,
    OrganizationUpdateIn,
)


async def create(db: Database, organization: OrganizationIn) -> Optional[Mapping[Any, Any]]:
    organization_create = OrganizationCreate(**organization.dict())

    organization_id = await db.execute(model.insert().values(**organization_create.dict()))

    return await get(db=db, organization_id=organization_id)


async def get(db: Database, organization_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == organization_id))


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, organization_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == organization_id))

    return


async def update(
    db: Database, organization: OrganizationUpdateIn, organization_id: int
) -> Optional[Mapping[Any, Any]]:
    organization_update = OrganizationUpdate(**organization.dict())

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
