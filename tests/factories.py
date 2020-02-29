from asyncio import iscoroutine

from factory import Factory, Sequence, SubFactory, Faker, List
from factory.base import FactoryOptions, OptionDefault

from lain_backend.database import database

from lain_backend.schemas import (
    ProjectIn,
    OrganizationIn,
    BuildingIn,
    PeopleIn,
    NetworkIn,
    HostIn,
    DomainIn,
    DomainTypeIn,
    ServiceIn,
    CredentialIn,
    ProtocolIn,
    ContactIn,
    ContactTypeIn,
    VulnerabilityIn,
)

from lain_backend.cruds import (
    project,
    organization,
    building,
    people,
    network,
    host,
    domain,
    domain_type,
    service,
    credential,
    protocol,
    contact,
    contact_type,
    vulnerability,
)


class DatabaseOptions(FactoryOptions):
    def _check_crud_create(self, meta, value):
        if value is None and not meta.abstract:
            raise TypeError(f"{meta}.crud_create must be initialize")

    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault("db", None, inherit=True),
            OptionDefault("crud_create", None, inherit=True, checker=self._check_crud_create),
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
                kwargs[kwarg] = (await fn)["id"]
            if isinstance(fn, list):
                kwargs[kwarg] = [(await subf)["id"] if iscoroutine(subf) else subf for subf in fn]

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


class NetworkFactory(BaseFactory):
    name = Sequence(lambda i: f"Network {i}")
    addr = Faker("ipv4", network=True)
    description = Sequence(lambda i: f"Description {i}")

    class Meta:
        model = NetworkIn
        crud_create = network.create


class NetworkFactoryWithOrganizations(NetworkFactory):
    organization_ids = List([SubFactory(OrganizationFactory) for _ in range(2)])

    class Meta:
        model = NetworkIn
        crud_create = network.create


class HostFactory(BaseFactory):
    addr = Faker("ipv4")
    os = Sequence(lambda i: f"OS {i}")
    description = Sequence(lambda i: f"Description {i}")
    network_id = SubFactory(NetworkFactory)

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

    class Meta:
        model = ServiceIn
        crud_create = service.create


class ServiceFactoryWithProtocols(ServiceFactory):
    protocol_ids = List([SubFactory(ProtocolFactory) for _ in range(2)])

    class Meta:
        model = ServiceIn
        crud_create = service.create


class PeopleFactory(BaseFactory):
    firstname = Sequence(lambda i: f"First name {i}")
    surname = Sequence(lambda i: f"Surname {i}")
    patronymic = Sequence(lambda i: f"Patronymic {i}")
    position = Sequence(lambda i: f"Position {i}")
    description = Sequence(lambda i: f"Description {i}")

    class Meta:
        model = PeopleIn
        crud_create = people.create


class PeopleFactoryWithOrganizations(PeopleFactory):
    organization_ids = List([SubFactory(OrganizationFactory) for _ in range(2)])

    class Meta:
        model = PeopleIn
        crud_create = people.create


class ContactTypeFactory(BaseFactory):
    name = Sequence(lambda i: f"Contact type {i}")

    class Meta:
        model = ContactTypeIn
        crud_create = contact_type.create


class ContactFactory(BaseFactory):
    value = Sequence(lambda i: f"Contact {i}")
    description = Sequence(lambda i: f"Description {i}")
    type_id = SubFactory(ContactTypeFactory)

    class Meta:
        model = ContactIn
        crud_create = contact.create


class ContactFactoryWithPeoples(ContactFactory):
    people_ids = List([SubFactory(PeopleFactory) for _ in range(2)])

    class Meta:
        model = ContactIn
        crud_create = contact.create


class ContactFactoryWithOrganizations(ContactFactory):
    organization_ids = List([SubFactory(OrganizationFactory) for _ in range(2)])

    class Meta:
        model = ContactIn
        crud_create = contact.create


class BuildingFactory(BaseFactory):
    name = Sequence(lambda i: f"Building {i}")
    addr = Faker("address")
    description = Sequence(lambda i: f"Description {i}")

    class Meta:
        model = BuildingIn
        crud_create = building.create


class BuildingFactoryWithOrganizations(BuildingFactory):
    organization_ids = List([SubFactory(OrganizationFactory) for _ in range(2)])

    class Meta:
        model = BuildingIn
        crud_create = building.create


class VulnerabilityFactory(BaseFactory):
    name = Sequence(lambda i: f"Vulnerability {i}")
    solution = Sequence(lambda i: f"Solution {i}")
    description = Sequence(lambda i: f"Description {i}")

    class Meta:
        model = VulnerabilityIn
        crud_create = vulnerability.create


class VulnerabilityFactoryWithPeoples(VulnerabilityFactory):
    people_ids = List([SubFactory(PeopleFactory) for _ in range(2)])

    class Meta:
        model = VulnerabilityIn
        crud_create = vulnerability.create


class VulnerabilityFactoryWithNetworks(VulnerabilityFactory):
    network_ids = List([SubFactory(NetworkFactory) for _ in range(2)])

    class Meta:
        model = VulnerabilityIn
        crud_create = vulnerability.create


class VulnerabilityFactoryWithHosts(VulnerabilityFactory):
    host_ids = List([SubFactory(HostFactory) for _ in range(2)])

    class Meta:
        model = VulnerabilityIn
        crud_create = vulnerability.create


class VulnerabilityFactoryWithServices(VulnerabilityFactory):
    service_ids = List([SubFactory(ServiceFactory) for _ in range(2)])

    class Meta:
        model = VulnerabilityIn
        crud_create = vulnerability.create
