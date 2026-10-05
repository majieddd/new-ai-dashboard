"""Ground the static research site in immutable experiment records."""
import copy
import json
import hashlib
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from benchmark_preview import public_protocol
from build_research_site import (HERE, build, check_publication, e19_accuracy_chart,
                                 e19_timing_chart, load_results, render, summarise)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        info = dict(attrs)
        self.tags.append(tag)
        if tag == "a":
            self.links.append(info.get("href"))
        if "id" in info:
            self.ids.add(info["id"])


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e14, cls.e15, cls.e16, cls.e17, cls.e18 = load_results()
        cls.page = render(cls.e14, cls.e15, cls.e16, cls.e17, cls.e18)

    def test_measured_verdicts_and_seed_isolation(self):
        s = summarise(self.e14, self.e15, self.e16, self.e17, self.e18)
        self.assertEqual((s["wins"], s["retention_pass"]), (0, 0))
        self.assertEqual(s["params_last"], 1467888)
        self.assertEqual(s["E16"]["scheduled_adapter"]["old"], 100.0)
        self.assertLess(s["E16"]["scheduled_adapter"]["new"], 20)
        self.assertEqual((s["E17"]["scheduled_adapter"]["old"],
                          s["E17"]["scheduled_adapter"]["new"]), (100.0, 100.0))
        self.assertEqual(len(set(r["seed"] for r in self.e17["runs"])), 5)
        self.assertIn("post-E16 hyperparameter choice", self.page)
        self.assertIn("not continuous model evolution", self.page)
        self.assertEqual(s["E18"]["concept_auc"], .5)
        self.assertEqual(s["E18"]["nuisance_accuracy"], 100)
        self.assertGreater(s["E18"]["val_fpr"], 5)
        self.assertEqual(s["E18"]["feedback_delay"], [32] * 5)
        for filename, expected in self.e18["provenance"]["source_sha256"].items():
            # Git's Windows checkout changes LF to CRLF; E18 recorded LF source bytes.
            source = (HERE / filename).read_bytes().replace(bytes([13, 10]), bytes([10]))
            self.assertEqual(hashlib.sha256(source).hexdigest(), expected)

    def test_one_graph_and_navigation(self):
        p = Tags()
        p.feed(self.page)
        self.assertEqual(p.tags.count("svg"), 1)
        self.assertEqual(p.tags.count("polyline"), 3)
        self.assertIn("rounds", p.ids)
        self.assertIn("corrected", p.ids)
        self.assertIn("trigger", p.ids)
        self.assertIn("roadmap", p.ids)
        self.assertIn("data", p.ids)
        self.assertNotIn("<script", self.page)
        self.assertNotIn("__WINS__", self.page)
        self.assertIn("0/10", self.page)
        self.assertIn("1,467,888", self.page)
        self.assertIn("5.078%", self.page)
        self.assertEqual(p.tags.count("tr"), 19)  # ten E15 rounds + six E16/E17 rows + three headers

    def test_built_bytes_and_downloads(self):
        dest = HERE / "research-site"
        page = build(out=dest)
        self.assertEqual((dest / "index.html").read_text(encoding="utf-8"), page)
        self.assertEqual(page.count('<section id="text-pilot">'), 1)
        self.assertEqual(page.count('<section id="progress">'), 1)
        self.assertLess(page.index('id="progress"'), page.index('id="text-pilot"'))
        self.assertIn('41 missing <em>evidence predicates</em>', page)
        self.assertIn('progress/index.html', page)
        self.assertIn('href="benchmarks/index.html"', page)
        self.assertIn("Feedback vs scheduled", page)
        self.assertIn("0.00 pts", page)
        self.assertIn("59.15%", page)
        self.assertIn("not a language model", page)
        self.assertEqual(page.count("<svg"), 3)
        self.assertLess(page.index('id="text-pilot"'), page.index('id="rounds"'))
        self.assertIn('id="e19-accuracy-title"', page)
        self.assertIn('id="e19-timing-title"', page)
        self.assertIn('id="e19-accuracy-desc"', page)
        self.assertIn('id="e19-timing-desc"', page)
        self.assertIn("Future-round publication gate", page)
        self.assertNotIn("<script", page)
        p = Tags()
        p.feed(page)
        for link in p.links:
            if link and not link.startswith("#"):
                self.assertTrue((dest / link).is_file(), link)
        progress = (dest / "progress/index.html").read_text(encoding="utf-8")
        self.assertIn('href="../benchmarks/index.html"', progress)
        self.assertIn("No confirmed LLM result", progress)
        self.assertIn("0 model trials inferred", progress)
        self.assertIn("no model predictions", progress)
        self.assertIn("matched functional parameter count", progress)
        self.assertNotIn("<script", progress)
        progress_tags = Tags()
        progress_tags.feed(progress)
        self.assertIn('https://github.com/majieddd/new-ai-dashboard/blob/main/source/PROGRESS_STATUS.md', progress_tags.links)
        for link in progress_tags.links:
            if link and not link.startswith(("#", "https://")):
                self.assertTrue((dest / "progress" / link.split("#", 1)[0]).is_file(), link)
        self.assertEqual(json.loads((dest / "data/progress.json").read_text(encoding="utf-8")),
                         json.loads((HERE / "results/PROGRESS/status.json").read_text(encoding="utf-8")))
        for exp in ("e15", "e16", "e17", "e18", "e19"):
            d = json.loads((dest / "data" / (exp + ".json")).read_text(encoding="utf-8"))
            self.assertIn("history" if exp == "e15" else "runs", d)
        self.assertEqual(len(json.loads((dest / "data/e14.json").read_text(encoding="utf-8"))), 5)
        self.assertEqual(json.loads((dest / "data/e19.json").read_text(encoding="utf-8"))["experiment"], "E19")
        benchmark = (dest / "benchmarks/index.html").read_text(encoding="utf-8")
        self.assertIn("Proposal, not a model result", benchmark)
        self.assertIn("E19’s recorded failed outcome is unchanged", benchmark)
        self.assertEqual(benchmark.count('class="card"'), 9)
        self.assertEqual(json.loads((dest / "benchmarks/suite.json").read_text(encoding="utf-8"))["official_results"], [])
        self.assertEqual((dest / "benchmarks/protocol.txt").read_text(encoding="utf-8"),
                         public_protocol())
        benchmark_tags = Tags()
        benchmark_tags.feed(benchmark)
        for link in benchmark_tags.links:
            if link and not link.startswith(("#", "https://")):
                self.assertTrue((dest / "benchmarks" / link.split("#", 1)[0]).is_file(), link)

    def test_e19_visuals_are_generated_from_raw_paired_seeds(self):
        record = json.loads((HERE / "results/E19/summary.json").read_text(encoding="utf-8"))
        runs = record["runs"]
        accuracy = e19_accuracy_chart(runs)
        timing = e19_timing_chart(runs)
        ElementTree.fromstring(accuracy)
        ElementTree.fromstring(timing)
        self.assertEqual(accuracy.count("seed "), 20)  # 4 distinct visible arms × 5 seeds
        self.assertEqual(timing.count("feedback minus "), 10)  # 2 controls × 5 paired seeds
        self.assertIn("scheduled = feedback", accuracy)
        self.assertIn("required ≥2 pts", timing)
        self.assertIn("feedback minus scheduled: 0.000", timing)
        modified = copy.deepcopy(runs)
        modified[0]["arms"]["frozen"]["new_test"] -= .01
        self.assertNotEqual(accuracy, e19_accuracy_chart(modified))
        for row in runs:
            for arm in ("frozen", "random", "scheduled", "feedback", "full_finetune"):
                old = 100 * row["arms"][arm]["old_test"]
                new = 100 * row["arms"][arm]["new_test"]
                self.assertTrue(80 <= old <= 95 and 48 <= new <= 80,
                                f"chart axes would clip {arm}, seed {row['seed']}")

    def test_new_summary_blocks_publication_until_site_includes_it(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            future = source / "results/E20/summary.json"
            future.parent.mkdir(parents=True)
            future.write_text('{"experiment":"E20"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "E20"):
                check_publication(source, 'data/e15.json data/e16.json data/e17.json data/e18.json data/e19.json')


if __name__ == "__main__":
    unittest.main()
