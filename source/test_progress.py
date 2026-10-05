"""Fail closed when a public preparation snapshot is mistaken for an outcome."""
import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from prepare_progress_snapshot import prepare
from progress_site import home_section, paired_chart, render, verify

HERE = Path(__file__).resolve().parent


class ProgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads((HERE / "results/PROGRESS/status.json").read_text(encoding="utf-8"))

    def test_snapshot_is_development_only_and_nonvacuous(self):
        e20, e21, e22 = verify(self.snapshot)
        self.assertEqual(e20["missing_evidence_predicates"], 41)
        self.assertFalse(e20["run_authorized"])
        self.assertEqual(len(e21["seeds"]), 5)
        self.assertEqual(sum(x > 0 for x in e21["paired_direct_minus_energy_k4_nll"]), 4)
        self.assertEqual(e22["factor_cells"], 16)
        self.assertEqual((e22["base_examples"], e22["variants"], e22["distinct_structural_groups"]),
                         (256, 768, 117))
        self.assertIsNone(e22["model_outcome"])
        self.assertEqual(sum(e22["counterfactual_directions"].values()), 256)
        for key in ("e20", "e21", "e22"):
            self.assertEqual(len(self.snapshot[key]["source_sha256"]), 64)

    def test_chart_and_cell_coverage_are_derived_from_snapshot(self):
        page = render(self.snapshot)
        home = home_section(self.snapshot)
        chart = paired_chart(self.snapshot["e21"])
        ElementTree.fromstring(chart)
        self.assertEqual(chart.count("feedback"), 0)
        self.assertEqual(chart.count("<circle"), 5)
        self.assertIn("4/5 paired NLL signs", page)
        self.assertIn("41 missing", home)
        self.assertIn("117 distinct numeric-free", page)
        self.assertEqual(page.count('class="tile"'), 16)
        self.assertNotIn("<script", page)
        shifted = copy.deepcopy(self.snapshot)
        shifted["e21"]["paired_direct_minus_energy_k4_nll"][0] += 0.004
        self.assertNotEqual(chart, paired_chart(shifted["e21"]))
        altered = copy.deepcopy(self.snapshot)
        altered["e22"]["per_cell_groups"]["depth1_arity1_distractors0"] = 1
        self.assertNotEqual(page, render(altered))

    def test_outcome_or_unreviewed_changes_fail_closed(self):
        mutations = (("scientific_verdict", "PASS"), ("e20.run_authorized", True),
                     ("e21.status", "PASS"), ("e22.model_outcome", {"accuracy": 1}))
        for key, value in mutations:
            record = copy.deepcopy(self.snapshot)
            if "." in key:
                group, name = key.split(".", 1)
                record[group][name] = value
            else:
                record[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                render(record)
        record = copy.deepcopy(self.snapshot)
        record["e21"]["paired_direct_minus_energy_k4_nll"].append(float("nan"))
        with self.assertRaises(ValueError):
            render(record)

    def test_source_projection_checks_real_inputs_and_rejects_corruption(self):
        root = HERE.parent
        paths = (root / "new-ai-e20-eval/RESEARCH/E20_PREPARATION_AUDIT_2026_10_05_02/BLOCKED_READINESS.json",
                 root / "new-ai-e21/results/E21_DEV/cpu-v1-run-001/summary.json",
                 root / "new-ai-e22-candidate/e22_candidate/dev_runs/SWEEP_2026_10_05_B/RECEIPT.json")
        if not all(path.is_file() for path in paths):
            self.skipTest("source worktrees absent; published projection still render-tested")
        self.assertEqual(prepare(*paths, self.snapshot["as_of_utc"]), self.snapshot)
        with tempfile.TemporaryDirectory() as temp:
            e20 = json.loads(paths[0].read_text(encoding="utf-8"))
            e20["blocker_count"] -= 1
            corrupt = Path(temp) / "e20.json"
            corrupt.write_text(json.dumps(e20), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "blocker count"):
                prepare(corrupt, paths[1], paths[2], self.snapshot["as_of_utc"])
        with self.assertRaisesRegex(ValueError, "aware UTC"):
            prepare(*paths, "2026-10-05T13:01:46")


if __name__ == "__main__":
    unittest.main()
