import pytest
from marshmallow.exceptions import ValidationError

from src.api.schemas import LoginRequestSchema


def test_status_schema_ok(caplog):
    """Тест на сериализацию объекта входного запроса схемой."""
    request = {
        "name": "user",
        "password": "user",
    }
    LoginRequestSchema().load(request)
    assert not caplog.records


@pytest.mark.parametrize("request_data", [
    {"sdf": 123},
    {},
    {"name": 123, "password": "3123"},
    {"name": 1234, "password": "asdf"}
])
def test_status_witch_error(caplog, request_data):
    """Тест на сериализацию объекта входного запроса схемой."""
    with pytest.raises(ValidationError) as ex:
        LoginRequestSchema().load(request_data)
    assert not caplog.records
