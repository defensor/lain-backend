import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import building as crud

from tests.factories import BuildingFactory

from lain_backend.schemas import BuildingUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"name": "buildign 0", "addr": "one addr", "description": "some description"},
            {"name": "buildign 0", "addr": "one addr", "description": "some description"},
        ),
        (
            {
                "name": "My Dream buildign",
                "addr": "another addr",
                "description": "another description",
            },
            {
                "name": "My Dream buildign",
                "addr": "another addr",
                "description": "another description",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    building = await BuildingFactory(**input)
    for key in expected:
        assert building[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await BuildingFactory(name=name)


@pytest.mark.asyncio
@pytest.mark.parametrize("addr", [None, ""])
async def test_validation_addr(db, addr):
    with pytest.raises(ValidationError):
        await BuildingFactory(addr=addr)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    buildings = await crud.get_all(db=db)
    assert len(buildings) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    buildings = [await BuildingFactory() for i in range(2)]

    db_buildings = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_buildings[i]):
            assert db_buildings[i][key] == buildings[i][key]


@pytest.mark.asyncio
async def test_create(db):
    building = await BuildingFactory()
    assert building is not None


@pytest.mark.asyncio
async def test_get_one(db):
    building = await BuildingFactory()

    db_building = await crud.get(db, building["id"])

    for key in dict(building):
        assert db_building[key] == building[key]


@pytest.mark.asyncio
async def test_delete(db):
    building_id = (await BuildingFactory())["id"]

    assert (await crud.delete(db, building_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One building name", "addr": "one addr", "description": "some description"},
            {
                "name": "Another building name",
                "addr": "another addr",
                "description": "another description",
            },
            {
                "name": "Another building name",
                "addr": "another addr",
                "description": "another description",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    building_id = (await BuildingFactory(**input))["id"]

    building = await crud.update(
        db=db, building_id=building_id, building=BuildingUpdateIn(**updateData)
    )

    for key in expected:
        assert building[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_building = await crud.get(db=db, building_id=666)

    assert db_building is None


@pytest.mark.asyncio
async def test_check(db):
    building = await BuildingFactory()

    assert await crud.check(db=db, building_id=building["id"])
