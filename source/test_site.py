"""Ground the static research site in immutable experiment records."""
import copy
import json
import hashlib
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from benchmark_preview import public_protocol
from build_research_site import (HERE, build, check_publication, e19_accuracy_chart,
                                 e19_timing_chart, load_results, render, summarise)
from oct7_update import DATA_NAMES, load as load_oct7
from openai_prep import DATA_NAMES as OPENAI_DATA_NAMES, load as load_openai


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
            if link and not link.startswith(("#", "https://")):
                self.assertTrue((dest / link.split("#", 1)[0]).is_file(), link)
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

    def test_openai_prep_publishes_zero_runs_honestly(self):
        dest = HERE / "research-site"
        build(out=dest)
        page = (dest / "index.html").read_text(encoding="utf-8")
        progress = (dest / "progress/index.html").read_text(encoding="utf-8")
        record = load_openai(HERE, HERE / "results" / "OPENAI")
        self.assertEqual(page.count('<section id="openai-prep">'), 1)
        self.assertEqual(progress.count('<section id="openai-updates">'), 1)
        self.assertIn("0 benchmark runs", page)
        self.assertIn("Actual benchmark calls: 0", progress)
        self.assertIn("Cost readback: unavailable", progress)
        self.assertIn("NOT temperature 0", progress)
        self.assertIn("exploratory calibration", progress)
        self.assertIn("2c1b0464a08806c78f3171b985423b6a8a9ada3280031ae1d8c06ca0578595ee", page)
        self.assertIn("d83a830e34f584bc634b99bfe67b1e9410118c3e17d8da4a51c0946efc1ea7d7", page)
        self.assertIn("69ff310ed4d1c4a277361a2d8d2ad7e0d710e051515fc0d7cd97865cbcaf166e", page)
        self.assertIn("1d787df5af0dd8adf4313a968e0217e329026e47", page)
        self.assertIn("51/51", page)
        # Every probe row equals the archived manifest entry.
        for m in record["_raw"]["probe"]["models"]:
            row = (f'<tr><th scope="row">{m["id"]}</th>'
                   f'<td>{m["cli"]}</td>'
                   f'<td>{m["completed_at_file_mtime_utc"]}</td>'
                   f'<td>{m["usage"]["input_tokens"]}</td>'
                   f'<td>{m["usage"].get("cached_input_tokens", 0)}</td>'
                   f'<td>{m["usage"]["output_tokens"]}</td>'
                   f'<td><code>{m["source_jsonl_sha256"]}</code></td></tr>')
            self.assertIn(row, progress)
        # Published data files are byte-identical to the archived originals.
        for name, expected in record["data_sha256"].items():
            path = dest / "data" / ("openai-" + name)
            self.assertTrue(path.is_file(), name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        self.assertTrue((dest / "data/openai-manifest.json").is_file())
        # No plot is published from probes: the OpenAI section has no chart.
        start = progress.index('<section id="openai-updates">')
        end = progress.index('<section id="oct7-updates">')
        self.assertNotIn("<svg", progress[start:end])

    def test_openai_archived_bytes_are_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            for name in OPENAI_DATA_NAMES:
                shutil.copyfile(HERE / "results/OPENAI" / name, temp / name)
            manifest = json.loads((HERE / "results/OPENAI/openai_manifest.json").read_text(encoding="utf-8"))
            (temp / "openai_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            for key, filename in manifest["report_paths"].items():
                shutil.copyfile(HERE / filename, temp / filename)
            self.assertEqual(load_openai(temp, temp)["schema"], "new-ai-openai-prep-record-v1")
            with (temp / "probe_gpt-5.5.jsonl").open("ab") as handle:
                handle.write(b" ")
            with self.assertRaisesRegex(ValueError, "Changed archived record"):
                load_openai(temp, temp)
            shutil.copyfile(HERE / "results/OPENAI/probe_gpt-5.5.jsonl", temp / "probe_gpt-5.5.jsonl")
            good = json.loads((HERE / "results/OPENAI/openai_manifest.json").read_text(encoding="utf-8"))
            good["data_sha256"]["s_b_pilot_manifest.json"] = "0" * 64
            (temp / "openai_manifest.json").write_text(json.dumps(good), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Changed archived record"):
                load_openai(temp, temp)

    def test_oct7_home_publishes_the_negative_verdict(self):
        dest = HERE / "research-site"
        build(out=dest)
        page = (dest / "index.html").read_text(encoding="utf-8")
        self.assertEqual(page.count('<section id="oct7">'), 1)
        self.assertIn("no advantage established", page)
        self.assertIn("-0.1302", page)          # mean paired difference, points
        self.assertIn("4/12", page)             # strict feedback wins
        self.assertIn("45/46", page)            # E21 correction suite
        self.assertIn("0.98046875", page)       # seed-23 old accuracy after promotion
        self.assertIn("0.99609375", page)       # seed-23 new accuracy after promotion
        self.assertIn("NOT RUN", page)
        self.assertIn("HELD", page)
        self.assertIn('<a href="#oct7">Latest · Oct 7</a>', page)
        self.assertIn('href="data/oct7-prospective_summary.json"', page)

    def test_oct7_progress_numbers_match_archived_bytes(self):
        dest = HERE / "research-site"
        build(out=dest)
        progress = (dest / "progress/index.html").read_text(encoding="utf-8")
        record = load_oct7(HERE, HERE / "results" / "OCT7")
        s = record["_raw"]["summary"]
        self.assertEqual(progress.count('<section id="oct7-updates">'), 1)
        self.assertIn("no advantage established", progress)
        # Every displayed per-seed row equals the archived receipt entry.
        for e in s["entries"]:
            row = (f'<tr><th scope="row">{e["seed"]}</th>'
                   f'<td>{100*e["feedback"]["new_test"]["accuracy"]:.6f}</td>'
                   f'<td>{100*e["schedule"]["new_test"]["accuracy"]:.6f}</td>'
                   f'<td>{100*e["paired_new_test_difference"]:+.6f}</td>')
            self.assertIn(row, progress)
        self.assertIn("6e8d71b", progress)      # protocol committed before execution
        self.assertIn("307c02884538d4ddf1481dd06d972e49c36b297c", progress)
        self.assertIn("86610ff3935009ecb204310b955a3402e651ca0c", progress)
        self.assertIn("3f1be602cf1d8cfbd6bbf8dae7ee1d736611c5f1", progress)  # reviewed pin
        self.assertIn("40224ff1a5aa27a32bf29d7f7d9664415dba290eb3190d155bb190b2fb4b47df", progress)
        self.assertIn("19/19 receipt mutations rejected", progress)
        self.assertIn("2,880 predictions", progress)
        self.assertIn("64 revealed labels and 7,680 growth presentations", progress)
        self.assertIn("96 and 11,520", progress)
        # The chart is generated from raw entries and parses as XML.
        start = progress.index('<svg class="chart" viewBox="0 0 960 420"')
        chart = progress[start:progress.index("</svg>", start) + len("</svg>")]
        ElementTree.fromstring(chart)
        self.assertEqual(chart.count("seed 101"), 1)   # axis label
        self.assertIn("Seed 101: feedback minus schedule +1.758 points", chart)  # tooltip
        self.assertIn("feedback minus schedule", chart)
        self.assertIn("required >= +2 pts", chart)
        # Archived data files are published and hash-verified by the loader.
        for name, expected in record["data_sha256"].items():
            path = dest / "data" / ("oct7-" + name)
            self.assertTrue(path.is_file(), name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        self.assertTrue((dest / "data/oct7-manifest.json").is_file())

    def test_oct7_archived_bytes_are_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            for name in DATA_NAMES:
                shutil.copyfile(HERE / "results/OCT7" / name, temp / name)
            manifest = json.loads((HERE / "results/OCT7/oct7_manifest.json").read_text(encoding="utf-8"))
            (temp / "oct7_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            for key, filename in manifest["report_paths"].items():
                shutil.copyfile(HERE / filename, temp / filename)
            # Baseline: the intact copy loads.
            self.assertEqual(load_oct7(temp, temp)["schema"],
                             "new-ai-oct7-verified-development-record-v1")
            # One mutated archived byte fails the build.
            with (temp / "prospective_summary.json").open("ab") as handle:
                handle.write(b" ")
            with self.assertRaisesRegex(ValueError, "Changed archived record"):
                load_oct7(temp, temp)
            # A manifest that no longer matches the bytes also fails.
            shutil.copyfile(HERE / "results/OCT7/prospective_summary.json",
                            temp / "prospective_summary.json")
            good = json.loads((HERE / "results/OCT7/oct7_manifest.json").read_text(encoding="utf-8"))
            good["data_sha256"]["prospective_summary.json"] = "0" * 64
            (temp / "oct7_manifest.json").write_text(json.dumps(good), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Changed archived record"):
                load_oct7(temp, temp)


if __name__ == "__main__":
    unittest.main()
