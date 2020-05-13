from typing import List, Optional
from databases import Database

from lain_backend.models import Organization as model
from lain_backend.schemas import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
)


async def create(
    db: Database, organization: OrganizationCreate
) -> Optional[Organization]:
    organization_id = await db.execute(model.insert().values(**organization.dict()))

    return await get(db=db, organization_id=organization_id)


async def get(db: Database, organization_id: int) -> Optional[Organization]:
    organization = await db.fetch_one(
        model.select().where(model.c.id == organization_id)
    )

    if organization is not None:
        return Organization(**organization)
    else:
        return None


async def list(
    db: Database, skip: int = 0, limit: int = 100, project_id: Optional[int] = None
) -> List[Organization]:
    if project_id is None:
        organizations = await db.fetch_all(model.select().offset(skip).limit(limit))
    else:
        organizations = await db.fetch_all(
            model.select()
            .where(model.c.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )

    return [Organization(**organization) for organization in organizations]


async def delete(db: Database, organization_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == organization_id))


async def update(
    db: Database, organization: OrganizationUpdate, organization_id: int
) -> Optional[Organization]:
    await db.execute(
        model.update()
        .values({**organization.dict(exclude_none=True)})
        .where(model.c.id == organization_id)
    )

    return await get(db=db, organization_id=organization_id)


async def exist(db: Database, organization_id: int) -> bool:
    return (await get(db=db, organization_id=organization_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
