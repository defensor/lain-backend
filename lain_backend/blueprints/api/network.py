from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import network as crud, organization, vulnerability
from lain_backend.schemas import (
    Network,
    NetworkIn,
    NetworkUpdateIn,
    NetworkFilter,
    Organization,
    OrganizationFilter,
    Vulnerability,
    VulnerabilityFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Network)
async def network_create(network: NetworkIn):
    return await crud.create(db=db, network=network)


@router.put("/", response_model=List[Network])
async def network_get_all(skip: int = 0, limit: int = 100, filter: Optional[NetworkFilter] = None):
    networks = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return networks


@router.get("/{network_id}/", response_model=Network)
async def network_get(network_id: int):
    db_network = await crud.get(db=db, network_id=network_id)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@router.delete("/{network_id}/", response_model=Network)
async def network_delete(network_id: int):
    db_network = await crud.get(db=db, network_id=network_id)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")

    await crud.delete(db=db, network_id=network_id)

    return


@router.put("/{network_id}/", response_model=Network)
async def network_update(network_id: int, network: NetworkUpdateIn):
    if not (await crud.check(db=db, network_id=network_id)):
        raise HTTPException(status_code=404, detail="Network not found")

    return await crud.update(db=db, network_id=network_id, network=network)


@router.get("/{network_id}/organizations", response_model=List[Organization])
async def network_get_organizations(network_id: int):
    if not (await crud.check(db=db, network_id=network_id)):
        raise HTTPException(status_code=404, detail="Network not found")

    return await organization.get_all(db=db, filter=OrganizationFilter(network_id=network_id))


@router.get("/{network_id}/vulnerabilities", response_model=List[Vulnerability])
async def network_get_vulnerabilitys(network_id: int):
    if not (await crud.check(db=db, network_id=network_id)):
        raise HTTPException(status_code=404, detail="Network not found")

    return await vulnerability.get_all(db=db, filter=VulnerabilityFilter(network_id=network_id))
