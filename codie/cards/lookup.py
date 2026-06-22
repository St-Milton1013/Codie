"""Local card lookup against the Scryfall-backed `cards` table."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from codie.db.repositories.core import CoreRepository
from codie.db.repositories.curated import CuratedRepository

from .normalization import normalize_card_name


@dataclass(frozen=True)
class LookupResult:
    status: str
    query: str
    normalized_query: str
    card: Any | None = None
    score: float = 0.0
    note: str | None = None


class CardLookup:
    """Resolve exact, alias, and local fuzzy card names from cached Scryfall rows."""

    def __init__(
        self,
        core_repository: CoreRepository,
        aliases: dict[str, str] | None = None,
        curated_repository: CuratedRepository | None = None,
    ) -> None:
        self.core_repository = core_repository
        self.curated_repository = curated_repository
        self.aliases = {
            normalize_card_name(alias): normalize_card_name(target)
            for alias, target in (aliases or {}).items()
        }

    def resolve(self, query: str, *, fuzzy_threshold: float = 0.74) -> LookupResult:
        normalized = normalize_card_name(query)
        if not normalized:
            return LookupResult("unresolved", query, normalized, note="empty query")

        exact = self.core_repository.get_card_by_normalized_name(normalized)
        if exact is not None:
            return LookupResult("exact", query, normalized, exact, 1.0)

        alias_target = self.aliases.get(normalized)
        if alias_target is not None:
            alias_card = self.core_repository.get_card_by_normalized_name(alias_target)
            if alias_card is not None:
                return LookupResult("alias", query, normalized, alias_card, 1.0)

        if self.curated_repository is not None:
            alias = self.curated_repository.get_alias(normalized)
            if alias is not None:
                if alias["target_scryfall_id"]:
                    alias_card = self.core_repository.get_card(alias["target_scryfall_id"])
                else:
                    alias_card = self.core_repository.get_card_by_normalized_name(alias["normalized_target_name"])
                if alias_card is not None:
                    return LookupResult("alias", query, normalized, alias_card, 1.0)

        best_card = None
        best_score = 0.0
        for card in self.core_repository.list_cards():
            score = SequenceMatcher(None, normalized, card["normalized_name"]).ratio()
            if score > best_score:
                best_score = score
                best_card = card
        if best_card is not None and best_score >= fuzzy_threshold:
            return LookupResult("fuzzy", query, normalized, best_card, best_score)
        return LookupResult("unresolved", query, normalized, score=best_score, note="no local match")
