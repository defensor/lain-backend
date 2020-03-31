from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import organization as crud, host, organizations_hosts
from lain_backend.schemas import (
    Organization,
    OrganizationCreate,
    OrganizationIn,
    OrganizationUpdate,
    OrganizationUpdateIn,
    Host,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Organization)
async def organization_create(organization: OrganizationIn):
    if await crud.exist_name(db=db, name=organization.name):
        raise HTTPException(
            status_code=400, detail="Organization with this name already exist"
        )

    return await crud.create(
        db=db, organization=OrganizationCreate(**organization.dict())
    )


@router.put("/", response_model=List[Organization])
async def organization_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{organization_id}/", response_model=Organization)
async def organization_get(organization_id: int):
    db_organization = await crud.get(db=db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@router.delete("/{organization_id}/", response_model=Organization)
async def organization_delete(organization_id: int):
    if not (await crud.exist(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    await crud.delete(db=db, organization_id=organization_id)


@router.put("/{organization_id}/", response_model=Organization)
async def organization_update(organization_id: int, organization: OrganizationUpdateIn):
    if not (await crud.exist(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    if organization.name is not None:
        if await crud.exist_name(db=db, name=organization.name):
            raise HTTPException(
                status_code=400, detail="Organization with this name already exist"
            )

    return await crud.update(
        db=db,
        organization_id=organization_id,
        organization=OrganizationUpdate(**organization.dict()),
    )


@router.get("/{organization_id}/hosts", response_model=List[Host])
async def organization_get_hosts(organization_id):
    if not (await crud.exist(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    return await host.get_all(db=db, organization_id=organization_id)


@router.post("/{organization_id}/hosts/{host_id}")
async def organization_append_host(organization_id: int, host_id: int):
    if not (await crud.exist(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    if not (await host.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    if await organizations_hosts.exist(
        db=db, organization_id=organization_id, host_id=host_id
    ):
        raise HTTPException(status_code=400, detail="Relation already exist")

    await organizations_hosts.create(
        db=db, organization_id=organization_id, host_id=host_id
    )


@router.delete("/{organization_id}/hosts/{host_id}")
async def organization_remove_host(organization_id: int, host_id: int):
    if not (await crud.exist(db=db, organization_id=organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    if not (await host.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    if not (
        await organizations_hosts.exist(
            db=db, organization_id=organization_id, host_id=host_id
        )
    ):
        raise HTTPException(status_code=400, detail="Relation not found")

    await organizations_hosts.delete(
        db=db, organization_id=organization_id, host_id=host_id
    )
