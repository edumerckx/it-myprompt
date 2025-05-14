import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from it_myprompt.app import app
from it_myprompt.database import get_session
from it_myprompt.models import User, table_registry
from it_myprompt.security import get_hash


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def _get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = _get_session
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(session):
    password = 'test'
    user = User(
        name='Test',
        email='test@it-myprompt.com',
        password=get_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    user.raw_password = password
    return user


@pytest.fixture
def token(client, user):
    resp = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.raw_password},
    )
    return resp.json()['access_token']
