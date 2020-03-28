from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import service as crud, protocol, services_protocols
from lain_backend.schemas import (
    Service,
    ServiceCreate,
    ServiceIn,
    ServiceUpdate,
    ServiceUpdateIn,
    Protocol,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Service)
async def service_create(service: ServiceIn):
    return await crud.create(db=db, service=ServiceCreate(**service.dict()))


@router.put("/", response_model=List[Service])
async def service_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


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


@router.get("/{service_id}/protocols", response_model=List[Protocol])
async def service_get_protocols(service_id):
    if not (await crud.exist(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await protocol.get_all(db=db, service_id=service_id)


@router.post("/{service_id}/protocols/{protocol_id}")
async def service_append_protocol(service_id: int, protocol_id: int):
    if not (await crud.exist(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    if not (await protocol.exist(db=db, protocol_id=protocol_id)):
        raise HTTPException(status_code=404, detail="Protocol not found")

    if await services_protocols.exist(
        db=db, service_id=service_id, protocol_id=protocol_id
    ):
        raise HTTPException(status_code=400, detail="Relation already exist")

    await services_protocols.create(
        db=db, service_id=service_id, protocol_id=protocol_id
    )


@router.delete("/{service_id}/protocols/{protocol_id}")
async def service_remove_protocol(service_id: int, protocol_id: int):
    if not (await crud.exist(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    if not (await protocol.exist(db=db, protocol_id=protocol_id)):
        raise HTTPException(status_code=404, detail="Protocol not found")

    if not (
        await services_protocols.exist(
            db=db, service_id=service_id, protocol_id=protocol_id
        )
    ):
        raise HTTPException(status_code=400, detail="Relation not found")

    await services_protocols.delete(
        db=db, service_id=service_id, protocol_id=protocol_id
    )
