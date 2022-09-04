from pathlib import Path

import pytest
import yaml
from aioresponses import aioresponses

from src.app import init_app


@pytest.fixture(scope='session')
def config():
    """Конфигурация сервиса в виде dict."""
    return yaml.safe_load(Path('config.yml', ).read_text())


@pytest.fixture
def cli(loop, aiohttp_client, config):
    app = init_app(config)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture()
def mock_resp():
    class MockResponse:
        def __int__(self, status, json=None):
            self.status = status
            if json is None:
                json = {}
            self._json = json

        async def json(self):
            return self._json

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def __aenter__(self):
            return self

    return MockResponse


@pytest.fixture
def http_async_mock(mocker):
    return mocker.path('aiohttp.ClientSession.get', mocker.AsyncMock())


@pytest.fixture
def http_mock(mocker):
    return mocker.path('aiohttp.ClientSession.get')
