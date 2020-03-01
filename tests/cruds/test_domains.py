import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import domain as crud

from tests.factories import DomainFactory

from lain_backend.schemas import DomainUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        ({"name": "domain 0"}, {"name": "domain 0"}),
        ({"name": "My Dream Domain"}, {"name": "My Dream Domain"}),
    ],
)
async def test_factory(db, input, expected):
    domain = await DomainFactory(**input)
    for key in expected:
        assert domain[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await DomainFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    domains = await crud.get_all(db=db)
    assert len(domains) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    domains = [await DomainFactory() for i in range(2)]

    db_domains = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_domains[i]):
            assert db_domains[i][key] == domains[i][key]


@pytest.mark.asyncio
async def test_create(db):
    domain = await DomainFactory()
    assert domain is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await DomainFactory(name="Dream One")

    with pytest.raises(IntegrityError):
        await DomainFactory(name="Dream One")


@pytest.mark.asyncio
async def test_get_one(db):
    domain = await DomainFactory()

    db_domain = await crud.get(db, domain["id"])

    for key in dict(domain):
        assert db_domain[key] == domain[key]


@pytest.mark.asyncio
async def test_delete(db):
    domain_id = (await DomainFactory())["id"]

    assert (await crud.delete(db, domain_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One Domain name"},
            {"name": "Another Domain name"},
            {"name": "Another Domain name"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    domain_id = (await DomainFactory(**input))["id"]

    domain = await crud.update(db=db, domain_id=domain_id, domain=DomainUpdateIn(**updateData))

    for key in expected:
        assert domain[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_domain = await crud.get(db=db, domain_id=666)

    assert db_domain is None


@pytest.mark.asyncio
async def test_exists(db):
    domain = await DomainFactory()

    assert await crud.exists(db=db, name=domain["name"])


@pytest.mark.asyncio
async def test_check(db):
    domain = await DomainFactory()

    assert await crud.check(db=db, domain_id=domain["id"])
