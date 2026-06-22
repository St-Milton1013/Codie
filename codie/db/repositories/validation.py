"""Repository queries for governance and data-health validation."""

from __future__ import annotations

from typing import Any

from .base import BaseRepository


class ValidationRepository(BaseRepository):
    def canonical_coverage_counts(self) -> dict[str, Any]:
        row = self.connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM source_events) AS source_event_count,
                (SELECT COUNT(*) FROM canonical_events) AS canonical_event_count,
                (
                    SELECT COUNT(*)
                    FROM source_events
                    WHERE canonical_event_id IS NOT NULL
                ) AS canonicalized_source_event_count,
                (
                    SELECT COUNT(*)
                    FROM source_events
                    WHERE canonical_event_id IS NULL
                        AND COALESCE(dedupe_status, 'pending') = 'pending'
                ) AS pending_source_event_count,
                (
                    SELECT COUNT(*)
                    FROM source_events
                    WHERE canonical_event_id IS NULL
                        AND COALESCE(dedupe_status, 'pending') != 'pending'
                ) AS unresolved_source_event_count,
                (SELECT COUNT(*) FROM canonical_event_sources) AS canonical_event_source_link_count,
                (SELECT COUNT(*) FROM source_decks) AS source_deck_count,
                (SELECT COUNT(*) FROM canonical_decks) AS canonical_deck_count,
                (
                    SELECT COUNT(*)
                    FROM source_decks
                    WHERE canonical_deck_id IS NOT NULL
                ) AS canonicalized_source_deck_count,
                (
                    SELECT COUNT(*)
                    FROM source_decks
                    WHERE canonical_deck_id IS NULL
                        AND COALESCE(dedupe_status, 'pending') = 'pending'
                ) AS pending_source_deck_count,
                (
                    SELECT COUNT(DISTINCT sd.source_deck_id)
                    FROM source_decks sd
                    LEFT JOIN source_deck_cards sdc ON sdc.source_deck_id = sd.source_deck_id
                    WHERE (
                        sd.canonical_deck_id IS NULL
                        AND COALESCE(sd.dedupe_status, 'pending') != 'pending'
                    )
                    OR sdc.resolution_status NOT IN ('exact', 'alias')
                ) AS unresolved_source_deck_count,
                (SELECT COUNT(*) FROM canonical_deck_sources) AS canonical_deck_source_link_count
            """
        ).fetchone()
        return dict(row)
