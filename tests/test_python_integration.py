from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from Codereview.python_codereview import app

client = TestClient(app)


class FakeResponse:

    def __init__(self, status_code):
        self.status_code = status_code


def test_healthz_endpoint_returns_up_when_host_alive():
    with patch(
        "Codereview.python_codereview.is_host_alive",
        return_value=True,
    ):
        response = client.get(
            "/healthz",
            params={"hostname": "example.com"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "up",
        "hostname": "example.com",
    }


def test_healthz_endpoint_returns_down_when_host_not_alive():
    with patch(
        "Codereview.python_codereview.is_host_alive",
        return_value=False,
    ):
        response = client.get(
            "/healthz",
            params={"hostname": "example.com"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "down",
        "hostname": "example.com",
    }


def test_healthz_endpoint_full_flow_with_stubbed_requests():
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(200)
    )

    with patch(
        "Codereview.python_codereview.httpx.AsyncClient"
    ) as mock_async_client_cls:

        mock_async_client_cls.return_value.__aenter__.return_value = (
            mock_client
        )

        response = client.get(
            "/healthz",
            params={"hostname": "example.com"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "up"


def test_healthz_endpoint_full_flow_with_stubbed_5xx_requests():
    

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(503)
    )

    with patch(
        "Codereview.python_codereview.httpx.AsyncClient"
    ) as mock_async_client_cls:

        mock_async_client_cls.return_value.__aenter__.return_value = (
            mock_client
        )

        response = client.get(
            "/healthz",
            params={"hostname": "example.com"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "down"