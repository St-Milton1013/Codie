from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from codie.exports import (
    ValidationSummary,
    build_checkpoint_export,
    checkpoint_markdown,
    write_checkpoint_markdown,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def recommendation_export():
    return {
        "metadata": {"export_type": "recommendation_run", "generated_at": GENERATED_AT, "schema_version": "1"},
        "run": {"recommendation_run_id": 1},
        "candidates": [{"oracle_id": "oracle-remora"}],
    }


def innovation_export():
    return {
        "metadata": {"export_type": "innovation_snapshot", "generated_at": GENERATED_AT, "schema_version": "1"},
        "snapshot": {"innovation_snapshot_run_id": 2},
        "items": [{"innovation_id": "innovation:remora"}],
    }


class CheckpointExportTest(unittest.TestCase):
    def test_checkpoint_dictionary_sorts_exports_and_preserves_validation(self) -> None:
        validation = ValidationSummary(
            command="python -m unittest discover -s tests -v",
            status="PASS",
            test_count=238,
            commit_hash="abc123",
            notes=("Boundary scans clean.",),
        )
        checkpoint = build_checkpoint_export(
            title="Codie Checkpoint",
            generated_at=GENERATED_AT,
            validation=validation,
            exports=(recommendation_export(), innovation_export()),
            review_notes=("No UI included.",),
        )

        self.assertEqual(checkpoint.validation.status, "pass")
        self.assertEqual([export["metadata"]["export_type"] for export in checkpoint.exports], ["innovation_snapshot", "recommendation_run"])
        self.assertEqual(checkpoint.validation.test_count, 238)

    def test_checkpoint_markdown_is_deterministic(self) -> None:
        checkpoint = build_checkpoint_export(
            title="Codie Checkpoint",
            generated_at=GENERATED_AT,
            validation=ValidationSummary(command="tests", status="pass", test_count=2),
            exports=(recommendation_export(), innovation_export()),
            review_notes=("Review ready.",),
        )

        first = checkpoint_markdown(checkpoint)
        second = checkpoint_markdown(checkpoint)

        self.assertEqual(first, second)
        self.assertIn("Validation Status: pass", first)
        self.assertIn("1 candidate(s)", first)
        self.assertIn("1 innovation signal(s)", first)

    def test_write_checkpoint_markdown_uses_writer(self) -> None:
        checkpoint = build_checkpoint_export(
            title="Codie Checkpoint",
            generated_at=GENERATED_AT,
            validation=ValidationSummary(command="tests", status="pass"),
            exports=(),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "checkpoint.md"

            result = write_checkpoint_markdown(checkpoint, target, output_root=root)

            self.assertEqual(result.content_type, "text/markdown")
            self.assertIn("# Codie Checkpoint", target.read_text(encoding="utf-8"))

    def test_invalid_checkpoint_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            ValidationSummary(command="", status="pass")
        with self.assertRaises(ValueError):
            ValidationSummary(command="tests", status="maybe")
        with self.assertRaises(ValueError):
            ValidationSummary(command="tests", status="pass", test_count=-1)
        with self.assertRaises(ValueError):
            build_checkpoint_export(
                title="You should play this card",
                generated_at=GENERATED_AT,
                validation=ValidationSummary(command="tests", status="pass"),
                exports=(),
            )


if __name__ == "__main__":
    unittest.main()
