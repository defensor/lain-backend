from xml.sax import saxutils, make_parser
from xml.sax.handler import ContentHandler
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from dataclasses import dataclass, field as dc_field
from lain_backend.schemas import HostIn, ServiceIn, DomainIn


class Method(Enum):
    CREATE = "create"
    SET = "set"
    APPEND = "append"
    MULTI_SET = "multi_set"


@dataclass
class Event:
    obj: type
    method: Method
    field: Optional[str] = None
    attr: Optional[str] = None
    attrs: List[str] = dc_field(default_factory=list)


class RoadMapType(Enum):
    START = auto()
    END = auto()


@dataclass
class RoadMap:
    route: str
    type: RoadMapType
    event: Event


routes_events_map = {
    "/nmaprun/host": [Event(obj=HostIn, method=Method("create"))],
    "/nmaprun/host/address": [Event(obj=HostIn, field="addr", method=Method("set"), attr="addr")],
    "/nmaprun/host/hostnames/hostname": [
        Event(obj=DomainIn, method=Method("create")),
        Event(obj=DomainIn, field="name", method=Method("set"), attr="name"),
    ],
    "/nmaprun/host/ports/port": [
        Event(obj=ServiceIn, method=Method("create")),
        Event(obj=ServiceIn, field="port", method=Method("set"), attr="portid"),
    ],
    "/nmaprun/host/ports/port/service": [
        Event(
            obj=ServiceIn,
            field="version",
            method=Method("multi_set"),
            attrs=["name", "product", "version", "extrainfo"],
        )
    ],
    "/nmaprun/host/os/osmatch": [
        Event(obj=HostIn, field="os", method=Method("append"), attr="name")
    ],
}


data: Dict[str, List[Dict[str, Any]]] = {
    HostIn.__name__: [],
    ServiceIn.__name__: [],
    DomainIn.__name__: [],
}


def method_create(objects, event, attrs):
    objects.append({})


def method_set(objects, event, attrs):
    objects[-1][event.field] = attrs[event.attr]


def method_append(objects, event, attrs):
    if objects[-1].get(event.field) is None:
        objects[-1][event.field] = attrs[event.attr]
    else:
        objects[-1][event.field] += attrs[event.attr]


def method_multi_set(objects, event, attrs):
    objects[-1][event.field] = "; ".join(
        [attrs[attr_key] for attr_key in event.attrs if attr_key in attrs]
    )


methods = {
    Method.CREATE: lambda objects, event, attrs: method_create(objects, event, attrs),
    Method.SET: lambda objects, event, attrs: method_set(objects, event, attrs),
    Method.APPEND: lambda objects, event, attrs: method_append(objects, event, attrs),
    Method.MULTI_SET: lambda objects, event, attrs: method_multi_set(objects, event, attrs),
}


def execute(events, attrs):
    for event in events:
        objects = data[event.obj.__name__]
        method = event.method

        methods[method](objects=objects, event=event, attrs=attrs)


class NmapHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self._path: str
        self.error: bool = False

    def startDocument(self):
        self._path = ""

    def startElement(self, name, attrs):
        self._path += f"/{name}"

        if self._path in routes_events_map:
            execute(routes_events_map[self._path], attrs)

    def endElement(self, name):
        if (self._path + "$") in routes_events_map:
            execute(routes_events_map[self._path], attrs)

        if self._path.endswith(name):
            self._path = self._path[: self._path.rfind("/")]
        else:
            self.error = True

    def endDocument(self):
        if not (self._path == ""):
            self.error = True


def import_data(file):
    parser = make_parser()
    handler = NmapHandler()
    parser.setContentHandler(handler)
    parser.parse(file)
    print(data)


if __name__ == "__main__":
    file = "lain_backend/tasks/nmap_example.xml"
    import_data(file)

