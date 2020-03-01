import pytest
from pydantic import ValidationError
from sqlite3 import IntegrityError
from lain_backend.cruds import credential as crud

from tests.factories import CredentialFactory

from lain_backend.schemas import CredentialUpdateIn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {
                "login": "login 0",
                "password": "password 0",
                "key": "key 0",
                "description": "desc 0",
            },
            {
                "login": "login 0",
                "password": "password 0",
                "key": "key 0",
                "description": "desc 0",
            },
        ),
        (
            {
                "login": "login another",
                "password": "password another",
                "key": "key another",
                "description": "desc another",
            },
            {
                "login": "login another",
                "password": "password another",
                "key": "key another",
                "description": "desc another",
            },
        ),
    ],
)
async def test_factory(db, input, expected):
    credential = await CredentialFactory(**input)
    for key in expected:
        assert credential[key] == expected[key]


@pytest.mark.asyncio
async def test_get_empty_list(db):
    credentials = await crud.get_all(db=db)
    assert len(credentials) == 0


@pytest.mark.asyncio
async def test_get_all(db):
    credentials = [await CredentialFactory() for i in range(2)]

    db_credentials = await crud.get_all(db=db)

    for i in range(2):
        for key in dict(db_credentials[i]):
            assert db_credentials[i][key] == credentials[i][key]


@pytest.mark.asyncio
async def test_create(db):
    credential = await CredentialFactory()
    assert credential is not None


@pytest.mark.asyncio
async def test_get_one(db):
    credential = await CredentialFactory()

    db_credential = await crud.get(db, credential["id"])

    for key in dict(credential):
        assert db_credential[key] == credential[key]


@pytest.mark.asyncio
async def test_delete(db):
    credential_id = (await CredentialFactory())["id"]

    assert (await crud.delete(db, credential_id)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, updateData, expected",
    [
        (
            {
                "login": "one login",
                "password": "one password",
                "key": "one key",
                "description": "one desc",
            },
            {
                "login": "another login",
                "password": "another password",
                "key": "another key",
                "description": "another desc",
            },
            {
                "login": "another login",
                "password": "another password",
                "key": "another key",
                "description": "another desc",
            },
        )
    ],
)
async def test_update(db, input, updateData, expected):
    credential_id = (await CredentialFactory(**input))["id"]

    credential = await crud.update(
        db=db, credential_id=credential_id, credential=CredentialUpdateIn(**updateData)
    )

    for key in expected:
        assert credential[key] == expected[key]


@pytest.mark.asyncio
async def test_get_unknown(db):
    db_credential = await crud.get(db=db, credential_id=666)

    assert db_credential is None


@pytest.mark.asyncio
async def test_check(db):
    credential = await CredentialFactory()

    assert await crud.check(db=db, credential_id=credential["id"])
