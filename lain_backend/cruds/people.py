__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import People as model
from lain_backend.schemas import (
    PeopleCreate,
    PeopleIn,
    PeopleUpdate,
    PeopleUpdateIn,
)


async def create(db: Database, people: PeopleIn) -> Optional[Mapping[Any, Any]]:
    people_create = PeopleCreate(**people.dict())

    people_id = await db.execute(model.insert().values(**people_create.dict()))

    return await get(db=db, people_id=people_id)


async def get(db: Database, people_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == people_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100
) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, people_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == people_id))

    return


async def update(
    db: Database, people: PeopleUpdateIn, people_id: int
) -> Optional[Mapping[Any, Any]]:
    people_update = PeopleUpdate(**people.dict())

    await db.execute(
        model.update()
        .values({**people_update.dict(exclude_none=True)})
        .where(model.c.id == people_id)
    )

    return await get(db=db, people_id=people_id)


async def check(db: Database, people_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == people_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
