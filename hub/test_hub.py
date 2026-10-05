"""Structural and local-link checks for the New AI hub preview."""
import json
import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        for key in ("href", "src"):
            if values.get(key):
                self.refs.append((tag, key, values[key]))


class HubTests(unittest.TestCase):
    def test_ledger_integrity(self):
        data = json.loads((ROOT / "blueprint-ledger.json").read_text(encoding="utf-8"))
        nodes = {item["id"] for item in data["nodes"]}
        edges = {item["id"] for item in data["edges"]}
        self.assertEqual((len(nodes), len(edges)), (14, 34))
        self.assertTrue(all(not node["running_now"] for node in data["nodes"]))
        for item in data["nodes"] + data["edges"]:
            self.assertTrue(item["evidence"])
            self.assertIn(item["gate"], data["gates"])
            self.assertIn(item["boundary"], data["boundaries"])
            self.assertIn(item["failure"], data["failures"])
        for edge in data["edges"]:
            self.assertIn(edge["from"], nodes)
            self.assertIn(edge["to"], nodes)
        self.assertEqual({v["id"]: len(v["nodes"]) for v in data["views"]},
                         {"e19": 8, "e20": 9, "e21": 8, "future": 14})
        for view in data["views"]:
            self.assertTrue(set(view["primary_edges"]) <= edges)
            for edge in data["edges"]:
                if edge["id"] in view["primary_edges"]:
                    self.assertIn(edge["from"], view["nodes"])
                    self.assertIn(edge["to"], view["nodes"])

    def test_finalized_archify_views(self):
        verification = json.loads((ROOT / "verification.json").read_text(encoding="utf-8"))
        for view, filename in (("e19", "e19"), ("e20", "e20"),
                               ("e21", "e21-v2"), ("future", "future-v3")):
            with self.subTest(name=view):
                record = verification["views"][view]
                self.assertEqual(set(record["gates"].values()), {"pass"})
                spec = ROOT / "diagrams" / f"blueprint-{view}.json"
                html = ROOT / f"blueprint-{filename}.html"
                self.assertEqual(hashlib.sha256(spec.read_bytes()).hexdigest(), record["spec_sha256"])
                self.assertEqual(hashlib.sha256(html.read_bytes()).hexdigest(), record["html_sha256"])

    def test_preview_links(self):
        pages = [ROOT / "index.html", *sorted((ROOT / "design-demos").glob("*.html"))]
        self.assertEqual(len(pages), 4)
        for page in pages:
            with self.subTest(page=page.name):
                parser = Links()
                parser.feed(page.read_text(encoding="utf-8"))
                for tag, key, value in parser.refs:
                    if value.startswith(("http:", "https:", "mailto:", "javascript:", "data:")):
                        continue
                    parts = urlsplit(value)
                    target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
                    self.assertTrue(target.is_file(), f"{page}: missing {tag}[{key}]={value}")
                    if target == page and parts.fragment:
                        self.assertIn(parts.fragment, parser.ids)

    def test_truthful_labels(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8").lower()
        self.assertIn("timing claim failed", text)
        self.assertIn("not a pretrained lm", text)
        self.assertIn("not sealed", text)
        self.assertIn("not implemented", text)
        self.assertIn("blueprint-future-v3.html", text)
        self.assertIn("blueprint-e21-v2.html", text)
        self.assertNotIn('href="blueprint.html"', text)


if __name__ == "__main__":
    unittest.main()
