from pytest import fixture
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from databases import DatabaseURL
from databases.importer import import_from_string

from lain_backend.app import create_app
from lain_backend.database import metadata, database


@fixture(scope="session")
def app() -> TestClient:
    app = create_app()
    return TestClient(app)


@fixture
def db(app):
    db_url = "sqlite:///./test.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    database.url = DatabaseURL(db_url)

    backend_cls = import_from_string(database.SUPPORTED_BACKENDS[database.url.dialect])
    database._backend = backend_cls(database.url, **database.options)

    metadata.create_all(engine)

    with app:
        yield database

    metadata.drop_all(engine)
