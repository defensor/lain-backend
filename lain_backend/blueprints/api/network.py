from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import network as crud
from lain_backend.schemas import (
    Network,
    NetworkCreate,
    NetworkIn,
    NetworkUpdate,
    NetworkUpdateIn,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Network)
async def network_create(network: NetworkIn):
    return await crud.create(db=db, network=NetworkCreate(**network.dict()))


@router.put("/", response_model=List[Network])
async def network_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{network_id}/", response_model=Network)
async def network_get(network_id: int):
    db_network = await crud.get(db=db, network_id=network_id)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@router.delete("/{network_id}/", response_model=Network)
async def network_delete(network_id: int):
    if not (await crud.exist(db=db, network_id=network_id)):
        raise HTTPException(status_code=404, detail="Network not found")

    await crud.delete(db=db, network_id=network_id)


@router.put("/{network_id}/", response_model=Network)
async def network_update(network_id: int, network: NetworkUpdateIn):
    if not (await crud.exist(db=db, network_id=network_id)):
        raise HTTPException(status_code=404, detail="Network not found")

    return await crud.update(
        db=db, network_id=network_id, network=NetworkUpdate(**network.dict())
    )
