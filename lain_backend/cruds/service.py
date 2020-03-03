__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import (
    Service as model,
    services_credentials,
    services_protocols,
    services_vulnerabilities,
)
from lain_backend.schemas import (
    ServiceCreate,
    ServiceIn,
    ServiceUpdate,
    ServiceUpdateIn,
    ServiceInnerFilter,
    ServiceOuterFilter,
    ServiceFilter,
)
from lain_backend.cruds import services_protocols


async def create(db: Database, service: ServiceIn) -> Optional[Mapping[Any, Any]]:
    service_create = ServiceCreate(**service.dict())

    service_id = await db.execute(model.insert().values(**service_create.dict()))

    if service.protocol_ids is not None:
        for pid in service.protocol_ids:
            await services_protocols.create(db=db, service_id=service_id, protocol_id=pid)

    return await get(db=db, service_id=service_id)


async def get(db: Database, service_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == service_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[ServiceFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, service_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == service_id))

    return


async def update(
    db: Database, service: ServiceUpdateIn, service_id: int
) -> Optional[Mapping[Any, Any]]:
    service_update = ServiceUpdate(**service.dict())

    if service_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**service_update.dict(exclude_none=True)})
            .where(model.c.id == service_id)
        )

    if service.protocol_ids is not None:
        await services_protocols.update(
            db=db, protocol_ids=service.protocol_ids, service_id=service_id
        )

    return await get(db=db, service_id=service_id)


async def check(db: Database, service_id: int) -> bool:
    return (await get(db=db, service_id=service_id)) is not None


def _compile_filter(filter: ServiceFilter) -> str:
    iFilter = ServiceInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = ServiceOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "service_id"

    relations = {
        "protocol_id": "services_protocols",
        "vulnerability_id": "services_vulnerabilities",
        "credential_id": "services_credentials",
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
