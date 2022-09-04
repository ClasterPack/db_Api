from dataclasses import dataclass, field
from typing import Optional

import marshmallow
from marshmallow_dataclass import class_schema


@dataclass
class LoginRequest:
    """Объект запроса на логин."""
    name: str
    password: str


@dataclass
class LoginResponse:
    """Объект результата запроса на логин"""
    response: bool
    token: str or None


@dataclass
class ListenerRequest:
    """"Эндпоинт прослушивания и записи сообщений."""
    name: str
    message: str


@dataclass
class ListenerResponse:
    """Объект результата запроса на сохранение сообшения в БД."""
    is_saved: str or bool


LoginRequestSchema = class_schema(LoginRequest)
LoginResponseSchema = class_schema(LoginResponse)
ListenerRequestSchema = class_schema(ListenerRequest)
ListenerResponseSchema = class_schema(ListenerResponse)
