import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import people as crud

from tests.factories import PeopleFactory

from lain_backend.schemas import PeopleUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "firstname": "name 0",
                "surname": "surname 0",
                "patronymic": "patronymic 0",
                "position": "position 0",
                "description": "desc 0",
            },
            {
                "firstname": "name 0",
                "surname": "surname 0",
                "patronymic": "patronymic 0",
                "position": "position 0",
                "description": "desc 0",
            },
        ),
        (
            {
                "firstname": "name another",
                "surname": "surname another",
                "patronymic": "patron another",
                "position": "position another",
                "description": "desc another",
            },
            {
                "firstname": "name another",
                "surname": "surname another",
                "patronymic": "patron another",
                "position": "position another",
                "description": "desc another",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    people = await PeopleFactory(**input)
    for key in expected:
        assert people[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("firstname", ["", " "])
async def test_validation_firstname(db, firstname):
    with pytest.raises(ValidationError):
        await PeopleFactory(firstname=firstname)


@pytest.mark.asyncio
@pytest.mark.parametrize("surname", ["", " "])
async def test_validation_surname(db, surname):
    with pytest.raises(ValidationError):
        await PeopleFactory(surname=surname)


@pytest.mark.asyncio
@pytest.mark.parametrize("patronymic", ["", " "])
async def test_validation_patronymic(db, patronymic):
    with pytest.raises(ValidationError):
        await PeopleFactory(patronymic=patronymic)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    peoples = await crud.get_all(db=db)
    assert len(peoples) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    peoples = [await PeopleFactory() for i in range(2)]

    db_peoples = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_peoples[i]):
            assert db_peoples[i][key] == peoples[i][key]


@pytest.mark.asyncio
async def test_create(db):
    people = await PeopleFactory()
    assert people is not None


@pytest.mark.asyncio
async def test_get_one(db):
    people = await PeopleFactory()

    db_people = await crud.get(db, people["id"])

    for key in dict(people):
        assert db_people[key] == people[key]


@pytest.mark.asyncio
async def test_delete(db):
    people_id = (await PeopleFactory())["id"]

    assert (await crud.delete(db, people_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "firstname": "one name",
                "surname": "one surname",
                "patronymic": "one patron",
                "position": "one position",
                "description": "one desc",
            },
            {
                "firstname": "another name",
                "surname": "another surname",
                "patronymic": "another patron",
                "position": "another position",
                "description": "another desc",
            },
            {
                "firstname": "another name",
                "surname": "another surname",
                "patronymic": "another patron",
                "position": "another position",
                "description": "another desc",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    people_id = (await PeopleFactory(**input))["id"]

    people = await crud.update(db=db, people_id=people_id, people=PeopleUpdateIn(**updateData))

    for key in expected:
        assert people[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_people = await crud.get(db=db, people_id=666)

    assert db_people is None


@pytest.mark.asyncio
async def test_check(db):
    people = await PeopleFactory()

    assert await crud.check(db=db, people_id=people["id"])
