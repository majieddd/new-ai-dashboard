"""Ground the static research site in immutable experiment records."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from build_research_site import HERE, build, load_results, render, summarise


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
        cls.e14, cls.e15, cls.e16, cls.e17 = load_results()
        cls.page = render(cls.e14, cls.e15, cls.e16, cls.e17)

    def test_measured_verdicts_and_seed_isolation(self):
        s = summarise(self.e14, self.e15, self.e16, self.e17)
        self.assertEqual((s["wins"], s["retention_pass"]), (0, 0))
        self.assertEqual(s["params_last"], 1467888)
        self.assertEqual(s["E16"]["scheduled_adapter"]["old"], 100.0)
        self.assertLess(s["E16"]["scheduled_adapter"]["new"], 20)
        self.assertEqual((s["E17"]["scheduled_adapter"]["old"],
                          s["E17"]["scheduled_adapter"]["new"]), (100.0, 100.0))
        self.assertEqual(len(set(r["seed"] for r in self.e17["runs"])), 5)
        self.assertIn("post-E16 hyperparameter choice", self.page)
        self.assertIn("not continuous model evolution", self.page)

    def test_one_graph_and_navigation(self):
        p = Tags()
        p.feed(self.page)
        self.assertEqual(p.tags.count("svg"), 1)
        self.assertEqual(p.tags.count("polyline"), 3)
        self.assertIn("rounds", p.ids)
        self.assertIn("corrected", p.ids)
        self.assertIn("roadmap", p.ids)
        self.assertIn("data", p.ids)
        self.assertNotIn("<script", self.page)
        self.assertNotIn("__WINS__", self.page)
        self.assertIn("0/10", self.page)
        self.assertIn("1,467,888", self.page)
        self.assertEqual(p.tags.count("tr"), 19)  # ten E15 rounds + six E16/E17 rows + three headers

    def test_built_bytes_and_downloads(self):
        dest = HERE / "research-site"
        page = build(out=dest)
        self.assertEqual((dest / "index.html").read_text(encoding="utf-8"), page)
        p = Tags()
        p.feed(page)
        for link in p.links:
            if link and not link.startswith("#"):
                self.assertTrue((dest / link).is_file(), link)
        for exp in ("e15", "e16", "e17"):
            d = json.loads((dest / "data" / (exp + ".json")).read_text(encoding="utf-8"))
            self.assertIn("history" if exp == "e15" else "runs", d)
        self.assertEqual(len(json.loads((dest / "data/e14.json").read_text(encoding="utf-8"))), 5)


if __name__ == "__main__":
    unittest.main()
