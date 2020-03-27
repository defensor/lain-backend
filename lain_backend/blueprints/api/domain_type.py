from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import domain_type as crud
from lain_backend.schemas import (
    DomainTypeCreate,
    DomainType,
    DomainTypeIn,
    DomainTypeUpdate,
    DomainTypeUpdateIn,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=DomainType)
async def domain_type_create(domain_type: DomainTypeIn):
    if await crud.exist_name(db=db, name=domain_type.name):
        raise HTTPException(
            status_code=400, detail="DomainType with this name already exist"
        )

    return await crud.create(db=db, domain_type=DomainTypeCreate(**domain_type.dict()))


@router.put("/", response_model=List[DomainType])
async def domain_type_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{domain_type_id}/", response_model=DomainType)
async def domain_type_get(domain_type_id: int):
    db_domain_type = await crud.get(db=db, domain_type_id=domain_type_id)
    if db_domain_type is None:
        raise HTTPException(status_code=404, detail="DomainType not found")
    return db_domain_type


@router.delete("/{domain_type_id}/", response_model=DomainType)
async def domain_type_delete(domain_type_id: int):
    if not (await crud.exist(db=db, domain_type_id=domain_type_id)):
        raise HTTPException(status_code=404, detail="DomainType not found")

    await crud.delete(db=db, domain_type_id=domain_type_id)


@router.put("/{domain_type_id}/", response_model=DomainType)
async def domain_type_update(domain_type_id: int, domain_type: DomainTypeUpdateIn):
    if not (await crud.exist(db=db, domain_type_id=domain_type_id)):
        raise HTTPException(status_code=404, detail="DomainType not found")

    if domain_type.name is not None:
        if await crud.exist_name(db=db, name=domain_type.name):
            raise HTTPException(
                status_code=400, detail="DomainType with this name already exist"
            )

    return await crud.update(
        db=db,
        domain_type_id=domain_type_id,
        domain_type=DomainTypeUpdate(**domain_type.dict()),
    )
