from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import host as crud, domain, vulnerability
from lain_backend.schemas import (
    Host,
    HostIn,
    HostUpdateIn,
    HostFilter,
    Domain,
    DomainFilter,
    Vulnerability,
    VulnerabilityFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Host)
async def host_create(host: HostIn):
    return await crud.create(db=db, host=host)


@router.put("/", response_model=List[Host])
async def host_get_all(skip: int = 0, limit: int = 100, filter: Optional[HostFilter] = None):
    hosts = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return hosts


@router.get("/{host_id}/", response_model=Host)
async def host_get(host_id: int):
    db_host = await crud.get(db=db, host_id=host_id)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host


@router.delete("/{host_id}/", response_model=Host)
async def host_delete(host_id: int):
    db_host = await crud.get(db=db, host_id=host_id)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")

    await crud.delete(db=db, host_id=host_id)

    return


@router.put("/{host_id}/", response_model=Host)
async def host_update(host_id: int, host: HostUpdateIn):
    if not (await crud.check(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await crud.update(db=db, host_id=host_id, host=host)


@router.get("/{host_id}/domains", response_model=List[Domain])
async def host_get_domains(host_id: int):
    if not (await crud.check(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await domain.get_all(db=db, filter=DomainFilter(host_id=host_id))


@router.get("/{host_id}/vulnerabilities", response_model=List[Vulnerability])
async def host_get_vulnerabilitys(host_id: int):
    if not (await crud.check(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await vulnerability.get_all(db=db, filter=VulnerabilityFilter(host_id=host_id))
