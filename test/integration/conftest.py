import pytest

from crypto_finder.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(loop, aiohttp_client, app):
    return loop.run_until_complete(aiohttp_client(app))
