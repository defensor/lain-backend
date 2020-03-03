from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import project as crud, organization
from lain_backend.schemas import (
    Project,
    ProjectIn,
    ProjectUpdateIn,
    ProjectFilter,
    Organization,
    OrganizationFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Project)
async def project_create(project: ProjectIn):
    if await crud.exists(db=db, name=project.name):
        raise HTTPException(status_code=400, detail="Project with this name already exist")

    return await crud.create(db=db, project=project)


@router.put("/", response_model=List[Project])
async def project_get_all(skip: int = 0, limit: int = 100, filter: Optional[ProjectFilter] = None):
    projects = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return projects


@router.get("/{project_id}/", response_model=Project)
async def project_get(project_id: int):
    db_project = await crud.get(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/{project_id}/", response_model=Project)
async def project_delete(project_id: int):
    db_project = await crud.get(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await crud.delete(db=db, project_id=project_id)

    return


@router.put("/{project_id}/", response_model=Project)
async def project_update(project_id: int, project: ProjectUpdateIn):
    if not (await crud.check(db=db, project_id=project_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    if project.name is not None:
        if await crud.exists(db=db, name=project.name):
            raise HTTPException(status_code=400, detail="Project with this name already exist")

    return await crud.update(db=db, project_id=project_id, project=project)


@router.get("/{project_id}/organizations", response_model=List[Organization])
async def project_get_organizations(project_id: int):
    if not (await crud.check(db=db, project_id=project_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    return await organization.get_all(db=db, filter=OrganizationFilter(project_id=project_id))
