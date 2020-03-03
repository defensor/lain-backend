__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Protocol as model
from lain_backend.schemas import (
    ProtocolCreate,
    ProtocolIn,
    ProtocolUpdate,
    ProtocolUpdateIn,
    ProtocolFilter,
    ProtocolInnerFilter,
    ProtocolOuterFilter,
)


async def create(db: Database, protocol: ProtocolIn) -> Optional[Mapping[Any, Any]]:
    protocol_create = ProtocolCreate(**protocol.dict())

    protocol_id = await db.execute(model.insert().values(**protocol_create.dict()))

    return await get(db=db, protocol_id=protocol_id)


async def get(db: Database, protocol_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == protocol_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[ProtocolFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, protocol_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == protocol_id))

    return


async def update(
    db: Database, protocol: ProtocolUpdateIn, protocol_id: int
) -> Optional[Mapping[Any, Any]]:
    protocol_update = ProtocolUpdate(**protocol.dict())

    if protocol_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**protocol_update.dict(exclude_none=True)})
            .where(model.c.id == protocol_id)
        )

    return await get(db=db, protocol_id=protocol_id)


async def check(db: Database, protocol_id: int) -> bool:
    return (await get(db=db, protocol_id=protocol_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None


def _compile_filter(filter: ProtocolFilter) -> str:
    iFilter = ProtocolInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = ProtocolOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "protocol_id"

    relations = {
        "service_id": "services_protocols",
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
