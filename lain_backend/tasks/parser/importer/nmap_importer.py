from lain_backend.schemas import nmap as nmap_scheme
from libnmap.parser import NmapParser

report = None
current_host = None


class NMapParser:
    def __init__(self, file: bytes):
        self.report = NmapParser.parse(file.decode("utf-8"))

    def hosts(self):
        for host in self.report.hosts:

            os = self.get_oss(host)
            domains = self.get_domains(host)
            services = self.get_services(host)

            yield nmap_scheme.HostCreate_Nmap(
                addr=host.address, os=os, domains=domains, services=services
            )

    @classmethod
    def get_services(cls, host):
        return [
            nmap_scheme.ServiceCreate_Nmap(
                port=service.port,
                state=service.state,
                proto3=service.protocol,
                proto7=service.service,
                version=service.service_dict.get("product"),
            )
            for service in host.services
        ]

    @classmethod
    def get_domains(cls, host):
        return [
            nmap_scheme.DomainCreate_Nmap(name=hostname) for hostname in host.hostnames
        ]

    @classmethod
    def get_oss(cls, host):
        return ", ".join(
            [os_class.__repr__() for os_class in host.os_class_probabilities()]
        )
