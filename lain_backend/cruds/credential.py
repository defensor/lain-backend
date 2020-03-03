__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Credential as model
from lain_backend.schemas import (
    CredentialCreate,
    CredentialIn,
    CredentialUpdate,
    CredentialUpdateIn,
    CredentialFilter,
    CredentialInnerFilter,
    CredentialOuterFilter,
)
from lain_backend.cruds import services_credentials


async def create(db: Database, credential: CredentialIn) -> Optional[Mapping[Any, Any]]:
    credential_create = CredentialCreate(**credential.dict())

    credential_id = await db.execute(model.insert().values(**credential_create.dict()))

    if credential.service_ids is not None:
        for sid in credential.service_ids:
            await services_credentials.create(db=db, service_id=sid, credential_id=credential_id)

    return await get(db=db, credential_id=credential_id)


async def get(db: Database, credential_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == credential_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[CredentialFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, credential_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == credential_id))

    return


async def update(
    db: Database, credential: CredentialUpdateIn, credential_id: int
) -> Optional[Mapping[Any, Any]]:
    credential_update = CredentialUpdate(**credential.dict())

    if credential_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**credential_update.dict(exclude_none=True)})
            .where(model.c.id == credential_id)
        )

    if credential.service_ids is not None:
        await services_credentials.update(
            db=db, service_ids=credential.service_ids, credential_id=credential_id
        )

    return await get(db=db, credential_id=credential_id)


async def check(db: Database, credential_id: int) -> bool:
    return (await get(db=db, credential_id=credential_id)) is not None


def _compile_filter(filter: CredentialFilter) -> str:
    iFilter = CredentialInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = CredentialOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "credential_id"

    relations = {
        "serivice_id": "services_credentials",
    }

    statement = (
        " AND ".join(
            [
                f"{table_name}.{key} = '{iFilter[key]}'"
                if isinstance(iFilter[key], str)
                else f"{table_name}.{key} = {iFilter[key]}"
                for key in iFilter
            ]
            + [
                f"{table_name}.id = {relations[key]}.{ref_name} AND {relations[key]}.{key} = {oFilter[key]}"
                for key in oFilter
            ]
        )
        or "TRUE"
    )

    sources = ", ".join([table_name] + [relations[key] for key in oFilter])

    query = f"SELECT * FROM {sources} WHERE {statement} LIMIT :limit OFFSET :offset"
    return query
