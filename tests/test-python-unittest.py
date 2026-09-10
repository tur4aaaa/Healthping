from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import ConnectionError, InvalidURL

from python_codereview import app, is_host_aliveHello




# Unittests

class FakeResponse:
    """A minimal fake replacement for requests.Response.

    Only implements what is_host_alive actually uses (.status_code),
    instead of mocking the whole requests library object.
    """

    def __init__(self, status_code: int):
        self.status_code = status_code


def test_is_host_alive_returns_true_for_2xx_using_stub():
    """Stub example: requests.get is replaced with a function that
    always returns a canned response, no call assertions made."""
    with patch(
        "python_codereview.requests.get",
        return_value=FakeResponse(200),
    ):
        assert is_host_alive("example.com") is True


def test_is_host_alive_returns_false_for_5xx_using_fake():
    """Fake example: FakeResponse behaves like a real Response object
    for the attributes our code under test actually touches."""
    with patch(
        "python_codereview.requests.get",
        return_value=FakeResponse(503),
    ):
        assert is_host_alive("example.com") is False


def test_is_host_alive_calls_requests_get_with_correct_url_using_mock():
    """Mock example: verifies not just the return value, but that
    requests.get was called correctly (URL, call count)."""
    mock_get = MagicMock(return_value=FakeResponse(200))
    with patch("python_codereview.requests.get", mock_get):
        is_host_alive("example.com")

    mock_get.assert_called_once()
    called_args, called_kwargs = mock_get.call_args
    assert called_args[0] == "http://example.com"
    assert "timeout" in called_kwargs


def test_is_host_alive_returns_false_on_connection_error():
    with patch(
        "python_codereview.requests.get",
        side_effect=ConnectionError,
    ):
        assert is_host_alive("unreachable-host.invalid") is False


def test_is_host_alive_returns_false_on_invalid_url():
    with patch(
        "python_codereview.requests.get",
        side_effect=InvalidURL,
    ):
        assert is_host_alive("not a valid url") is False


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
def test_is_host_alive_status_code_boundaries(status_code, expected):
    with patch(
        "python_codereview.requests.get",
        return_value=FakeResponse(status_code),
    ):
        assert is_host_alive("example.com") is expected
