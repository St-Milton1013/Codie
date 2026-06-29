"""Pure deck and target parsing for simulator inputs."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from .models import SimulationDeck, SimulationDeckCard, SimulationTargetCondition


ALLOWED_ZONES = {"main", "command", "sideboard", "considering", "unknown"}
IGNORED_ZONES = {"sideboard", "considering", "unknown"}
TARGET_ZONES = {"hand", "stack", "battlefield", "graveyard", "exile", "library", "top_of_library", "accessible"}
CONDITION_TYPES = {"cast", "cast_or_access", "access", "draw", "find_to_hand", "find_to_top", "put_onto_battlefield"}

_SECTION_ALIASES = {
    "commander": "command",
    "commanders": "command",
    "command zone": "command",
    "main": "main",
    "main deck": "main",
    "maindeck": "main",
    "deck": "main",
    "sideboard": "sideboard",
    "side board": "sideboard",
    "maybeboard": "considering",
    "maybe board": "considering",
    "considering": "considering",
    "consider": "considering",
}

_ROW_RE = re.compile(r"^\s*(?:(?P<quantity>[+-]?\d+)(?:x)?\s+)?(?P<name>.+?)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class DeckParseIssue:
    line_number: int | None
    raw_line: str | None
    issue_type: str
    message: str
    severity: str

    def __post_init__(self) -> None:
        if self.severity not in {"info", "warning", "error"}:
            raise ValueError("severity must be info, warning, or error")
        if not self.issue_type:
            raise ValueError("issue_type is required")
        if not self.message:
            raise ValueError("message is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "line_number": self.line_number,
            "raw_line": self.raw_line,
            "issue_type": self.issue_type,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass(frozen=True)
class ParsedDeckInput:
    deck: SimulationDeck | None
    issues: tuple[DeckParseIssue, ...]
    raw_input_hash: str
    source_format: str
    cards_total: int
    commanders_total: int
    unresolved_cards: tuple[str, ...] = ()
    ignored_rows: tuple[dict[str, Any], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "issues", tuple(self.issues))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))
        object.__setattr__(self, "ignored_rows", tuple(dict(row) for row in self.ignored_rows))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck": self.deck.to_dict() if self.deck is not None else None,
            "issues": [issue.to_dict() for issue in self.issues],
            "raw_input_hash": self.raw_input_hash,
            "source_format": self.source_format,
            "cards_total": self.cards_total,
            "commanders_total": self.commanders_total,
            "unresolved_cards": list(self.unresolved_cards),
            "ignored_rows": [dict(row) for row in self.ignored_rows],
        }


@dataclass(frozen=True)
class ParsedTargetInput:
    target_condition: SimulationTargetCondition | None
    issues: tuple[DeckParseIssue, ...]
    raw_target: dict[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "issues", tuple(self.issues))
        object.__setattr__(self, "raw_target", dict(self.raw_target))

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_condition": self.target_condition.to_dict() if self.target_condition is not None else None,
            "issues": [issue.to_dict() for issue in self.issues],
            "raw_target": dict(self.raw_target),
        }


def parse_simulation_deck_text(
    text: str,
    *,
    source_format: str = "plain_text",
    source: str | None = None,
    commander_names: Iterable[str] = (),
    unresolved_names: Iterable[str] = (),
    require_model_ids: bool = False,
    allow_partial: bool = False,
) -> ParsedDeckInput:
    if not isinstance(text, str):
        raise ValueError("deck text must be a string")
    rows: list[dict[str, Any]] = []
    issues: list[DeckParseIssue] = []
    current_zone = "main"
    unresolved = {_normalize_name(name) for name in unresolved_names}
    commander_set = {_normalize_name(name) for name in commander_names}
    seen_commanders: set[str] = set()

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            issues.append(_issue(line_number, raw_line, "ignored_blank", "Blank line ignored.", "info"))
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            issues.append(_issue(line_number, raw_line, "ignored_comment", "Comment line ignored.", "info"))
            continue
        section = _section_from_line(stripped)
        if section is not None:
            current_zone = section
            if section in IGNORED_ZONES:
                issues.append(_issue(line_number, raw_line, "ignored_section", f"{section} section ignored.", "info"))
            continue

        row, row_issue = _parse_text_row(stripped, current_zone, line_number, raw_line)
        if row_issue is not None:
            issues.append(row_issue)
            continue
        assert row is not None
        normalized_row_name = _normalize_name(row["name"])
        if normalized_row_name in commander_set:
            row["zone"] = "command"
            seen_commanders.add(normalized_row_name)
        if current_zone in IGNORED_ZONES:
            issues.append(_issue(line_number, raw_line, "ignored_section", f"{current_zone} row ignored.", "info"))
        if _normalize_name(row["name"]) in unresolved:
            row["unresolved"] = True
        rows.append(row)

    for commander_name in commander_names:
        name = _clean_name(commander_name)
        if name and _normalize_name(name) not in seen_commanders:
            rows.append({"quantity": 1, "name": name, "zone": "command", "model_id": None, "raw_line": name})

    return parse_simulation_deck_rows(
        rows,
        source_format=source_format,
        source=source,
        raw_input=text,
        inherited_issues=issues,
        require_model_ids=require_model_ids,
        allow_partial=allow_partial,
    )


def parse_simulation_deck_rows(
    rows: Iterable[dict[str, Any]],
    *,
    source_format: str = "rows",
    source: str | None = None,
    raw_input: str | None = None,
    inherited_issues: Iterable[DeckParseIssue] = (),
    require_model_ids: bool = False,
    allow_partial: bool = False,
) -> ParsedDeckInput:
    row_list = list(rows)
    issues = list(inherited_issues)
    combined: dict[tuple[str, str, str | None], SimulationDeckCard] = {}
    ignored_rows: list[dict[str, Any]] = []
    unresolved_cards: list[str] = []

    for index, row in enumerate(row_list, start=1):
        raw_line = row.get("raw_line")
        zone = str(row.get("zone", "main")).strip().lower() or "main"
        if zone not in ALLOWED_ZONES:
            issues.append(_issue(index, raw_line, "unsupported_section", f"Unsupported zone: {zone}.", "warning"))
            zone = "unknown"
        if zone in IGNORED_ZONES:
            ignored_rows.append(dict(row))
            continue

        quantity = row.get("quantity", 1)
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            issues.append(_issue(index, raw_line, "invalid_quantity", "Quantity must be a positive integer.", "error"))
            unresolved_cards.append(str(row.get("name", raw_line or "unknown")))
            continue
        name = _clean_name(str(row.get("name", "")))
        if not name:
            issues.append(_issue(index, raw_line, "missing_card_name", "Card name is required.", "error"))
            unresolved_cards.append(str(raw_line or "missing card name"))
            continue
        model_id = row.get("model_id")
        if model_id is not None:
            model_id = _clean_name(str(model_id))
        if row.get("unresolved") or (require_model_ids and not model_id):
            issues.append(_issue(index, raw_line, "unresolved_card", f"Card remains unresolved: {name}.", "warning"))
            unresolved_cards.append(name)

        key = (zone, _normalize_name(name), model_id)
        existing = combined.get(key)
        if existing is None:
            combined[key] = SimulationDeckCard(quantity=quantity, name=name, model_id=model_id, zone=zone)
        else:
            combined[key] = SimulationDeckCard(
                quantity=existing.quantity + quantity,
                name=existing.name,
                model_id=existing.model_id,
                zone=existing.zone,
            )
            issues.append(_issue(index, raw_line, "duplicate_combined", f"Duplicate row combined: {name}.", "info"))

    deck_cards = tuple(_sort_cards(card for card in combined.values() if card.zone == "main"))
    commanders = tuple(_sort_cards(card for card in combined.values() if card.zone == "command"))
    errors = [issue for issue in issues if issue.severity == "error"]
    deck = None
    if (not errors or allow_partial) and (deck_cards or commanders):
        deck = build_simulation_deck(deck_cards, commanders=commanders, source=source, unresolved_cards=unresolved_cards)

    return ParsedDeckInput(
        deck=deck,
        issues=tuple(issues),
        raw_input_hash=_raw_hash(raw_input if raw_input is not None else json.dumps(row_list, sort_keys=True)),
        source_format=source_format,
        cards_total=sum(card.quantity for card in deck_cards),
        commanders_total=sum(card.quantity for card in commanders),
        unresolved_cards=tuple(dict.fromkeys(unresolved_cards)),
        ignored_rows=tuple(ignored_rows),
    )


def parse_target_condition(raw_target: dict[str, Any]) -> ParsedTargetInput:
    issues: list[DeckParseIssue] = []
    raw = dict(raw_target)
    target_card = _clean_name(str(raw.get("target_card", "")))
    target_zone = _clean_name(str(raw.get("target_zone", ""))).lower()
    condition_type = _clean_name(str(raw.get("condition_type", ""))).lower()
    turn = raw.get("turn")

    if not target_card:
        issues.append(_issue(None, None, "missing_card_name", "Target card is required.", "error"))
    if target_zone not in TARGET_ZONES:
        issues.append(_issue(None, None, "unsupported_section", f"Unsupported target zone: {target_zone}.", "error"))
    if condition_type not in CONDITION_TYPES:
        issues.append(_issue(None, None, "malformed_row", f"Unsupported condition type: {condition_type}.", "error"))
    if isinstance(turn, bool) or not isinstance(turn, int) or turn <= 0:
        issues.append(_issue(None, None, "invalid_quantity", "Target turn must be a positive integer.", "error"))

    target = None
    if not issues:
        target = SimulationTargetCondition(
            target_card=target_card,
            target_card_id=raw.get("target_card_id"),
            target_zone=target_zone,
            turn=turn,
            condition_type=condition_type,
            required_support_tags=tuple(raw.get("required_support_tags", ())),
            notes=raw.get("notes"),
        )
    return ParsedTargetInput(target_condition=target, issues=tuple(issues), raw_target=raw)


def build_simulation_deck(
    cards: Iterable[SimulationDeckCard],
    *,
    commanders: Iterable[SimulationDeckCard] = (),
    source: str | None = None,
    unresolved_cards: Iterable[str] = (),
) -> SimulationDeck:
    main_cards = tuple(_sort_cards(cards))
    commander_cards = tuple(_sort_cards(commanders))
    return SimulationDeck(
        deck_hash=stable_deck_hash(main_cards, commanders=commander_cards),
        cards=main_cards,
        commanders=commander_cards,
        source=source,
        unresolved_cards=tuple(dict.fromkeys(unresolved_cards)),
    )


def stable_deck_hash(
    cards: Iterable[SimulationDeckCard],
    *,
    commanders: Iterable[SimulationDeckCard] = (),
) -> str:
    rows = [
        {
            "zone": card.zone,
            "quantity": card.quantity,
            "name": _normalize_name(card.name),
            "model_id": card.model_id,
        }
        for card in (*tuple(cards), *tuple(commanders))
    ]
    rows.sort(key=lambda row: (row["zone"], row["name"], row["model_id"] or "", row["quantity"]))
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parse_text_row(
    stripped: str,
    zone: str,
    line_number: int,
    raw_line: str,
) -> tuple[dict[str, Any] | None, DeckParseIssue | None]:
    match = _ROW_RE.match(stripped)
    if match is None:
        return None, _issue(line_number, raw_line, "malformed_row", "Deck row could not be parsed.", "error")
    quantity_text = match.group("quantity")
    name = _clean_name(match.group("name"))
    if quantity_text is None and _looks_like_bad_quantity(stripped):
        return None, _issue(line_number, raw_line, "invalid_quantity", "Quantity must be a positive integer.", "error")
    quantity = 1
    if quantity_text is not None:
        quantity = int(quantity_text)
        if quantity <= 0:
            return None, _issue(line_number, raw_line, "invalid_quantity", "Quantity must be a positive integer.", "error")
    if not name or name in {"-", "--"}:
        return None, _issue(line_number, raw_line, "missing_card_name", "Card name is required.", "error")
    return {"quantity": quantity, "name": name, "zone": zone, "model_id": None, "raw_line": raw_line}, None


def _looks_like_bad_quantity(value: str) -> bool:
    return bool(re.match(r"^\s*(?:[+-]?\d+\.\d+|[+-]?\d+x?\s*$)", value, re.IGNORECASE))


def _section_from_line(value: str) -> str | None:
    normalized = _normalize_name(value.rstrip(":"))
    return _SECTION_ALIASES.get(normalized)


def _sort_cards(cards: Iterable[SimulationDeckCard]) -> list[SimulationDeckCard]:
    return sorted(cards, key=lambda card: (card.zone, _normalize_name(card.name), card.model_id or ""))


def _issue(
    line_number: int | None,
    raw_line: str | None,
    issue_type: str,
    message: str,
    severity: str,
) -> DeckParseIssue:
    return DeckParseIssue(
        line_number=line_number,
        raw_line=raw_line,
        issue_type=issue_type,
        message=message,
        severity=severity,
    )


def _raw_hash(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _clean_name(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_name(value: str) -> str:
    return _clean_name(value).lower()
