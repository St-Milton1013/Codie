"""Persist primer discovery metadata."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Iterable, Protocol

from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.base import BaseRepository
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.source import SourceRepository


class PrimerCandidate(Protocol):
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
    raw_payload: Any
    author_url: str | None


@dataclass(frozen=True)
class PrimerSyncResult:
    source_primer_count: int
    registry_primer_count: int
    evidence_count_count: int
    skipped_registry_count: int


def _key(value: str | None) -> str | None:
    if value is None:
        return None
    lowered = value.lower().replace("//", " ")
    lowered = lowered.replace(chr(8217), "")
    lowered = re.sub(r"[']", "", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    normalized = re.sub(r"\s+", " ", lowered).strip()
    return normalized or None


def _metadata(candidate: PrimerCandidate, key: str, default: Any = None) -> Any:
    return candidate.objective_metadata.get(key, default)


def _quality_score(candidate: PrimerCandidate) -> float:
    score = 0.0
    score += 0.25 if _metadata(candidate, "has_primer_route", 0) else 0
    score += 0.25 if _metadata(candidate, "primer_content_present", 0) else 0
    score += min(int(_metadata(candidate, "primer_heading_count", 0) or 0), 8) * 0.03
    score += min(int(_metadata(candidate, "primer_external_link_count", 0) or 0), 10) * 0.01
    score += 0.05 if _metadata(candidate, "primer_toc_present", 0) else 0
    score += 0.05 if candidate.updated_at else 0
    return min(score, 1.0)


class PrimerMetadataSync:
    """Sync primer candidates into source and registry tables."""

    def __init__(
        self,
        source: SourceRepository,
        curated: CuratedRepository,
        analytics: AnalyticsRepository,
    ) -> None:
        self.source = source
        self.curated = curated
        self.analytics = analytics

    def sync_candidates(self, candidates: Iterable[PrimerCandidate]) -> PrimerSyncResult:
        now = BaseRepository.now()
        source_count = registry_count = evidence_count = skipped_count = 0

        for candidate in candidates:
            source_tags = _metadata(candidate, "source_tags", [])
            self.source.create_source_primer(
                {
                    "provider": candidate.provider,
                    "deck_url": candidate.deck_url,
                    "primer_url": candidate.primer_url,
                    "commander_text": candidate.commander_text,
                    "partner_text": candidate.partner_text,
                    "deck_title": candidate.deck_title,
                    "primer_title": candidate.primer_title,
                    "author": candidate.author,
                    "author_url": candidate.author_url,
                    "modified_at": candidate.updated_at,
                    "source_tags_json": json.dumps(source_tags, sort_keys=True, ensure_ascii=False),
                    "raw_metadata_json": candidate.raw_payload.raw_payload_json,
                    "imported_at": now,
                }
            )
            source_count += 1

            if not _metadata(candidate, "has_primer_route", 0):
                skipped_count += 1
                continue

            self.curated.upsert_primer(
                {
                    "source": candidate.provider,
                    "deck_url": candidate.deck_url,
                    "primer_url": candidate.primer_url,
                    "commander_key": _key(candidate.commander_text),
                    "partner_key": _key(candidate.partner_text),
                    "deck_title": candidate.deck_title,
                    "primer_title": candidate.primer_title,
                    "author": candidate.author,
                    "author_url": candidate.author_url,
                    "modified_at": candidate.updated_at,
                    "primer_updated_at_text": candidate.updated_at,
                    "primer_updated_at_parsed": candidate.updated_at,
                    "likes": candidate.likes,
                    "views": candidate.views,
                    "comments": candidate.comments,
                    "bracket": _metadata(candidate, "bracket"),
                    "has_primer_route": _metadata(candidate, "has_primer_route", 0),
                    "primer_content_present": _metadata(candidate, "primer_content_present", 0),
                    "primer_toc_present": _metadata(candidate, "primer_toc_present", 0),
                    "primer_heading_count": _metadata(candidate, "primer_heading_count", 0),
                    "primer_section_names_json": json.dumps(
                        _metadata(candidate, "primer_section_names", []),
                        sort_keys=True,
                        ensure_ascii=False,
                    ),
                    "primer_external_link_count": _metadata(candidate, "primer_external_link_count", 0),
                    "primer_video_count": _metadata(candidate, "primer_video_count", 0),
                    "primer_image_count": _metadata(candidate, "primer_image_count", 0),
                    "cedh_title_signal": _metadata(candidate, "cedh_title_signal", 0),
                    "cedh_tag_signal": _metadata(candidate, "cedh_tag_signal", 0),
                    "competitive_tag_signal": _metadata(candidate, "competitive_tag_signal", 0),
                    "tournament_title_signal": _metadata(candidate, "tournament_title_signal", 0),
                    "content_length_estimate": _metadata(candidate, "content_length_estimate"),
                    "primer_quality_score": _quality_score(candidate),
                    "raw_metadata_json": candidate.raw_payload.raw_payload_json,
                    "created_at": now,
                    "updated_at": now,
                }
            )
            registry_count += 1
            self.analytics.upsert_evidence_count(
                {
                    "entity_type": "primer",
                    "entity_id": candidate.primer_url,
                    "primer_evidence_count": 1,
                    "updated_at": now,
                }
            )
            evidence_count += 1

        return PrimerSyncResult(
            source_primer_count=source_count,
            registry_primer_count=registry_count,
            evidence_count_count=evidence_count,
            skipped_registry_count=skipped_count,
        )
