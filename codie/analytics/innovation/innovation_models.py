"""Data models for evidence-first innovation detection."""

from __future__ import annotations

from dataclasses import dataclass


INNOVATION_TYPES = frozenset(
    {
        "new_innovation",
        "recent_breakout",
        "old_card_resurgence",
        "new_release_adoption",
        "commander_specific_innovation",
        "regional_innovation",
    }
)
_COLOR_ORDER = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}


@dataclass(frozen=True)
class InnovationObservation:
    oracle_id: str
    source_deck_id: str
    source_event_id: str
    event_date: str
    scryfall_id: str | None = None
    card_name: str | None = None
    type_line: str | None = None
    color_identity: tuple[str, ...] = ()
    commander_signature: str | None = None
    region_code: str | None = None
    country_code: str | None = None
    placement: int | None = None
    top_cut: bool = False
    winner: bool = False
    player_count: int | None = None
    card_released_at: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.source_deck_id, "source_deck_id")
        _require_text(self.source_event_id, "source_event_id")
        _require_text(self.event_date, "event_date")
        if self.placement is not None and self.placement <= 0:
            raise ValueError("placement must be positive when provided")
        if self.player_count is not None and self.player_count < 0:
            raise ValueError("player_count must be non-negative when provided")
        object.__setattr__(
            self,
            "color_identity",
            tuple(
                sorted(
                    {str(color).strip().upper() for color in self.color_identity if str(color).strip()},
                    key=lambda color: (_COLOR_ORDER.get(color, len(_COLOR_ORDER)), color),
                )
            ),
        )


@dataclass(frozen=True)
class InnovationSignal:
    innovation_id: str
    oracle_id: str
    scryfall_id: str | None
    commander_signature: str | None
    region_code: str | None
    innovation_type: str
    recent_window: str
    baseline_window: str
    recent_inclusion_rate: float | None
    baseline_inclusion_rate: float | None
    usage_delta: float | None
    recent_topcut_count: int
    recent_winner_count: int
    first_recent_seen_at: str
    last_seen_before_recent_window: str | None
    card_released_at: str | None
    is_new_release: bool
    sample_size: int
    confidence_score: float
    source_event_ids_json: str
    source_deck_ids_json: str
    generated_at: str

    def __post_init__(self) -> None:
        _require_text(self.innovation_id, "innovation_id")
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.innovation_type, "innovation_type")
        _require_text(self.recent_window, "recent_window")
        _require_text(self.baseline_window, "baseline_window")
        _require_text(self.first_recent_seen_at, "first_recent_seen_at")
        _require_text(self.source_event_ids_json, "source_event_ids_json")
        _require_text(self.source_deck_ids_json, "source_deck_ids_json")
        _require_text(self.generated_at, "generated_at")
        if self.innovation_type not in INNOVATION_TYPES:
            raise ValueError(f"unsupported innovation_type: {self.innovation_type}")
        if self.sample_size < 0:
            raise ValueError("sample_size must be non-negative")
        if self.confidence_score < 0 or self.confidence_score > 1:
            raise ValueError("confidence_score must be between 0 and 1")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
