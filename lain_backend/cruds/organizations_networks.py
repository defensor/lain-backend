__all__ = ["create", "delete", "get_all", "exist"]

from typing import List, Optional
from databases import Database
from sqlalchemy import and_

from lain_backend.models import organizations_networks as model
from lain_backend.schemas import OrganizationNetwork


async def create(db: Database, organization_id: int, network_id: int) -> None:
    await db.execute(
        model.insert().values(network_id=network_id, organization_id=organization_id)
    )


async def delete(db: Database, organization_id: int, network_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(network_id == network_id, organization_id == organization_id)
        )
    )


async def get_all(
    db: Database,
    network_id: Optional[int] = None,
    organization_id: Optional[int] = None,
) -> List[OrganizationNetwork]:
    if network_id is not None:
        organizations_networks = await db.fetch_all(
            model.select().where(model.c.network_id == network_id)
        )
    elif organization_id is not None:
        organizations_networks = await db.fetch_all(
            model.select().where(model.c.organization_id == organization_id)
        )
    else:
        organizations_networks = await db.fetch_all(model.select().where())

    return [
        OrganizationNetwork(**organization_network)
        for organization_network in organizations_networks
    ]


async def exist(db: Database, network_id: int, organization_id: int) -> bool:
    return (
        db.fetch_one(
            model.select().where(
                and_(
                    model.c.network_id == network_id,
                    model.c.organization_id == organization_id,
                )
            )
        )
    ) is not None
