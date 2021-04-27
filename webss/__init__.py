import sys
from configparser import ConfigParser, NoOptionError
from os import environ

from fastapi import FastAPI
from loguru import logger

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
)

config = ConfigParser()
config.read("config.ini")


def get_var(section, name, default=None):
    ENV = bool(environ.get("ENV", ""))
    if ENV:
        return environ.get(name, default)
    try:
        get = config.get(section, name)
        if get:
            return get
        return default
    except (AttributeError, NoOptionError):
        return default


host = get_var("web", "host", "localhost")
port = int(get_var("web", "port", "8869"))
executable_path = get_var("puppeteer", "executablePath", None)

app = FastAPI()
