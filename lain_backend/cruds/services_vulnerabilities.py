__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_, not_

from lain_backend.models import services_vulnerabilities as model


async def create(db: Database, service_id: int, vulnerability_id: int) -> None:
    await db.execute(
        model.insert().values(vulnerability_id=vulnerability_id, service_id=service_id)
    )

    return


async def update(db: Database, service_ids: List[int], vulnerability_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(
                model.c.vulnerability_id == vulnerability_id,
                not_(model.c.service_id.in_(service_ids)),
            )
        )
    )

    for oid in service_ids:
        if not await db.execute(
            model.exists().where(
                and_(model.c.vulnerability_id == vulnerability_id, model.c.service_id == oid,)
            )
        ):
            await db.execute(
                model.insert().values(vulnerability_id=vulnerability_id, service_id=oid)
            )

    return


async def get_all(
    db: Database, vulnerability_id: Optional[int] = None, service_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if vulnerability_id is not None:
        return await db.fetch_all(
            model.select().where(model.c.vulnerability_id == vulnerability_id)
        )
    elif service_id is not None:
        return await db.fetch_all(model.select().where(model.c.service_id == service_id))
    else:
        return await db.fetch_all(model.select().where())
