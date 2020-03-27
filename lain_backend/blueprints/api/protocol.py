from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import protocol as crud
from lain_backend.schemas import (
    Protocol,
    ProtocolCreate,
    ProtocolIn,
    ProtocolUpdate,
    ProtocolUpdateIn,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Protocol)
async def protocol_create(protocol: ProtocolIn):
    if await crud.exist_name(db=db, name=protocol.name):
        raise HTTPException(
            status_code=400, detail="Protocol with this name already exist"
        )

    return await crud.create(db=db, protocol=ProtocolCreate(**protocol.dict()))


@router.put("/", response_model=List[Protocol])
async def protocol_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{protocol_id}/", response_model=Protocol)
async def protocol_get(protocol_id: int):
    db_protocol = await crud.get(db=db, protocol_id=protocol_id)
    if db_protocol is None:
        raise HTTPException(status_code=404, detail="Protocol not found")
    return db_protocol


@router.delete("/{protocol_id}/", response_model=Protocol)
async def protocol_delete(protocol_id: int):
    if not (await crud.exist(db=db, protocol_id=protocol_id)):
        raise HTTPException(status_code=404, detail="Protocol not found")

    await crud.delete(db=db, protocol_id=protocol_id)


@router.put("/{protocol_id}/", response_model=Protocol)
async def protocol_update(protocol_id: int, protocol: ProtocolUpdateIn):
    if not (await crud.exist(db=db, protocol_id=protocol_id)):
        raise HTTPException(status_code=404, detail="Protocol not found")

    if protocol.name is not None:
        if await crud.exist_name(db=db, name=protocol.name):
            raise HTTPException(
                status_code=400, detail="Protocol with this name already exist"
            )

    return await crud.update(
        db=db, protocol_id=protocol_id, protocol=ProtocolUpdate(**protocol.dict())
    )
