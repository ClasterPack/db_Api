from aiohttp import web
from webargs import aiohttpparser

from src.api.schemas import (HistoryResponse, HistoryResponseSchema,
                             ListenerRequest, ListenerRequestSchema,
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
            token=controller().jwt_token(login_request.name),
        )
        return web.json_response(LoginResponseSchema().dump(login_response))
    if not db_respounce:
        login_response = LoginResponse(
            token=False,
        )
        return web.json_response(LoginResponseSchema().dump(login_response))


async def msg_listener(request: web.Request) -> web.Response:
    """Функция для приема сообшений в БД и отправки сообшений обратно пользователю по проверке."""
    controller = request.app['users_auth']
    msg_request: ListenerRequest = await aiohttpparser.parser.parse(
        argmap=ListenerRequestSchema,
        req=request,
        location='json',
    )
    """Получаем токен и проверяем его."""
    header = request.headers.get('Authorization')
    if header is not None and header.startswith('Bearer_'):
        token = request.headers.get('Authorization')[7:]
    else:
        token = None
    valid_jwt = controller().verify_bearer_token(token, msg_request.name)
    message = msg_request.message
    """Проверяем валидность токена и сообшение на наличие запроса истории сообщений."""
    if valid_jwt:
        if message == 'history 10':
            msg_response = HistoryResponse(
                name=msg_request.name,
                history=controller().msg_history(msg_request.name),
            )
            """Возращаем историю сообщений."""
            return web.json_response(HistoryResponseSchema().dump(msg_response))
        if message != 'history 10':
            msg_response = ListenerResponse(
                is_saved=controller().save_msg(
                    msg_request.name,
                    msg_request.message,
                ),
            )
            """Возврашаем bool о результате проверок и сохранении в БД."""
            return web.json_response(ListenerResponseSchema().dump(msg_response))
    else:
        msg_response = ListenerResponse(False)
        return web.json_response(ListenerResponseSchema().dump(msg_response))
