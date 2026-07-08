from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    ChatAnswer,
    ChatAnswerCaveat,
    ChatAnswerCitation,
    ChatAnswerMissingEvidence,
    ChatAnswerSection,
    ChatEvidenceNeed,
    ChatQueryPlan,
    ChatQueryRequest,
    ChatQuerySubject,
    ChatUIBoundaryOptions,
    ChatUIErrorPacket,
    LocalAPIContractError,
    LocalAPIErrorEnvelope,
    LocalAPIOptions,
    LocalAPIRouteSpec,
    build_chat_route_spec,
    build_chat_ui_error_packet,
    build_chat_ui_request_packet,
    build_chat_ui_response_packet,
    build_local_api_error_envelope,
    build_local_api_request_envelope,
    build_local_api_response_envelope,
    local_api_error_envelope_to_dict,
    local_api_request_envelope_to_dict,
    local_api_response_envelope_to_dict,
    local_api_route_spec_to_dict,
)


GENERATED_AT = "2026-07-07T00:00:00+00:00"


def subject() -> ChatQuerySubject:
    return ChatQuerySubject(
        subject_type="deck",
        subject_key="deck:fixture",
        display_name="Fixture Deck",
    )


def request(**overrides) -> ChatQueryRequest:
    data = {
        "request_id": "request:local-api",
        "question_text": "Summarize this deck.",
        "generated_at": GENERATED_AT,
        "subject": subject(),
        "constraints": (),
        "allowed_privacy_scopes": ("public",),
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return ChatQueryRequest(**data)


def plan(**overrides) -> ChatQueryPlan:
    data = {
        "plan_id": "plan:local-api",
        "request_id": "request:local-api",
        "question_class": "deck_summary",
        "subject": subject(),
        "evidence_needs": (
            ChatEvidenceNeed(
                need_id="need:deck",
                need_type="deck_memory",
                reason="Deck memory summary is needed.",
            ),
        ),
        "allowed_operations": ("inspect_deck_memory",),
        "generated_at": GENERATED_AT,
    }
    data.update(overrides)
    return ChatQueryPlan(**data)


def citation() -> ChatAnswerCitation:
    return ChatAnswerCitation(
        citation_id="citation:deck",
        source_type="deck_memory",
        source_id="deck:fixture",
        record_type="deck_memory_summary",
        generated_at=GENERATED_AT,
    )


def caveat() -> ChatAnswerCaveat:
    return ChatAnswerCaveat(
        caveat_id="caveat:sample",
        caveat_type="low_evidence",
        message="Low sample caveat remains visible.",
        severity="warning",
    )


def missing_evidence() -> ChatAnswerMissingEvidence:
    return ChatAnswerMissingEvidence(
        missing_evidence_id="missing:regional",
        need_id="need:regional",
        need_type="manual_note",
        reason="Regional evidence is unavailable.",
    )


def answer(**overrides) -> ChatAnswer:
    data = {
        "answer_id": "answer:local-api",
        "request_id": "request:local-api",
        "plan_id": "plan:local-api",
        "answer_mode": "deck_summary",
        "sections": (
            ChatAnswerSection(
                section_id="section:answer",
                section_type="summary",
                title="Evidence Summary",
                statements=("Sanitized evidence supports this summary.",),
                citation_ids=("citation:deck",),
                caveat_ids=("caveat:sample",),
                missing_evidence_ids=("missing:regional",),
            ),
        ),
        "citations": (citation(),),
        "caveats": (caveat(),),
        "blockers": ({"message": "Manual review required"},),
        "missing_evidence": (missing_evidence(),),
        "privacy_scope": "public",
        "generated_at": GENERATED_AT,
    }
    data.update(overrides)
    return ChatAnswer(**data)


def request_packet(**overrides):
    data = {
        "request": request(),
        "client_surface": "test_fixture",
    }
    data.update(overrides)
    return build_chat_ui_request_packet(data["request"], data["client_surface"])


def response_packet(**overrides):
    req = request_packet()
    data = {
        "request_packet": req,
        "plan": plan(),
        "answer": answer(),
    }
    data.update(overrides)
    return build_chat_ui_response_packet(data["request_packet"], data["plan"], data["answer"])


def error_packet(**overrides):
    req = request_packet()
    data = {
        "request_packet": req,
        "error_type": "missing_evidence",
        "message": "Evidence unavailable.",
    }
    data.update(overrides)
    return build_chat_ui_error_packet(data["request_packet"], data["error_type"], data["message"])


class IntelligenceLocalAPITest(unittest.TestCase):
    def test_valid_chat_route_spec_serializes_deterministically(self) -> None:
        route = build_chat_route_spec("chat_request", GENERATED_AT)

        payload = local_api_route_spec_to_dict(route)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["path"], "/local/chat/request")
        self.assertTrue(payload["local_only"])

    def test_route_spec_requires_local_path(self) -> None:
        with self.assertRaises(LocalAPIContractError):
            LocalAPIRouteSpec(
                route_id="route:bad",
                method="POST",
                path="/chat/request",
                operation="chat_request",
                request_packet_type="ChatUIRequestPacket",
                response_packet_type="ChatUIRequestPacket",
                allowed_client_surfaces=("test_fixture",),
                generated_at=GENERATED_AT,
            )

    def test_route_spec_rejects_non_local_paths_by_default(self) -> None:
        with self.assertRaises(LocalAPIContractError):
            LocalAPIRouteSpec(
                route_id="route:remote",
                method="POST",
                path="https://example.test/local/chat/request",
                operation="chat_request",
                request_packet_type="ChatUIRequestPacket",
                response_packet_type="ChatUIRequestPacket",
                allowed_client_surfaces=("test_fixture",),
                generated_at=GENERATED_AT,
            )

    def test_route_spec_rejects_unsupported_methods(self) -> None:
        with self.assertRaises(LocalAPIContractError):
            LocalAPIRouteSpec(
                route_id="route:bad-method",
                method="PUT",
                path="/local/chat/request",
                operation="chat_request",
                request_packet_type="ChatUIRequestPacket",
                response_packet_type="ChatUIRequestPacket",
                allowed_client_surfaces=("test_fixture",),
                generated_at=GENERATED_AT,
            )

    def test_request_envelope_validates_method_path_against_route(self) -> None:
        route = build_chat_route_spec("chat_request", GENERATED_AT)
        envelope = build_local_api_request_envelope(route, request_packet(), GENERATED_AT)

        self.assertEqual(envelope.method, route.method)
        self.assertEqual(envelope.path, route.path)

    def test_request_envelope_rejects_unsupported_client_surface(self) -> None:
        route = LocalAPIRouteSpec(
            route_id="route:local-ui-only",
            method="POST",
            path="/local/chat/request",
            operation="chat_request",
            request_packet_type="ChatUIRequestPacket",
            response_packet_type="ChatUIRequestPacket",
            allowed_client_surfaces=("local_ui",),
            generated_at=GENERATED_AT,
        )

        with self.assertRaises(LocalAPIContractError):
            build_local_api_request_envelope(route, request_packet(), GENERATED_AT)

    def test_response_envelope_preserves_chat_ui_response_packet(self) -> None:
        route = build_chat_route_spec("chat_response", GENERATED_AT)
        envelope = build_local_api_response_envelope(route, response_packet(), GENERATED_AT)

        self.assertEqual(envelope.status_code, 200)
        self.assertEqual(envelope.response_packet.citations[0].citation_id, "citation:deck")

    def test_error_envelope_preserves_chat_ui_error_packet(self) -> None:
        route = build_chat_route_spec("chat_error", GENERATED_AT)
        envelope = build_local_api_error_envelope(route, error_packet(), 422, GENERATED_AT)

        self.assertEqual(envelope.status_code, 422)
        self.assertEqual(envelope.error_packet.error_type, "missing_evidence")

    def test_error_envelope_rejects_stack_trace_metadata(self) -> None:
        route = build_chat_route_spec("chat_error", GENERATED_AT)

        with self.assertRaises(LocalAPIContractError):
            build_local_api_error_envelope(route, error_packet(), 500, GENERATED_AT, metadata={"stack-trace": "secret"})

    def test_local_user_data_is_blocked_by_default(self) -> None:
        route = build_chat_route_spec("chat_request", GENERATED_AT)
        packet = build_chat_ui_request_packet(
            request(allowed_privacy_scopes=("local_user_data",)),
            "test_fixture",
            options=ChatUIBoundaryOptions(allow_local_user_data=True),
        )

        with self.assertRaises(LocalAPIContractError):
            build_local_api_request_envelope(route, packet, GENERATED_AT)

    def test_sensitive_scope_is_blocked_by_default(self) -> None:
        route = build_chat_route_spec("chat_response", GENERATED_AT)
        packet = build_chat_ui_response_packet(
            request_packet(),
            plan(),
            answer(privacy_scope="sensitive"),
            options=ChatUIBoundaryOptions(allow_sensitive=True),
        )

        with self.assertRaises(LocalAPIContractError):
            build_local_api_response_envelope(route, packet, GENERATED_AT)

    def test_private_metadata_keys_fail_cleanly(self) -> None:
        route = build_chat_route_spec("chat_request", GENERATED_AT)
        blocked_keys = (
            "raw_" + "input",
            "private_" + "deck_text",
            "full_" + "primer_body",
            "raw_" + "provider_payload",
            "provider_" + "payload",
            "original_" + "import_text",
        )
        for blocked_key in blocked_keys:
            with self.subTest(blocked_key=blocked_key):
                with self.assertRaises(LocalAPIContractError):
                    build_local_api_request_envelope(route, request_packet(), GENERATED_AT, metadata={blocked_key: "secret"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        route = build_chat_route_spec("chat_request", GENERATED_AT)

        with self.assertRaises(LocalAPIContractError):
            build_local_api_request_envelope(route, request_packet(), GENERATED_AT, metadata={"safe": [{"private-deck-text": "secret"}]})

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        bad_phrase = "you " + "should " + "play"
        route = build_chat_route_spec("chat_error", GENERATED_AT)
        bad_error = ChatUIErrorPacket(
            error_packet_id="error:bad",
            request_packet_id="request-packet:bad",
            request_id="request:local-api",
            error_type="validation_error",
            message="Validation failed.",
            retryable=False,
            generated_at=GENERATED_AT,
        )

        with self.assertRaises(LocalAPIContractError):
            build_local_api_error_envelope(route, bad_error, 400, GENERATED_AT, metadata={"message": f"{bad_phrase} this card."})

    def test_serialization_is_deterministic(self) -> None:
        request_route = build_chat_route_spec("chat_request", GENERATED_AT)
        response_route = build_chat_route_spec("chat_response", GENERATED_AT)
        error_route = build_chat_route_spec("chat_error", GENERATED_AT)
        payloads = (
            local_api_route_spec_to_dict(request_route),
            local_api_request_envelope_to_dict(build_local_api_request_envelope(request_route, request_packet(), GENERATED_AT)),
            local_api_response_envelope_to_dict(build_local_api_response_envelope(response_route, response_packet(), GENERATED_AT)),
            local_api_error_envelope_to_dict(build_local_api_error_envelope(error_route, error_packet(), 422, GENERATED_AT)),
        )

        for payload in payloads:
            json.dumps(payload, sort_keys=True)

    def test_options_reject_invalid_payload_size(self) -> None:
        with self.assertRaises(LocalAPIContractError):
            LocalAPIOptions(maximum_payload_bytes=0)

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.intelligence.local_api as local_api_module

        source = Path(local_api_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "open" + "ai",
            "anth" + "ropic",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "open(",
            "write_text(",
            "write_bytes(",
            "Path(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
