from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import domain as crud
from lain_backend.schemas import (
    Domain,
    DomainCreate,
    DomainIn,
    DomainUpdate,
    DomainUpdateIn,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Domain)
async def domain_create(domain: DomainIn):
    if await crud.exist_name(db=db, name=domain.name):
        raise HTTPException(
            status_code=400, detail="Domain with this name already exist"
        )

    return await crud.create(db=db, domain=DomainCreate(**domain.dict()))


@router.put("/", response_model=List[Domain])
async def domain_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{domain_id}/", response_model=Domain)
async def domain_get(domain_id: int):
    db_domain = await crud.get(db=db, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


@router.delete("/{domain_id}/", response_model=Domain)
async def domain_delete(domain_id: int):
    if not (await crud.exist(db=db, domain_id=domain_id)):
        raise HTTPException(status_code=404, detail="Domain not found")

    await crud.delete(db=db, domain_id=domain_id)


@router.put("/{domain_id}/", response_model=Domain)
async def domain_update(domain_id: int, domain: DomainUpdateIn):
    if not (await crud.exist(db=db, domain_id=domain_id)):
        raise HTTPException(status_code=404, detail="Domain not found")

    if domain.name is not None:
        if await crud.exist_name(db=db, name=domain.name):
            raise HTTPException(
                status_code=400, detail="Domain with this name already exist"
            )

    return await crud.update(
        db=db, domain_id=domain_id, domain=DomainUpdate(**domain.dict())
    )
