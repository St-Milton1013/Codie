"""Filters and thresholds for innovation detection."""

from __future__ import annotations

from dataclasses import dataclass


BASELINE_WINDOW_DAYS = {
    "90d": 90,
    "180d": 180,
    "365d": 365,
}
_COLOR_ORDER = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}


@dataclass(frozen=True)
class InnovationFilter:
    window_end_date: str
    recent_window_days: int = 30
    baseline_window: str = "180d"
    commander_signature: str | None = None
    card_type_contains: tuple[str, ...] = ()
    color_identity: tuple[str, ...] = ()
    region_code: str | None = None
    minimum_event_size: int = 16
    minimum_placement: int = 16
    include_newly_released_cards: bool = True
    include_old_card_resurgences: bool = True
    minimum_sample_size: int = 1
    adoption_window_days: int = 30
    low_baseline_inclusion_threshold: float = 0.02
    breakout_delta_threshold: float = 0.05
    resurgence_inactive_days: int = 180

    def __post_init__(self) -> None:
        _require_text(self.window_end_date, "window_end_date")
        if self.recent_window_days <= 0:
            raise ValueError("recent_window_days must be positive")
        if self.baseline_window != "all_time" and self.baseline_window not in BASELINE_WINDOW_DAYS:
            raise ValueError("baseline_window must be 90d, 180d, 365d, or all_time")
        if self.minimum_event_size < 0:
            raise ValueError("minimum_event_size must be non-negative")
        if self.minimum_placement <= 0:
            raise ValueError("minimum_placement must be positive")
        if self.minimum_sample_size <= 0:
            raise ValueError("minimum_sample_size must be positive")
        if self.adoption_window_days <= 0:
            raise ValueError("adoption_window_days must be positive")
        if self.low_baseline_inclusion_threshold < 0 or self.low_baseline_inclusion_threshold > 1:
            raise ValueError("low_baseline_inclusion_threshold must be between 0 and 1")
        if self.breakout_delta_threshold < 0:
            raise ValueError("breakout_delta_threshold must be non-negative")
        if self.resurgence_inactive_days <= 0:
            raise ValueError("resurgence_inactive_days must be positive")
        object.__setattr__(
            self,
            "card_type_contains",
            tuple(str(value).strip().lower() for value in self.card_type_contains if str(value).strip()),
        )
        object.__setattr__(
            self,
            "color_identity",
            tuple(
                sorted(
                    {str(value).strip().upper() for value in self.color_identity if str(value).strip()},
                    key=lambda color: (_COLOR_ORDER.get(color, len(_COLOR_ORDER)), color),
                )
            ),
        )


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
