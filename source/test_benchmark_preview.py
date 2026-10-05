"""Integrity, status-boundary and rendering checks for the benchmark preview."""
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import benchmark_preview as preview


class BenchmarkPreviewTests(unittest.TestCase):
    def setUp(self):
        self.source = preview.MANIFEST.read_bytes()
        self.suite = json.loads(self.source)

    def test_suite_has_all_distinct_defined_lanes(self):
        preview.validate(self.suite)
        tests = self.suite["tests"]
        self.assertEqual(len(tests), 9)
        self.assertEqual(len({item["id"] for item in tests}), len(tests))
        self.assertEqual([sum(item["group"] == group for item in tests)
                          for group in ("BENCHMARKS", "AGENT TASKS")], [4, 5])
        self.assertEqual({item["status"] for item in tests}, {"not_run"})

    def test_rejects_synthetic_receipt_as_official_result(self):
        suite = {**self.suite, "official_results": [{"score": 1.0}]}
        with self.assertRaisesRegex(ValueError, "official score"):
            preview.validate(suite)

    def test_rejects_scored_status(self):
        suite = {**self.suite, "tests": [dict(row) for row in self.suite["tests"]]}
        suite["tests"][0]["status"] = "pass"
        with self.assertRaisesRegex(ValueError, "scored"):
            preview.validate(suite)

    def test_requires_a_method_and_controls(self):
        suite = {**self.suite, "tests": [dict(row) for row in self.suite["tests"]]}
        suite["tests"][0]["method"] = ""
        with self.assertRaisesRegex(ValueError, "nonempty"):
            preview.validate(suite)

    def test_escapes_untrusted_test_text(self):
        test = dict(self.suite["tests"][0], title='<script>alert("bad")</script>')
        card = preview.render_card(test)
        self.assertNotIn("<script>", card)
        self.assertIn("&lt;script&gt;", card)

    def test_build_is_byte_matched_and_never_claims_an_official_run(self):
        path, digest = preview.build()
        page = path.read_text(encoding="utf-8")
        self.assertEqual(digest, hashlib.sha256(self.source).hexdigest())
        self.assertEqual((path.parent / "suite.json").read_bytes(), self.source)
        protocol = (path.parent / "protocol.txt").read_text(encoding="utf-8")
        self.assertEqual(protocol, preview.public_protocol())
        self.assertTrue(protocol.startswith("# A benchmark format"))
        self.assertEqual(page.count('class="card"'), 9)
        self.assertIn("Official model result</span><b>— · No receipt", page)
        self.assertIn("No New AI model has an authorized run under this suite", page)
        self.assertIn("E19’s recorded failed outcome is unchanged", page)
        self.assertIn("Luke’s Dev Lab video", page)
        self.assertIn('href="protocol.txt"', page)
        self.assertIn('href="../index.html"', page)
        self.assertIn('href="../progress/index.html"', page)
        self.assertIn("Showing 9 of 9", page)
        self.assertIn(digest, page)
        self.assertNotIn("__CARDS__", page)
        self.assertNotIn("__SUITE_SHA__", page)

    def test_status_boundary_applies_before_files_are_written(self):
        altered = {**self.suite, "official_results": [{"score": 0.75}]}
        with patch.object(preview.MANIFEST.__class__, "read_bytes", return_value=json.dumps(altered).encode()):
            with self.assertRaises(ValueError):
                preview.build()


if __name__ == "__main__":
    unittest.main()
