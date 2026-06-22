"""EDHTop16 GraphQL client.

The client is transport-injected for tests. Unit tests use fixture transports
and never make live network calls.
"""

from __future__ import annotations

import json
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from codie.providers.errors import NetworkError, ParseError, RateLimitError

Transport = Callable[[str, dict[str, str], float], tuple[int, str]]

TOURNAMENTS_QUERY = """
query CodieEDHTop16Tournaments($first: Int!, $filters: TournamentFilters) {
  tournaments(first: $first, filters: $filters) {
    edges {
      node {
        TID
        name
        size
        tournamentDate
        bracketUrl
        entries {
          id
          standing
          decklist
          winsSwiss
          winsBracket
          draws
          lossesSwiss
          lossesBracket
          winRate
          commander { name }
          player { name }
          maindeck { name }
        }
      }
    }
  }
}
""".strip()

DECKLIST_QUERY = """
query CodieEDHTop16Decklist($id: ID!) {
  node(id: $id) {
    ... on Entry {
      id
      standing
      decklist
      winsSwiss
      winsBracket
      draws
      lossesSwiss
      lossesBracket
      winRate
      commander { name }
      player { name }
      maindeck { name }
      tournament { TID }
    }
  }
}
""".strip()


def _urllib_transport(url: str, headers: dict[str, str], timeout_seconds: float) -> tuple[int, str]:
    body = headers.pop("X-Codie-Body", "{}")
    request = Request(url, data=body.encode("utf-8"), headers=headers, method="POST")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return int(response.status), response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body
    except (TimeoutError, OSError, URLError) as exc:
        raise NetworkError(str(exc)) from exc


class EDHTop16Client:
    """Small rate-limited JSON client for EDHTop16 GraphQL."""

    def __init__(
        self,
        *,
        endpoint_url: str = "https://edhtop16.com/graphql",
        timeout_seconds: float = 10.0,
        min_interval_seconds: float = 0.2,
        transport: Transport | None = None,
    ) -> None:
        self.endpoint_url = endpoint_url
        self.timeout_seconds = timeout_seconds
        self.min_interval_seconds = min_interval_seconds
        self.transport = transport or _urllib_transport
        self._last_request_at = 0.0

    def fetch_tournaments(self, filters: dict[str, Any] | None = None, *, first: int = 20) -> dict[str, Any]:
        return self._request_json(TOURNAMENTS_QUERY, {"filters": filters or {}, "first": first})

    def fetch_decklist(self, deck_id: str) -> dict[str, Any]:
        return self._request_json(DECKLIST_QUERY, {"id": deck_id})

    def _request_json(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        self._rate_limit()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Codie/0.1 (+https://edhtop16.com attribution; local research client)",
        }
        body = json.dumps({"query": query, "variables": variables or {}})
        status, response_body = self.transport(
            self.endpoint_url,
            headers | {"X-Codie-Body": body},
            self.timeout_seconds,
        )
        if status == 429:
            raise RateLimitError("EDHTop16 rate limit response")
        if status >= 500:
            raise NetworkError(f"EDHTop16 server error: HTTP {status}")
        if status >= 400:
            raise NetworkError(f"EDHTop16 request failed: HTTP {status}", retryable=False)
        try:
            payload = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise ParseError(f"EDHTop16 returned invalid JSON: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ParseError("EDHTop16 GraphQL response must be an object")
        if payload.get("errors") and not payload.get("data"):
            raise ParseError("EDHTop16 GraphQL response contained errors without data")
        return payload

    def _rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if self._last_request_at and elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()
