from databases import Database
from lain_backend.cruds import domain, host, service
from . import nmap_importer


async def import_data(db: Database, filename: str):
    nmap_importer.parse(filename=filename)

    for in_host in nmap_importer.hosts():
        db_host = await host.create(db=db, host=in_host)
        if db_host is None:
            return None

        host_id = db_host.id

        for in_domain in nmap_importer.domains():
            domain_id = await domain.create(db=db, domain=in_domain)

        for in_service in nmap_importer.services():
            in_service.host_id = host_id

            await service.create(db=db, service=in_service)
