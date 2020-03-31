from asyncio import iscoroutine

from factory import Factory, Sequence, SubFactory, Faker, List
from factory.base import FactoryOptions, OptionDefault

from lain_backend.database import database

from lain_backend.schemas import (
    ProjectIn,
    OrganizationIn,
    HostIn,
    DomainIn,
    DomainTypeIn,
    ServiceIn,
    ProtocolIn,
)

from lain_backend.cruds import (
    project,
    organization,
    host,
    domain,
    domain_type,
    service,
    protocol,
)


class DatabaseOptions(FactoryOptions):
    def _check_crud_create(self, meta, value):
        if value is None and not meta.abstract:
            raise TypeError(f"{meta}.crud_create must be initialize")

    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault("db", None, inherit=True),
            OptionDefault(
                "crud_create", None, inherit=True, checker=self._check_crud_create
            ),
        ]


class DatabaseModelFactory(Factory):

    _options_class = DatabaseOptions

    class Meta:
        abstract = True

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        db = cls._meta.db
        create = cls._meta.crud_create

        for kwarg in kwargs:
            fn = kwargs[kwarg]
            if iscoroutine(fn):
                kwargs[kwarg] = (await fn).id
            if isinstance(fn, list):
                kwargs[kwarg] = [
                    (await subf).id if iscoroutine(subf) else subf for subf in fn
                ]

        obj = model_class(*args, **kwargs)
        if db is None:
            raise RuntimeError("DB connection is not provided.")

        return await create(db, obj)


class BaseFactory(DatabaseModelFactory):
    class Meta:
        abstract = True
        db = database


class ProjectFactory(BaseFactory):
    name = Sequence(lambda i: f"Project {i}")

    class Meta:
        model = ProjectIn
        crud_create = project.create


class OrganizationFactory(BaseFactory):
    name = Sequence(lambda i: f"Organization {i}")
    description = Sequence(lambda i: f"Description {i}")
    project_id = SubFactory(ProjectFactory)

    class Meta:
        model = OrganizationIn
        crud_create = organization.create

class HostFactory(BaseFactory):
    addr = Faker("ipv4", network=False)
    os = Sequence(lambda i: f"OS {i}")
    description = Sequence(lambda i: f"Description {i}")

    class Meta:
        model = HostIn
        crud_create = host.create


class DomainTypeFactory(BaseFactory):
    name = Sequence(lambda i: f"DT {i}")

    class Meta:
        model = DomainTypeIn
        crud_create = domain_type.create


class DomainFactory(BaseFactory):
    name = Sequence(lambda i: f"Domain {i}")
    description = Sequence(lambda i: f"Description {i}")
    type_id = SubFactory(DomainTypeFactory)

    class Meta:
        model = DomainIn
        crud_create = domain.create


class ProtocolFactory(BaseFactory):
    name = Sequence(lambda i: f"Protocol {i}")

    class Meta:
        model = ProtocolIn
        crud_create = protocol.create


class ServiceFactory(BaseFactory):
    name = Sequence(lambda i: f"Service {i}")
    port = Sequence(lambda i: i)
    version = Sequence(lambda i: f"Version {i}")
    description = Sequence(lambda i: f"Description {i}")
    host_id = SubFactory(HostFactory)

    class Meta:
        model = ServiceIn
        crud_create = service.create


class ServiceFactoryWithProtocols(ServiceFactory):
    protocol_ids = List([SubFactory(ProtocolFactory) for _ in range(2)])

    class Meta:
        model = ServiceIn
        crud_create = service.create
