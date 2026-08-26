"""User-initiated card-catalog and public-deck sources for the local app."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from codie.frequency_pools import (
    MoxfieldFrequencyPoolBuildError,
    extract_moxfield_public_id,
)
from codie.providers.errors import NetworkError, ParseError, RateLimitError
from codie.providers.moxfield import MoxfieldClient

SCRYFALL_BULK_API = "https://api.scryfall.com/bulk-data"
SCRYFALL_BULK_TYPE = "oracle_cards"
DEFAULT_MAX_CATALOG_BYTES = 512 * 1024 * 1024
DEFAULT_MAX_UNCOMPRESSED_CATALOG_BYTES = 1024 * 1024 * 1024
DEFAULT_MAX_CATALOG_RECORDS = 100_000
_JSON_METADATA_LIMIT = 4 * 1024 * 1024
_USER_AGENT = "Codie/0.1 (local user-initiated card catalog)"
_MOXFIELD_BASE_URLS = (
    "https://api2.moxfield.com/v3/decks/all",
    "https://api.moxfield.com/v2/decks/all",
)


class LocalSourceError(ValueError):
    """A safe source failure that the local service can translate."""

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


@dataclass(frozen=True)
class CatalogSnapshotRef:
    path: Path
    content_hash: str
    source_uri: str
    source_updated_at: str | None
    from_cache: bool
    content_format: str = "json"


@dataclass(frozen=True)
class FetchedDeck:
    deck_name: str | None
    decklist: str
    source_url: str
    provider: str = "moxfield"


class ScryfallCatalogSource:
    """Download or reuse one contained Scryfall oracle-card snapshot."""

    def __init__(
        self,
        *,
        metadata_url: str = SCRYFALL_BULK_API,
        timeout_seconds: float = 60.0,
        max_catalog_bytes: int = DEFAULT_MAX_CATALOG_BYTES,
    ) -> None:
        self.metadata_url = metadata_url
        self.timeout_seconds = timeout_seconds
        self.max_catalog_bytes = max_catalog_bytes

    def prepare(self, workspace_root: Path, *, refresh: bool) -> CatalogSnapshotRef:
        cache_root = (workspace_root / "cache" / "card-catalog").resolve()
        _require_contained(workspace_root, cache_root)
        manifest_path = cache_root / "manifest.json"
        if manifest_path.is_file() and not refresh:
            return _cached_catalog_ref(cache_root, manifest_path)

        cache_root.mkdir(parents=True, exist_ok=True)
        metadata_url = _safe_scryfall_download_uri(self.metadata_url)
        metadata = _read_json_url(
            metadata_url,
            timeout_seconds=self.timeout_seconds,
            max_bytes=_JSON_METADATA_LIMIT,
        )
        record = _bulk_record(metadata, SCRYFALL_BULK_TYPE)
        download_uri, content_format, cache_file = _catalog_download(record)
        catalog_path = cache_root / cache_file
        temporary_path = cache_root / f"{cache_file}.part"
        try:
            content_hash = _download_to_path(
                download_uri,
                temporary_path,
                timeout_seconds=self.timeout_seconds,
                max_bytes=self.max_catalog_bytes,
            )
            os.replace(temporary_path, catalog_path)
            manifest = {
                "bulk_type": SCRYFALL_BULK_TYPE,
                "content_hash": content_hash,
                "content_format": content_format,
                "cache_file": cache_file,
                "download_uri": download_uri,
                "source_updated_at": _optional_text(record.get("updated_at")),
            }
            _write_json_atomically(manifest_path, manifest)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
        return CatalogSnapshotRef(
            path=catalog_path,
            content_hash=content_hash,
            source_uri=download_uri,
            source_updated_at=_optional_text(record.get("updated_at")),
            from_cache=False,
            content_format=content_format,
        )


class MoxfieldDeckSource:
    """Fetch a public Moxfield deck with a stable manual-paste fallback."""

    def __init__(self, clients: tuple[MoxfieldClient, ...] | None = None) -> None:
        self.clients = clients or tuple(
            MoxfieldClient(base_url=base_url) for base_url in _MOXFIELD_BASE_URLS
        )

    def fetch(self, source_url: str) -> FetchedDeck:
        try:
            public_id = extract_moxfield_public_id(source_url)
        except MoxfieldFrequencyPoolBuildError as exc:
            raise LocalSourceError(
                "invalid_moxfield_url",
                "Enter a public Moxfield deck link or paste the decklist text.",
            ) from exc

        failures: list[Exception] = []
        for client in self.clients:
            try:
                payload = client.fetch_deck(public_id)
                return moxfield_payload_to_deck(payload, public_id=public_id)
            except RateLimitError as exc:
                raise LocalSourceError(
                    "moxfield_rate_limited",
                    "Moxfield is temporarily rate limiting this request. Retry later or paste an export.",
                    retryable=True,
                ) from exc
            except (NetworkError, ParseError) as exc:
                failures.append(exc)
        raise LocalSourceError(
            "moxfield_fetch_failed",
            "The public Moxfield deck could not be loaded. It may be private, unavailable, or changed; paste its text export instead.",
            retryable=any(getattr(failure, "retryable", False) for failure in failures),
        )


def is_moxfield_deck_reference(value: str) -> bool:
    stripped = value.strip()
    if "\n" in stripped or "\r" in stripped:
        return False
    try:
        return (urlparse(stripped).hostname or "").lower() in {
            "moxfield.com",
            "www.moxfield.com",
        }
    except ValueError:
        return False


def moxfield_payload_to_deck(payload: Mapping[str, Any], *, public_id: str) -> FetchedDeck:
    if not isinstance(payload, Mapping):
        raise LocalSourceError(
            "moxfield_schema_changed",
            "Moxfield returned an unsupported public-deck response. Paste the deck export instead.",
        )
    boards = payload.get("boards")
    board_root = boards if isinstance(boards, Mapping) else payload
    sections = (
        ("Commander", ("commanders", "commander")),
        ("Mainboard", ("mainboard", "mainBoard", "main")),
        ("Sideboard", ("sideboard", "sideBoard")),
        ("Maybeboard", ("maybeboard", "maybeboardCards", "considering")),
    )
    output: list[str] = []
    imported_cards = 0
    for heading, keys in sections:
        board = next(
            (board_root.get(key) for key in keys if board_root.get(key) is not None),
            None,
        )
        rows = tuple(_moxfield_board_rows(board))
        if not rows:
            continue
        output.append(heading)
        output.extend(f"{quantity} {name}" for quantity, name in rows)
        output.append("")
        imported_cards += len(rows)
    if imported_cards == 0:
        raise LocalSourceError(
            "moxfield_schema_changed",
            "Moxfield returned no recognized deck sections. Paste the deck export instead.",
        )
    source_url = f"https://www.moxfield.com/decks/{public_id}"
    return FetchedDeck(
        deck_name=_optional_text(payload.get("name") or payload.get("title")),
        decklist="\n".join(output).strip() + "\n",
        source_url=source_url,
    )


def read_catalog_payloads(
    snapshot: CatalogSnapshotRef,
    *,
    max_uncompressed_bytes: int = DEFAULT_MAX_UNCOMPRESSED_CATALOG_BYTES,
    max_records: int = DEFAULT_MAX_CATALOG_RECORDS,
) -> tuple[Mapping[str, Any], ...]:
    if snapshot.content_format == "json":
        try:
            with snapshot.path.open("r", encoding="utf-8") as source_file:
                payload = json.load(source_file)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LocalSourceError(
                "catalog_cache_invalid", "The prepared card data was unreadable."
            ) from exc
        if isinstance(payload, Mapping):
            payload = payload.get("data", payload.get("cards"))
        if not isinstance(payload, list) or not payload:
            raise LocalSourceError(
                "catalog_cache_invalid", "The prepared card data was unreadable."
            )
        if len(payload) > max_records or not all(isinstance(item, Mapping) for item in payload):
            raise LocalSourceError("catalog_cache_invalid", "The prepared card data was invalid.")
        return tuple(payload)

    if snapshot.content_format != "jsonl_gzip":
        raise LocalSourceError(
            "catalog_cache_invalid", "The prepared card-data format was invalid."
        )
    payloads: list[Mapping[str, Any]] = []
    total = 0
    try:
        with gzip.open(snapshot.path, "rb") as source_file:
            for line in source_file:
                total += len(line)
                if total > max_uncompressed_bytes or len(payloads) >= max_records:
                    raise LocalSourceError(
                        "catalog_expansion_limit",
                        "The prepared card data exceeded its safe expansion limit.",
                    )
                if not line.strip():
                    continue
                payload = json.loads(line)
                if not isinstance(payload, Mapping):
                    raise LocalSourceError(
                        "catalog_cache_invalid",
                        "The prepared card data contained an invalid record.",
                    )
                payloads.append(payload)
    except LocalSourceError:
        raise
    except (OSError, EOFError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocalSourceError(
            "catalog_cache_invalid", "The prepared card data was unreadable."
        ) from exc
    if not payloads:
        raise LocalSourceError("catalog_cache_invalid", "The prepared card data was empty.")
    return tuple(payloads)


def _moxfield_board_rows(board: Any) -> Iterator[tuple[int, str]]:
    if isinstance(board, Mapping) and isinstance(board.get("cards"), Mapping | list | tuple):
        board = board["cards"]
    entries: Iterable[Any]
    if isinstance(board, Mapping):
        entries = board.values()
    elif isinstance(board, list | tuple):
        entries = board
    else:
        return
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        card = entry.get("card")
        card_mapping = card if isinstance(card, Mapping) else entry
        name = _optional_text(
            card_mapping.get("name") or card_mapping.get("cardName") or entry.get("name")
        )
        raw_quantity = entry.get("quantity", entry.get("count", 1))
        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            continue
        if name and quantity > 0:
            yield quantity, name


def _read_json_url(url: str, *, timeout_seconds: float, max_bytes: int) -> Mapping[str, Any]:
    body = _read_url_bytes(url, timeout_seconds=timeout_seconds, max_bytes=max_bytes)
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocalSourceError(
            "catalog_metadata_invalid", "Card-catalog metadata was invalid."
        ) from exc
    if not isinstance(payload, Mapping):
        raise LocalSourceError("catalog_metadata_invalid", "Card-catalog metadata was invalid.")
    return payload


def _read_url_bytes(url: str, *, timeout_seconds: float, max_bytes: int) -> bytes:
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": _USER_AGENT},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            _safe_scryfall_download_uri(_response_url(response, url))
            length = _content_length(response.headers.get("Content-Length"))
            if length is not None and length > max_bytes:
                raise LocalSourceError(
                    "source_too_large", "The remote source exceeded the safe size limit."
                )
            body = response.read(max_bytes + 1)
    except LocalSourceError:
        raise
    except OSError as exc:
        raise LocalSourceError(
            "catalog_network_failed",
            "The card catalog could not be reached. Retry when online.",
            retryable=True,
        ) from exc
    if len(body) > max_bytes:
        raise LocalSourceError(
            "source_too_large", "The remote source exceeded the safe size limit."
        )
    return body


def _download_to_path(url: str, path: Path, *, timeout_seconds: float, max_bytes: int) -> str:
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": _USER_AGENT},
        method="GET",
    )
    digest = hashlib.sha256()
    total = 0
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            _safe_scryfall_download_uri(_response_url(response, url))
            length = _content_length(response.headers.get("Content-Length"))
            if length is not None and length > max_bytes:
                raise LocalSourceError(
                    "source_too_large", "The card catalog exceeded the safe size limit."
                )
            with path.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > max_bytes:
                        raise LocalSourceError(
                            "source_too_large", "The card catalog exceeded the safe size limit."
                        )
                    digest.update(chunk)
                    output.write(chunk)
    except LocalSourceError:
        raise
    except OSError as exc:
        raise LocalSourceError(
            "catalog_network_failed",
            "The card catalog could not be downloaded. Retry when online.",
            retryable=True,
        ) from exc
    if total == 0:
        raise LocalSourceError("catalog_download_empty", "The downloaded card catalog was empty.")
    return "sha256:" + digest.hexdigest()


def _bulk_record(metadata: Mapping[str, Any], bulk_type: str) -> Mapping[str, Any]:
    records = metadata.get("data")
    if not isinstance(records, list):
        raise LocalSourceError("catalog_metadata_invalid", "Card-catalog metadata was invalid.")
    for record in records:
        if isinstance(record, Mapping) and record.get("type") == bulk_type:
            return record
    raise LocalSourceError("catalog_type_unavailable", "The required card catalog is unavailable.")


def _catalog_download(record: Mapping[str, Any]) -> tuple[str, str, str]:
    legacy_uri = _optional_text(record.get("download_uri"))
    if legacy_uri is not None:
        return _safe_scryfall_download_uri(legacy_uri), "json", "oracle_cards.json"
    jsonl_uri = _optional_text(record.get("jsonl_download_uri"))
    if jsonl_uri is not None:
        return _safe_scryfall_download_uri(jsonl_uri), "jsonl_gzip", "oracle_cards.jsonl.gz"
    raise LocalSourceError(
        "catalog_metadata_invalid", "Card-catalog download metadata was missing."
    )


def _safe_scryfall_download_uri(value: Any) -> str:
    if not isinstance(value, str):
        raise LocalSourceError(
            "catalog_metadata_invalid", "Card-catalog download metadata was missing."
        )
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (
        host == "scryfall.com"
        or host.endswith(".scryfall.com")
        or host == "scryfall.io"
        or host.endswith(".scryfall.io")
    ):
        raise LocalSourceError(
            "catalog_source_rejected", "The card-catalog source was not trusted."
        )
    return value


def _cached_catalog_ref(cache_root: Path, manifest_path: Path) -> CatalogSnapshotRef:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LocalSourceError(
            "catalog_cache_invalid",
            "The cached card catalog is invalid. Refresh it while online.",
        ) from exc
    if not isinstance(manifest, Mapping):
        raise LocalSourceError("catalog_cache_invalid", "The cached card catalog is invalid.")
    content_hash = _optional_text(manifest.get("content_hash"))
    source_uri = _optional_text(manifest.get("download_uri"))
    content_format = _optional_text(manifest.get("content_format")) or "json"
    cache_file = _optional_text(manifest.get("cache_file")) or "oracle_cards.json"
    if content_format not in {"json", "jsonl_gzip"} or cache_file not in {
        "oracle_cards.json",
        "oracle_cards.jsonl.gz",
    }:
        raise LocalSourceError("catalog_cache_invalid", "The cached card catalog is invalid.")
    catalog_path = cache_root / cache_file
    if content_hash is None or source_uri is None or not catalog_path.is_file():
        raise LocalSourceError("catalog_cache_invalid", "The cached card catalog is invalid.")
    if _file_sha256(catalog_path) != content_hash:
        raise LocalSourceError(
            "catalog_cache_invalid",
            "The cached card catalog failed its integrity check. Refresh it while online.",
        )
    return CatalogSnapshotRef(
        path=catalog_path,
        content_hash=content_hash,
        source_uri=source_uri,
        source_updated_at=_optional_text(manifest.get("source_updated_at")),
        from_cache=True,
        content_format=content_format,
    )


def _write_json_atomically(path: Path, payload: Mapping[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(
        json.dumps(dict(payload), sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source_file:
            while chunk := source_file.read(1024 * 1024):
                digest.update(chunk)
    except OSError as exc:
        raise LocalSourceError(
            "catalog_cache_invalid", "The cached card catalog is unreadable."
        ) from exc
    return "sha256:" + digest.hexdigest()


def _response_url(response: Any, fallback: str) -> str:
    geturl = getattr(response, "geturl", None)
    if not callable(geturl):
        return fallback
    value = geturl()
    return value if isinstance(value, str) else fallback


def _content_length(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _require_contained(root: Path, candidate: Path) -> None:
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise LocalSourceError(
            "workspace_path_escape", "The source cache left the workspace."
        ) from exc


def _optional_text(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
