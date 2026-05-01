from pathlib import Path

import psycopg2
import pytest
from pytest_postgresql import factories

from page_analyzer.app import app as flask_app

DATABASE_SQL = Path(__file__).resolve().parent.parent / 'database.sql'

postgresql_proc = factories.postgresql_proc(load=[DATABASE_SQL])
postgresql = factories.postgresql('postgresql_proc')


@pytest.fixture
def app(monkeypatch, postgresql):
    info = postgresql.info
    dsn = (
        f'postgres://{info.user}:@'
        f'{info.host}:{info.port}/'
        f'{info.dbname}'
    )
    monkeypatch.setenv('DATABASE_URL', dsn)
    flask_app.config.update(TESTING=True)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def conn(postgresql):
    info = postgresql.info
    c = psycopg2.connect(
        host=info.host,
        port=info.port,
        user=info.user,
        dbname=info.dbname,
    )
    yield c
    c.close()
