"""Fail closed on missing/corrupt October 6 evidence or a premature bot claim."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from build_research_site import build
from goal_status import RECEIPT_KEYS, home_section, results_section, verify
from status_update import load

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class GoalStatusTests(unittest.TestCase):
    def test_verified_goal_and_raw_receipts(self):
        record = load(HERE, ROOT / "data")
        derived = record["_goal_evidence"]
        self.assertFalse(record["original_goal"]["runnable_real_language_bot_meeting_spec"])
        self.assertEqual(record["original_goal"]["e8_composition"], "NOT_STARTED")
        self.assertEqual(record["e20_verified_preparation"]["gpu_chargeable_balance"], "UNKNOWN")
        cpu = json.loads((ROOT / "data/e20-cpu-preflight.json").read_text())
        readback = json.loads((ROOT / "data/e20-cpu-readback.json").read_text())
        self.assertEqual([c["exit_code"] for c in cpu["commands"]], [1, 0, 0, 0])
        self.assertIn("Ran 46 tests", cpu["commands"][1]["stderr"])
        self.assertEqual((readback["rows"][0]["audit_events"],
                          readback["rows"][0]["snapshots_checked"],
                          readback["rows"][0]["reconstruction"]["scored_targets"]), (775, 8, 329))
        self.assertEqual(len(derived["gpu"]), 4)
        home = home_section(record, derived)
        detail = results_section(record, derived)
        self.assertIn("No runnable real-language bot", home)
        self.assertIn("E8 composition NOT STARTED", home)
        self.assertIn("46/46 passed, zero skipped", detail)
        self.assertIn("329 scored targets", detail)
        self.assertIn("70 passed / 71 discovered", detail)
        self.assertIn("snapshot release", detail)
        self.assertIn("GPU balance <strong>UNKNOWN</strong>", detail)
        self.assertNotIn("LM capability PASS", home + detail)
        for item in (record["e20_verified_preparation"]["cpu_receipt"],
                     record["e20_verified_preparation"]["cpu_readback"],
                     *record["e20_verified_preparation"]["gpu_receipts"].values()):
            path = ROOT / "data" / item["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
        for key in RECEIPT_KEYS:
            self.assertIn("../data/" + record["e20_verified_preparation"]["gpu_receipts"][key]["path"], detail)

    def test_mutations_and_missing_receipts_fail_closed(self):
        record = json.loads((HERE / "status_update_2026_10_06.json").read_text())
        for group, key, changed in (("original_goal", "runnable_real_language_bot_meeting_spec", True),
                                    ("original_goal", "e8_composition", "PASSED"),
                                    ("e20_verified_preparation", "gpu_chargeable_balance", "24h"),
                                    ("e20_verified_preparation", "rights_cleared_articles", 1)):
            mutated = copy.deepcopy(record)
            mutated[group][key] = changed
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify(mutated, HERE, ROOT / "data")
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            for item in (record["e20_verified_preparation"]["cpu_receipt"],
                         record["e20_verified_preparation"]["cpu_readback"],
                         *record["e20_verified_preparation"]["gpu_receipts"].values()):
                shutil.copyfile(ROOT / "data" / item["path"], data / item["path"])
            bad = data / record["e20_verified_preparation"]["gpu_receipts"]["stream"]["path"]
            bad.write_bytes(bad.read_bytes() + b"x")
            with self.assertRaisesRegex(ValueError, "Changed public evidence"):
                verify(record, HERE, data)
            bad.unlink()
            with self.assertRaisesRegex(ValueError, "Missing or unsafe public evidence"):
                verify(record, HERE, data)

    def test_generated_routes_and_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(HERE, Path(tmp))
            root = Path(tmp)
            home = (root / "index.html").read_text()
            detail = (root / "progress/index.html").read_text()
            self.assertLess(home.index('id="goal"'), home.index('id="review-update"'))
            self.assertLess(detail.index('id="oct6-results"'), detail.index('id="e20"'))
            self.assertIn("October 5 readiness snapshot", detail)
            self.assertIn("41 missing evidence predicates", detail)
            self.assertIn("one explicit no-corpus-read skip", detail)
            record = load(HERE, ROOT / "data")
            for item in (record["e20_verified_preparation"]["cpu_receipt"],
                         record["e20_verified_preparation"]["cpu_readback"],
                         *record["e20_verified_preparation"]["gpu_receipts"].values()):
                self.assertEqual((root / "data" / item["path"]).read_bytes(),
                                 (ROOT / "data" / item["path"]).read_bytes())
            for item in record["e20_verified_preparation"]["reports"].values():
                self.assertEqual((root / "source" / item["path"]).read_bytes(),
                                 (HERE / item["path"]).read_bytes())


if __name__ == "__main__":
    unittest.main()
