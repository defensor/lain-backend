__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Project as model
from lain_backend.schemas import (
    ProjectCreate,
    ProjectIn,
    ProjectUpdate,
    ProjectUpdateIn,
)


async def create(db: Database, project: ProjectIn) -> Optional[Mapping[Any, Any]]:
    project_create = ProjectCreate(**project.dict())

    project_id = await db.execute(model.insert().values(**project_create.dict()))

    return await get(db=db, project_id=project_id)


async def get(db: Database, project_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == project_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100
) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, project_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == project_id))

    return


async def update(
    db: Database, project: ProjectUpdateIn, project_id: int
) -> Optional[Mapping[Any, Any]]:
    project_update = ProjectUpdate(**project.dict())

    await db.execute(
        model.update()
        .values({**project_update.dict(exclude_none=True)})
        .where(model.c.id == project_id)
    )

    return await get(db=db, project_id=project_id)


async def check(db: Database, project_id: int) -> bool:
    return await db.execute(model.exists().where(model.c.id == project_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
