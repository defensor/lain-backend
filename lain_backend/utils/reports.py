import json

from databases import Database
from lain_backend.cruds import domain as domain_crud
from lain_backend.cruds import host as host_crud
from lain_backend.cruds import service as service_crud
from lain_backend.schemas.domain import DomainOut
from lain_backend.schemas.host import HostOut
from lain_backend.schemas.service import ServiceOut


async def make_json_report(db: Database):
    report = {}
    hosts = await host_crud.list(db)

    for host in hosts:
        host_id = host.id

        # get all domains
        host_domains = []

        domains = await domain_crud.list(db, host_id=host_id)

        for domain in domains:
            host_domains.append(DomainOut(**domain.dict()).dict())

        # get all services
        host_services = []

        services = await service_crud.list(db, host_id=host_id)

        for service in services:
            host_services.append(ServiceOut(**service.dict()).dict())

        report[str(host.addr)] = {
            **HostOut(**host.dict()).dict(exclude={"addr"}),
            "domains": host_domains,
            "services": host_services,
        }

    return report
