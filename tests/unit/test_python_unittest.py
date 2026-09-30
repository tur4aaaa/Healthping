from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.main import is_host_alive


class FakeResponse:
    """A minimal fake replacement for httpx.Response."""

    def __init__(self, status_code: int):
        self.status_code = status_code


@pytest.mark.asyncio
async def test_is_host_alive_returns_true_for_2xx_using_stub():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(200)
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        assert await is_host_alive("example.com") is True


@pytest.mark.asyncio
async def test_is_host_alive_returns_false_for_5xx_using_fake():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(503)
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        assert await is_host_alive("example.com") is False


@pytest.mark.asyncio
async def test_is_host_alive_calls_httpx_with_correct_url():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(200)
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        await is_host_alive("example.com")

    mock_client.get.assert_called_once()

    called_args, called_kwargs = mock_client.get.call_args

    assert called_args[0] == "http://example.com"
    assert "timeout" not in called_kwargs


@pytest.mark.asyncio
async def test_is_host_alive_returns_false_on_connection_error():
    mock_client = AsyncMock()

    mock_client.get = AsyncMock(
        side_effect=httpx.ConnectError("Connection failed")
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        assert await is_host_alive(
            "unreachable-host.invalid"
        ) is False


@pytest.mark.asyncio
async def test_is_host_alive_returns_false_on_invalid_url():
    mock_client = AsyncMock()

    mock_client.get = AsyncMock(
        side_effect=httpx.InvalidURL("Invalid URL")
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        assert await is_host_alive(
            "not a valid url"
        ) is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code,expected",
    [
        (200, True),
        (301, True),
        (404, True),
        (499, True),
        (500, False),
        (503, False),
        (599, False),
    ],
)
async def test_is_host_alive_status_code_boundaries(
    status_code,
    expected,
):
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        return_value=FakeResponse(status_code)
    )

    with patch(
        "app.main.httpx.AsyncClient"
    ) as mock_async_client:

        mock_async_client.return_value.__aenter__.return_value = (
            mock_client
        )

        assert await is_host_alive(
            "example.com"
        ) is expected