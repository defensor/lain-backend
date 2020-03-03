from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import organization as crud, building, network, people, contact
from lain_backend.schemas import (
    Organization,
    OrganizationIn,
    OrganizationUpdateIn,
    Organization,
    OrganizationFilter,
    Building,
    BuildingFilter,
    Network,
    NetworkFilter,
    People,
    PeopleFilter,
    Contact,
    ContactFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Organization)
async def organization_create(organization: OrganizationIn):
    if await crud.exists(db=db, name=organization.name):
        raise HTTPException(status_code=400, detail="Organization with this name already exist")

    return await crud.create(db=db, organization=organization)


@router.put("/", response_model=List[Organization])
async def organization_get_all(
    skip: int = 0, limit: int = 100, filter: Optional[OrganizationFilter] = None
):
    organizations = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return organizations


@router.get("/{organization_id}/", response_model=Organization)
async def organization_get(organization_id: int):
    db_organization = await crud.get(db=db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@router.delete("/{organization_id}/", response_model=Organization)
async def organization_delete(organization_id: int):
    db_organization = await crud.get(db=db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")

    await crud.delete(db=db, organization_id=organization_id)

    return


@router.put("/{organization_id}/", response_model=Organization)
async def organization_update(organization_id: int, organization: OrganizationUpdateIn):
    if not (await crud.check(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    if organization.name is not None:
        if await crud.exists(db=db, name=organization.name):
            raise HTTPException(status_code=400, detail="Organization with this name already exist")

    return await crud.update(db=db, organization_id=organization_id, organization=organization)


@router.get("/{organization_id}/buildings", response_model=List[Building])
async def organization_get_buildings(organization_id: int):
    if not (await crud.check(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    return await building.get_all(db=db, filter=BuildingFilter(organization_id=organization_id))


@router.get("/{organization_id}/networks", response_model=List[Network])
async def organization_get_networks(organization_id: int):
    if not (await crud.check(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    return await network.get_all(db=db, filter=NetworkFilter(organization_id=organization_id))


@router.get("/{organization_id}/peoples", response_model=List[People])
async def organization_get_peoples(organization_id: int):
    if not (await crud.check(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    return await people.get_all(db=db, filter=PeopleFilter(organization_id=organization_id))


@router.get("/{organization_id}/contacts", response_model=List[Contact])
async def organization_get_contacts(organization_id: int):
    if not (await crud.check(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    return await contact.get_all(db=db, filter=ContactFilter(organization_id=organization_id))
