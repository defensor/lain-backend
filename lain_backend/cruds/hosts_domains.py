__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import hosts_domains as model


async def create(db: Database, host_id: int, domain_id: int) -> None:
    await db.execute(model.insert().values(domain_id=domain_id, host_id=host_id))

    return


async def update(db: Database, host_ids: List[int], domain_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.domain_id == domain_id, not_(model.c.host_id.in_(host_ids)),)
        )
    )

    for oid in host_ids:
        if not await db.execute(
            model.exists().where(and_(model.c.domain_id == domain_id, model.c.host_id == oid,))
        ):
            await db.execute(model.insert().values(domain_id=domain_id, host_id=oid))

    return


async def get_all(
    db: Database, domain_id: Optional[int] = None, host_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if domain_id is not None:
        return await db.fetch_all(model.select().where(model.c.domain_id == domain_id))
    elif host_id is not None:
        return await db.fetch_all(model.select().where(model.c.host_id == host_id))
    else:
        return await db.fetch_all(model.select().where())
