import argparse
import logging
import sys
from logging.config import dictConfig
from pathlib import Path

import yaml
from aiohttp import web

from src.service import middlewares, resources, routes


def init_app(config) -> web.Application:
    """Инициализация приложения со всеми настройками."""
    app = web.Application(
        middlewares=middlewares.build_middlewares(),
    )
    app['config'] = config
    dictConfig(config['logging'])
    routes.setup_routes(app)
    app.on_startup.append(resources.user_auth)
    return app


def start():
    """Запуск конфигурируемого приложения."""
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '-c',
        '--config',
        type=str,
        required=True,
        help='Path to configuration file',
    )
    options, _ = ap.parse_known_args(sys.argv[1:])

    config = yaml.safe_load(Path(options.config).read_text())
    logging.info(config)
    app = init_app(config)
    web.run_app(
        app,
        port=config['service']['port'],
        access_log=None,
    )


if __name__ == '__main__':
    start()
