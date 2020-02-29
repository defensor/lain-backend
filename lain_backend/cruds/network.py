__all__ = ["create", "get", "get_all", "update", "delete", "check", "exists"]

from typing import List, Optional, Mapping, Any
from databases import Database

from lain_backend.models import Network as model
from lain_backend.schemas import (
    NetworkCreate,
    NetworkIn,
    NetworkUpdate,
    NetworkUpdateIn,
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


async def get_all(db: Database, skip: int = 0, limit: int = 100) -> List[Mapping[Any, Any]]:
    return await db.fetch_all(model.select().offset(skip).limit(limit))


async def delete(db: Database, network_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == network_id))

    return


async def update(
    db: Database, network: NetworkUpdateIn, network_id: int
) -> Optional[Mapping[Any, Any]]:
    network_update = NetworkUpdate(**network.dict())

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
    return await db.execute(model.exists().where(model.c.id == network_id))


async def exists(db: Database, name: str) -> bool:
    return await db.execute(model.exists().where(model.c.name == name))
