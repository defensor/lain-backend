from libnmap.parser import NmapParser
from pydantic import IPvAnyAddress
from lain_backend.schemas import HostCreate, ServiceCreate, DomainCreate


report = None
current_host = None


def parse(filename: str):
    global report

    report = NmapParser.parse_fromfile(filename)


def hosts():
    global current_host
    if report is None:
        return None

    for host in report.hosts:
        current_host = host
        yield HostCreate(addr=host.address, os=host.os_fingerprint or None)


def domains():
    if current_host is None:
        return None

    for hostname in current_host.hostnames:
        try:
            IPvAnyAddress.validate(hostname)
        except:
            yield DomainCreate(name=hostname)


def services():
    if current_host is None:
        return None

    for port in current_host.get_ports():
        service = current_host.get_service(portno=port[0])

        yield ServiceCreate(
            port=port[0],
            proto3=service.protocol,
            proto7=service.service,
            version=service.service_dict["product"]
            if "product" in service.service_dict
            else None,
            host_id=0,
        )
