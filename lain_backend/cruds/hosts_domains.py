from typing import List, Optional
from databases import Database
from sqlalchemy import and_

from lain_backend.models import hosts_domains as model
from lain_backend.schemas import HostDomain


async def create(db: Database, host_id: int, domain_id: int) -> None:
    await db.execute(model.insert().values(domain_id=domain_id, host_id=host_id))


async def delete(db: Database, host_id: int, domain_id: int) -> None:
    await db.execute(
        model.delete().where(
            and_(model.c.domain_id == domain_id, model.c.host_id == host_id)
        )
    )


async def list(
    db: Database, domain_id: Optional[int] = None, host_id: Optional[int] = None
) -> List[HostDomain]:
    if domain_id is not None:
        hosts_domains = await db.fetch_all(
            model.select().where(model.c.domain_id == domain_id)
        )
    elif host_id is not None:
        hosts_domains = await db.fetch_all(
            model.select().where(model.c.host_id == host_id)
        )
    else:
        hosts_domains = await db.fetch_all(model.select().where())

    return [HostDomain(**host_domain) for host_domain in hosts_domains]


async def exist(db: Database, domain_id: int, host_id: int) -> bool:
    return (
        db.fetch_one(
            model.select().where(
                and_(model.c.domain_id == domain_id, model.c.host_id == host_id)
            )
        )
    ) is not None
