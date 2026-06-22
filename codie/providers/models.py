"""Provider output candidate models.

Providers return these candidates and never persist them directly.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def normalize_provider_name(name: str) -> str:
    """Normalize names inside provider candidate models without importing app layers."""
    folded = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower().strip()
    lowered = lowered.replace("//", " ")
    lowered = re.sub(r"['’]", "", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


@dataclass(frozen=True)
class RawPayload:
    provider: str
    object_type: str
    provider_id: str | None
    source_url: str | None
    retrieved_at: str
    payload: Any
    raw_file_path: str | None = None

    @property
    def raw_payload_json(self) -> str:
        return _stable_json(self.payload)

    @property
    def payload_hash(self) -> str:
        digest = hashlib.sha256(self.raw_payload_json.encode("utf-8")).hexdigest()
        return f"sha256:{digest}"


@dataclass(frozen=True)
class SourceEventCandidate:
    provider: str
    provider_event_id: str | None
    source_url: str | None
    original_source: str | None
    original_source_url: str | None
    event_name: str | None
    event_date: str | None
    format: str | None
    region: str | None
    country: str | None
    store_tag: str | None
    language: str | None
    player_count: int | None
    deck_count: int | None
    raw_payload: RawPayload
    event_key: str | None = None


@dataclass(frozen=True)
class SourceDeckCandidate:
    provider: str
    provider_deck_id: str | None
    source_event_key: str | None
    source_url: str | None
    download_url: str | None
    deck_title: str | None
    commander_text: str | None
    pilot_name: str | None
    rank: int | None
    rank_label: str | None
    record: str | None
    win_rate: float | None
    archetype_name: str | None
    raw_payload: RawPayload
    deck_key: str | None = None
    cards: tuple["SourceDeckCardCandidate", ...] = ()


@dataclass(frozen=True)
class SourceDeckCardCandidate:
    source_deck_key: str
    raw_name: str
    quantity: int
    source_zone: str
    source_order: int | None
    raw_entry: str | None


@dataclass(frozen=True)
class SourcePrimerCandidate:
    provider: str
    primer_url: str
    deck_url: str | None
    commander_text: str | None
    partner_text: str | None
    deck_title: str | None
    primer_title: str | None
    author: str | None
    updated_at: str | None
    likes: int | None
    views: int | None
    comments: int | None
    objective_metadata: dict[str, Any]
    raw_payload: RawPayload


@dataclass(frozen=True)
class SourceComboCandidate:
    provider: str
    provider_combo_id: str | None
    combo_url: str | None
    combo_name: str | None
    components: tuple[str, ...]
    outputs: tuple[str, ...]
    raw_payload: RawPayload
    cards: tuple["SourceComboCardCandidate", ...] = ()


@dataclass(frozen=True)
class SourceComboCardCandidate:
    raw_name: str
    role: str | None
    required: bool = True
    raw_entry: Any | None = None
