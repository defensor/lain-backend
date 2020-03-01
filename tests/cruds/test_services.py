import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import service as crud

from tests.factories import ServiceFactory

from lain_backend.schemas import ServiceUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "port": 1024,
                "name": "service 0",
                "description": "some description",
                "version": "some version",
            },
            {
                "port": 1024,
                "name": "service 0",
                "description": "some description",
                "version": "some version",
            },
        ),
        (
            {
                "port": 256,
                "name": "my dream service",
                "description": "another description",
                "version": "another version",
            },
            {
                "port": 256,
                "name": "my dream service",
                "description": "another description",
                "version": "another version",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    service = await ServiceFactory(**input)
    for key in expected:
        assert service[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await ServiceFactory(name=name)


@pytest.mark.asyncio
@pytest.mark.parametrize("port", [None, "", -1, 65536])
async def test_validation_port(db, port):
    with pytest.raises(ValidationError):
        await ServiceFactory(port=port)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    services = await crud.get_all(db=db)
    assert len(services) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    services = [await ServiceFactory() for i in range(2)]

    db_services = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_services[i]):
            assert db_services[i][key] == services[i][key]


@pytest.mark.asyncio
async def test_create(db):
    service = await ServiceFactory()
    assert service is not None


@pytest.mark.asyncio
async def test_get_one(db):
    service = await ServiceFactory()

    db_service = await crud.get(db, service["id"])

    for key in dict(service):
        assert db_service[key] == service[key]


@pytest.mark.asyncio
async def test_delete(db):
    service_id = (await ServiceFactory())["id"]

    assert (await crud.delete(db, service_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "port": 1024,
                "name": "one service",
                "description": "some description",
                "version": "one verson",
            },
            {
                "port": 65000,
                "name": "another service",
                "description": "some description",
                "version": "another verson",
            },
            {
                "port": 65000,
                "name": "another service",
                "description": "some description",
                "version": "another verson",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    service_id = (await ServiceFactory(**input))["id"]

    service = await crud.update(db=db, service_id=service_id, service=ServiceUpdateIn(**updateData))

    for key in expected:
        assert service[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_service = await crud.get(db=db, service_id=666)

    assert db_service is None


@pytest.mark.asyncio
async def test_check(db):
    service = await ServiceFactory()

    assert await crud.check(db=db, service_id=service["id"])
