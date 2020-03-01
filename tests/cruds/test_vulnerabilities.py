import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import vulnerability as crud

from tests.factories import VulnerabilityFactory

from lain_backend.schemas import VulnerabilityUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "name": "vulnerability 0",
                "description": "one description",
                "solution": "one solution",
            },
            {
                "name": "vulnerability 0",
                "description": "one description",
                "solution": "one solution",
            },
        ),
        (
            {
                "name": "My Dream Vulnerability",
                "description": "another description",
                "solution": "another solution",
            },
            {
                "name": "My Dream Vulnerability",
                "description": "another description",
                "solution": "another solution",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    vulnerability = await VulnerabilityFactory(**input)
    for key in expected:
        assert vulnerability[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await VulnerabilityFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    vulnerabilities = await crud.get_all(db=db)
    assert len(vulnerabilities) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    vulnerabilities = [await VulnerabilityFactory() for i in range(2)]

    db_vulnerabilities = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_vulnerabilities[i]):
            assert db_vulnerabilities[i][key] == vulnerabilities[i][key]


@pytest.mark.asyncio
async def test_create(db):
    vulnerability = await VulnerabilityFactory()
    assert vulnerability is not None


@pytest.mark.asyncio
async def test_get_one(db):
    vulnerability = await VulnerabilityFactory()

    db_vulnerability = await crud.get(db, vulnerability["id"])

    for key in dict(vulnerability):
        assert db_vulnerability[key] == vulnerability[key]


@pytest.mark.asyncio
async def test_delete(db):
    vulnerability_id = (await VulnerabilityFactory())["id"]

    assert (await crud.delete(db, vulnerability_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "name": "One Vulnerability name",
                "solution": "one solution",
                "description": "one description",
            },
            {
                "name": "Another Vulnerability name",
                "solution": "another solution",
                "description": "another description",
            },
            {
                "name": "Another Vulnerability name",
                "solution": "another solution",
                "description": "another description",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    vulnerability_id = (await VulnerabilityFactory(**input))["id"]

    vulnerability = await crud.update(
        db=db, vulnerability_id=vulnerability_id, vulnerability=VulnerabilityUpdateIn(**updateData)
    )

    for key in expected:
        assert vulnerability[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_vulnerability = await crud.get(db=db, vulnerability_id=666)

    assert db_vulnerability is None


@pytest.mark.asyncio
async def test_check(db):
    vulnerability = await VulnerabilityFactory()

    assert await crud.check(db=db, vulnerability_id=vulnerability["id"])
