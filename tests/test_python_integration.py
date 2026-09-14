from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import ConnectionError, InvalidURL

from Codereview.python_codereview import app, is_host_alive

client = TestClient(app)


class FakeResponse:
    """Minimal stand-in for an httpx.Response object."""
    def __init__(self, status_code):
        self.status_code = status_code


def test_healthz_endpoint_returns_up_when_host_alive():
    with patch("Codereview.python_codereview.is_host_alive", return_value=True):
        response = client.get("/healthz", params={"hostname": "example.com"})

    assert response.status_code == 200
    assert response.json() == {"status": "up", "hostname": "example.com"}


def test_healthz_endpoint_returns_down_when_host_not_alive():
    with patch("Codereview.python_codereview.is_host_alive", return_value=False):
        response = client.get("/healthz", params={"hostname": "example.com"})

    assert response.status_code == 200
    assert response.json() == {"status": "down", "hostname": "example.com"}


def test_healthz_endpoint_full_flow_with_stubbed_requests():
    """Full integration through the FastAPI layer down to httpx.get,
    only the network call itself is stubbed out. A 200 OK means the
    host is reachable and healthy, so status should be 'up'."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=FakeResponse(200))

    with patch("Codereview.python_codereview.httpx.AsyncClient") as mock_async_client_cls:
        mock_async_client_cls.return_value.__aenter__.return_value = mock_client
        response = client.get("/healthz", params={"hostname": "example.com"})

    assert response.status_code == 200
    assert response.json()["status"] == "up"


def test_healthz_endpoint_full_flow_with_stubbed_5xx_requests():
    """Same as above, but with a 5xx stubbed response, which means the
    server is up but erroring, so we report the host as 'down'."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=FakeResponse(503))

    with patch("Codereview.python_codereview.httpx.AsyncClient") as mock_async_client_cls:
        mock_async_client_cls.return_value.__aenter__.return_value = mock_client
        response = client.get("/healthz", params={"hostname": "example.com"})

    assert response.status_code == 200
    assert response.json()["status"] == "down"