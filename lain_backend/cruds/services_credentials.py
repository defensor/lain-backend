__all__ = ["create", "update", "get"]

from typing import List, Optional, Mapping, Any
from databases import Database
from sqlalchemy import and_

from lain_backend.models import services_credentials as model


async def create(db: Database, service_id: int, credential_id: int) -> None:
    await db.execute(model.insert().values(credential_id=credential_id, service_id=service_id))

    return


async def update(db: Database, service_ids: List[int], credential_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.credential_id == credential_id, model.c.service_id.notin_(service_ids))
        )
    )

    for sid in service_ids:
        if (
            await db.fetch_one(
                model.select().where(
                    and_(model.c.credential_id == credential_id, model.c.service_id == sid)
                )
            )
        ) is None:
            await db.execute(model.insert().values(credential_id=credential_id, service_id=sid))

    return


async def get_all(
    db: Database, credential_id: Optional[int] = None, service_id: Optional[int] = None
) -> List[Mapping[Any, Any]]:
    if credential_id is not None:
        return await db.fetch_all(model.select().where(model.c.credential_id == credential_id))
    elif service_id is not None:
        return await db.fetch_all(model.select().where(model.c.service_id == service_id))
    else:
        return await db.fetch_all(model.select().where())
