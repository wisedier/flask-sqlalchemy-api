import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database

from api.app import create_app
from config import config
from db import base
from db.base import Base
from utils.sqlalchemy import import_models, turn_off_alchemy_log

turn_off_alchemy_log()


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session', autouse=True)
def db():
    import_models()
    db_uri = config.SQLALCHEMY_DATABASE_URI
    if database_exists(db_uri):
        drop_database(db_uri)
    create_database(db_uri)
    Base.metadata.create_all(bind=base.db_engine)

    yield

    drop_database(config.SQLALCHEMY_DATABASE_URI)
