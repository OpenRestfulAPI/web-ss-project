import re
import sys
from io import BytesIO
from typing import Union

import pyppeteer
import uvicorn
from fastapi.responses import StreamingResponse
from pyppeteer.browser import Browser
from pyppeteer.errors import NetworkError, PageError

from . import app, host, port, executable_path

browser: Union[Browser, None] = None
browser_is_started = False


async def start_browser():
    global browser, browser_is_started
    options = {"headless": True, "args": ["--no-sandbox", "--disable-setuid-sandbox"]}
    if executable_path:
        options["executablePath"] = executable_path
    browser = await pyppeteer.launch(**options)
    browser_is_started = True


@app.get("/")
async def endpoint(url: str, width: int = 1280, height: int = 720):
    """
    __[Web-SS Endpoint]__
    __Args:__
        `url (str)`: `[website url]`
        optional `width (int)`: `[viewport width]` (default: 1280)
        optional `height (int)`: `[viewport height]` (default: 720)
    __Returns:__
        `[type]`: `[StreamingResponse]` = image: mime_type: image/jpeg
    __Exceptions:__
        `[error]`: `[pyppeteer.errors]`
    """
    global browser, browser_is_started
    if not browser_is_started:
        await start_browser()
    if re.match(r"^https?://", url):
        _url = url
    else:
        _url = "http://" + url
    page = await browser.newPage()
    try:
        await page.goto(_url)
        await page.setViewport({"width": width, "height": height})
    except (NetworkError, PageError) as e:
        return {"error": str(e)}
    screenshot = await page.screenshot({"type": "jpeg"})
    await page.close()
    return StreamingResponse(BytesIO(screenshot), media_type="image/jpeg")


if __name__ == "__main__":
    try:
        uvicorn.run(app=app, host=host, port=port)
    except (KeyboardInterrupt, RuntimeError, RuntimeWarning):
        sys.exit(0)
