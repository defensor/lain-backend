from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import contact_type as crud
from lain_backend.schemas import (
    ContactType,
    ContactTypeIn,
    ContactTypeUpdateIn,
    ContactTypeFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=ContactType)
async def contact_type_create(contact_type: ContactTypeIn):
    if await crud.exists(db=db, name=contact_type.name):
        raise HTTPException(status_code=400, detail="ContactType with this name already exist")

    return await crud.create(db=db, contact_type=contact_type)


@router.put("/", response_model=List[ContactType])
async def contact_type_get_all(
    skip: int = 0, limit: int = 100, filter: Optional[ContactTypeFilter] = None
):
    contact_types = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return contact_types


@router.get("/{contact_type_id}/", response_model=ContactType)
async def contact_type_get(contact_type_id: int):
    db_contact_type = await crud.get(db=db, contact_type_id=contact_type_id)
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="ContactType not found")
    return db_contact_type


@router.delete("/{contact_type_id}/", response_model=ContactType)
async def contact_type_delete(contact_type_id: int):
    db_contact_type = await crud.get(db=db, contact_type_id=contact_type_id)
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="ContactType not found")

    await crud.delete(db=db, contact_type_id=contact_type_id)

    return


@router.put("/{contact_type_id}/", response_model=ContactType)
async def contact_type_update(contact_type_id: int, contact_type: ContactTypeUpdateIn):
    if not (await crud.check(db=db, contact_type_id=contact_type_id)):
        raise HTTPException(status_code=404, detail="ContactType not found")

    if contact_type.name is not None:
        if await crud.exists(db=db, name=contact_type.name):
            raise HTTPException(status_code=400, detail="ContactType with this name already exist")

    return await crud.update(db=db, contact_type_id=contact_type_id, contact_type=contact_type)
