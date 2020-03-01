import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import contact_type as crud

from tests.factories import ContactTypeFactory

from lain_backend.schemas import ContactTypeUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        ({"name": "contact_type 0"}, {"name": "contact_type 0"}),
        ({"name": "My Dream ContactType"}, {"name": "My Dream ContactType"}),
    ],
)
async def test_factory(db, input, expected):
    contact_type = await ContactTypeFactory(**input)
    for key in expected:
        assert contact_type[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await ContactTypeFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    contact_types = await crud.get_all(db=db)
    assert len(contact_types) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    contact_types = [await ContactTypeFactory() for i in range(2)]

    db_contact_types = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_contact_types[i]):
            assert db_contact_types[i][key] == contact_types[i][key]


@pytest.mark.asyncio
async def test_create(db):
    contact_type = await ContactTypeFactory()
    assert contact_type is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await ContactTypeFactory(name="Dream One")

    with pytest.raises(IntegrityError):
        await ContactTypeFactory(name="Dream One")


@pytest.mark.asyncio
async def test_get_one(db):
    contact_type = await ContactTypeFactory()

    db_contact_type = await crud.get(db, contact_type["id"])

    for key in dict(contact_type):
        assert db_contact_type[key] == contact_type[key]


@pytest.mark.asyncio
async def test_delete(db):
    contact_type_id = (await ContactTypeFactory())["id"]

    assert (await crud.delete(db, contact_type_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One ContactType name"},
            {"name": "Another ContactType name"},
            {"name": "Another ContactType name"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    contact_type_id = (await ContactTypeFactory(**input))["id"]

    contact_type = await crud.update(
        db=db, contact_type_id=contact_type_id, contact_type=ContactTypeUpdateIn(**updateData)
    )

    for key in expected:
        assert contact_type[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_contact_type = await crud.get(db=db, contact_type_id=666)

    assert db_contact_type is None


@pytest.mark.asyncio
async def test_exists(db):
    contact_type = await ContactTypeFactory()

    assert await crud.exists(db=db, name=contact_type["name"])


@pytest.mark.asyncio
async def test_check(db):
    contact_type = await ContactTypeFactory()

    assert await crud.check(db=db, contact_type_id=contact_type["id"])
