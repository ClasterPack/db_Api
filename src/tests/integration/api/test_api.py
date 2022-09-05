import pytest
from pytest_mock import MockFixture


async def test_get_token(cli, mock_resp):
    resp = await cli.put('')
