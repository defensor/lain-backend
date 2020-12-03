from databases import Database
from lain_backend.cruds import domain as domain_crud
from lain_backend.cruds import host as host_crud
from lain_backend.cruds import hosts_domains as hosts_domains_crud
from lain_backend.cruds import service as service_crud
from lain_backend.schemas.domain import DomainCreate
from lain_backend.schemas.host import HostCreate
from lain_backend.schemas.service import ServiceCreate

from .nmap_importer import NMapParser


async def import_data(db: Database, file: bytes):
    nmap_rep = NMapParser(file)

    for host in nmap_rep.hosts():
        db_host = await host_crud.create(
            db=db, host=HostCreate(**host.dict(exclude_none=True))
        )
        if db_host is None:
            raise ValueError("Invalid host data")

        host_id = db_host.id

        for domain in host.domains:
            db_domain = await domain_crud.create(
                db=db, domain=DomainCreate(**domain.dict(exclude_none=True))
            )
            if db_domain is None:
                raise ValueError("Invalid domain data")

            await hosts_domains_crud.create(
                db=db, host_id=host_id, domain_id=db_domain.id
            )

        for service in host.services:
            db_service = await service_crud.create(
                db=db,
                service=ServiceCreate(
                    **service.dict(exclude_none=True), host_id=host_id
                ),
            )
            if db_service is None:
                raise ValueError("Invalid service data")
