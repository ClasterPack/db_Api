from aiohttp import web
from webargs import aiohttpparser

from src.api.schemas import (ListenerRequest, ListenerRequestSchema,
                             ListenerResponse, ListenerResponseSchema,
                             LoginRequest, LoginRequestSchema, LoginResponse,
                             LoginResponseSchema)


async def authorization(request: web.Request) -> web.Response:
    """Функция авторизации по бд и возврашения токена."""
    controller = request.app['users_auth']
    login_request: LoginRequest = await aiohttpparser.parser.parse(
        argmap=LoginRequestSchema,
        req=request,
        location='json',
    )
    db_respounce = controller().check_password(login_request.name, login_request.password)
    if db_respounce:
        login_response = LoginResponse(
            response=db_respounce,
            token=controller().jwt_token(login_request.name)
        )
    else:
        login_response = LoginResponse(
            response=db_respounce,
            token=None,
        )
    return web.json_response(LoginResponseSchema().dump(login_response))


async def msg_listener(request: web.Request) -> web.Response:
    controller = request.app['users_auth']
    msg_request: ListenerRequest = await aiohttpparser.parser.parse(
        argmap=ListenerRequestSchema,
        req=request,
        location='json',
    )
    header = request.headers.get('Authorization')
    if header.startswith('Bearer_'):
        token = request.headers.get('Authorization')[7:]
    else:
        token = None
    valid_jwt = controller().verify_bearer_token(token, msg_request.name)
    message = msg_request.message
    if valid_jwt:
        if message == 'history 10':
            msg_response = ListenerResponse(
                is_saved=controller().msg_history(msg_request.name)
            )
        else:
            msg_response = ListenerResponse(
                is_saved=controller().save_msg(msg_request.name, msg_request.message)
            )
    else:
        msg_response = ListenerResponse(False)
    return web.json_response(ListenerResponseSchema().dump(msg_response))
