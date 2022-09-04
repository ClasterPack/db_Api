from aiohttp import web

from src.api.controller import UsersAuth


async def user_auth(app: web.Application):
    app['users_auth'] = UsersAuth
