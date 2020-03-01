__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import organizations_networks as model


async def create(db: Database, organization_id: int, network_id: int) -> None:
    await db.execute(model.insert().values(network_id=network_id, organization_id=organization_id))

    return


async def update(db: Database, organization_ids: List[int], network_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(
                model.c.network_id == network_id,
                not_(model.c.organization_id.in_(organization_ids)),
            )
        )
    )

    for oid in organization_ids:
        if not await db.execute(
            model.exists().where(
                and_(model.c.network_id == network_id, model.c.organization_id == oid,)
            )
        ):
            await db.execute(model.insert().values(network_id=network_id, organization_id=oid))

    return


async def get_all(
    db: Database, network_id: Optional[int] = None, organization_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if network_id is not None:
        return await db.fetch_all(model.select().where(model.c.network_id == network_id))
    elif organization_id is not None:
        return await db.fetch_all(model.select().where(model.c.organization_id == organization_id))
    else:
        return await db.fetch_all(model.select().where())
