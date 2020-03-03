from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import service as crud, vulnerability, credential, protocol
from lain_backend.schemas import (
    Service,
    ServiceIn,
    ServiceUpdateIn,
    ServiceFilter,
    Vulnerability,
    VulnerabilityFilter,
    Credential,
    CredentialFilter,
    Protocol,
    ProtocolFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Service)
async def service_create(service: ServiceIn):
    return await crud.create(db=db, service=service)


@router.put("/", response_model=List[Service])
async def service_get_all(skip: int = 0, limit: int = 100, filter: Optional[ServiceFilter] = None):
    services = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return services


@router.get("/{service_id}/", response_model=Service)
async def service_get(service_id: int):
    db_service = await crud.get(db=db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@router.delete("/{service_id}/", response_model=Service)
async def service_delete(service_id: int):
    db_service = await crud.get(db=db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    await crud.delete(db=db, service_id=service_id)

    return


@router.put("/{service_id}/", response_model=Service)
async def service_update(service_id: int, service: ServiceUpdateIn):
    if not (await crud.check(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await crud.update(db=db, service_id=service_id, service=service)


@router.get("/{service_id}/vulnerabilitys", response_model=List[Vulnerability])
async def service_get_vulnerabilities(service_id: int):
    if not (await crud.check(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await vulnerability.get_all(db=db, filter=VulnerabilityFilter(service_id=service_id))


@router.get("/{service_id}/credentials", response_model=List[Credential])
async def service_get_credentials(service_id: int):
    if not (await crud.check(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await credential.get_all(db=db, filter=CredentialFilter(service_id=service_id))


@router.get("/{service_id}/protocols", response_model=List[Protocol])
async def service_get_protocols(service_id: int):
    if not (await crud.check(db=db, service_id=service_id)):
        raise HTTPException(status_code=404, detail="Service not found")

    return await protocol.get_all(db=db, filter=ProtocolFilter(service_id=service_id))
