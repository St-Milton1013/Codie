"""Local Scryfall Tagger functional ontology helpers.

This module builds deterministic ontology packets from local fixture payloads.
It does not call Scryfall Tagger, scrape pages, write files, access SQLite,
calculate analytics, build graphs, or generate recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence


SCRYFALL_TAGGER_ONTOLOGY_VERSION = "scryfall-tagger-ontology-v1"


class ScryfallTaggerOntologyError(ValueError):
    """Raised when a local Scryfall Tagger ontology payload is unsafe."""


@dataclass(frozen=True)
class ScryfallTaggerSourceRef:
    source: str
    source_url: str | None = None
    source_snapshot_id: str | None = None
    raw_source_ref: str | None = None


@dataclass(frozen=True)
class ScryfallFunctionalTag:
    oracle_id: str
    scryfall_id: str | None
    tag: str
    normalized_tag: str
    tag_namespace: str
    source: str
    confidence: float
    source_url: str | None
    source_snapshot_id: str | None
    raw_source_ref: str | None
    is_functional: bool
    is_excluded: bool
    exclusion_reason: str | None
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class ScryfallTaggerCorrection:
    correction_type: str
    tag: str
    tag_namespace: str
    correction_source: str
    correction_reason: str
    created_at: str | None
    review_status: str
    oracle_id: str | None = None
    replacement_tag: str | None = None


@dataclass(frozen=True)
class ScryfallTagAlias:
    alias_tag: str
    canonical_tag: str
    tag_namespace: str
    source: str
    reason: str | None = None


@dataclass(frozen=True)
class ScryfallDeprecatedTag:
    deprecated_tag: str
    replacement_tag: str | None
    tag_namespace: str
    source: str
    reason: str | None = None


@dataclass(frozen=True)
class ScryfallTagConflict:
    conflict_type: str
    tag: str
    namespaces: tuple[str, ...]
    sources: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class ScryfallTagReplacementChain:
    original_tag: str
    replacement_tags: tuple[str, ...]
    tag_namespace: str
    has_cycle: bool


@dataclass(frozen=True)
class ScryfallTaggerCoverageReport:
    coverage_report_id: str
    ontology_version: str
    source_snapshot_id: str | None
    generated_at: str | None
    total_cards_seen: int
    cards_with_functional_tags: int
    cards_without_functional_tags: int
    functional_tag_count: int
    excluded_tag_count: int
    unknown_namespace_count: int
    duplicate_tag_count: int
    alias_count: int
    deprecated_tag_count: int
    conflict_count: int
    manual_correction_count: int
    coverage_ratio: float
    warnings: tuple[str, ...]
    manual_review_items: tuple[str, ...]


@dataclass(frozen=True)
class ScryfallTaggerOntologyOptions:
    ontology_id: str | None = None
    source_snapshot_id: str | None = None
    source_uri: str | None = None
    generated_at: str | None = None
    imported_at: str | None = None
    low_coverage_threshold: float = 0.5


@dataclass(frozen=True)
class ScryfallTaggerOntology:
    ontology_id: str
    ontology_version: str
    source_snapshot_id: str | None
    source_uri: str | None
    generated_at: str | None
    imported_at: str | None
    tags: tuple[ScryfallFunctionalTag, ...]
    aliases: tuple[ScryfallTagAlias, ...]
    deprecated_tags: tuple[ScryfallDeprecatedTag, ...]
    replacement_chains: tuple[ScryfallTagReplacementChain, ...]
    conflicts: tuple[ScryfallTagConflict, ...]
    corrections: tuple[ScryfallTaggerCorrection, ...]
    validation_errors: tuple[str, ...]
    validation_warnings: tuple[str, ...]
    manual_review_items: tuple[str, ...]


_FUNCTIONAL_NAMESPACES = frozenset(
    {
        "functional_role",
        "game_action",
        "resource",
        "interaction",
        "combo_role",
        "mana_role",
        "card_advantage",
        "protection",
        "stax",
        "win_condition",
    }
)
_EXCLUDED_NAMESPACES = frozenset(
    {
        "artwork_subject",
        "aesthetic",
        "flavor",
        "print_treatment",
        "image_description",
        "illustration_style",
        "artist_theme",
        "cosmetic_print",
    }
)


def build_scryfall_tagger_ontology(
    payload: Mapping[str, Any],
    *,
    options: ScryfallTaggerOntologyOptions | None = None,
) -> ScryfallTaggerOntology:
    """Build a deterministic local Scryfall Tagger ontology packet."""

    if not isinstance(payload, Mapping):
        raise ScryfallTaggerOntologyError("payload must be an object")
    options = options or ScryfallTaggerOntologyOptions()
    if not isinstance(options, ScryfallTaggerOntologyOptions):
        raise ScryfallTaggerOntologyError("options must be ScryfallTaggerOntologyOptions")

    raw_records = payload.get("tags", ())
    if not isinstance(raw_records, Sequence) or isinstance(raw_records, (str, bytes)):
        raise ScryfallTaggerOntologyError("payload.tags must be a list")
    source_snapshot_id = options.source_snapshot_id or _optional_text(payload.get("source_snapshot_id"))
    source_uri = options.source_uri or _optional_text(payload.get("source_uri"))

    tags: list[ScryfallFunctionalTag] = []
    warnings: list[str] = []
    manual_review_items: list[str] = []
    seen_keys: set[tuple[str, str, str, str]] = set()
    duplicate_count = 0
    cards_seen: set[str] = set()
    cards_with_functional_tags: set[str] = set()

    for index, record in enumerate(raw_records):
        if not isinstance(record, Mapping):
            raise ScryfallTaggerOntologyError(f"tags[{index}] must be an object")
        oracle_id = _required_text(record.get("oracle_id"), f"tags[{index}].oracle_id")
        tag = _required_text(record.get("tag"), f"tags[{index}].tag")
        tag_namespace = _required_text(record.get("tag_namespace"), f"tags[{index}].tag_namespace")
        source = _required_text(record.get("source"), f"tags[{index}].source")
        normalized_tag = _normalize_tag(tag)
        confidence = _confidence(record.get("confidence", 1.0), f"tags[{index}].confidence")
        key = (oracle_id, normalized_tag, tag_namespace, source)
        if key in seen_keys:
            duplicate_count += 1
            warnings.append(f"duplicate tag ignored: {oracle_id}/{tag_namespace}/{normalized_tag}/{source}")
            continue
        seen_keys.add(key)
        cards_seen.add(oracle_id)
        is_excluded = tag_namespace in _EXCLUDED_NAMESPACES or bool(record.get("is_excluded", False))
        is_functional = tag_namespace in _FUNCTIONAL_NAMESPACES and not is_excluded
        exclusion_reason = _optional_text(record.get("exclusion_reason"))
        if is_excluded and not exclusion_reason:
            exclusion_reason = "non-functional tag namespace"
        if tag_namespace not in _FUNCTIONAL_NAMESPACES and tag_namespace not in _EXCLUDED_NAMESPACES:
            warning = f"unknown tag namespace: {tag_namespace}"
            warnings.append(warning)
            manual_review_items.append(warning)
        if is_functional:
            cards_with_functional_tags.add(oracle_id)
        tags.append(
            ScryfallFunctionalTag(
                oracle_id=oracle_id,
                scryfall_id=_optional_text(record.get("scryfall_id")),
                tag=tag,
                normalized_tag=normalized_tag,
                tag_namespace=tag_namespace,
                source=source,
                confidence=confidence,
                source_url=_optional_text(record.get("source_url")),
                source_snapshot_id=_optional_text(record.get("source_snapshot_id")) or source_snapshot_id,
                raw_source_ref=_optional_text(record.get("raw_source_ref")),
                is_functional=is_functional,
                is_excluded=is_excluded,
                exclusion_reason=exclusion_reason,
                provenance=_freeze_json(
                    {
                        "source": source,
                        "source_snapshot_id": _optional_text(record.get("source_snapshot_id")) or source_snapshot_id,
                        "raw_source_ref": _optional_text(record.get("raw_source_ref")),
                    }
                ),
            )
        )

    aliases = _build_aliases(payload.get("aliases", ()))
    deprecated_tags = _build_deprecated_tags(payload.get("deprecated_tags", ()))
    corrections = _build_corrections(payload.get("corrections", ()))
    conflicts = _detect_conflicts(tags, corrections)
    replacement_chains = _build_replacement_chains(deprecated_tags, warnings, manual_review_items)
    for deprecated in deprecated_tags:
        message = f"deprecated tag remains visible: {deprecated.deprecated_tag}"
        warnings.append(message)
        manual_review_items.append(message)
    manual_review_items.extend(conflict.reason for conflict in conflicts)

    ontology = ScryfallTaggerOntology(
        ontology_id=options.ontology_id or _optional_text(payload.get("ontology_id")) or "scryfall-tagger-ontology",
        ontology_version=SCRYFALL_TAGGER_ONTOLOGY_VERSION,
        source_snapshot_id=source_snapshot_id,
        source_uri=source_uri,
        generated_at=options.generated_at or _optional_text(payload.get("generated_at")),
        imported_at=options.imported_at or _optional_text(payload.get("imported_at")),
        tags=tuple(sorted(tags, key=_tag_sort_key)),
        aliases=tuple(sorted(aliases, key=lambda item: (item.tag_namespace, item.alias_tag, item.canonical_tag))),
        deprecated_tags=tuple(sorted(deprecated_tags, key=lambda item: (item.tag_namespace, item.deprecated_tag))),
        replacement_chains=tuple(sorted(replacement_chains, key=lambda item: (item.tag_namespace, item.original_tag))),
        conflicts=tuple(sorted(conflicts, key=lambda item: (item.conflict_type, item.tag))),
        corrections=tuple(sorted(corrections, key=lambda item: (item.correction_type, item.tag, item.tag_namespace))),
        validation_errors=(),
        validation_warnings=tuple(sorted(set(warnings))),
        manual_review_items=tuple(sorted(set(manual_review_items))),
    )
    coverage = build_scryfall_tagger_coverage_report(
        ontology,
        total_cards_seen=len(cards_seen),
        cards_with_functional_tags=len(cards_with_functional_tags),
        duplicate_tag_count=duplicate_count,
        low_coverage_threshold=options.low_coverage_threshold,
    )
    if coverage.warnings:
        ontology = ScryfallTaggerOntology(
            **{
                **ontology.__dict__,
                "validation_warnings": tuple(sorted(set(ontology.validation_warnings + coverage.warnings))),
                "manual_review_items": tuple(sorted(set(ontology.manual_review_items + coverage.manual_review_items))),
            }
        )
    return validate_scryfall_tagger_ontology(ontology)


def validate_scryfall_tagger_ontology(ontology: ScryfallTaggerOntology) -> ScryfallTaggerOntology:
    """Validate that an ontology packet is deterministic and JSON-compatible."""

    if not isinstance(ontology, ScryfallTaggerOntology):
        raise ScryfallTaggerOntologyError("ontology must be a ScryfallTaggerOntology")
    _required_text(ontology.ontology_id, "ontology_id")
    if ontology.ontology_version != SCRYFALL_TAGGER_ONTOLOGY_VERSION:
        raise ScryfallTaggerOntologyError("unsupported ontology_version")
    for tag in ontology.tags:
        if not isinstance(tag, ScryfallFunctionalTag):
            raise ScryfallTaggerOntologyError("ontology tags must contain ScryfallFunctionalTag values")
        _required_text(tag.oracle_id, "tag.oracle_id")
        _required_text(tag.tag, "tag.tag")
        _required_text(tag.normalized_tag, "tag.normalized_tag")
        _required_text(tag.tag_namespace, "tag.tag_namespace")
        if tag.is_excluded and not tag.exclusion_reason:
            raise ScryfallTaggerOntologyError("excluded tags require exclusion_reason")
    _ensure_json_compatible(scryfall_tagger_ontology_to_dict(ontology))
    return ontology


def scryfall_tagger_ontology_to_dict(ontology: ScryfallTaggerOntology) -> dict[str, Any]:
    """Serialize a Scryfall Tagger ontology packet deterministically."""

    if not isinstance(ontology, ScryfallTaggerOntology):
        raise ScryfallTaggerOntologyError("ontology must be a ScryfallTaggerOntology")
    return {
        "aliases": [
            {
                "alias_tag": alias.alias_tag,
                "canonical_tag": alias.canonical_tag,
                "reason": alias.reason,
                "source": alias.source,
                "tag_namespace": alias.tag_namespace,
            }
            for alias in ontology.aliases
        ],
        "conflicts": [
            {
                "conflict_type": conflict.conflict_type,
                "namespaces": list(conflict.namespaces),
                "reason": conflict.reason,
                "sources": list(conflict.sources),
                "tag": conflict.tag,
            }
            for conflict in ontology.conflicts
        ],
        "corrections": [
            {
                "correction_reason": correction.correction_reason,
                "correction_source": correction.correction_source,
                "correction_type": correction.correction_type,
                "created_at": correction.created_at,
                "oracle_id": correction.oracle_id,
                "replacement_tag": correction.replacement_tag,
                "review_status": correction.review_status,
                "tag": correction.tag,
                "tag_namespace": correction.tag_namespace,
            }
            for correction in ontology.corrections
        ],
        "deprecated_tags": [
            {
                "deprecated_tag": deprecated.deprecated_tag,
                "reason": deprecated.reason,
                "replacement_tag": deprecated.replacement_tag,
                "source": deprecated.source,
                "tag_namespace": deprecated.tag_namespace,
            }
            for deprecated in ontology.deprecated_tags
        ],
        "generated_at": ontology.generated_at,
        "imported_at": ontology.imported_at,
        "manual_review_items": list(ontology.manual_review_items),
        "ontology_id": ontology.ontology_id,
        "ontology_version": ontology.ontology_version,
        "replacement_chains": [
            {
                "has_cycle": chain.has_cycle,
                "original_tag": chain.original_tag,
                "replacement_tags": list(chain.replacement_tags),
                "tag_namespace": chain.tag_namespace,
            }
            for chain in ontology.replacement_chains
        ],
        "source_snapshot_id": ontology.source_snapshot_id,
        "source_uri": ontology.source_uri,
        "tags": [_tag_to_dict(tag) for tag in ontology.tags],
        "validation_errors": list(ontology.validation_errors),
        "validation_warnings": list(ontology.validation_warnings),
    }


def build_scryfall_tagger_coverage_report(
    ontology: ScryfallTaggerOntology,
    *,
    total_cards_seen: int | None = None,
    cards_with_functional_tags: int | None = None,
    duplicate_tag_count: int = 0,
    low_coverage_threshold: float = 0.5,
) -> ScryfallTaggerCoverageReport:
    """Build an in-memory coverage report for an ontology packet."""

    if not isinstance(ontology, ScryfallTaggerOntology):
        raise ScryfallTaggerOntologyError("ontology must be a ScryfallTaggerOntology")
    if duplicate_tag_count < 0:
        raise ScryfallTaggerOntologyError("duplicate_tag_count must not be negative")
    seen_cards = {tag.oracle_id for tag in ontology.tags}
    functional_cards = {tag.oracle_id for tag in ontology.tags if tag.is_functional}
    resolved_total = total_cards_seen if total_cards_seen is not None else len(seen_cards)
    resolved_functional_cards = cards_with_functional_tags if cards_with_functional_tags is not None else len(functional_cards)
    if resolved_total < 0 or resolved_functional_cards < 0:
        raise ScryfallTaggerOntologyError("coverage counts must not be negative")
    cards_without = max(resolved_total - resolved_functional_cards, 0)
    coverage_ratio = 0.0 if resolved_total == 0 else resolved_functional_cards / resolved_total
    warnings = list(ontology.validation_warnings)
    manual_review_items = list(ontology.manual_review_items)
    if coverage_ratio < low_coverage_threshold:
        message = "low functional tag coverage"
        warnings.append(message)
        manual_review_items.append(message)
    report = ScryfallTaggerCoverageReport(
        coverage_report_id=f"{ontology.ontology_id}-coverage",
        ontology_version=ontology.ontology_version,
        source_snapshot_id=ontology.source_snapshot_id,
        generated_at=ontology.generated_at,
        total_cards_seen=resolved_total,
        cards_with_functional_tags=resolved_functional_cards,
        cards_without_functional_tags=cards_without,
        functional_tag_count=sum(1 for tag in ontology.tags if tag.is_functional),
        excluded_tag_count=sum(1 for tag in ontology.tags if tag.is_excluded),
        unknown_namespace_count=sum(1 for item in ontology.manual_review_items if item.startswith("unknown tag namespace")),
        duplicate_tag_count=duplicate_tag_count,
        alias_count=len(ontology.aliases),
        deprecated_tag_count=len(ontology.deprecated_tags),
        conflict_count=len(ontology.conflicts),
        manual_correction_count=len(ontology.corrections),
        coverage_ratio=coverage_ratio,
        warnings=tuple(sorted(set(warnings))),
        manual_review_items=tuple(sorted(set(manual_review_items))),
    )
    _ensure_json_compatible(scryfall_tagger_coverage_report_to_dict(report))
    return report


def scryfall_tagger_coverage_report_to_dict(report: ScryfallTaggerCoverageReport) -> dict[str, Any]:
    """Serialize a Scryfall Tagger coverage report deterministically."""

    if not isinstance(report, ScryfallTaggerCoverageReport):
        raise ScryfallTaggerOntologyError("report must be a ScryfallTaggerCoverageReport")
    return {
        "alias_count": report.alias_count,
        "cards_with_functional_tags": report.cards_with_functional_tags,
        "cards_without_functional_tags": report.cards_without_functional_tags,
        "conflict_count": report.conflict_count,
        "coverage_ratio": report.coverage_ratio,
        "coverage_report_id": report.coverage_report_id,
        "deprecated_tag_count": report.deprecated_tag_count,
        "duplicate_tag_count": report.duplicate_tag_count,
        "excluded_tag_count": report.excluded_tag_count,
        "functional_tag_count": report.functional_tag_count,
        "generated_at": report.generated_at,
        "manual_correction_count": report.manual_correction_count,
        "manual_review_items": list(report.manual_review_items),
        "ontology_version": report.ontology_version,
        "source_snapshot_id": report.source_snapshot_id,
        "total_cards_seen": report.total_cards_seen,
        "unknown_namespace_count": report.unknown_namespace_count,
        "warnings": list(report.warnings),
    }


def _build_aliases(values: Any) -> tuple[ScryfallTagAlias, ...]:
    aliases = []
    for index, value in enumerate(_sequence(values, "aliases")):
        aliases.append(
            ScryfallTagAlias(
                alias_tag=_required_text(value.get("alias_tag"), f"aliases[{index}].alias_tag"),
                canonical_tag=_normalize_tag(_required_text(value.get("canonical_tag"), f"aliases[{index}].canonical_tag")),
                tag_namespace=_required_text(value.get("tag_namespace"), f"aliases[{index}].tag_namespace"),
                source=_required_text(value.get("source"), f"aliases[{index}].source"),
                reason=_optional_text(value.get("reason")),
            )
        )
    return tuple(aliases)


def _build_deprecated_tags(values: Any) -> tuple[ScryfallDeprecatedTag, ...]:
    deprecated = []
    for index, value in enumerate(_sequence(values, "deprecated_tags")):
        deprecated.append(
            ScryfallDeprecatedTag(
                deprecated_tag=_normalize_tag(_required_text(value.get("deprecated_tag"), f"deprecated_tags[{index}].deprecated_tag")),
                replacement_tag=_normalize_tag(value["replacement_tag"]) if _optional_text(value.get("replacement_tag")) else None,
                tag_namespace=_required_text(value.get("tag_namespace"), f"deprecated_tags[{index}].tag_namespace"),
                source=_required_text(value.get("source"), f"deprecated_tags[{index}].source"),
                reason=_optional_text(value.get("reason")),
            )
        )
    return tuple(deprecated)


def _build_corrections(values: Any) -> tuple[ScryfallTaggerCorrection, ...]:
    corrections = []
    for index, value in enumerate(_sequence(values, "corrections")):
        corrections.append(
            ScryfallTaggerCorrection(
                correction_type=_required_text(value.get("correction_type"), f"corrections[{index}].correction_type"),
                tag=_required_text(value.get("tag"), f"corrections[{index}].tag"),
                tag_namespace=_required_text(value.get("tag_namespace"), f"corrections[{index}].tag_namespace"),
                correction_source=_required_text(value.get("correction_source"), f"corrections[{index}].correction_source"),
                correction_reason=_required_text(value.get("correction_reason"), f"corrections[{index}].correction_reason"),
                created_at=_optional_text(value.get("created_at")),
                review_status=_required_text(value.get("review_status"), f"corrections[{index}].review_status"),
                oracle_id=_optional_text(value.get("oracle_id")),
                replacement_tag=_optional_text(value.get("replacement_tag")),
            )
        )
    return tuple(corrections)


def _detect_conflicts(
    tags: Sequence[ScryfallFunctionalTag],
    corrections: Sequence[ScryfallTaggerCorrection],
) -> tuple[ScryfallTagConflict, ...]:
    conflicts: list[ScryfallTagConflict] = []
    by_tag: dict[str, list[ScryfallFunctionalTag]] = {}
    for tag in tags:
        by_tag.setdefault(tag.normalized_tag, []).append(tag)
    for normalized_tag, grouped in sorted(by_tag.items()):
        namespaces = tuple(sorted({tag.tag_namespace for tag in grouped}))
        sources = tuple(sorted({tag.source for tag in grouped}))
        functional_flags = {tag.is_functional for tag in grouped}
        excluded_flags = {tag.is_excluded for tag in grouped}
        if len(namespaces) > 1:
            conflicts.append(
                ScryfallTagConflict(
                    conflict_type="namespace_conflict",
                    tag=normalized_tag,
                    namespaces=namespaces,
                    sources=sources,
                    reason=f"tag {normalized_tag} appears in multiple namespaces",
                )
            )
        if len(functional_flags) > 1 or len(excluded_flags) > 1:
            conflicts.append(
                ScryfallTagConflict(
                    conflict_type="functional_exclusion_conflict",
                    tag=normalized_tag,
                    namespaces=namespaces,
                    sources=sources,
                    reason=f"tag {normalized_tag} has conflicting functional/excluded classification",
                )
            )
    correction_index: dict[tuple[str, str], set[str]] = {}
    for correction in corrections:
        key = (_normalize_tag(correction.tag), correction.tag_namespace)
        correction_index.setdefault(key, set()).add(correction.correction_type)
    for (tag, namespace), correction_types in sorted(correction_index.items()):
        if "add" in correction_types and "remove" in correction_types:
            conflicts.append(
                ScryfallTagConflict(
                    conflict_type="manual_correction_conflict",
                    tag=tag,
                    namespaces=(namespace,),
                    sources=("manual_correction",),
                    reason=f"manual corrections both add and remove tag {tag}",
                )
            )
    return tuple(conflicts)


def _build_replacement_chains(
    deprecated_tags: Sequence[ScryfallDeprecatedTag],
    warnings: list[str],
    manual_review_items: list[str],
) -> tuple[ScryfallTagReplacementChain, ...]:
    replacements = {
        (item.tag_namespace, item.deprecated_tag): item.replacement_tag
        for item in deprecated_tags
        if item.replacement_tag
    }
    chains: list[ScryfallTagReplacementChain] = []
    for namespace, original in sorted(replacements):
        chain: list[str] = []
        seen = {original}
        current = replacements[(namespace, original)]
        has_cycle = False
        while current:
            if current in seen:
                has_cycle = True
                message = f"cyclic replacement chain detected for tag {original}"
                warnings.append(message)
                manual_review_items.append(message)
                break
            chain.append(current)
            seen.add(current)
            current = replacements.get((namespace, current))
        chains.append(
            ScryfallTagReplacementChain(
                original_tag=original,
                replacement_tags=tuple(chain),
                tag_namespace=namespace,
                has_cycle=has_cycle,
            )
        )
    return tuple(chains)


def _tag_to_dict(tag: ScryfallFunctionalTag) -> dict[str, Any]:
    return {
        "confidence": tag.confidence,
        "exclusion_reason": tag.exclusion_reason,
        "is_excluded": tag.is_excluded,
        "is_functional": tag.is_functional,
        "normalized_tag": tag.normalized_tag,
        "oracle_id": tag.oracle_id,
        "provenance": _thaw_json(tag.provenance),
        "raw_source_ref": tag.raw_source_ref,
        "scryfall_id": tag.scryfall_id,
        "source": tag.source,
        "source_snapshot_id": tag.source_snapshot_id,
        "source_url": tag.source_url,
        "tag": tag.tag,
        "tag_namespace": tag.tag_namespace,
    }


def _sequence(values: Any, field_name: str) -> tuple[Mapping[str, Any], ...]:
    if values is None:
        return ()
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ScryfallTaggerOntologyError(f"{field_name} must be a list")
    result = []
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise ScryfallTaggerOntologyError(f"{field_name}[{index}] must be an object")
        result.append(value)
    return tuple(result)


def _tag_sort_key(tag: ScryfallFunctionalTag) -> tuple[str, str, str, str]:
    return (tag.oracle_id, tag.tag_namespace, tag.normalized_tag, tag.source)


def _normalize_tag(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", " ").replace("-", " ").split())


def _confidence(value: Any, field_name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ScryfallTaggerOntologyError(f"{field_name} must be numeric")
    resolved = float(value)
    if resolved < 0 or resolved > 1:
        raise ScryfallTaggerOntologyError(f"{field_name} must be between 0 and 1")
    return resolved


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ScryfallTaggerOntologyError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(value[key]) for key in sorted(value)})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_json(item) for item in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _ensure_json_compatible(value: Any) -> None:
    try:
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except TypeError as exc:
        raise ScryfallTaggerOntologyError("ontology payload must be JSON-compatible") from exc
