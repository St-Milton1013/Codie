"""MTGDecks HTML/text client.

The client is transport-injected for tests. Unit tests use fixture transports
and never make live network calls.
"""

from __future__ import annotations

import time
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from codie.providers.errors import NetworkError, RateLimitError

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


class MTGDecksClient:
    """Small rate-limited text/HTML client for MTGDecks pages."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 10.0,
        min_interval_seconds: float = 0.2,
        transport: Transport | None = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.min_interval_seconds = min_interval_seconds
        self.transport = transport or _urllib_transport
        self._last_request_at = 0.0

    def fetch_event_page(self, event_url: str) -> str:
        return self._request_text(event_url)

    def fetch_deck_page(self, deck_url: str) -> str:
        return self._request_text(deck_url)

    def _request_text(self, url: str) -> str:
        self._rate_limit()
        headers = {
            "Accept": "text/html,text/plain,application/xhtml+xml",
            "User-Agent": "Codie/0.1 (+https://mtgdecks.net attribution; local research client)",
        }
        status, body = self.transport(url, headers, self.timeout_seconds)
        if status == 429:
            raise RateLimitError("MTGDecks rate limit response")
        if status >= 500:
            raise NetworkError(f"MTGDecks server error: HTTP {status}")
        if status >= 400:
            raise NetworkError(f"MTGDecks request failed: HTTP {status}", retryable=False)
        return body

    def _rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if self._last_request_at and elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()
