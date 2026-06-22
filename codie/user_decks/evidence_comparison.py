"""Evidence-only comparison between user decks and card evidence candidates."""

from __future__ import annotations

from dataclasses import dataclass

from .analysis_input import UserDeckAnalysisInput


FORBIDDEN_COMPARISON_FRAGMENTS = (
    "should play",
    "must include",
    "correct card",
    "breaks the format",
    "secretly optimal",
)


@dataclass(frozen=True)
class UserDeckEvidenceCandidate:
    oracle_id: str
    card_name: str
    evidence_type: str
    score: float | None = None
    sample_size: int | None = None
    source_record_id: str | None = None
    source_url: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.card_name, "card_name")
        _require_text(self.evidence_type, "evidence_type")
        if self.score is not None and (self.score < 0 or self.score > 1):
            raise ValueError("score must be between 0 and 1")
        if self.sample_size is not None and self.sample_size < 0:
            raise ValueError("sample_size must be non-negative")


@dataclass(frozen=True)
class UserDeckEvidenceComparisonRow:
    oracle_id: str
    card_name: str
    evidence_type: str
    presence_status: str
    quantity_in_deck: int
    zones: tuple[str, ...]
    score: float | None
    sample_size: int | None
    source_record_id: str | None
    source_url: str | None
    evidence_line: str

    def __post_init__(self) -> None:
        if self.presence_status not in {"present", "absent"}:
            raise ValueError("presence_status must be present or absent")
        object.__setattr__(self, "evidence_line", _validate_evidence_line(self.evidence_line))


@dataclass(frozen=True)
class UserDeckEvidenceComparison:
    user_deck_id: int
    deck_hash: str
    commander_hash: str | None
    rows: tuple[UserDeckEvidenceComparisonRow, ...]
    present_count: int
    absent_count: int
    generated_at: str


def compare_user_deck_to_evidence(
    analysis_input: UserDeckAnalysisInput,
    candidates: tuple[UserDeckEvidenceCandidate, ...],
    *,
    generated_at: str,
) -> UserDeckEvidenceComparison:
    """Compare a resolved user deck to evidence candidates without ranking advice."""

    _require_text(generated_at, "generated_at")
    quantities: dict[str, int] = {}
    zones: dict[str, set[str]] = {}
    for card in analysis_input.cards:
        if not card.oracle_id:
            continue
        quantities[card.oracle_id] = quantities.get(card.oracle_id, 0) + card.quantity
        zones.setdefault(card.oracle_id, set()).add(card.zone)

    rows = tuple(
        _comparison_row(candidate, quantities=quantities, zones=zones)
        for candidate in sorted(candidates, key=lambda item: (item.evidence_type, item.card_name, item.oracle_id))
    )
    return UserDeckEvidenceComparison(
        user_deck_id=analysis_input.user_deck_id,
        deck_hash=analysis_input.deck_hash,
        commander_hash=analysis_input.commander_hash,
        rows=rows,
        present_count=sum(1 for row in rows if row.presence_status == "present"),
        absent_count=sum(1 for row in rows if row.presence_status == "absent"),
        generated_at=generated_at,
    )


def _comparison_row(
    candidate: UserDeckEvidenceCandidate,
    *,
    quantities: dict[str, int],
    zones: dict[str, set[str]],
) -> UserDeckEvidenceComparisonRow:
    quantity = quantities.get(candidate.oracle_id, 0)
    status = "present" if quantity > 0 else "absent"
    zone_tuple = tuple(sorted(zones.get(candidate.oracle_id, set())))
    line = (
        f"{candidate.card_name} is {status} in the imported user deck; "
        f"evidence type {candidate.evidence_type}; sample size {candidate.sample_size or 0}."
    )
    return UserDeckEvidenceComparisonRow(
        oracle_id=candidate.oracle_id,
        card_name=candidate.card_name,
        evidence_type=candidate.evidence_type,
        presence_status=status,
        quantity_in_deck=quantity,
        zones=zone_tuple,
        score=candidate.score,
        sample_size=candidate.sample_size,
        source_record_id=candidate.source_record_id,
        source_url=candidate.source_url,
        evidence_line=line,
    )


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _validate_evidence_line(text: str) -> str:
    _require_text(text, "evidence_line")
    normalized = " ".join(text.lower().split())
    for fragment in FORBIDDEN_COMPARISON_FRAGMENTS:
        if fragment in normalized:
            raise ValueError(f"unsupported strategic comparison text: {fragment}")
    return text.strip()
