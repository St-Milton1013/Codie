"""Pure local API route and envelope packets for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.query_planner import ALLOWED_PRIVACY_SCOPES
from codie.intelligence.ui_api_boundary import (
    ChatUIErrorPacket,
    ChatUIRequestPacket,
    ChatUIResponsePacket,
    chat_ui_error_packet_to_dict,
    chat_ui_request_packet_to_dict,
    chat_ui_response_packet_to_dict,
)


ALLOWED_METHODS = frozenset({"GET", "POST"})
ALLOWED_OPERATIONS = frozenset({"chat_request", "chat_response", "chat_error", "health"})
ALLOWED_PACKET_TYPES = frozenset({"ChatUIRequestPacket", "ChatUIResponsePacket", "ChatUIErrorPacket", "None"})
ALLOWED_CLIENT_SURFACES = frozenset({"local_ui", "local_api", "cli", "test_fixture"})
ALLOWED_ERROR_STATUS_CODES = frozenset({400, 403, 404, 409, 422, 500})

FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "raw_input",
        "private_deck_text",
        "full_primer_body",
        "raw_" + "provider_payload",
        "provider_payload",
        "original_import_text",
    }
)

FORBIDDEN_TEXT_FRAGMENTS = (
    "should " + "play",
    "should be " + "played",
    "should be " + "cut",
    "must " + "include",
    "correct " + "card",
    "breaks the " + "format",
    "secretly " + "optimal",
    "cut " + "this",
    "strict " + "upgrade",
    "auto-" + "include",
    "recommended " + "cut",
    "recommended " + "include",
)

STACK_TRACE_KEYS = frozenset({"traceback", "stack", "stack_trace", "exception_trace"})


class LocalAPIContractError(ValueError):
    """Raised when local API contract packets cannot be built safely."""


@dataclass(frozen=True)
class LocalAPIOptions:
    allow_non_local_paths: bool = False
    allow_non_local_hosts: bool = False
    allow_sensitive: bool = False
    allow_local_user_data: bool = False
    maximum_payload_bytes: int = 262144
    require_local_only_routes: bool = True

    def __post_init__(self) -> None:
        if self.maximum_payload_bytes < 1:
            raise LocalAPIContractError("maximum_payload_bytes must be positive")


@dataclass(frozen=True)
class LocalAPIRouteSpec:
    route_id: str
    method: str
    path: str
    operation: str
    request_packet_type: str
    response_packet_type: str
    allowed_client_surfaces: tuple[str, ...]
    requires_auth: bool = False
    local_only: bool = True
    privacy_scope: str = "public"
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.route_id, "route_id")
        object.__setattr__(self, "method", _normalize_allowed(self.method.upper(), ALLOWED_METHODS, "method"))
        object.__setattr__(self, "path", _validate_path(self.path))
        object.__setattr__(self, "operation", _normalize_allowed(self.operation, ALLOWED_OPERATIONS, "operation"))
        object.__setattr__(self, "request_packet_type", _normalize_allowed(self.request_packet_type, ALLOWED_PACKET_TYPES, "request_packet_type"))
        object.__setattr__(self, "response_packet_type", _normalize_allowed(self.response_packet_type, ALLOWED_PACKET_TYPES, "response_packet_type"))
        if not self.allowed_client_surfaces:
            raise LocalAPIContractError("allowed_client_surfaces must not be empty")
        surfaces = tuple(sorted(_normalize_allowed(item, ALLOWED_CLIENT_SURFACES, "client_surface") for item in self.allowed_client_surfaces))
        object.__setattr__(self, "allowed_client_surfaces", surfaces)
        if not isinstance(self.requires_auth, bool):
            raise LocalAPIContractError("requires_auth must be a bool")
        if not isinstance(self.local_only, bool):
            raise LocalAPIContractError("local_only must be a bool")
        if not self.local_only:
            raise LocalAPIContractError("local_only must be true")
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LocalAPIRequestEnvelope:
    envelope_id: str
    route_id: str
    method: str
    path: str
    client_surface: str
    request_packet: ChatUIRequestPacket
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.envelope_id, "envelope_id")
        _require_text(self.route_id, "route_id")
        object.__setattr__(self, "method", _normalize_allowed(self.method.upper(), ALLOWED_METHODS, "method"))
        object.__setattr__(self, "path", _validate_path(self.path))
        object.__setattr__(self, "client_surface", _normalize_allowed(self.client_surface, ALLOWED_CLIENT_SURFACES, "client_surface"))
        if not isinstance(self.request_packet, ChatUIRequestPacket):
            raise LocalAPIContractError("request_packet must be a ChatUIRequestPacket")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LocalAPIResponseEnvelope:
    envelope_id: str
    route_id: str
    status_code: int
    response_packet: ChatUIResponsePacket
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.envelope_id, "envelope_id")
        _require_text(self.route_id, "route_id")
        if self.status_code != 200:
            raise LocalAPIContractError("success response status_code must be 200")
        if not isinstance(self.response_packet, ChatUIResponsePacket):
            raise LocalAPIContractError("response_packet must be a ChatUIResponsePacket")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LocalAPIErrorEnvelope:
    envelope_id: str
    route_id: str
    status_code: int
    error_packet: ChatUIErrorPacket
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.envelope_id, "envelope_id")
        _require_text(self.route_id, "route_id")
        if self.status_code not in ALLOWED_ERROR_STATUS_CODES:
            raise LocalAPIContractError("unsupported error status_code")
        if not isinstance(self.error_packet, ChatUIErrorPacket):
            raise LocalAPIContractError("error_packet must be a ChatUIErrorPacket")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_error_metadata(self.metadata))


def build_chat_route_spec(
    operation: str,
    generated_at: str,
    options: LocalAPIOptions | None = None,
) -> LocalAPIRouteSpec:
    """Build one deterministic local chat route specification."""

    resolved_options = options or LocalAPIOptions()
    route_map = {
        "chat_request": ("POST", "/local/chat/request", "ChatUIRequestPacket", "ChatUIRequestPacket"),
        "chat_response": ("POST", "/local/chat/response", "ChatUIResponsePacket", "ChatUIResponsePacket"),
        "chat_error": ("POST", "/local/chat/error", "ChatUIErrorPacket", "ChatUIErrorPacket"),
        "health": ("GET", "/local/health", "None", "None"),
    }
    normalized_operation = _normalize_allowed(operation, ALLOWED_OPERATIONS, "operation")
    method, path, request_type, response_type = route_map[normalized_operation]
    route = LocalAPIRouteSpec(
        route_id=f"local-route:{normalized_operation}",
        method=method,
        path=path,
        operation=normalized_operation,
        request_packet_type=request_type,
        response_packet_type=response_type,
        allowed_client_surfaces=("local_ui", "local_api", "cli", "test_fixture"),
        requires_auth=False,
        local_only=True,
        privacy_scope="public",
        generated_at=generated_at,
        metadata={"source": "local_api_contract"},
    )
    _validate_route_against_options(route, resolved_options)
    return route


def build_local_api_request_envelope(
    route: LocalAPIRouteSpec,
    request_packet: ChatUIRequestPacket,
    generated_at: str,
    metadata: dict[str, Any] | None = None,
    options: LocalAPIOptions | None = None,
) -> LocalAPIRequestEnvelope:
    """Wrap one UI request packet for a local route spec."""

    resolved_options = options or LocalAPIOptions()
    _validate_route_against_options(route, resolved_options)
    if route.request_packet_type != "ChatUIRequestPacket":
        raise LocalAPIContractError("route does not accept ChatUIRequestPacket")
    if request_packet.client_surface not in route.allowed_client_surfaces:
        raise LocalAPIContractError("client_surface is not allowed for route")
    _validate_privacy_scope(request_packet.allowed_privacy_scopes, resolved_options)
    envelope = LocalAPIRequestEnvelope(
        envelope_id=f"local-api-request:{request_packet.request_id}",
        route_id=route.route_id,
        method=route.method,
        path=route.path,
        client_surface=request_packet.client_surface,
        request_packet=request_packet,
        generated_at=generated_at,
        metadata=metadata or {},
    )
    _validate_payload_size(local_api_request_envelope_to_dict(envelope), resolved_options)
    return envelope


def build_local_api_response_envelope(
    route: LocalAPIRouteSpec,
    response_packet: ChatUIResponsePacket,
    generated_at: str,
    metadata: dict[str, Any] | None = None,
    options: LocalAPIOptions | None = None,
) -> LocalAPIResponseEnvelope:
    """Wrap one UI response packet for a local route spec."""

    resolved_options = options or LocalAPIOptions()
    _validate_route_against_options(route, resolved_options)
    if route.response_packet_type != "ChatUIResponsePacket":
        raise LocalAPIContractError("route does not emit ChatUIResponsePacket")
    _validate_privacy_scope((response_packet.privacy_scope,), resolved_options)
    envelope = LocalAPIResponseEnvelope(
        envelope_id=f"local-api-response:{response_packet.request_id}",
        route_id=route.route_id,
        status_code=200,
        response_packet=response_packet,
        generated_at=generated_at,
        metadata=metadata or {},
    )
    _validate_payload_size(local_api_response_envelope_to_dict(envelope), resolved_options)
    return envelope


def build_local_api_error_envelope(
    route: LocalAPIRouteSpec,
    error_packet: ChatUIErrorPacket,
    status_code: int,
    generated_at: str,
    metadata: dict[str, Any] | None = None,
    options: LocalAPIOptions | None = None,
) -> LocalAPIErrorEnvelope:
    """Wrap one UI error packet for a local route spec."""

    resolved_options = options or LocalAPIOptions()
    _validate_route_against_options(route, resolved_options)
    envelope = LocalAPIErrorEnvelope(
        envelope_id=f"local-api-error:{error_packet.request_id}",
        route_id=route.route_id,
        status_code=status_code,
        error_packet=error_packet,
        generated_at=generated_at,
        metadata=metadata or {},
    )
    _validate_payload_size(local_api_error_envelope_to_dict(envelope), resolved_options)
    return envelope


def local_api_route_spec_to_dict(route: LocalAPIRouteSpec) -> dict[str, Any]:
    """Serialize one local API route spec deterministically."""

    return {
        "route_id": route.route_id,
        "method": route.method,
        "path": route.path,
        "operation": route.operation,
        "request_packet_type": route.request_packet_type,
        "response_packet_type": route.response_packet_type,
        "allowed_client_surfaces": list(route.allowed_client_surfaces),
        "requires_auth": route.requires_auth,
        "local_only": route.local_only,
        "privacy_scope": route.privacy_scope,
        "generated_at": route.generated_at,
        "metadata": _sorted_json_object(route.metadata),
    }


def local_api_request_envelope_to_dict(envelope: LocalAPIRequestEnvelope) -> dict[str, Any]:
    """Serialize one local API request envelope deterministically."""

    return {
        "envelope_id": envelope.envelope_id,
        "route_id": envelope.route_id,
        "method": envelope.method,
        "path": envelope.path,
        "client_surface": envelope.client_surface,
        "request_packet": chat_ui_request_packet_to_dict(envelope.request_packet),
        "generated_at": envelope.generated_at,
        "metadata": _sorted_json_object(envelope.metadata),
    }


def local_api_response_envelope_to_dict(envelope: LocalAPIResponseEnvelope) -> dict[str, Any]:
    """Serialize one local API response envelope deterministically."""

    return {
        "envelope_id": envelope.envelope_id,
        "route_id": envelope.route_id,
        "status_code": envelope.status_code,
        "response_packet": chat_ui_response_packet_to_dict(envelope.response_packet),
        "generated_at": envelope.generated_at,
        "metadata": _sorted_json_object(envelope.metadata),
    }


def local_api_error_envelope_to_dict(envelope: LocalAPIErrorEnvelope) -> dict[str, Any]:
    """Serialize one local API error envelope deterministically."""

    return {
        "envelope_id": envelope.envelope_id,
        "route_id": envelope.route_id,
        "status_code": envelope.status_code,
        "error_packet": chat_ui_error_packet_to_dict(envelope.error_packet),
        "generated_at": envelope.generated_at,
        "metadata": _sorted_json_object(envelope.metadata),
    }


def _validate_route_against_options(route: LocalAPIRouteSpec, options: LocalAPIOptions) -> None:
    if not isinstance(route, LocalAPIRouteSpec):
        raise LocalAPIContractError("route must be a LocalAPIRouteSpec")
    if options.require_local_only_routes and not route.local_only:
        raise LocalAPIContractError("route must be local_only")
    if not options.allow_non_local_paths and not route.path.startswith("/local/"):
        raise LocalAPIContractError("route path must be local")
    _validate_privacy_scope((route.privacy_scope,), options)


def _validate_privacy_scope(scopes: tuple[str, ...], options: LocalAPIOptions) -> None:
    for scope in scopes:
        normalized = _normalize_allowed(scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope")
        if normalized == "local_user_data" and not options.allow_local_user_data:
            raise LocalAPIContractError("local_user_data is disabled by default")
        if normalized == "sensitive" and not options.allow_sensitive:
            raise LocalAPIContractError("sensitive scope is disabled by default")


def _validate_payload_size(payload: dict[str, Any], options: LocalAPIOptions) -> None:
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    if len(encoded) > options.maximum_payload_bytes:
        raise LocalAPIContractError("payload exceeds maximum size")


def _validate_path(path: str) -> str:
    value = _require_text(path, "path")
    if not value.startswith("/"):
        raise LocalAPIContractError("path must start with /")
    if "://" in value:
        raise LocalAPIContractError("path must not contain a remote URL")
    if not value.startswith("/local/"):
        raise LocalAPIContractError("path must start with /local/")
    return value


def _validate_error_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_metadata(metadata)
    for key in _iter_keys(validated):
        if _normalize_metadata_key(key) in STACK_TRACE_KEYS:
            raise LocalAPIContractError("error metadata must not expose stack traces")
    return validated


def _iter_keys(value: Any) -> tuple[str, ...]:
    if isinstance(value, dict):
        keys: list[str] = []
        for key, child in value.items():
            keys.append(key)
            keys.extend(_iter_keys(child))
        return tuple(keys)
    if isinstance(value, (list, tuple)):
        keys = []
        for child in value:
            keys.extend(_iter_keys(child))
        return tuple(keys)
    return ()


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).strip()
    if field_name == "method":
        normalized = normalized.upper()
    else:
        if normalized in allowed:
            return normalized
        normalized = normalized.lower()
        lowered_allowed = {item.lower(): item for item in allowed}
        if normalized in lowered_allowed:
            return lowered_allowed[normalized]
    if normalized not in allowed:
        raise LocalAPIContractError(f"unsupported {field_name}: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LocalAPIContractError(f"{field_name} is required")
    return value.strip()


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if any(fragment in text.lower() for fragment in FORBIDDEN_TEXT_FRAGMENTS):
        raise LocalAPIContractError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise LocalAPIContractError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise LocalAPIContractError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise LocalAPIContractError(f"{path} contains forbidden metadata key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise LocalAPIContractError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
