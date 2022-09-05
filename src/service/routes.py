import aiohttp_cors
from aiohttp.web_app import Application

from src.api.handler import authorization, msg_listener


def setup_routes(app: Application):
    """Настраивает эндпоинты сервиса с поддержкой CORS."""
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        ),
    })

    cors.add(app.router.add_post('', authorization))
    cors.add(app.router.add_post('/msg', msg_listener))
