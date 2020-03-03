__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import organizations_buildings as model


async def create(db: Database, organization_id: int, building_id: int) -> None:
    await db.execute(
        model.insert().values(building_id=building_id, organization_id=organization_id)
    )

    return


async def update(db: Database, organization_ids: List[int], building_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(
                model.c.building_id == building_id,
                model.c.organization_id.notin_(organization_ids),
            )
        )
    )

    for oid in organization_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.building_id == building_id, model.c.organization_id == oid,)
                )
            )
        ) is None:
            await db.execute(model.insert().values(building_id=building_id, organization_id=oid))

    return


async def get_all(
    db: Database, building_id: Optional[int] = None, organization_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if building_id is not None:
        return await db.fetch_all(model.select().where(model.c.building_id == building_id))
    elif organization_id is not None:
        return await db.fetch_all(model.select().where(model.c.organization_id == organization_id))
    else:
        return await db.fetch_all(model.select().where())
