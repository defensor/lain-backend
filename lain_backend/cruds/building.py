__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import Building as model
from lain_backend.schemas import (
    BuildingCreate,
    BuildingIn,
    BuildingUpdate,
    BuildingUpdateIn,
)
from lain_backend.cruds import organizations_buildings


async def create(db: Database, building: BuildingIn) -> Optional[Mapping[Any, Any]]:
    building_create = BuildingCreate(**building.dict())

    building_id = await db.execute(model.insert().values(**building_create.dict()))

    if building.organization_ids is not None:
        for oid in building.organization_ids:
            await organizations_buildings.create(
                db=db, building_id=building_id, organization_id=oid
            )

    return await get(db=db, building_id=building_id)


async def get(db: Database, building_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == building_id))


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, building_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == building_id))

    return


async def update(
    db: Database, building: BuildingUpdateIn, building_id: int
) -> Optional[Mapping[Any, Any]]:
    building_update = BuildingUpdate(**building.dict())

    await db.execute(
        model.update()
        .values({**building_update.dict(exclude_none=True)})
        .where(model.c.id == building_id)
    )

    if building.organization_ids is not None:
        await organizations_buildings.update(
            db=db, organization_ids=building.organization_ids, building_id=building_id
        )

    return await get(db=db, building_id=building_id)


async def check(db: Database, building_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == building_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
