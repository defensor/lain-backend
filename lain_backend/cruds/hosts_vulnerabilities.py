__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import hosts_vulnerabilities as model


async def create(db: Database, host_id: int, vulnerability_id: int) -> None:
    await db.execute(model.insert().values(vulnerability_id=vulnerability_id, host_id=host_id))

    return


async def update(db: Database, host_ids: List[int], vulnerability_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.vulnerability_id == vulnerability_id, model.c.host_id.notin_(host_ids),)
        )
    )

    for hid in host_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.vulnerability_id == vulnerability_id, model.c.host_id == hid,)
                )
            )
        ) is None:
            await db.execute(model.insert().values(vulnerability_id=vulnerability_id, host_id=hid))

    return


async def get_all(
    db: Database, vulnerability_id: Optional[int] = None, host_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if vulnerability_id is not None:
        return await db.fetch_all(
            model.select().where(model.c.vulnerability_id == vulnerability_id)
        )
    elif host_id is not None:
        return await db.fetch_all(model.select().where(model.c.host_id == host_id))
    else:
        return await db.fetch_all(model.select().where())
