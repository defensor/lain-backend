from typing import List, Optional

from databases import Database
from lain_backend.models import organizations_hosts as model
from lain_backend.schemas.organizations_hosts import OrganizationHost
from sqlalchemy import and_


async def create(db: Database, organization_id: int, host_id: int) -> None:
    await db.execute(
        model.insert().values(host_id=host_id, organization_id=organization_id)
    )


async def delete(db: Database, organization_id: int, host_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(host_id == host_id, organization_id == organization_id)
        )
    )


async def list(
    db: Database, host_id: Optional[int] = None, organization_id: Optional[int] = None,
) -> List[OrganizationHost]:
    if host_id is not None:
        organizations_hosts = await db.fetch_all(
            model.select().where(model.c.host_id == host_id)
        )
    elif organization_id is not None:
        organizations_hosts = await db.fetch_all(
            model.select().where(model.c.organization_id == organization_id)
        )
    else:
        organizations_hosts = await db.fetch_all(model.select().where())

    return [
        OrganizationHost(**organization_host)
        for organization_host in organizations_hosts
    ]


async def exist(db: Database, host_id: int, organization_id: int) -> bool:
    return (
        db.fetch_one(
            model.select().where(
                and_(
                    model.c.host_id == host_id,
                    model.c.organization_id == organization_id,
                )
            )
        )
    ) is not None
