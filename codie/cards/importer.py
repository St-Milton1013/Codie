"""Import Scryfall card truth records into the core repository."""

from __future__ import annotations

from collections.abc import Iterable

from codie.db.repositories.core import CoreRepository
from codie.providers.scryfall.models import ScryfallCard


class ScryfallImporter:
    """Persist parsed Scryfall cards through the repository layer."""

    def __init__(self, core_repository: CoreRepository) -> None:
        self.core_repository = core_repository

    def import_cards(self, cards: Iterable[ScryfallCard]) -> int:
        imported = 0
        for card in cards:
            self.core_repository.upsert_card(card.to_card_row())
            imported += 1
        return imported
