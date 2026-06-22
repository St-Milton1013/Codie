"""TopDeck HTTP client.

The client is isolated from tests through an injectable transport. Unit tests use
fixture transports and do not make live network calls.
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
    method = headers.pop("X-Codie-Method", "GET")
    body = headers.pop("X-Codie-Body", "{}")
    data = body.encode("utf-8") if method == "POST" else None
    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return int(response.status), response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body
    except (TimeoutError, OSError, URLError) as exc:
        raise NetworkError(str(exc)) from exc


class TopDeckClient:
    """Small rate-limited JSON client for TopDeck endpoints."""

    def __init__(
        self,
        *,
        base_url: str = "https://topdeck.gg/api",
        api_key: str | None = None,
        timeout_seconds: float = 10.0,
        min_interval_seconds: float = 0.2,
        transport: Transport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.min_interval_seconds = min_interval_seconds
        self.transport = transport or _urllib_transport
        self._last_request_at = 0.0

    def fetch_event(self, event_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/v2/tournaments/{event_id}")

    def fetch_deck(self, deck_id: str) -> dict[str, Any]:
        if ":" not in deck_id:
            raise ParseError("TopDeck deck IDs must use 'tournament_id:player_id' for player deck details")
        tournament_id, player_id = deck_id.split(":", 1)
        return self._request_json("GET", f"/v2/tournaments/{tournament_id}/players/{player_id}")

    def fetch_tournaments(self, query: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("POST", "/v2/tournaments", query)

    def _request_json(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        self._rate_limit()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Codie/0.1 (+https://topdeck.gg attribution; local research client)",
        }
        if self.api_key:
            headers["Authorization"] = self.api_key
        status, response_body = self.transport(
            f"{self.base_url}{path}",
            headers | {"X-Codie-Method": method, "X-Codie-Body": json.dumps(body or {})},
            self.timeout_seconds,
        )
        if status == 429:
            raise RateLimitError("TopDeck rate limit response")
        if status >= 500:
            raise NetworkError(f"TopDeck server error: HTTP {status}")
        if status >= 400:
            raise NetworkError(f"TopDeck request failed: HTTP {status}", retryable=False)
        try:
            payload = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise ParseError(f"TopDeck returned invalid JSON: {exc.msg}") from exc
        if isinstance(payload, list):
            return {"items": payload}
        if isinstance(payload, dict):
            return payload
        raise ParseError("TopDeck JSON response must be an object or array")

    def _rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if self._last_request_at and elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()
