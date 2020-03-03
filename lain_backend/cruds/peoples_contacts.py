__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import peoples_contacts as model


async def create(db: Database, people_id: int, contact_id: int) -> None:
    await db.execute(model.insert().values(contact_id=contact_id, people_id=people_id))

    return


async def update(db: Database, people_ids: List[int], contact_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.contact_id == contact_id, model.c.people_id.notin_(people_ids))
        )
    )

    for pid in people_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.contact_id == contact_id, model.c.people_id == pid)
                )
            )
        ) is None:
            await db.execute(model.insert().values(contact_id=contact_id, people_id=pid))

    return


async def get_all(
    db: Database, contact_id: Optional[int] = None, people_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if contact_id is not None:
        return await db.fetch_all(model.select().where(model.c.contact_id == contact_id))
    elif people_id is not None:
        return await db.fetch_all(model.select().where(model.c.people_id == people_id))
    else:
        return await db.fetch_all(model.select().where())
