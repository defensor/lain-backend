from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import credential as crud, service
from lain_backend.schemas import (
    Credential,
    CredentialIn,
    CredentialUpdateIn,
    CredentialFilter,
    Service,
    ServiceFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Credential)
async def credential_create(credential: CredentialIn):
    return await crud.create(db=db, credential=credential)


@router.put("/", response_model=List[Credential])
async def credential_get_all(
    skip: int = 0, limit: int = 100, filter: Optional[CredentialFilter] = None
):
    credentials = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return credentials


@router.get("/{credential_id}/", response_model=Credential)
async def credential_get(credential_id: int):
    db_credential = await crud.get(db=db, credential_id=credential_id)
    if db_credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    return db_credential


@router.delete("/{credential_id}/", response_model=Credential)
async def credential_delete(credential_id: int):
    db_credential = await crud.get(db=db, credential_id=credential_id)
    if db_credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")

    await crud.delete(db=db, credential_id=credential_id)

    return


@router.put("/{credential_id}/", response_model=Credential)
async def credential_update(credential_id: int, credential: CredentialUpdateIn):
    if not (await crud.check(db=db, credential_id=credential_id)):
        raise HTTPException(status_code=404, detail="Credential not found")

    return await crud.update(db=db, credential_id=credential_id, credential=credential)


@router.get("/{credential_id}/services", response_model=List[Service])
async def credential_get_services(credential_id: int):
    if not (await crud.check(db=db, credential_id=credential_id)):
        raise HTTPException(status_code=404, detail="Credential not found")

    return await service.get_all(db=db, filter=ServiceFilter(credential_id=credential_id))
