import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import contact as crud

from tests.factories import ContactFactory

from lain_backend.schemas import ContactUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"value": "contact 0", "description": "one desc"},
            {"value": "contact 0", "description": "one desc"},
        ),
        (
            {"value": "My Dream Contact", "description": "second desc"},
            {"value": "My Dream Contact", "description": "second desc"},
        ),
    ],
)
async def test_factory(db, input, expected):
    contact = await ContactFactory(**input)
    for key in expected:
        assert contact[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("value", [None, ""])
async def test_validation_value(db, value):
    with pytest.raises(ValidationError):
        await ContactFactory(value=value)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    contacts = await crud.get_all(db=db)
    assert len(contacts) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    contacts = [await ContactFactory() for i in range(2)]

    db_contacts = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_contacts[i]):
            assert db_contacts[i][key] == contacts[i][key]


@pytest.mark.asyncio
async def test_create(db):
    contact = await ContactFactory()
    assert contact is not None


@pytest.mark.asyncio
async def test_get_one(db):
    contact = await ContactFactory()

    db_contact = await crud.get(db, contact["id"])

    for key in dict(contact):
        assert db_contact[key] == contact[key]


@pytest.mark.asyncio
async def test_delete(db):
    contact_id = (await ContactFactory())["id"]

    assert (await crud.delete(db, contact_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"value": "One Contact value", "description": "one desc"},
            {"value": "Another Contact value", "description": "another desc"},
            {"value": "Another Contact value", "description": "another desc"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    contact_id = (await ContactFactory(**input))["id"]

    contact = await crud.update(db=db, contact_id=contact_id, contact=ContactUpdateIn(**updateData))

    for key in expected:
        assert contact[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_contact = await crud.get(db=db, contact_id=666)

    assert db_contact is None


@pytest.mark.asyncio
async def test_check(db):
    contact = await ContactFactory()

    assert await crud.check(db=db, contact_id=contact["id"])
