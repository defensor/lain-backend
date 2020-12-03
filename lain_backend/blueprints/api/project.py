from typing import List

from fastapi import APIRouter, HTTPException
from lain_backend.cruds import organization
from lain_backend.cruds import project as crud
from lain_backend.database import database as db
from lain_backend.schemas.organization import Organization
from lain_backend.schemas.project import (
    Project,
    ProjectCreate,
    ProjectIn,
    ProjectUpdate,
    ProjectUpdateIn,
)

router = APIRouter()


@router.post("/", response_model=Project)
async def project_create(project: ProjectIn):
    if await crud.exist_name(db=db, name=project.name):
        raise HTTPException(
            status_code=400, detail="Project with this name already exist"
        )

    return await crud.create(db=db, project=ProjectCreate(**project.dict()))


@router.get("/", response_model=List[Project])
async def project_list(skip: int = 0, limit: int = 100):
    return await crud.list(db=db, skip=skip, limit=limit)


@router.get("/{project_id}/", response_model=Project)
async def project_get(project_id: int):
    db_project = await crud.get(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/{project_id}/", response_model=Project)
async def project_delete(project_id: int):
    if not (await crud.exist(db=db, project_id=project_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    await crud.delete(db=db, project_id=project_id)


@router.put("/{project_id}/", response_model=Project)
async def project_update(project_id: int, project: ProjectUpdateIn):
    if not (await crud.exist(db=db, project_id=project_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    if project.name is not None:
        if await crud.exist_name(db=db, name=project.name):
            raise HTTPException(
                status_code=400, detail="Project with this name already exist"
            )

    return await crud.update(
        db=db, project_id=project_id, project=ProjectUpdate(**project.dict())
    )


@router.get("/{project_id}/organizations", response_model=List[Organization])
async def project_list_organizations(project_id):
    if not (await crud.exist(db=db, project_id=project_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    return await organization.list(db=db, project_id=project_id)
