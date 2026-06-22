"""Evidence bundle primitives for future recommendation candidates."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass


ALLOWED_SOURCE_TYPES = frozenset(
    {
        "tournament",
        "primer",
        "combo",
        "package",
        "simulation",
        "analytics",
        "historical",
        "regional",
        "curated",
    }
)

FORBIDDEN_CLAIM_FRAGMENTS = (
    "this deck is trying to",
    "the game plan is",
    "this deck should",
    "should play",
    "must include",
    "strictly better",
    "cut this",
    "always include",
)


@dataclass(frozen=True)
class EvidenceItem:
    claim_type: str
    claim_text: str
    source_type: str
    source_name: str
    metric_value: float
    metric_unit: str
    sample_size: int
    confidence: float
    recency_window: str
    generated_at: str
    reproducibility_notes: str
    source_url: str | None = None
    source_record_id: str | None = None
    formula: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.claim_type, "claim_type")
        object.__setattr__(self, "claim_text", validate_claim_text(self.claim_text))
        source_type = self.source_type.strip().lower()
        if source_type not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"unsupported source_type: {self.source_type}")
        object.__setattr__(self, "source_type", source_type)
        _require_text(self.source_name, "source_name")
        _require_text(self.metric_unit, "metric_unit")
        _require_text(self.recency_window, "recency_window")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.reproducibility_notes, "reproducibility_notes")
        if self.source_url in (None, "") and self.source_record_id in (None, ""):
            raise ValueError("source_url or source_record_id is required")
        if self.sample_size < 0:
            raise ValueError("sample_size must be non-negative")
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class EvidenceBundle:
    entity_type: str
    entity_id: str
    generated_at: str
    items: tuple[EvidenceItem, ...]

    def __post_init__(self) -> None:
        _require_text(self.entity_type, "entity_type")
        _require_text(self.entity_id, "entity_id")
        _require_text(self.generated_at, "generated_at")
        if not self.items:
            raise ValueError("EvidenceBundle requires at least one item")


@dataclass(frozen=True)
class EvidenceStackSummary:
    entity_type: str
    entity_id: str
    total_evidence_count: int
    source_type_counts: dict[str, int]
    volume_score: float
    generated_at: str
    reproducibility_notes: str


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def validate_claim_text(text: str) -> str:
    _require_text(text, "claim_text")
    normalized = " ".join(text.strip().lower().split())
    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in normalized:
            raise ValueError(f"unsupported strategic claim text: {fragment}")
    return text.strip()


def build_evidence_bundle(
    *,
    entity_type: str,
    entity_id: str,
    items: Iterable[EvidenceItem],
    generated_at: str,
) -> EvidenceBundle:
    ordered_items = tuple(sorted(items, key=lambda item: (item.source_type, item.claim_type, item.source_name)))
    return EvidenceBundle(
        entity_type=entity_type,
        entity_id=entity_id,
        generated_at=generated_at,
        items=ordered_items,
    )


def evidence_stack_summary(bundle: EvidenceBundle, *, cap_per_type: int = 10) -> EvidenceStackSummary:
    if cap_per_type <= 0:
        raise ValueError("cap_per_type must be greater than zero")
    counts = Counter(item.source_type for item in bundle.items)
    possible_volume = cap_per_type * len(ALLOWED_SOURCE_TYPES)
    capped_volume = sum(min(count, cap_per_type) for count in counts.values())
    return EvidenceStackSummary(
        entity_type=bundle.entity_type,
        entity_id=bundle.entity_id,
        total_evidence_count=len(bundle.items),
        source_type_counts=dict(sorted(counts.items())),
        volume_score=capped_volume / possible_volume,
        generated_at=bundle.generated_at,
        reproducibility_notes="Evidence stack score is evidence volume only, capped per source type.",
    )
