import asyncio
from .import app, host, port
import pyppeteer
from fastapi.responses import FileResponse
from typing import Optional
from temp import tempfile
import uvicorn


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
    browser = await pyppeteer.launch(
        headless=True
    )
    page = await browser.newPage()
    file = tempfile() + ".png"
    try:
        await page.goto(site)
    except pyppeteer.errors.NetworkError as e:
        return {
            "error": str(e)
        }
    await page.screenshot({'path': file})
    return FileResponse(file)

if __name__ == "__main__":
    uvicorn.run("webss:app", host=host, port=port, log_level="info")