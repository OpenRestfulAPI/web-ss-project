import sys, re
import pyppeteer
from fastapi import FastAPI
from fastapi.responses import FileResponse
from temp import tempfile
import uvicorn
from loguru import logger
from configparser import ConfigParser
from os import environ


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


logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")


app = FastAPI()


@app.get("/")
async def endpoint(site: str):
    """__[Web-SS Endpoint]__
    __Args:__
        `site (str)`: `[website url]`
    __Returns:__
        `[type]`: `[FileResponse]` = image: mime_type: image/png
    
    __Exception:__
        `[error]`: `[pyppeteer.errors]`
    """
    if re.match(r'^https?://', site):
        url = site
    else:
        url = 'http://'+site
    browser = await pyppeteer.launch(headless=True)
    page = await browser.newPage()
    file tempfile() + ".png"
    try:
        await page.goto(url)
        await page.setViewport({'width': 1280, 'height': 720})
    except pyppeteer.errors.NetworkError as e:
        return {"error": str(e)}
    await page.screenshot({'path': file})
    return FileResponse(file)


if __name__ == "__main__":
    uvicorn.run(app=app, host=host, port=port)
