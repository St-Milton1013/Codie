"""Moxfield JSON client.

The client is transport-injected for tests. Unit tests use fixtures and do not
make live network calls.
"""

from __future__ import annotations

import json
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from codie.providers.errors import NetworkError, ParseError, RateLimitError

Transport = Callable[[str, dict[str, str], float], tuple[int, str]]


def _urllib_transport(url: str, headers: dict[str, str], timeout_seconds: float) -> tuple[int, str]:
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return int(response.status), response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body
    except (TimeoutError, OSError, URLError) as exc:
        raise NetworkError(str(exc)) from exc


class MoxfieldClient:
    """Small rate-limited JSON client for Moxfield deck metadata."""

    def __init__(
        self,
        *,
        base_url: str = "https://api.moxfield.com/v2/decks/all",
        timeout_seconds: float = 10.0,
        min_interval_seconds: float = 0.2,
        transport: Transport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.min_interval_seconds = min_interval_seconds
        self.transport = transport or _urllib_transport
        self._last_request_at = 0.0

    def fetch_deck(self, deck_id: str) -> dict[str, Any]:
        return self._request_json(f"{self.base_url}/{deck_id}")

    def _request_json(self, url: str) -> dict[str, Any]:
        self._rate_limit()
        headers = {
            "Accept": "application/json",
            "User-Agent": "Codie/0.1 (+https://moxfield.com attribution; local research client)",
        }
        status, body = self.transport(url, headers, self.timeout_seconds)
        if status == 429:
            raise RateLimitError("Moxfield rate limit response")
        if status >= 500:
            raise NetworkError(f"Moxfield server error: HTTP {status}")
        if status >= 400:
            raise NetworkError(f"Moxfield request failed: HTTP {status}", retryable=False)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ParseError("Moxfield response was not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ParseError("Moxfield response must be a JSON object")
        return payload

    def _rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if self._last_request_at and elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()
