__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Contact as model
from lain_backend.schemas import (
    ContactCreate,
    ContactIn,
    ContactUpdate,
    ContactUpdateIn,
)


async def create(db: Database, contact: ContactIn) -> Optional[Mapping[Any, Any]]:
    contact_create = ContactCreate(**contact.dict())

    contact_id = await db.execute(model.insert().values(**contact_create.dict()))

    return await get(db=db, contact_id=contact_id)


async def get(db: Database, contact_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == contact_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100
) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, contact_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == contact_id))

    return


async def update(
    db: Database, contact: ContactUpdateIn, contact_id: int
) -> Optional[Mapping[Any, Any]]:
    contact_update = ContactUpdate(**contact.dict())

    await db.execute(
        model.update()
        .values({**contact_update.dict(exclude_none=True)})
        .where(model.c.id == contact_id)
    )

    return await get(db=db, contact_id=contact_id)


async def check(db: Database, contact_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == contact_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
