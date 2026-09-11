"""Tests for REST API health checking."""

import httpx
import pytest

from cloudops.api import ApiCheckError, check_api


def test_successful_api_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """A successful JSON response should return an API check result."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        assert url == "https://example.com/get"
        assert timeout == 10

        request = httpx.Request("GET", url)
        return httpx.Response(
            status_code=200,
            request=request,
            json={"status": "healthy"},
        )

    monkeypatch.setattr(httpx, "get", fake_get)

    result = check_api("https://example.com", 10)

    assert result.url == "https://example.com/get"
    assert result.status_code == 200
    assert result.response_time_ms >= 0
    assert result.data == {"status": "healthy"}


def test_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A non-successful HTTP status should raise ApiCheckError."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        request = httpx.Request("GET", url)
        return httpx.Response(status_code=503, request=request)

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(ApiCheckError, match="HTTP 503"):
        check_api("https://example.com", 10)


def test_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """A request timeout should raise ApiCheckError."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        request = httpx.Request("GET", url)
        raise httpx.TimeoutException("Request timed out", request=request)

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(ApiCheckError, match="timed out"):
        check_api("https://example.com", 10)


def test_connection_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A connection failure should raise ApiCheckError."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        request = httpx.Request("GET", url)
        raise httpx.ConnectError("Connection refused", request=request)

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(ApiCheckError, match="Could not connect"):
        check_api("https://example.com", 10)


def test_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    """A response containing invalid JSON should be rejected."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        request = httpx.Request("GET", url)
        return httpx.Response(
            status_code=200,
            request=request,
            content=b"this is not JSON",
        )

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(ApiCheckError, match="invalid JSON"):
        check_api("https://example.com", 10)


def test_json_array_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The API response must be a JSON object rather than an array."""

    def fake_get(url: str, timeout: float) -> httpx.Response:
        request = httpx.Request("GET", url)
        return httpx.Response(
            status_code=200,
            request=request,
            json=["healthy"],
        )

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(ApiCheckError, match="was not an object"):
        check_api("https://example.com", 10)
