import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import organization as crud

from tests.factories import OrganizationFactory

from lain_backend.schemas import OrganizationUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"name": "organization 0", "description": "some description"},
            {"name": "organization 0", "description": "some description"},
        ),
        (
            {"name": "My Dream Organization", "description": "another description"},
            {"name": "My Dream Organization", "description": "another description"},
        ),
    ],
)
async def test_factory(db, input, expected):
    organization = await OrganizationFactory(**input)
    for key in expected:
        assert organization[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await OrganizationFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    organizations = await crud.get_all(db=db)
    assert len(organizations) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    organizations = [await OrganizationFactory() for i in range(2)]

    db_organizations = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_organizations[i]):
            assert db_organizations[i][key] == organizations[i][key]


@pytest.mark.asyncio
async def test_create(db):
    organization = await OrganizationFactory()
    assert organization is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await OrganizationFactory(name="Dream One")

    with pytest.raises(IntegrityError):
        await OrganizationFactory(name="Dream One")


@pytest.mark.asyncio
async def test_get_one(db):
    organization = await OrganizationFactory()

    db_organization = await crud.get(db, organization["id"])

    for key in dict(organization):
        assert db_organization[key] == organization[key]


@pytest.mark.asyncio
async def test_delete(db):
    organization_id = (await OrganizationFactory())["id"]

    assert (await crud.delete(db, organization_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One Organization name", "description": "some description"},
            {"name": "Another Organization name", "description": "another description"},
            {"name": "Another Organization name", "description": "another description"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    organization_id = (await OrganizationFactory(**input))["id"]

    organization = await crud.update(
        db=db, organization_id=organization_id, organization=OrganizationUpdateIn(**updateData)
    )

    for key in expected:
        assert organization[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_organization = await crud.get(db=db, organization_id=666)

    assert db_organization is None


@pytest.mark.asyncio
async def test_exists(db):
    organization = await OrganizationFactory()

    assert await crud.exists(db=db, name=organization["name"])


@pytest.mark.asyncio
async def test_check(db):
    organization = await OrganizationFactory()

    assert await crud.check(db=db, organization_id=organization["id"])
