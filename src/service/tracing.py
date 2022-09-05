import logging
import time
from types import SimpleNamespace

from aiohttp import (ClientSession, TraceConfig, TraceRequestEndParams,
                     TraceRequestExceptionParams, TraceRequestStartParams)


async def _on_request_start(
    session: ClientSession,
    trace_config_ctx: SimpleNamespace,
    params: TraceRequestStartParams,
):
    trace_config_ctx.req_time_monotonic = time.monotonic()


async def _on_request_end(
    session: ClientSession,
    trace_config_ctx: SimpleNamespace,
    params: TraceRequestEndParams,
) -> None:
    logging.info({
        'request': {
            'method': params.method,
            'url': {
                'host': params.url.host,
                'path': params.url.path,
                'query': [(qparam, qvalue) for qparam, qvalue in params.url.query.items()],
            },
            'headers': [(pkey, pvalue) for pkey, pvalue in params.headers.items()],
        },
        'status': params.response.status,
        'response': await params.response.text(),
        'time': time.monotonic() - trace_config_ctx.req_time_monotonic,
    })


async def _on_request_exception(
    session: ClientSession,
    trace_config_ctx: SimpleNamespace,
    params: TraceRequestExceptionParams,
) -> None:
    logging.exception({
        'request': {
            'method': params.method,
            'url': {
                'host': params.url.host,
                'path': params.url.path,
                'query': [(qparam, qvalue) for qparam, qvalue in params.url.query.items()],
            },
            'headers': [(pkey, pvalue) for pkey, pvalue in params.headers.items()],
        },
        'error': {
            'type': type(params.exception),
            'message': str(params.exception),
        },
        'time': time.monotonic() - trace_config_ctx.req_time_monotonic,
    })


def build_log_trace_config() -> TraceConfig:
    """Создаёт TraceConfig для логирования http ответа ClientSession."""
    trace_config = TraceConfig()
    trace_config.on_request_start.append(_on_request_start)
    trace_config.on_request_end.append(_on_request_end)
    trace_config.on_request_exception.append(_on_request_exception)
    return trace_config
