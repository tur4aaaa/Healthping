"""
External Host Availability Checker API.

A lightweight public API service for checking the alive state of external hostnames.
This module provides functionality to verify and monitor the availability status
of remote hosts through HTTP/HTTPS protocols.

"""

import requests
from fastapi import FastAPI
from requests.exceptions import ConnectionError, InvalidURL

app = FastAPI()

REQUEST_TIMEOUT_SECONDS = 10


@app.get("/healthz")
async def healthz(hostname: str) -> dict:
    """
    Checks if the host is up or down.
    :param hostname: The name of the host being checked.
    """
    print("request", hostname)
    status = "up" if is_host_alive(hostname) else "down"
    print("response", status)

    return {"status": status, "hostname": hostname}


def is_host_alive(h: str) -> bool:
    url = "http://" + h
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        return response.status_code < 500

    except ConnectionError:
        return False

    except InvalidURL:
        return False
