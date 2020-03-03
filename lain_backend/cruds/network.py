__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Network as model
from lain_backend.schemas import (
    NetworkCreate,
    NetworkIn,
    NetworkUpdate,
    NetworkUpdateIn,
    NetworkFilter,
    NetworkInnerFilter,
    NetworkOuterFilter,
)
from lain_backend.cruds import organizations_networks


async def create(db: Database, network: NetworkIn) -> Optional[Mapping[Any, Any]]:
    network_create = NetworkCreate(**network.dict())

    network_id = await db.execute(model.insert().values(**network_create.dict()))

    if network.organization_ids is not None:
        for oid in network.organization_ids:
            await organizations_networks.create(db=db, organization_id=oid, network_id=network_id)

    return await get(db=db, network_id=network_id)


async def get(db: Database, network_id: int) -> Optional[Mapping[Any, Any]]:
    return await db.fetch_one(model.select().where(model.c.id == network_id))


async def get_all(
    db: Database, skip: int = 0, limit: int = 100, filter: Optional[NetworkFilter] = None
) -> List[Mapping[Any, Any]]:
    if filter is None:
        return await db.fetch_all(model.select().offset(skip).limit(limit))

    return await db.fetch_all(
        query=_compile_filter(filter), values={"offset": skip, "limit": limit}
    )


async def delete(db: Database, network_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == network_id))

    return


async def update(
    db: Database, network: NetworkUpdateIn, network_id: int
) -> Optional[Mapping[Any, Any]]:
    network_update = NetworkUpdate(**network.dict())

    if network_update.dict(exclude_none=True):
        await db.execute(
            model.update()
            .values({**network_update.dict(exclude_none=True)})
            .where(model.c.id == network_id)
        )

    if network.organization_ids is not None:
        await organizations_networks.update(
            db=db, organization_ids=network.organization_ids, network_id=network_id
        )

    return await get(db=db, network_id=network_id)


async def check(db: Database, network_id: int) -> bool:
    return (await get(db=db, network_id=network_id)) is not None


async def exists(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None


def _compile_filter(filter: NetworkFilter) -> str:
    iFilter = NetworkInnerFilter(**filter.dict()).dict(exclude_none=True)
    oFilter = NetworkOuterFilter(**filter.dict()).dict(exclude_none=True)

    table_name = model.fullname
    ref_name = "network_id"

    relations = {
        "organization_id": "organizations_networks",
        "vulnerability_id": "networks_vulnerabilities",
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
