import logging
from urllib.parse import urlparse
import os
import httpx
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIME_SECONDS",10))


@app.get("/healthz")
async def healthz(hostname: str) -> dict:
    """
    Checks if the host is up or down.
    :param hostname: The name of the host being checked.
    """
    logger.info("request: %s", hostname)

    status = "up" if await is_host_alive(hostname) else "down"

    logger.info("response: %s", status)

    return {"status": status, "hostname": hostname}


async def is_host_alive(hostname: str) -> bool:
    parsed_url = urlparse(hostname)

    if not parsed_url.scheme:
        url = f"http://{hostname}"
    else:
        url = hostname

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            return response.status_code < 500

    except (httpx.ConnectError, httpx.InvalidURL):
        return False
