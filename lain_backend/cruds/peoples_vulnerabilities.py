__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import peoples_vulnerabilities as model


async def create(db: Database, people_id: int, vulnerability_id: int) -> None:
    await db.execute(model.insert().values(vulnerability_id=vulnerability_id, people_id=people_id))

    return


async def update(db: Database, people_ids: List[int], vulnerability_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(
                model.c.vulnerability_id == vulnerability_id,
                not_(model.c.people_id.in_(people_ids)),
            )
        )
    )

    for oid in people_ids:
        if not await db.execute(
            model.exists().where(
                and_(model.c.vulnerability_id == vulnerability_id, model.c.people_id == oid,)
            )
        ):
            await db.execute(
                model.insert().values(vulnerability_id=vulnerability_id, people_id=oid)
            )

    return


async def get_all(
    db: Database, vulnerability_id: Optional[int] = None, people_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if vulnerability_id is not None:
        return await db.fetch_all(
            model.select().where(model.c.vulnerability_id == vulnerability_id)
        )
    elif people_id is not None:
        return await db.fetch_all(model.select().where(model.c.people_id == people_id))
    else:
        return await db.fetch_all(model.select().where())
