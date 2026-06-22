"""Export helpers for user deck evidence comparisons."""

from __future__ import annotations

from codie.user_decks import UserDeckEvidenceComparison


def user_deck_comparison_export(comparison: UserDeckEvidenceComparison) -> dict:
    """Return a deterministic JSON-compatible comparison payload."""

    return {
        "user_deck_id": comparison.user_deck_id,
        "deck_hash": comparison.deck_hash,
        "commander_hash": comparison.commander_hash,
        "present_count": comparison.present_count,
        "absent_count": comparison.absent_count,
        "generated_at": comparison.generated_at,
        "rows": [
            {
                "oracle_id": row.oracle_id,
                "card_name": row.card_name,
                "evidence_type": row.evidence_type,
                "presence_status": row.presence_status,
                "quantity_in_deck": row.quantity_in_deck,
                "zones": list(row.zones),
                "score": row.score,
                "sample_size": row.sample_size,
                "source_record_id": row.source_record_id,
                "source_url": row.source_url,
                "evidence_line": row.evidence_line,
            }
            for row in comparison.rows
        ],
    }


def user_deck_comparison_markdown(comparison: UserDeckEvidenceComparison) -> str:
    """Return an evidence-only Markdown report for a user deck comparison."""

    lines = [
        "# User Deck Evidence Comparison",
        "",
        f"- User deck ID: {comparison.user_deck_id}",
        f"- Deck hash: `{comparison.deck_hash}`",
        f"- Commander hash: `{comparison.commander_hash or 'unknown'}`",
        f"- Generated at: {comparison.generated_at}",
        f"- Present evidence cards: {comparison.present_count}",
        f"- Absent evidence cards: {comparison.absent_count}",
        "",
        "| Card | Evidence Type | Status | Quantity | Zones | Sample Size | Source |",
        "| --- | --- | --- | ---: | --- | ---: | --- |",
    ]
    for row in comparison.rows:
        source = row.source_url or row.source_record_id or ""
        zones = ", ".join(row.zones)
        sample_size = "" if row.sample_size is None else str(row.sample_size)
        lines.append(
            "| "
            + " | ".join(
                (
                    _escape_table(row.card_name),
                    _escape_table(row.evidence_type),
                    row.presence_status,
                    str(row.quantity_in_deck),
                    _escape_table(zones),
                    sample_size,
                    _escape_table(source),
                )
            )
            + " |"
        )
    lines.extend(["", "## Evidence Lines", ""])
    for row in comparison.rows:
        lines.append(f"- {row.evidence_line}")
    return "\n".join(lines).rstrip() + "\n"


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|")
