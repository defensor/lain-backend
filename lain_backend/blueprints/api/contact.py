from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import contact as crud, organization, people
from lain_backend.schemas import (
    Contact,
    ContactIn,
    ContactUpdateIn,
    ContactFilter,
    Organization,
    OrganizationFilter,
    People,
    PeopleFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Contact)
async def contact_create(contact: ContactIn):
    return await crud.create(db=db, contact=contact)


@router.put("/", response_model=List[Contact])
async def contact_get_all(skip: int = 0, limit: int = 100, filter: Optional[ContactFilter] = None):
    contacts = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return contacts


@router.get("/{contact_id}/", response_model=Contact)
async def contact_get(contact_id: int):
    db_contact = await crud.get(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}/", response_model=Contact)
async def contact_delete(contact_id: int):
    db_contact = await crud.get(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    await crud.delete(db=db, contact_id=contact_id)

    return


@router.put("/{contact_id}/", response_model=Contact)
async def contact_update(contact_id: int, contact: ContactUpdateIn):
    if not (await crud.check(db=db, contact_id=contact_id)):
        raise HTTPException(status_code=404, detail="Contact not found")

    return await crud.update(db=db, contact_id=contact_id, contact=contact)


@router.get("/{contact_id}/organizations", response_model=List[Organization])
async def contact_get_organizations(contact_id: int):
    if not (await crud.check(db=db, contact_id=contact_id)):
        raise HTTPException(status_code=404, detail="Contact not found")

    return await organization.get_all(db=db, filter=OrganizationFilter(contact_id=contact_id))


@router.get("/{contact_id}/peoples", response_model=List[People])
async def contact_get_peoples(contact_id: int):
    if not (await crud.check(db=db, contact_id=contact_id)):
        raise HTTPException(status_code=404, detail="Contact not found")

    return await people.get_all(db=db, filter=PeopleFilter(contact_id=contact_id))
