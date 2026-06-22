from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.exports import ExportWriteResult, write_json_export, write_markdown_export


class ExportWriterTest(unittest.TestCase):
    def test_json_writer_creates_deterministic_file_and_parents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "nested" / "export.json"

            result = write_json_export({"b": 2, "a": {"z": 1}}, target, output_root=root)

            self.assertIsInstance(result, ExportWriteResult)
            self.assertEqual(result.content_type, "application/json")
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"a": {"z": 1}, "b": 2})
            self.assertEqual(target.read_text(encoding="utf-8"), '{\n  "a": {\n    "z": 1\n  },\n  "b": 2\n}\n')
            self.assertEqual(result.bytes_written, len(target.read_bytes()))

    def test_markdown_writer_creates_file_and_final_newline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "reports" / "checkpoint.md"

            result = write_markdown_export("# Checkpoint", target, output_root=root)

            self.assertEqual(result.content_type, "text/markdown")
            self.assertEqual(target.read_text(encoding="utf-8"), "# Checkpoint\n")
            self.assertEqual(result.bytes_written, len("# Checkpoint\n".encode("utf-8")))

    def test_output_root_containment_rejects_outside_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / "outside.json"

            with self.assertRaises(ValueError):
                write_json_export({"ok": True}, outside, output_root=root)

    def test_unsupported_suffix_and_invalid_inputs_fail_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                write_json_export({"ok": True}, root / "export.txt", output_root=root)
            with self.assertRaises(ValueError):
                write_markdown_export("# ok", root / "export.txt", output_root=root)
            with self.assertRaises(ValueError):
                write_markdown_export("", root / "export.md", output_root=root)
            with self.assertRaises(TypeError):
                write_json_export(["not", "dict"], root / "export.json", output_root=root)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
