"""Build the proposed, explicitly unscored New AI benchmark dashboard."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "benchmark_suite_v0_1.json"
TEMPLATE = ROOT / "benchmark_preview_template.html"
OUTPUT = ROOT / "research-site" / "benchmarks"
REQUIRED = ("id", "group", "title", "subtitle", "measures", "method", "grade", "controls", "status")
GROUPS = {"BENCHMARKS", "AGENT TASKS"}


def validate(suite: dict) -> None:
    if suite.get("schema") != "new-ai-benchmark-program-proposal-v0.1":
        raise ValueError("Unexpected benchmark schema")
    if suite.get("status") != "proposal_not_approved" or suite.get("official_results") != []:
        raise ValueError("This preview cannot publish an approved result or nonempty official score")
    tests = suite.get("tests")
    if not isinstance(tests, list) or not tests:
        raise ValueError("The proposal needs test definitions")
    seen = set()
    for test in tests:
        if not isinstance(test, dict) or any(not isinstance(test.get(key), str) or not test[key] for key in REQUIRED):
            raise ValueError("Every test requires a nonempty method, grade, controls and metadata")
        if test["status"] != "not_run" or test["group"] not in GROUPS:
            raise ValueError("A proposed suite cannot display a scored or unknown test state")
        if test["id"] in seen or not test["id"].replace("-", "").isalnum():
            raise ValueError("Test IDs must be unique and alphanumeric")
        seen.add(test["id"])


def render_card(test: dict) -> str:
    esc = lambda key: html.escape(test[key], quote=True)
    definitions = "".join(
        f"<dt>{html.escape(label)}</dt><dd>{esc(field)}</dd>"
        for field, label in (("measures", "Measures"), ("method", "Method"),
                             ("grade", "Scoring"), ("controls", "Controls"))
    )
    return (f'<article class="card" id="test-{esc("id")}" data-group="{esc("group")}">'
            f'<div class="card-top"><span class="group">{esc("group")}</span>'
            '<span class="state">NOT RUN</span></div>'
            f'<h3>{esc("title")}</h3><p class="subtitle">{esc("subtitle")}</p>'
            '<div class="score"><span>Official model result</span><b>— · No receipt</b></div>'
            f'<details><summary>See method &amp; grading</summary><dl>{definitions}</dl></details></article>')


def build(out: Path | None = None) -> tuple[Path, str]:
    source = MANIFEST.read_bytes()
    suite = json.loads(source)
    validate(suite)
    sha = hashlib.sha256(source).hexdigest()
    counts = {group: sum(test["group"] == group for test in suite["tests"]) for group in GROUPS}
    replacements = {
        "__TOTAL__": str(len(suite["tests"])),
        "__BENCH_COUNT__": str(counts["BENCHMARKS"]),
        "__AGENT_COUNT__": str(counts["AGENT TASKS"]),
        "__CARDS__": "\n".join(map(render_card, suite["tests"])),
        "__SUITE_SHA__": sha,
    }
    page = TEMPLATE.read_text(encoding="utf-8")
    for key, value in replacements.items():
        if key not in page:
            raise ValueError(f"Missing template placeholder: {key}")
        page = page.replace(key, value)
    if "__CARDS__" in page or "__SUITE_SHA__" in page:
        raise ValueError("Unrendered template marker")
    output = Path(out) if out else OUTPUT
    output.mkdir(parents=True, exist_ok=True)
    (output / "suite.json").write_bytes(source)
    # GitHub Pages processes .md into .html, so keep this exact source as .txt.
    (output / "protocol.txt").write_bytes((ROOT / "BENCHMARK_PREVIEW_PROTOCOL.md").read_bytes())
    dest = output / "index.html"
    dest.write_text(page, encoding="utf-8")
    return dest, sha


if __name__ == "__main__":
    path, digest = build()
    print(f"Built {path} | manifest SHA-256 {digest} | official model results: 0")
