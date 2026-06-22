"""Foundation analytics derived from canonical tournament records."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, UTC
from typing import Any

from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.regional import RegionalRepository

from .weights import AnalyticsError, final_entry_weight, normalize_time_window


WINDOW_DAYS = {
    "30d": 30,
    "30_day": 30,
    "30-day": 30,
    "90d": 90,
    "90_day": 90,
    "90-day": 90,
    "365d": 365,
    "1y": 365,
    "1_year": 365,
    "1-year": 365,
}


@dataclass(frozen=True)
class AnalyticsBuildResult:
    time_window: str
    window_end_date: str
    generated_at: str
    eligible_entry_count: int
    skipped_entry_count: int
    card_metric_count: int
    regional_metric_count: int
    evidence_count_count: int
    historical_snapshot_id: int | None


@dataclass
class TournamentEntry:
    row: Any
    entry_weight: float
    cards_by_oracle: dict[str, str]


def _today_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError as exc:
        raise AnalyticsError(f"Invalid event date: {value}") from exc


def _within_window(event_date: str | None, window_end_date: str, time_window: str) -> bool:
    normalized = normalize_time_window(time_window)
    if normalized == "all_time":
        return True
    event_day = _parse_day(event_date)
    if event_day is None:
        return False
    window_end = _parse_day(window_end_date)
    assert window_end is not None
    days = WINDOW_DAYS.get(normalized)
    if days is None:
        raise AnalyticsError(f"Unsupported analytics window: {time_window}")
    return window_end - timedelta(days=days) <= event_day <= window_end


def _dedupe_key(row: Any) -> tuple[Any, ...]:
    pilot = (row["pilot_name"] or "").strip().casefold()
    placement = row["placement"] if row["placement"] is not None else row["placement_label"] or ""
    return (row["canonical_event_id"], row["canonical_deck_id"], pilot, placement)


def _is_topcut(entry_or_row: Any) -> bool:
    row = entry_or_row.row if isinstance(entry_or_row, TournamentEntry) else entry_or_row
    if row["top_cut_made"] or row["final_pod"] or row["winner"]:
        return True
    placement = row["placement"]
    return placement is not None and placement <= 16


def _win_rate(rows: list[TournamentEntry]) -> float | None:
    wins = losses = draws = 0
    for entry in rows:
        wins += int(entry.row["wins"] or 0)
        losses += int(entry.row["losses"] or 0)
        draws += int(entry.row["draws"] or 0)
    total = wins + losses + draws
    if total == 0:
        return None
    return wins / total


def _rate(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


class AnalyticsFoundationBuilder:
    """Build reproducible analytics from canonical tournament records."""

    def __init__(
        self,
        analytics: AnalyticsRepository,
        regional: RegionalRepository,
        *,
        minimum_player_count: int = 16,
    ) -> None:
        self.analytics = analytics
        self.regional = regional
        self.minimum_player_count = minimum_player_count

    def build_card_metrics(self, time_window: str, window_end_date: str) -> AnalyticsBuildResult:
        normalized_window = normalize_time_window(time_window)
        generated_at = _today_utc()
        entries, skipped = self._eligible_entries(normalized_window, window_end_date)

        snapshot_id: int | None = None
        metric_count = 0
        regional_count = 0
        evidence_count = 0

        if entries:
            card_metrics = self._card_metrics(entries, normalized_window, window_end_date, generated_at)
            for metric in card_metrics:
                self.analytics.upsert_card_performance_metric(metric)
                self.analytics.upsert_evidence_count(
                    {
                        "entity_type": "card",
                        "entity_id": metric["oracle_id"],
                        "tournament_evidence_count": metric["sample_size"],
                        "updated_at": generated_at,
                    }
                )
                metric_count += 1
                evidence_count += 1

            snapshot_id = self.analytics.get_or_create_historical_snapshot(
                window_end_date,
                normalized_window,
                generated_at,
            )
            self.analytics.delete_historical_card_metrics(snapshot_id)
            for metric in card_metrics:
                self.analytics.create_historical_card_metric(
                    {
                        "snapshot_id": snapshot_id,
                        "oracle_id": metric["oracle_id"],
                        "inclusion_rate": metric["raw_inclusion_rate"],
                        "weighted_inclusion_rate": metric["weighted_inclusion_rate"],
                        "sample_size": metric["sample_size"],
                    }
                )

            for metric in self._regional_card_metrics(entries, normalized_window, window_end_date, generated_at):
                self.regional.upsert_card_metric(metric)
                regional_count += 1

        return AnalyticsBuildResult(
            time_window=normalized_window,
            window_end_date=window_end_date,
            generated_at=generated_at,
            eligible_entry_count=len(entries),
            skipped_entry_count=skipped,
            card_metric_count=metric_count,
            regional_metric_count=regional_count,
            evidence_count_count=evidence_count,
            historical_snapshot_id=snapshot_id,
        )

    def _eligible_entries(self, time_window: str, window_end_date: str) -> tuple[list[TournamentEntry], int]:
        seen: set[tuple[Any, ...]] = set()
        entries: list[TournamentEntry] = []
        skipped = 0

        for row in self.analytics.list_tournament_entry_inputs(window_end_date):
            key = _dedupe_key(row)
            if key in seen:
                skipped += 1
                continue
            seen.add(key)

            if not _within_window(row["event_date"], window_end_date, time_window):
                skipped += 1
                continue

            weight = final_entry_weight(
                player_count=row["player_count"],
                placement=row["placement"],
                placement_label=row["placement_label"],
                event_date=row["event_date"],
                window_end_date=window_end_date,
                time_window=time_window,
                source_confidence=row["source_confidence"],
                card_count=row["card_count"],
                minimum_player_count=self.minimum_player_count,
            )
            self.analytics.update_event_deck_entry_weight(int(row["event_deck_entry_id"]), weight)
            if weight <= 0:
                skipped += 1
                continue

            cards_by_oracle = self._deck_cards_by_oracle(int(row["canonical_deck_id"]))
            if not cards_by_oracle:
                skipped += 1
                continue
            entries.append(TournamentEntry(row=row, entry_weight=weight, cards_by_oracle=cards_by_oracle))

        return entries, skipped

    def _deck_cards_by_oracle(self, canonical_deck_id: int) -> dict[str, str]:
        cards: dict[str, str] = {}
        for card in self.analytics.list_canonical_deck_cards(canonical_deck_id):
            oracle_id = card["oracle_id"]
            if not oracle_id:
                continue
            cards.setdefault(str(oracle_id), str(card["scryfall_id"]))
        return cards

    def _card_metrics(
        self,
        entries: list[TournamentEntry],
        time_window: str,
        window_end_date: str,
        generated_at: str,
    ) -> list[dict[str, Any]]:
        total_entries = len(entries)
        total_weight = sum(entry.entry_weight for entry in entries)
        winner_entries = [entry for entry in entries if entry.row["winner"]]
        topcut_entries = [entry for entry in entries if _is_topcut(entry)]
        all_oracles = sorted({oracle for entry in entries for oracle in entry.cards_by_oracle})
        metrics: list[dict[str, Any]] = []

        for oracle_id in all_oracles:
            with_card = [entry for entry in entries if oracle_id in entry.cards_by_oracle]
            without_card = [entry for entry in entries if oracle_id not in entry.cards_by_oracle]
            weighted_with = sum(entry.entry_weight for entry in with_card)
            topcut_with = [entry for entry in topcut_entries if oracle_id in entry.cards_by_oracle]
            winner_with = [entry for entry in winner_entries if oracle_id in entry.cards_by_oracle]
            with_rate = _win_rate(with_card)
            without_rate = _win_rate(without_card)
            raw_inclusion = len(with_card) / total_entries
            topcut_inclusion = _rate(len(topcut_with), len(topcut_entries))
            metrics.append(
                {
                    "oracle_id": oracle_id,
                    "scryfall_id": sorted({entry.cards_by_oracle[oracle_id] for entry in with_card})[0],
                    "time_window": time_window,
                    "window_end_date": window_end_date,
                    "raw_inclusion_rate": raw_inclusion,
                    "weighted_inclusion_rate": _rate(weighted_with, total_weight),
                    "winner_inclusion_rate": _rate(len(winner_with), len(winner_entries)),
                    "topcut_inclusion_rate": topcut_inclusion,
                    "winrate_with_card": with_rate,
                    "winrate_without_card": without_rate,
                    "winrate_delta": None if with_rate is None or without_rate is None else with_rate - without_rate,
                    "topcut_delta": None if topcut_inclusion is None else topcut_inclusion - raw_inclusion,
                    "confidence_score": min(1.0, len(with_card) / 30),
                    "sample_size": len(with_card),
                    "updated_at": generated_at,
                }
            )
        return metrics

    def _regional_card_metrics(
        self,
        entries: list[TournamentEntry],
        time_window: str,
        window_end_date: str,
        generated_at: str,
    ) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, str], list[TournamentEntry]] = defaultdict(list)
        for entry in entries:
            region = (entry.row["region"] or "UNKNOWN").strip() or "UNKNOWN"
            country = (entry.row["country"] or "ALL").strip() or "ALL"
            grouped[(region, country)].append(entry)

        metrics: list[dict[str, Any]] = []
        for (region, country), group_entries in sorted(grouped.items()):
            total_weight = sum(entry.entry_weight for entry in group_entries)
            all_oracles = sorted({oracle for entry in group_entries for oracle in entry.cards_by_oracle})
            for oracle_id in all_oracles:
                with_card = [entry for entry in group_entries if oracle_id in entry.cards_by_oracle]
                weighted_with = sum(entry.entry_weight for entry in with_card)
                metrics.append(
                    {
                        "region_code": region,
                        "country_code": country,
                        "time_window": time_window,
                        "window_end_date": window_end_date,
                        "oracle_id": oracle_id,
                        "inclusion_rate": len(with_card) / len(group_entries),
                        "weighted_inclusion_rate": _rate(weighted_with, total_weight),
                        "sample_size": len(with_card),
                        "updated_at": generated_at,
                    }
                )
        return metrics
