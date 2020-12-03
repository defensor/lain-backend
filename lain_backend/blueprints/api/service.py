from typing import List

from fastapi import APIRouter, HTTPException
from lain_backend.cruds import service as crud
from lain_backend.database import database as db
from lain_backend.schemas.service import (
    Service,
    ServiceCreate,
    ServiceIn,
    ServiceUpdate,
    ServiceUpdateIn,
)

router = APIRouter()


@router.post("/", response_model=Service)
async def service_create(service: ServiceIn):
    return await crud.create(db=db, service=ServiceCreate(**service.dict()))


@router.get("/", response_model=List[Service])
async def service_list(skip: int = 0, limit: int = 100):
    return await crud.list(db=db, skip=skip, limit=limit)


@router.get("/{service_id}/", response_model=Service)
async def service_get(service_id: int):
    db_service = await crud.get(db=db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@router.delete("/{service_id}/", response_model=Service)
async def service_delete(service_id: int):
    if not (await crud.exist(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    await crud.delete(db=db, service_id=service_id)


@router.put("/{service_id}/", response_model=Service)
async def service_update(service_id: int, service: ServiceUpdateIn):
    if not (await crud.exist(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await crud.update(
        db=db, service_id=service_id, service=ServiceUpdate(**service.dict())
    )
