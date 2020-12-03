from typing import List

from lain_backend.schemas import domain, host, service


class ServiceCreate_Nmap(service.ServiceCreate):
    pass


class DomainCreate_Nmap(domain.DomainCreate):
    pass


class HostCreate_Nmap(host.HostCreate):
    domains: List[DomainCreate_Nmap] = []
    services: List[ServiceCreate_Nmap] = []
