import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import domain_type as crud

from tests.factories import DomainTypeFactory

from lain_backend.schemas import DomainTypeUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [({"name": "dt 0"}, {"name": "dt 0"}), ({"name": "My dt"}, {"name": "My dt"}),],
)
async def test_factory(db, input, expected):
    domain_type = await DomainTypeFactory(**input)
    for key in expected:
        assert domain_type.dict()[key] == expected[key]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", [None, ""])
async def test_validation_name(db, name):
    with pytest.raises(ValidationError):
        await DomainTypeFactory(name=name)


@pytest.mark.asyncio
async def test_get_empty_list(db):
    domain_types = await crud.get_all(db=db)
    assert len(domain_types) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    domain_types = [await DomainTypeFactory() for i in range(2)]

    db_domain_types = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_domain_types[i]):
            assert db_domain_types[i].dict()[key] == domain_types[i].dict()[key]


@pytest.mark.asyncio
async def test_create(db):
    domain_type = await DomainTypeFactory()
    assert domain_type is not None


@pytest.mark.asyncio
async def test_unique_create(db):
    await DomainTypeFactory(name="DT")

    with pytest.raises(IntegrityError):
        await DomainTypeFactory(name="DT")


@pytest.mark.asyncio
async def test_get_one(db):
    domain_type = await DomainTypeFactory()

    db_domain_type = await crud.get(db, domain_type.id)

    for key in dict(domain_type):
        assert db_domain_type.dict()[key] == domain_type.dict()[key]


@pytest.mark.asyncio
async def test_delete(db):
    domain_type_id = (await DomainTypeFactory()).id

    assert (await crud.delete(db, domain_type_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [({"name": "One dt"}, {"name": "Another"}, {"name": "Another"},)],
)
async def test_update(db, input, updateData, expected):
    domain_type_id = (await DomainTypeFactory(**input)).id

    domain_type = await crud.update(
        db=db,
        domain_type_id=domain_type_id,
        domain_type=DomainTypeUpdateIn(**updateData),
    )

    for key in expected:
        assert domain_type.dict()[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_domain_type = await crud.get(db=db, domain_type_id=666)

    assert db_domain_type is None


@pytest.mark.asyncio
async def test_exist_name(db):
    domain_type = await DomainTypeFactory()

    assert await crud.exist_name(db=db, name=domain_type.name)


@pytest.mark.asyncio
async def test_exist(db):
    domain_type = await DomainTypeFactory()

    assert await crud.exist(db=db, domain_type_id=domain_type.id)
