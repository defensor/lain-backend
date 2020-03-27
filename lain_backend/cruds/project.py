__all__ = ["create", "get", "get_all", "update", "delete", "exist", "exist_name"]

from typing import List, Optional
from databases import Database

from lain_backend.models import Project as model
from lain_backend.schemas import (
    Project,
    ProjectCreate,
    ProjectUpdate,
)


async def create(db: Database, project: ProjectCreate) -> Optional[Project]:
    project_id = await db.execute(model.insert().values(**project.dict()))

    return await get(db=db, project_id=project_id)


async def get(db: Database, project_id: int) -> Optional[Project]:
    project = await db.fetch_one(model.select().where(model.c.id == project_id))

    if project is not None:
        return Project(**project)
    else:
        return None


async def get_all(db: Database, skip: int = 0, limit: int = 100,) -> List[Project]:
    projects = await db.fetch_all(model.select().offset(skip).limit(limit))

    return [Project(**project) for project in projects]


async def delete(db: Database, project_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == project_id))


async def update(
    db: Database, project: ProjectUpdate, project_id: int
) -> Optional[Project]:
    await db.execute(
        model.update()
        .values({**project.dict(exclude_none=True)})
        .where(model.c.id == project_id)
    )

    return await get(db=db, project_id=project_id)


async def exist(db: Database, project_id: int) -> bool:
    return (await get(db=db, project_id=project_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
