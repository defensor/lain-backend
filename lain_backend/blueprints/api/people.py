from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import people as crud, organization, contact, vulnerability
from lain_backend.schemas import (
    People,
    PeopleIn,
    PeopleUpdateIn,
    PeopleFilter,
    Organization,
    OrganizationFilter,
    Contact,
    ContactFilter,
    Vulnerability,
    VulnerabilityFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=People)
async def people_create(people: PeopleIn):
    return await crud.create(db=db, people=people)


@router.put("/", response_model=List[People])
async def people_get_all(skip: int = 0, limit: int = 100, filter: Optional[PeopleFilter] = None):
    peoples = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return peoples


@router.get("/{people_id}/", response_model=People)
async def people_get(people_id: int):
    db_people = await crud.get(db=db, people_id=people_id)
    if db_people is None:
        raise HTTPException(status_code=404, detail="People not found")
    return db_people


@router.delete("/{people_id}/", response_model=People)
async def people_delete(people_id: int):
    db_people = await crud.get(db=db, people_id=people_id)
    if db_people is None:
        raise HTTPException(status_code=404, detail="People not found")

    await crud.delete(db=db, people_id=people_id)

    return


@router.put("/{people_id}/", response_model=People)
async def people_update(people_id: int, people: PeopleUpdateIn):
    if not (await crud.check(db=db, people_id=people_id)):
        raise HTTPException(status_code=404, detail="People not found")

    return await crud.update(db=db, people_id=people_id, people=people)


@router.get("/{people_id}/organizations", response_model=List[Organization])
async def people_get_organizations(people_id: int):
    if not (await crud.check(db=db, people_id=people_id)):
        raise HTTPException(status_code=404, detail="People not found")

    return await organization.get_all(db=db, filter=OrganizationFilter(people_id=people_id))


@router.get("/{people_id}/contacts", response_model=List[Contact])
async def people_get_contacts(people_id: int):
    if not (await crud.check(db=db, people_id=people_id)):
        raise HTTPException(status_code=404, detail="People not found")

    return await contact.get_all(db=db, filter=ContactFilter(people_id=people_id))


@router.get("/{people_id}/vulnerabilities", response_model=List[Vulnerability])
async def people_get_vulnerabilitys(people_id: int):
    if not (await crud.check(db=db, people_id=people_id)):
        raise HTTPException(status_code=404, detail="People not found")

    return await vulnerability.get_all(db=db, filter=VulnerabilityFilter(people_id=people_id))
