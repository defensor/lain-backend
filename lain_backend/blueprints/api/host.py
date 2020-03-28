from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import host as crud, domain, service, hosts_domains
from lain_backend.schemas import (
    Host,
    HostCreate,
    HostIn,
    HostUpdate,
    HostUpdateIn,
    Service,
    Domain,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Host)
async def host_create(host: HostIn):
    return await crud.create(db=db, host=HostCreate(**host.dict()))


@router.put("/", response_model=List[Host])
async def host_get_all(skip: int = 0, limit: int = 100):
    return await crud.get_all(db=db, skip=skip, limit=limit)


@router.get("/{host_id}/", response_model=Host)
async def host_get(host_id: int):
    db_host = await crud.get(db=db, host_id=host_id)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host


@router.delete("/{host_id}/", response_model=Host)
async def host_delete(host_id: int):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    await crud.delete(db=db, host_id=host_id)


@router.put("/{host_id}/", response_model=Host)
async def host_update(host_id: int, host: HostUpdateIn):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await crud.update(db=db, host_id=host_id, host=HostUpdate(**host.dict()))


@router.get("/{host_id}/services", response_model=List[Service])
async def host_get_services(host_id: int):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await service.get_all(db=db, host_id=host_id)


@router.get("/{host_id}/domains", response_model=List[Domain])
async def host_get_domains(host_id: int):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    return await domain.get_all(db=db, host_id=host_id)


@router.post("/{host_id}/domains/{domain_id}")
async def host_append_domain(host_id: int, domain_id: int):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    if not (await domain.exist(db=db, domain_id=domain_id)):
        raise HTTPException(status_code=404, detail="Domain not found")

    if await hosts_domains.exist(db=db, host_id=host_id, domain_id=domain_id):
        raise HTTPException(status_code=400, detail="Relation already exist")

    await hosts_domains.create(db=db, host_id=host_id, domain_id=domain_id)


@router.delete("/{host_id}/domains/{domain_id}")
async def host_remove_domain(host_id: int, domain_id: int):
    if not (await crud.exist(db=db, host_id=host_id)):
        raise HTTPException(status_code=404, detail="Host not found")

    if not (await domain.exist(db=db, domain_id=domain_id)):
        raise HTTPException(status_code=404, detail="Domain not found")

    if not (await hosts_domains.exist(db=db, host_id=host_id, domain_id=domain_id)):
        raise HTTPException(status_code=400, detail="Relation not found")

    await hosts_domains.delete(db=db, host_id=host_id, domain_id=domain_id)
