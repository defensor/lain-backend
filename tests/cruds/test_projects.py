import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import project as crud

from tests.factories import ProjectFactory

from lain_backend.schemas import ProjectUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        ({"name": "project 0"}, {"name": "project 0"}),
        ({"name": "My Dream Project"}, {"name": "My Dream Project"}),
    ],
)
async def test_factory(db, input, expected):
    project = await ProjectFactory(**input)
    for key in expected:
        assert project.dict()[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await ProjectFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    projects = await crud.get_all(db=db)
    assert len(projects) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    projects = [await ProjectFactory() for i in range(2)]

    db_projects = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_projects[i]):
            assert db_projects[i].dict()[key] == projects[i].dict()[key]


@pytest.mark.asyncio
async def test_create(db):
    project = await ProjectFactory()
    assert project is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await ProjectFactory(name="Dream One")

    with pytest.raises(IntegrityError):
        await ProjectFactory(name="Dream One")


@pytest.mark.asyncio
async def test_get_one(db):
    project = await ProjectFactory()

    db_project = await crud.get(db, project.id)

    for key in dict(project):
        assert db_project.dict()[key] == project.dict()[key]


@pytest.mark.asyncio
async def test_delete(db):
    project_id = (await ProjectFactory()).id

    assert (await crud.delete(db, project_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {"name": "One Project name"},
            {"name": "Another Project name"},
            {"name": "Another Project name"},
        )
    ],
)
async def test_update(db, input, updateData, expected):
    project_id = (await ProjectFactory(**input)).id

    project = await crud.update(
        db=db, project_id=project_id, project=ProjectUpdateIn(**updateData)
    )

    for key in expected:
        assert project.dict()[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_project = await crud.get(db=db, project_id=666)

    assert db_project is None


@pytest.mark.asyncio
async def test_exist_name(db):
    project = await ProjectFactory()

    assert await crud.exist_name(db=db, name=project.name)


@pytest.mark.asyncio
async def test_exist(db):
    project = await ProjectFactory()

    assert await crud.exist(db=db, project_id=project.id)
