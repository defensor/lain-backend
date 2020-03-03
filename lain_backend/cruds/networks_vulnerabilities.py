__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import networks_vulnerabilities as model


async def create(db: Database, network_id: int, vulnerability_id: int) -> None:
    await db.execute(
        model.insert().values(vulnerability_id=vulnerability_id, network_id=network_id)
    )

    return


async def update(db: Database, network_ids: List[int], vulnerability_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(
                model.c.vulnerability_id == vulnerability_id,
                model.c.network_id.notin_(network_ids),
            )
        )
    )

    for nid in network_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.vulnerability_id == vulnerability_id, model.c.network_id == nid,)
                )
            )
        ) is None:
            await db.execute(
                model.insert().values(vulnerability_id=vulnerability_id, network_id=nid)
            )

    return


async def get_all(
    db: Database, vulnerability_id: Optional[int] = None, network_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if vulnerability_id is not None:
        return await db.fetch_all(
            model.select().where(model.c.vulnerability_id == vulnerability_id)
        )
    elif network_id is not None:
        return await db.fetch_all(model.select().where(model.c.network_id == network_id))
    else:
        return await db.fetch_all(model.select().where())
