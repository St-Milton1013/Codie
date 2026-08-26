"""Application service for Codie's local evidence-only working iteration."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from codie.cards.importer import ScryfallImporter
from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.connection import connect
from codie.db.repositories import CoreRepository, UserRepository
from codie.db.repositories.base import BaseRepository
from codie.exports.user_deck_reports import (
    user_deck_comparison_export,
    user_deck_comparison_markdown,
)
from codie.local_app.sources import (
    LocalSourceError,
    MoxfieldDeckSource,
    ScryfallCatalogSource,
    is_moxfield_deck_reference,
    read_catalog_payloads,
)
from codie.providers.scryfall.models import ScryfallCard, ScryfallParseError
from codie.user_decks import (
    DeckMemoryFilters,
    DeckMemoryReadError,
    SavedAnalysisReadError,
    UserDeckAnalysisInputError,
    UserDeckEvidenceCandidate,
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
    UserDeckImporter,
    UserDeckImportError,
    build_user_deck_analysis_input,
    compare_user_deck_to_evidence,
    get_deck_memory_detail,
    get_saved_user_deck_analysis,
    list_deck_memory,
    list_saved_user_deck_analyses,
    save_user_deck_comparison_analysis,
)

REQUIRED_TABLES = frozenset({"cards", "user_decks", "user_deck_cards", "saved_analysis"})
FORBIDDEN_EVIDENCE_FRAGMENTS = (
    "recommend",
    "should_play",
    "should play",
    "must_include",
    "must include",
    "cut_candidate",
    "cut candidate",
    "optimal",
)


class LocalAppError(ValueError):
    """Safe, structured failure that can cross the loopback HTTP boundary."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status: int = 400,
        field: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.field = field
        self.details = dict(details or {})


class LocalAppService:
    """Orchestrate existing Codie domain APIs against one contained workspace."""

    def __init__(
        self,
        workspace_root: str | Path,
        database_path: str | Path,
        *,
        catalog_source: Any | None = None,
        moxfield_source: Any | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root).expanduser().resolve()
        self.database_path = _contained_path(self.workspace_root, database_path)
        self.catalog_source = catalog_source or ScryfallCatalogSource()
        self.moxfield_source = moxfield_source or MoxfieldDeckSource()

    def health(self, *, ui_ready: bool) -> dict[str, Any]:
        database_ready = self._database_ready()
        return {
            "service": "ready",
            "database_ready": database_ready,
            "catalog_ready": database_ready and self._count("cards") > 0,
            "ui_ready": ui_ready,
            "privacy": "loopback-only; local persistence; no telemetry",
        }

    def workspace_summary(self, *, ui_ready: bool) -> dict[str, Any]:
        database_ready = self._database_ready()
        counts = {
            "cards": 0,
            "decks": 0,
            "saved_analyses": 0,
        }
        if database_ready:
            counts = {
                "cards": self._count("cards"),
                "decks": self._count("user_decks"),
                "saved_analyses": self._count("saved_analysis"),
            }
        return {
            "workspace_root": str(self.workspace_root),
            "database_path": str(self.database_path),
            "database_ready": database_ready,
            "ui_ready": ui_ready,
            "counts": counts,
        }

    def bootstrap(self) -> dict[str, Any]:
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        if self.database_path.exists():
            if not self._database_ready():
                raise LocalAppError(
                    "database_not_ready",
                    "The configured database exists but is not a complete Codie workspace.",
                    status=409,
                    field="database_path",
                )
            return {"initialized": True, "created": False, "database_path": str(self.database_path)}

        connection = bootstrap_database(self.database_path)
        connection.close()
        return {"initialized": True, "created": True, "database_path": str(self.database_path)}

    def import_catalog(self, request: Mapping[str, Any]) -> dict[str, Any]:
        payloads = _catalog_payloads(request)
        canonical = json.dumps(payloads, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        snapshot_hash = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return self._import_catalog_payloads(payloads, snapshot_hash=snapshot_hash)

    def prepare_catalog(self, request: Mapping[str, Any]) -> dict[str, Any]:
        if request.get("allow_network") is not True:
            raise LocalAppError(
                "network_consent_required",
                "Preparing card data requires an explicit user action that allows this download.",
                status=422,
                field="allow_network",
            )
        refresh = request.get("refresh", False)
        if not isinstance(refresh, bool):
            raise LocalAppError(
                "invalid_refresh_option",
                "The refresh option must be true or false.",
                status=422,
                field="refresh",
            )
        self.bootstrap()
        try:
            snapshot = self.catalog_source.prepare(self.workspace_root, refresh=refresh)
            payloads = read_catalog_payloads(snapshot)
        except LocalSourceError as exc:
            raise _source_error(exc, field="refresh") from exc

        result = self._import_catalog_payloads(payloads, snapshot_hash=snapshot.content_hash)
        result.update(
            {
                "from_cache": snapshot.from_cache,
                "source_updated_at": snapshot.source_updated_at,
            }
        )
        return result

    def _import_catalog_payloads(
        self,
        payloads: tuple[Mapping[str, Any], ...],
        *,
        snapshot_hash: str,
    ) -> dict[str, Any]:
        imported_at = _now()
        try:
            parsed_cards = tuple(
                ScryfallCard.from_payload(dict(payload), imported_at=imported_at)
                for payload in payloads
            )
        except (TypeError, ValueError, ScryfallParseError) as exc:
            raise LocalAppError(
                "invalid_catalog_snapshot",
                "The selected Scryfall snapshot contains an invalid card record.",
                status=422,
                field="snapshot",
            ) from exc
        cards = tuple(card for card in parsed_cards if card.normalized_name)
        rejected_count = len(parsed_cards) - len(cards)
        if not cards:
            raise LocalAppError(
                "invalid_catalog_snapshot",
                "The selected Scryfall snapshot contained no safely matchable card records.",
                status=422,
                field="snapshot",
            )

        connection = self._ready_connection()
        try:
            with connection:
                with BaseRepository.transaction(connection, "local_catalog_import"):
                    imported = ScryfallImporter(CoreRepository(connection)).import_cards(cards)
        except Exception as exc:
            raise LocalAppError(
                "catalog_import_failed",
                "The Scryfall snapshot could not be imported; no partial import was saved.",
                status=422,
                field="snapshot",
            ) from exc
        finally:
            connection.close()

        return {
            "imported_count": imported,
            "rejected_count": rejected_count,
            "snapshot_hash": snapshot_hash,
            "warnings": (
                [f"Skipped {rejected_count} card record(s) whose names cannot be matched safely."]
                if rejected_count
                else []
            ),
            "evidence_class": "card_truth",
        }

    def list_decks(self) -> dict[str, Any]:
        connection = self._ready_connection()
        try:
            rows = list_deck_memory(UserRepository(connection), DeckMemoryFilters(limit=200))
            return {"decks": [_deck_summary(row) for row in rows]}
        finally:
            connection.close()

    def get_deck(self, user_deck_id: int, *, include_raw: bool = False) -> dict[str, Any]:
        connection = self._ready_connection()
        try:
            try:
                detail = get_deck_memory_detail(UserRepository(connection), user_deck_id)
            except DeckMemoryReadError as exc:
                raise LocalAppError(
                    "deck_not_found", "The requested deck was not found.", status=404
                ) from exc
            payload = {
                "summary": _deck_summary(detail.summary),
                "cards": [
                    {
                        "card_name": card.raw_name,
                        "quantity": card.quantity,
                        "zone": card.zone,
                        "oracle_id": card.oracle_id,
                        "resolution_status": card.resolution_status,
                    }
                    for card in detail.cards
                ],
                "analyses": [
                    {
                        "saved_analysis_id": row.saved_analysis_id,
                        "user_deck_id": detail.summary.user_deck_id,
                        "analysis_type": row.analysis_type,
                        "generated_at": row.generated_at,
                        "deck_hash": row.deck_hash,
                    }
                    for row in detail.saved_analyses
                ],
                "raw_input_included": include_raw,
            }
            if include_raw:
                payload["raw_input"] = detail.raw_input
            return payload
        finally:
            connection.close()

    def import_deck(self, request: Mapping[str, Any]) -> dict[str, Any]:
        deck_input = _required_text(
            request.get("deck_input", request.get("decklist")),
            "deck_input",
        )
        deck_name = _optional_text(request.get("deck_name"), "deck_name")
        source_url: str | None = None
        source_type = "pasted_decklist"
        if is_moxfield_deck_reference(deck_input):
            if request.get("allow_network") is not True:
                raise LocalAppError(
                    "network_consent_required",
                    "Loading a public Moxfield link requires an explicit user import action.",
                    status=422,
                    field="allow_network",
                )
            try:
                fetched = self.moxfield_source.fetch(deck_input)
            except LocalSourceError as exc:
                raise _source_error(exc, field="deck_input") from exc
            decklist = fetched.decklist
            deck_name = deck_name or fetched.deck_name
            source_url = fetched.source_url
            source_type = "moxfield_public_link"
        else:
            decklist = deck_input

        if not self._database_ready() or self._count("cards") == 0:
            raise LocalAppError(
                "catalog_not_ready",
                "Prepare Codie's card data before importing a deck.",
                status=409,
                field="deck_input",
            )
        connection = self._ready_connection()
        try:
            user_repository = UserRepository(connection)
            importer = UserDeckImporter(
                user_repository,
                CardLookup(CoreRepository(connection)),
            )
            try:
                with connection:
                    result = importer.import_text(
                        decklist,
                        deck_name=deck_name,
                        source_url=source_url,
                        is_temporary=False,
                    )
            except UserDeckImportError as exc:
                unresolved = _unresolved_names(str(exc))
                code = "unresolved_cards" if unresolved else "invalid_decklist"
                message = (
                    "Some card names could not be resolved from the local catalog; no deck was saved."
                    if unresolved
                    else "The decklist could not be imported; no deck was saved."
                )
                raise LocalAppError(
                    code,
                    message,
                    status=422,
                    field="deck_input",
                    details={
                        "unresolved_names": unresolved[:20],
                        "unresolved_count": len(unresolved),
                    },
                ) from exc
            return {
                "user_deck_id": result.user_deck_id,
                "analysis_session_id": result.analysis_session_id,
                "deck_hash": result.deck_hash,
                "commander_hash": result.commander_hash,
                "card_count": result.card_count,
                "unresolved_names": [],
                "source_type": source_type,
                "source_url": source_url,
            }
        finally:
            connection.close()

    def compare_deck(self, user_deck_id: int, request: Mapping[str, Any]) -> dict[str, Any]:
        candidates = _evidence_candidates(request)
        connection = self._ready_connection()
        try:
            user_repository = UserRepository(connection)
            try:
                analysis_input = build_user_deck_analysis_input(user_repository, user_deck_id)
            except UserDeckAnalysisInputError as exc:
                raise LocalAppError(
                    "deck_not_found", "The requested deck was not found.", status=404
                ) from exc
            comparison = compare_user_deck_to_evidence(
                analysis_input,
                candidates,
                generated_at=_now(),
            )
            with connection:
                saved = save_user_deck_comparison_analysis(user_repository, comparison)
            return {
                "saved_analysis_id": saved.saved_analysis_id,
                "comparison": user_deck_comparison_export(comparison),
                "notice": "Evidence presence is descriptive and is not a recommendation.",
            }
        finally:
            connection.close()

    def list_analyses(self, user_deck_id: int) -> dict[str, Any]:
        connection = self._ready_connection()
        try:
            user_repository = UserRepository(connection)
            if user_repository.get_user_deck(user_deck_id) is None:
                raise LocalAppError(
                    "deck_not_found", "The requested deck was not found.", status=404
                )
            analyses = list_saved_user_deck_analyses(user_repository, user_deck_id)
            return {
                "analyses": [
                    {
                        "saved_analysis_id": row.saved_analysis_id,
                        "user_deck_id": row.user_deck_id,
                        "analysis_type": row.analysis_type,
                        "generated_at": row.generated_at,
                        "deck_hash": row.deck_hash,
                    }
                    for row in analyses
                ]
            }
        finally:
            connection.close()

    def get_analysis(self, saved_analysis_id: int) -> dict[str, Any]:
        detail = self._analysis_detail(saved_analysis_id)
        return {
            "summary": {
                "saved_analysis_id": detail.summary.saved_analysis_id,
                "user_deck_id": detail.summary.user_deck_id,
                "analysis_type": detail.summary.analysis_type,
                "generated_at": detail.summary.generated_at,
                "deck_hash": detail.summary.deck_hash,
            },
            "comparison": detail.summary_payload,
            "notice": "Evidence presence is descriptive and is not a recommendation.",
        }

    def export_analysis(self, saved_analysis_id: int, export_format: str) -> dict[str, Any]:
        if export_format not in {"json", "markdown"}:
            raise LocalAppError(
                "unsupported_export_format",
                "Export format must be json or markdown.",
                status=422,
                field="format",
            )
        detail = self._analysis_detail(saved_analysis_id)
        comparison = _comparison_from_payload(detail.summary_payload)
        if export_format == "json":
            content = (
                json.dumps(
                    user_deck_comparison_export(comparison),
                    sort_keys=True,
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n"
            )
            media_type = "application/json"
        elif export_format == "markdown":
            content = user_deck_comparison_markdown(comparison)
            media_type = "text/markdown"
        extension = "json" if export_format == "json" else "md"
        return {
            "filename": f"codie-analysis-{saved_analysis_id}.{extension}",
            "media_type": media_type,
            "content": content,
        }

    def _analysis_detail(self, saved_analysis_id: int):
        connection = self._ready_connection()
        try:
            try:
                return get_saved_user_deck_analysis(UserRepository(connection), saved_analysis_id)
            except SavedAnalysisReadError as exc:
                raise LocalAppError(
                    "analysis_not_found",
                    "The requested saved analysis was not found.",
                    status=404,
                ) from exc
        finally:
            connection.close()

    def _database_ready(self) -> bool:
        if not self.database_path.is_file():
            return False
        try:
            connection = connect(self.database_path)
            try:
                rows = connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
                names = {str(row["name"]) for row in rows}
                return REQUIRED_TABLES.issubset(names)
            finally:
                connection.close()
        except Exception:
            return False

    def _ready_connection(self) -> Any:
        if not self._database_ready():
            raise LocalAppError(
                "database_not_initialized",
                "Initialize the local workspace database before using this action.",
                status=409,
            )
        return connect(self.database_path)

    def _count(self, table: str) -> int:
        if table not in {"cards", "user_decks", "saved_analysis"}:
            raise ValueError("unsupported count table")
        connection = connect(self.database_path)
        try:
            row = connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
            return int(row["count"])
        finally:
            connection.close()


def _catalog_payloads(request: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    snapshot = request.get("snapshot")
    if isinstance(snapshot, Mapping):
        if isinstance(snapshot.get("data"), list):
            snapshot = snapshot["data"]
        elif isinstance(snapshot.get("cards"), list):
            snapshot = snapshot["cards"]
    if not isinstance(snapshot, list) or not snapshot:
        raise LocalAppError(
            "invalid_catalog_snapshot",
            "The selected Scryfall snapshot must contain a non-empty card list.",
            status=422,
            field="snapshot",
        )
    if not all(isinstance(item, Mapping) for item in snapshot):
        raise LocalAppError(
            "invalid_catalog_snapshot",
            "Every Scryfall snapshot entry must be an object.",
            status=422,
            field="snapshot",
        )
    return tuple(snapshot)


def _evidence_candidates(request: Mapping[str, Any]) -> tuple[UserDeckEvidenceCandidate, ...]:
    raw_candidates = request.get("candidates")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise LocalAppError(
            "invalid_evidence_packet",
            "The evidence packet must contain a non-empty candidates list.",
            status=422,
            field="candidates",
        )
    candidates: list[UserDeckEvidenceCandidate] = []
    allowed_fields = {
        "oracle_id",
        "card_name",
        "evidence_type",
        "score",
        "sample_size",
        "source_record_id",
        "source_url",
    }
    for index, raw in enumerate(raw_candidates):
        if not isinstance(raw, Mapping):
            raise _candidate_error(index, "Every evidence candidate must be an object.")
        unknown = sorted(set(raw) - allowed_fields)
        if unknown:
            raise _candidate_error(index, f"Unknown evidence field: {unknown[0]}")
        evidence_type = _required_text(raw.get("evidence_type"), "evidence_type")
        normalized_type = " ".join(evidence_type.lower().split())
        if any(fragment in normalized_type for fragment in FORBIDDEN_EVIDENCE_FRAGMENTS):
            raise _candidate_error(index, "Evidence type cannot encode strategic advice.")
        source_url = _optional_text(raw.get("source_url"), "source_url")
        if (
            source_url is not None
            and _is_hareruya(source_url)
            and "tournament" not in normalized_type
        ):
            raise _candidate_error(index, "Hareruya references must remain tournament evidence.")
        score = raw.get("score")
        if score is not None and (isinstance(score, bool) or not isinstance(score, int | float)):
            raise _candidate_error(index, "score must be a number between 0 and 1.")
        sample_size = raw.get("sample_size")
        if sample_size is not None and (
            isinstance(sample_size, bool) or not isinstance(sample_size, int)
        ):
            raise _candidate_error(index, "sample_size must be a non-negative integer.")
        try:
            candidates.append(
                UserDeckEvidenceCandidate(
                    oracle_id=_required_text(raw.get("oracle_id"), "oracle_id"),
                    card_name=_required_text(raw.get("card_name"), "card_name"),
                    evidence_type=evidence_type,
                    score=float(score) if score is not None else None,
                    sample_size=sample_size,
                    source_record_id=_optional_text(
                        raw.get("source_record_id"), "source_record_id"
                    ),
                    source_url=source_url,
                )
            )
        except ValueError as exc:
            raise _candidate_error(index, str(exc)) from exc
    return tuple(candidates)


def _candidate_error(index: int, message: str) -> LocalAppError:
    return LocalAppError(
        "invalid_evidence_candidate",
        message,
        status=422,
        field=f"candidates[{index}]",
    )


def _source_error(error: LocalSourceError, *, field: str) -> LocalAppError:
    return LocalAppError(
        error.code,
        error.message,
        status=503 if error.retryable else 422,
        field=field,
        details={"retryable": error.retryable},
    )


def _comparison_from_payload(payload: Mapping[str, Any]) -> UserDeckEvidenceComparison:
    try:
        raw_rows = payload["rows"]
        if not isinstance(raw_rows, list):
            raise TypeError("rows")
        rows = tuple(
            UserDeckEvidenceComparisonRow(
                oracle_id=str(row["oracle_id"]),
                card_name=str(row["card_name"]),
                evidence_type=str(row["evidence_type"]),
                presence_status=str(row["presence_status"]),
                quantity_in_deck=int(row["quantity_in_deck"]),
                zones=tuple(str(zone) for zone in row.get("zones", [])),
                score=float(row["score"]) if row.get("score") is not None else None,
                sample_size=int(row["sample_size"]) if row.get("sample_size") is not None else None,
                source_record_id=row.get("source_record_id"),
                source_url=row.get("source_url"),
                evidence_line=str(row["evidence_line"]),
            )
            for row in raw_rows
            if isinstance(row, Mapping)
        )
        if len(rows) != len(raw_rows):
            raise TypeError("row")
        return UserDeckEvidenceComparison(
            user_deck_id=int(payload["user_deck_id"]),
            deck_hash=str(payload["deck_hash"]),
            commander_hash=payload.get("commander_hash"),
            rows=rows,
            present_count=int(payload["present_count"]),
            absent_count=int(payload["absent_count"]),
            generated_at=str(payload["generated_at"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise LocalAppError(
            "invalid_saved_analysis",
            "The saved analysis cannot be exported safely.",
            status=422,
        ) from exc


def _deck_summary(row: Any) -> dict[str, Any]:
    return {
        "user_deck_id": row.user_deck_id,
        "deck_name": row.deck_name,
        "deck_hash": row.deck_hash,
        "commander_hash": row.commander_hash,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "is_temporary": row.is_temporary,
        "card_count": row.card_count,
        "saved_analysis_count": row.saved_analysis_count,
        "latest_analysis_generated_at": row.latest_analysis_generated_at,
    }


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LocalAppError(
            "invalid_request",
            f"{field} is required.",
            status=422,
            field=field,
        )
    return value.strip()


def _optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise LocalAppError(
            "invalid_request",
            f"{field} must be text when provided.",
            status=422,
            field=field,
        )
    return value.strip() or None


def _unresolved_names(message: str) -> list[str]:
    prefix = "Unresolved card(s): "
    if not message.startswith(prefix):
        return []
    return [name.strip() for name in message[len(prefix) :].split(",") if name.strip()]


def _is_hareruya(source_url: str) -> bool:
    try:
        host = (urlparse(source_url).hostname or "").lower()
    except ValueError:
        return False
    return "hareruya" in host


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _contained_path(root: Path, candidate: str | Path) -> Path:
    path = Path(candidate).expanduser()
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise LocalAppError(
            "workspace_path_escape",
            "The configured database path must remain inside the workspace root.",
            status=422,
            field="database_path",
        ) from exc
    return resolved
