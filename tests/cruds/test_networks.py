import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import network as crud

from tests.factories import NetworkFactory

from lain_backend.schemas import NetworkUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"addr": "192.168.10.1/24", "name": "network 0", "description": "some description"},
            {"addr": "192.168.10.1/24", "name": "network 0", "description": "some description"},
        ),
        (
            {
                "addr": "192.168.15.1/16",
                "name": "my dream network",
                "description": "another description",
            },
            {
                "addr": "192.168.15.1/16",
                "name": "my dream network",
                "description": "another description",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    network = await NetworkFactory(**input)
    for key in expected:
        assert network[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await NetworkFactory(name=name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "addr",
    [
        None,
        "",
        "192.270.10.1/13",
        "192.128/15",
        "192.168.10.1./12",
        "192.168.9.1",
        "127.0.0.0.1/16",
    ],
)
async def test_validation_addr(db, addr):
    with pytest.raises(ValidationError):
        await NetworkFactory(addr=addr)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    networks = await crud.get_all(db=db)
    assert len(networks) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    networks = [await NetworkFactory() for i in range(2)]

    db_networks = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_networks[i]):
            assert db_networks[i][key] == networks[i][key]


@pytest.mark.asyncio
async def test_create(db):
    network = await NetworkFactory()
    assert network is not None


@pytest.mark.asyncio
async def test_get_one(db):
    network = await NetworkFactory()

    db_network = await crud.get(db, network["id"])

    for key in dict(network):
        assert db_network[key] == network[key]


@pytest.mark.asyncio
async def test_delete(db):
    network_id = (await NetworkFactory())["id"]

    assert (await crud.delete(db, network_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "addr": "192.168.16.1/24",
                "name": "one network name",
                "description": "some description",
            },
            {
                "addr": "192.168.20.1/30",
                "name": "another network",
                "description": "another description",
            },
            {
                "addr": "192.168.20.1/30",
                "name": "another network",
                "description": "another description",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    network_id = (await NetworkFactory(**input))["id"]

    network = await crud.update(db=db, network_id=network_id, network=NetworkUpdateIn(**updateData))

    for key in expected:
        assert network[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_network = await crud.get(db=db, network_id=666)

    assert db_network is None


@pytest.mark.asyncio
async def test_check(db):
    network = await NetworkFactory()

    assert await crud.check(db=db, network_id=network["id"])
