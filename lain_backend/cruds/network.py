__all__ = ["create", "get", "get_all", "update", "delete", "exist", "exist_name"]

from typing import List, Optional
from databases import Database

from lain_backend.models import Network as model
from lain_backend.schemas import (
    Network,
    NetworkCreate,
    NetworkUpdate,
)
from lain_backend.cruds import organizations_networks


async def create(db: Database, network: NetworkCreate) -> Optional[Network]:
    network_id = await db.execute(model.insert().values(**network.dict()))

    return await get(db=db, network_id=network_id)


async def get(db: Database, network_id: int) -> Optional[Network]:
    network = await db.fetch_one(model.select().where(model.c.id == network_id))

    if network is not None:
        return Network(**network)
    else:
        return None


async def get_all(db: Database, skip: int = 0, limit: int = 100,) -> List[Network]:
    networks = await db.fetch_all(model.select().offset(skip).limit(limit))

    return [Network(**network) for network in networks]


async def delete(db: Database, network_id: int) -> None:
    await db.execute(model.delete().where(model.c.id == network_id))


async def update(
    db: Database, network: NetworkUpdate, network_id: int
) -> Optional[Network]:
    await db.execute(
        model.update()
        .values({**network.dict(exclude_none=True)})
        .where(model.c.id == network_id)
    )

    return await get(db=db, network_id=network_id)


async def exist(db: Database, network_id: int) -> bool:
    return (await get(db=db, network_id=network_id)) is not None


async def exist_name(db: Database, name: str) -> bool:
    return (await db.fetch_one(model.select().where(model.c.name == name))) is not None
