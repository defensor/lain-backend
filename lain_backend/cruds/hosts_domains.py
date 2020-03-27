__all__ = ["create", "delete", "get_all", "exist"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import hosts_domains as model


async def create(db: Database, host_id: int, domain_id: int) -> None:
    await db.execute(model.insert().values(domain_id=domain_id, host_id=host_id))


async def delete(db: Database, host_id: int, domain_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.domain_id == domain_id, model.c.host_id == host_id)
        )
    )


async def get_all(
    db: Database, domain_id: Optional[int] = None, host_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if domain_id is not None:
        return await db.fetch_all(model.select().where(model.c.domain_id == domain_id))
    elif host_id is not None:
        return await db.fetch_all(model.select().where(model.c.host_id == host_id))
    else:
        return await db.fetch_all(model.select().where())


async def exist(db: Database, domain_id: int, host_id: int) -> bool:
    return (
        db.fetch_one(
            model.select().where(
                and_(model.c.domain_id == domain_id, model.c.host_id == host_id)
            )
        )
    ) is not None
