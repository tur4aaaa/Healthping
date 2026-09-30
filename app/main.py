import logging
import os
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = int(
    os.environ.get("REQUEST_TIMEOUT_SECONDS", "10")
)


@app.get("/healthz")
async def healthz(hostname: str) -> dict:
    """
    Checks if the host is up or down.
    :param hostname: The name of the host being checked.
    """
    logger.info("request: %s", hostname)

    status = "up" if await is_host_alive(hostname) else "down"

    logger.info("response: %s", status)

    return {
        "status": status,
        "hostname": hostname,
    }


async def is_host_alive(hostname: str) -> bool:
    """
    Checks whether the specified host is reachable.
    """

    #Если пользовател ввел просто google.com то добавляет https://
    if not hostname.startswith(("http://", "https://")):
        hostname = f"http://{hostname}"

    # ППроверяем URL ли корректный введен
    parsed_url = urlparse(hostname)

    if not parsed_url.netloc:
        return False

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
        ) as client:
            response = await client.get(hostname)

        return response.status_code < 500

    except (
        httpx.TimeoutException,
        httpx.ConnectError,
        httpx.InvalidURL,
        httpx.RequestError,
    ):
        return False