from dataclasses import dataclass

from marshmallow_dataclass import class_schema


@dataclass
class LoginRequest:
    """Объект запроса на логин."""

    name: str
    password: str


@dataclass
class LoginResponse:
    """Объект результата запроса на логин."""

    token: str or bool


@dataclass
class ListenerRequest:
    """Эндпоинт прослушивания и записи сообщений."""

    name: str
    message: str


@dataclass
class ListenerResponse:
    """Объект результата запроса на сохранение сообшения в БД."""

    is_saved: bool


@dataclass
class HistoryResponse:
    """Объект результата запроса истории сообщений."""

    name: str
    history: str


LoginRequestSchema = class_schema(LoginRequest)
LoginResponseSchema = class_schema(LoginResponse)
ListenerRequestSchema = class_schema(ListenerRequest)
ListenerResponseSchema = class_schema(ListenerResponse)
HistoryResponseSchema = class_schema(HistoryResponse)
