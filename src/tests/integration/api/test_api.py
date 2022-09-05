import pytest
from pytest_mock import MockFixture

good_headers = {
    'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0Mzk5ODI1NzIsImlhdCI6MTY2MjM4MjU3MiwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.rleKnAXPsqH-PkVGiYH3KKbRuLOCzdJxO9ygFrnmim8',
    'Content-Type': 'application/json',
}
bad_headers = {
    'Bearer': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI0Mzk5ODI1NzIsImlhdCI6MTY2MjM4MjU3MiwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.rleKnAXPsqH-PkVGiYH3KKbRuLOCzdJxO9ygFrnmim8',
    'Content-Type': 'application/json',
}

async def test_get_token(cli, mock_resp):
    resp = await cli.post('/', json={
        "name": "user",
        "password": "user",
    })
    resp_json = await resp.json()
    assert resp_json != {
        "token": "null"
    }


async def test_failed_authorization(cli, mock_resp):
    resp = await cli.post('/', json={
        "name": "zxcvasdf",
        "password": "123"
    })
    resp_json = await resp.json()
    assert resp_json == {
        "token": "False"
    }


async def test_failed_authorization_wrong_data(cli, mock_resp):
    resp = await cli.post('/', json={
        "name": "zxcvasdf",
        "password": 123,
    },
                          )
    resp_json = await resp.json()
    assert resp_json == {
        'json': {'password': ['Not a valid string.']},
    }


async def test_not_saved_msg(cli, mock_resp):
    resp = await cli.post('/msg', headers=bad_headers, json={
        "name": "user",
        "message": "my test message",
    })
    resp_json = await resp.json()
    assert resp_json == {
        "is_saved": False
    }


async def test_saved_msg(cli, mock_resp):
    resp = await cli.post('/msg', headers=good_headers, json={
        "name": "user",
        "message": "hiscvbn",
    })
    resp_json = await resp.json()
    assert resp_json == {
        "is_saved": True
    }


async def test_history_correct(cli, mock_resp):
    resp = await cli.post('/msg', headers=good_headers, json={
        "name": "user",
        "message": "history 10",
    })
    resp_json = await resp.json()
    assert resp_json == {
        'name': 'user',
        'history': "[('hiscvbn',), ('hiscvbn',), ('hiscvbn',), ('hiscvbn',), "
                   "('hiscvbn',), ('hiscvbn',), ('hiscvbn',), ('hiscvbn',), "
                   "('hiscvbn',), ('hiscvbn',)]",
    }

