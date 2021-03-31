import asyncio
from .import app, host, port
import pyppeteer
from fastapi.responses import FileResponse
from typing import Optional
from temp import tempfile
import uvicorn

browser = None
is_browser_started = False

async def start_browser():
    global browser, is_browser_started
    browser = await pyppeteer.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
            )
    is_browser_started = True


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
    global browser
    if not is_browser_started:
        print("started")
        await start_browser()
        is_browser_started = True
    page = await browser.newPage()
    file = tempfile() + ".png"
    await page.setViewport({'width': 2000, 'height': 1381, 'deviceScaleFactor': 2.0})
    try:
        await page.goto(site)
    except pyppeteer.errors.NetworkError as e:
        return {
            "error": str(e)
        }
    
    await page.screenshot({'path': file})
    await page.close()
    return FileResponse(file)

if __name__ == "__main__":
    uvicorn.run("webss:app", host=host, port=port, log_level="info")
