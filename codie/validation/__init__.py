"""Governance and data-health validation helpers."""

from .coverage import CanonicalCoverageReport, build_canonical_coverage_report
from .local_gate import (
    AggregatedValidationResult,
    ValidationFinding,
    ValidationGateOptions,
    ValidatorReport,
    aggregate_validator_reports,
    render_markdown_summary,
    run_validation_gate,
    validate_report_payload,
)
from .repair_controller import (
    RepairControllerOptions,
    RepairControllerResult,
    RepairExecutionResult,
    ValidationCycleResult,
    run_repair_controller,
    unauthorized_repair_paths,
)

__all__ = [
    "AggregatedValidationResult",
    "CanonicalCoverageReport",
    "ValidationFinding",
    "ValidationGateOptions",
    "RepairControllerOptions",
    "RepairControllerResult",
    "RepairExecutionResult",
    "ValidationCycleResult",
    "ValidatorReport",
    "aggregate_validator_reports",
    "build_canonical_coverage_report",
    "render_markdown_summary",
    "run_repair_controller",
    "run_validation_gate",
    "unauthorized_repair_paths",
    "validate_report_payload",
]
