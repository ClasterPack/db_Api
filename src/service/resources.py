from aiohttp import web

from src.api.controller import UsersAuth


async def user_auth(app: web.Application):
    """Собирает класс авторизации и запросов."""
    app['users_auth'] = UsersAuth
