from lxml import etree
from typing import List, Dict, Any


def parse():
    f = open("./nmap_example.xml")
    tree = etree.parse(f)

    nodes = tree.xpath("/nmaprun/host")

    hosts: List[Dict[str, Any]] = []
    for node in nodes:
        host = {}
        addr = node.find("address").attrib["addr"]
        ports = [port.attrib["portid"] for port in node.xpath("ports/port")]
        os = "; ".join(
            [
                " ".join([_os.get(attrib) for attrib in _os.attrib])
                for _os in node.xpath("os/osclass")
            ]
        )
        host["ip"] = addr
        host["os"] = os
        host["ports"] = ports
        hosts.append(host)

    for host in hosts:
        print(host)


if __name__ == "__main__":
    parse()
