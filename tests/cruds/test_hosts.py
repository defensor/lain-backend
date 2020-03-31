import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import host as crud
from ipaddress import ip_address

from tests.factories import HostFactory

from lain_backend.schemas import HostUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "addr": ip_address("192.168.10.1"),
                "os": "os 0",
                "description": "some description",
            },
            {
                "addr": ip_address("192.168.10.1"),
                "os": "os 0",
                "description": "some description",
            },
        ),
        (
            {
                "addr": ip_address("192.168.15.1"),
                "os": "my dream os",
                "description": "another description",
            },
            {
                "addr": ip_address("192.168.15.1"),
                "os": "my dream os",
                "description": "another description",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    host = await HostFactory(**input)
    for key in expected:
        assert host.dict()[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("os", ["", " "])
async def test_validation_os(db, os):
    with pytest.raises(ValidationError):
        await HostFactory(os=os)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    hosts = await crud.get_all(db=db)
    assert len(hosts) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    hosts = [await HostFactory() for i in range(2)]

    db_hosts = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_hosts[i]):
            assert db_hosts[i].dict()[key] == hosts[i].dict()[key]


@pytest.mark.asyncio
async def test_create(db):
    host = await HostFactory()
    assert host is not None


@pytest.mark.asyncio
async def test_get_one(db):
    host = await HostFactory()

    db_host = await crud.get(db, host.id)

    for key in dict(host):
        assert db_host.dict()[key] == host.dict()[key]


@pytest.mark.asyncio
async def test_delete(db):
    host_id = (await HostFactory()).id

    assert (await crud.delete(db, host_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "addr": ip_address("192.168.16.1"),
                "os": "one os name",
                "description": "some description",
            },
            {
                "addr": ip_address("192.168.20.1"),
                "os": "another os",
                "description": "another description",
            },
            {
                "addr": ip_address("192.168.20.1"),
                "os": "another os",
                "description": "another description",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    host_id = (await HostFactory(**input)).id

    host = await crud.update(db=db, host_id=host_id, host=HostUpdateIn(**updateData))

    for key in expected:
        assert host.dict()[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_host = await crud.get(db=db, host_id=666)

    assert db_host is None


@pytest.mark.asyncio
async def test_exist(db):
    host = await HostFactory()

    assert await crud.exist(db=db, host_id=host.id)
