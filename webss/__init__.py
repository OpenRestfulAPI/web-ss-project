import sys
from fastapi import FastAPI
from loguru import logger
from configparser import ConfigParser
from os import environ


logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
)

config = ConfigParser()
config.read('config.ini')


def get_var(name, default=None):
    ENV = bool(environ.get('ENV', False))
    if ENV:
        return environ.get(name, default)

    try:
        return config.get('web', name)
    except AttributeError:
        return None


host = get_var('host', 'localhost')
port = int(get_var('port', 8869))


app = FastAPI()