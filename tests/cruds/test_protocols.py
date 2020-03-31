import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import protocol as crud

from tests.factories import ProtocolFactory

from lain_backend.schemas import ProtocolUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        ({"name": "protocol 0"}, {"name": "protocol 0"}),
        ({"name": "My Dream Protocol"}, {"name": "My Dream Protocol"}),
    ],
)
async def test_factory(db, input, expected):
    protocol = await ProtocolFactory(**input)
    for key in expected:
        assert protocol.dict()[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await ProtocolFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    protocols = await crud.get_all(db=db)
    assert len(protocols) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    protocols = [await ProtocolFactory() for i in range(2)]

    db_protocols = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_protocols[i]):
            assert db_protocols[i].dict()[key] == protocols[i].dict()[key]


@pytest.mark.asyncio
async def test_create(db):
    protocol = await ProtocolFactory()
    assert protocol is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await ProtocolFactory(name="Dream One")

    with pytest.raises(IntegrityError):
        await ProtocolFactory(name="Dream One")


@pytest.mark.asyncio
async def test_get_one(db):
    protocol = await ProtocolFactory()

    db_protocol = await crud.get(db, protocol.id)

    for key in dict(protocol):
        assert db_protocol.dict()[key] == protocol.dict()[key]


@pytest.mark.asyncio
async def test_delete(db):
    protocol_id = (await ProtocolFactory()).id

    assert (await crud.delete(db, protocol_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One Protocol name"},
            {"name": "Another Protocol name"},
            {"name": "Another Protocol name"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    protocol_id = (await ProtocolFactory(**input)).id

    protocol = await crud.update(
        db=db, protocol_id=protocol_id, protocol=ProtocolUpdateIn(**updateData)
    )

    for key in expected:
        assert protocol.dict()[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_protocol = await crud.get(db=db, protocol_id=666)

    assert db_protocol is None


@pytest.mark.asyncio
async def test_exist_name(db):
    protocol = await ProtocolFactory()

    assert await crud.exist_name(db=db, name=protocol.name)


@pytest.mark.asyncio
async def test_exist(db):
    protocol = await ProtocolFactory()

    assert await crud.exist(db=db, protocol_id=protocol.id)
