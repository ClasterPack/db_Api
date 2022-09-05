import logging
import time
from http import HTTPStatus

from aiohttp import web


@web.middleware
async def _log_request_data_middleware(request: web.Request, handler) -> web.StreamResponse:
    """Логирует информацию о запросе."""
    start_time = time.monotonic()
    response = await handler(request)
    logging.info({
        'time': time.monotonic() - start_time,
        'status_code': response.status,
        'request': {
            'method': request.method,
            'path': request.path,
            'headers': [
                '{pkey}: {pvalue}'.format(pkey=pkey, pvalue=pvalue)
                for pkey, pvalue in request.headers.items()
            ],
        },
    })
    return response


def build_middlewares():
    """Возвращает мидлвари сервиса."""
    return (
        _log_request_data_middleware,
    )
