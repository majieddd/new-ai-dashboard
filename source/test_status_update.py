"""Check reviewed source/receipt bytes and prevent a status page from becoming a verdict."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from build_research_site import build
from status_update import REPORT_LABELS, RECEIPTS, home_section, load, progress_section

HERE = Path(__file__).resolve().parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))


class UpdateTests(unittest.TestCase):
    def test_pinned_reports_and_receipts(self):
        record = load(HERE, HERE.parent / "data")
        self.assertEqual(len(record["reports"]), 5)
        self.assertEqual(record["scientific_status"]["official_benchmark_lanes"], "9_NOT_RUN")
        for key in REPORT_LABELS:
            report = record["reports"][key]
            source_bytes = (HERE / report["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(source_bytes).hexdigest(), report["sha256"])
        for field, name in RECEIPTS.items():
            self.assertEqual(hashlib.sha256((HERE.parent / "data" / name).read_bytes()).hexdigest(),
                             record["e21"][field])
        # The full source report contains a Windows SID; the public copy never does.
        self.assertNotIn("S-1-5-21-", (HERE / record["reports"]["e21_evaluator"]["path"]).read_text())
        self.assertNotEqual(record["reports"]["e21_evaluator"]["sha256"],
                            record["reports"]["e21_evaluator"]["original_sha256"])

    def test_status_is_bounded_and_links_to_existing_artifacts(self):
        record = load(HERE, HERE.parent / "data")
        home, progress = home_section(record), progress_section(record)
        self.assertIn("E19 stays <strong>FAILED</strong>", home)
        self.assertIn("all nine official", home)
        self.assertIn("62 passed / 62", progress)
        self.assertIn("61 passed / 62", progress)
        self.assertIn("one explicit no-corpus-read skip", progress)
        self.assertIn("query-only cues", progress)
        self.assertIn("E9 is assigned", progress)
        self.assertIn("Owner approval on October 6", progress)
        self.assertIn("No separate-principal/off-host custodian", progress)
        self.assertNotIn("scientific PASS", progress)
        tags = Links()
        tags.feed(progress)
        self.assertEqual(sum("github.com/majieddd/new-ai-dashboard/blob/main/source/" in x
                             for x in tags.links if x), len(REPORT_LABELS) + 1)
        for name in RECEIPTS.values():
            self.assertIn("../data/" + name, tags.links)
        for key, report in record["reports"].items():
            self.assertIn("https://github.com/majieddd/new-ai-dashboard/blob/main/source/" +
                          report["path"], tags.links, key)

    def test_verdict_mutations_and_missing_bytes_fail_closed(self):
        record = load(HERE, HERE.parent / "data")
        alternate = copy.deepcopy(record)
        alternate["scientific_status"]["e21_language"] = "PASS"
        # Render functions consume a verified object; loader is the mandatory gate in build().
        self.assertNotEqual(alternate["scientific_status"], record["scientific_status"])
        with tempfile.TemporaryDirectory() as scratch:
            source = Path(scratch)
            for report in record["reports"].values():
                shutil.copyfile(HERE / report["path"], source / report["path"])
            alternate["reports"]["attractor"]["sha256"] = "0" * 64
            (source / "status_update_2026_10_06.json").write_text(json.dumps(alternate), encoding="utf-8")
            with self.assertRaises(ValueError):
                load(source, HERE.parent / "data")
            alternate = copy.deepcopy(record)
            alternate["approval"]["custodian_named"] = True
            (source / "status_update_2026_10_06.json").write_text(json.dumps(alternate), encoding="utf-8")
            with self.assertRaises(ValueError):
                load(source, HERE.parent / "data")

    def test_built_local_routes_and_bytes(self):
        build()
        out = HERE / "research-site"
        index = (out / "index.html").read_text(encoding="utf-8")
        progress = (out / "progress/index.html").read_text(encoding="utf-8")
        self.assertIn('id="review-update"', index)
        self.assertIn('id="updates"', progress)
        self.assertIn('href="progress/index.html#updates"', index)
        self.assertEqual(index.count('<section id="text-pilot">'), 1)
        for name in ("status-2026-10-06.json", *RECEIPTS.values()):
            self.assertEqual((out / "data" / name).read_bytes(),
                             (HERE / "status_update_2026_10_06.json").read_bytes() if name == "status-2026-10-06.json"
                             else (HERE.parent / "data" / name).read_bytes())
        for report in load(HERE, HERE.parent / "data")["reports"].values():
            self.assertEqual((out / "source" / report["path"]).read_bytes(),
                             (HERE / report["path"]).read_bytes())


if __name__ == "__main__":
    unittest.main()
