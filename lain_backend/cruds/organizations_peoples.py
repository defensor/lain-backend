__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import organizations_peoples as model


async def create(db: Database, organization_id: int, people_id: int) -> None:
    await db.execute(model.insert().values(people_id=people_id, organization_id=organization_id))

    return


async def update(db: Database, organization_ids: List[int], people_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.people_id == people_id, model.c.organization_id.notin_(organization_ids))
        )
    )

    for oid in organization_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.people_id == people_id, model.c.organization_id == oid)
                )
            )
        ) is None:
            await db.execute(model.insert().values(people_id=people_id, organization_id=oid))

    return


async def get_all(
    db: Database, people_id: Optional[int] = None, organization_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if people_id is not None:
        return await db.fetch_all(model.select().where(model.c.people_id == people_id))
    elif organization_id is not None:
        return await db.fetch_all(model.select().where(model.c.organization_id == organization_id))
    else:
        return await db.fetch_all(model.select().where())
