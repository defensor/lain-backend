__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any, Dict
from databases import Database

from lain_backend.models import Project as model
from lain_backend.schemas import (
    ProjectCreate,
    ProjectIn,
    ProjectUpdate,
    ProjectUpdateIn,
    ProjectFilter,
    ProjectInnerFilter,
    ProjectOuterFilter,
)


async def create(db: Database, project: ProjectIn) -> Optional[Mapping[Any, Any]]:
    project_create = ProjectCreate(**project.dict())

    project_id = await db.execute(model.insert().values(**project_create.dict()))

    return await get(db=db, project_id=project_id)


async def get(db: Database, project_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == project_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[ProjectFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, project_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == project_id))

    return


async def update(
    db: Database, project: ProjectUpdateIn, project_id: int
) -> Optional[Mapping[Any, Any]]:
    project_update = ProjectUpdate(**project.dict())

    if project_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**project_update.dict(exclude_none=True)})
            .where(model.c.id == project_id)
        )

    return await get(db=db, project_id=project_id)


async def check(db: Database, project_id: int) -> bool:
    return (await get(db=db, project_id=project_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None


def _compile_filter(filter: ProjectFilter) -> str:
    iFilter = ProjectInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = ProjectOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "project_id"

    relations: Dict[str, str] = {}

    statement = (
        " AND ".join(
            [
                f"{table_name}.{key} = '{iFilter[key]}'"
                if isinstance(iFilter[key], str)
                else f"{table_name}.{key} = {iFilter[key]}"
                for key in iFilter
            ]
            + [
                f"{table_name}.id = {relations[key]}.{ref_name} AND {relations[key]}.{key} = {oFilter[key]}"
                for key in oFilter
            ]
        )
        or "TRUE"
    )

    sources = ", ".join([table_name] + [relations[key] for key in oFilter])

    query = f"SELECT * FROM {sources} WHERE {statement} LIMIT :limit OFFSET :offset"
    return query
