"""Render the reviewed October 6 development update, never a scientific verdict.

The reviewed report copies and two CPU receipts are pinned by byte hash. Report
links point to GitHub's Markdown viewer because Pages/Jekyll changes .md routes.
"""
import hashlib
import html
import json
from pathlib import Path

REPORT_LABELS = {
    "attractor": "Archived Attractor 1.1.0 reading",
    "principia": "Archived Principia II 1.1.0 reading",
    "harness": "Harness Engineering R1 application review",
    "e21_implementer": "E21 v0.2 implementer report",
    "e21_evaluator": "E21 independent contract review (SID-redacted public copy)",
}
RECEIPTS = {
    "command_receipt_sha256": "e21-public-v02-command.json",
    "independent_pinned_receipt_sha256": "e21-independent-pinned-suite.json",
}
OWNER_APPROVAL = "875101f24904db17a0c2b5f9bb0592d3a9077e01ce5be85590fb77dd5dcd7bd3"
DECISION_SHEET_SHA256 = "4aa92eda05be3bfd6e5c9d6ff2717207f1339996a6f93293bdbb5fec6e9a3b31"


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(source, data):
    source, data = Path(source), Path(data)
    record = json.loads((source / "status_update_2026_10_06.json").read_text(encoding="utf-8"))
    if record["schema"] != "new-ai-reviewed-development-update-v1":
        raise ValueError("Unknown review-update schema")
    expected = {"e19": "FAILED", "e20_language": "NOT_RUN_BLOCKED",
                "e21_language": "NOT_RUN_BLOCKED", "e22_validity": "REVIEW_OPEN",
                "official_benchmark_lanes": "9_NOT_RUN",
                "e9": "ASSIGNED_PROVIDER_RECOVERY_UNVERIFIED"}
    if record["scientific_status"] != expected:
        raise ValueError("Review update cannot change scientific status")
    if record["model_fixture"] != "PUBLIC_DEVELOPMENT_ONLY_QUERY_ONLY_MEMORY_SHORTCUT_OPEN":
        raise ValueError("Model-fixture validity must remain open")
    approval = record["approval"]
    if (approval["event_id"], approval["decision_sheet_sha256"], approval["e20_gpu_hour_ceiling"],
            approval["e20_development_hour_ceiling"], approval["e21_gpu_hour_ceiling"],
            approval["e21_development_hour_ceiling"], approval["custodian_named"],
            approval["language_outcomes_run"]) != (
            OWNER_APPROVAL, DECISION_SHEET_SHA256, 24, 1, 4, 1, False, False):
        raise ValueError("Approval scope or unfulfilled boundary changed")
    if set(record["reports"]) != set(REPORT_LABELS):
        raise ValueError("Missing or unexpected report")
    for key, report in record["reports"].items():
        path = source / report["path"]
        if path.name != report["path"] or _sha(path) != report["sha256"]:
            raise ValueError(f"Changed report: {key}")
    for key, filename in RECEIPTS.items():
        if _sha(data / filename) != record["e21"][key]:
            raise ValueError(f"Changed raw receipt: {filename}")
    return record


def home_section(record):
    date = html.escape(record["as_of_utc"])
    return (f'<section id="review-update"><h2>October 6 · reviewed evidence, not a new result</h2>'
            f'<p class="lede">As of {date}: archived-source reviews and the E21 public CPU contract review '
            'have advanced. The owner approved bounded E20/E21 preparation, not a study outcome. '
            'E19 stays <strong>FAILED</strong>; E20/E21 language and all nine official '
            'benchmark lanes remain <strong>NOT RUN</strong>. The E22 validity review remains open. '
            'A public memory-fixture shortcut can reconstruct answers without retrieval.</p>'
            '<p><a href="progress/index.html#updates">Read the bounded update, source reports and exact CPU receipts</a> · '
            '<a href="data/status-2026-10-06.json" download>Download the reviewed status manifest</a></p></section>')


def progress_section(record):
    links = []
    for key, label in REPORT_LABELS.items():
        item = record["reports"][key]
        # GitHub displays the source Markdown without relying on Jekyll's .md -> .html mapping.
        url = "https://github.com/majieddd/new-ai-dashboard/blob/main/source/" + item["path"]
        links.append(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a> '
                     f'— {html.escape(item["revision"])}; SHA-256 <code>{item["sha256"]}</code></li>')
    e21 = record["e21"]
    return (f'<section id="updates"><h2>October 6 · review and source-reading update</h2>'
            f'<p class="muted">As of {html.escape(record["as_of_utc"])}. '
            'These are source and public software reviews—not new model trials, accepted evaluator gates, '
            'current-version or reuse-rights clearance.</p>'
            '<div class="block"><h3>Scientific and instrument status</h3><ul>'
            '<li>E19 <strong>FAILED</strong>; E20 and E21 pretrained language studies <strong>NOT RUN</strong>. '
            'The last E20 public readiness checker reported BLOCKED/41 missing evidence predicates, not failed trials. '
            'That receipt predates the owner approval; authorization alone does not clear its remaining checks.</li>'
            '<li>Owner approval on October 6 authorizes preparation toward the full E20 SmolLM2-1.7B '
            'fresh-prose/grounded-QA proxy (NLL-only is a fallback), 192/64/512 human-verified QA targets '
            'subject to rights and lineage review, and separate exclusive GPU ceilings: E20 24h total '
            '(at most 1h development) before E21 4h total (at most 1h development), without overlap. '
            'No pretrained fit, GPU reservation, model/data download, license clearance or allowance '
            f'consumption is established by this review. Approval event <code>{OWNER_APPROVAL}</code>; '
            f'original decision-sheet SHA-256 <code>{DECISION_SHEET_SHA256}</code>.</li>'
            '<li>All nine official benchmark lanes <strong>NOT RUN</strong>. The five-seed memory-fixture '
            'answer can be reconstructed from query-only cues: public grader validity is <strong>open</strong>, '
            'not a model accuracy result. Repair stays with its existing owner.</li>'
            '<li>E22 remains a public development instrument; independent shortcut/validity review is open. '
            'E9 is assigned to Generalist, but its October 6 provider retry failed; execution recovery is unverified.</li>'
            '</ul></div><div class="block"><h3>E21 · different CPU test scopes</h3>'
            f'<p>Implementer source <code>{html.escape(e21["implementer_source_revision"])}</code> '
            f'(archived <code>{html.escape(e21["implementer_archive_revision"])}</code>): '
            f'<strong>{html.escape(e21["implementer_suite"])}</strong>. Independent evaluator: '
            f'<strong>{html.escape(e21["independent_suite"])}</strong> at the same pinned producing source; '
            'the one skipped test would read a historical AG News corpus. These counts are not contradictory. '
            'The independent review is a draft on a separate unchanged worktree, not a new training run.</p>'
            '<p>v0.2 fixes public stop-policy binding and integer-rank precision only as development software. '
            'Three boundaries remain in the existing code review: malformed aggregate rows, K0 nonfinite logits, '
            'and overflowing radial projection. Defect-characterization tests being green do not clear them. '
            'Matched token exposure did not match measured training work (energy/direct CPU fixture ≈1.84×); '
            'a prospective E21 QA/difficulty and scoring lock, rights/lineage review, measured fit, and '
            'independent final custody are still required. No separate-principal/off-host custodian has '
            'been named or denied-read canary check accepted; no final-data release is authorized. '
            'Five-seed consistency remains exploratory, not significance.</p>'
            '<p><a href="../data/e21-public-v02-command.json">Raw implementer command receipt</a> '
            '· <a href="../data/e21-independent-pinned-suite.json">Raw independent pinned-suite receipt</a> '
            '· <a href="../data/progress.json">Original five-seed fixture projection</a></p></div>'
            '<div class="block"><h3>Accepted, bounded reading closures</h3><p>Archived Attractor and '
            'Principia II have coordinate and citation-accounting closures, not validated physics/model claims; '
            'their current versions and complete reuse rights remain unverified. The Harness Engineering '
            'survey supports a proposed read-only kr8 handoff pilot, not model self-improvement. The pilot '
            'has not been run or approved.</p><ul>' + "".join(links) + '</ul>'
            '<p>The E21 independent public copy redacts exactly one same-user Windows SID; its displayed '
            f'original report SHA-256 is <code>{html.escape(record["reports"]["e21_evaluator"]["original_sha256"])}</code>. '
            'Other report copies preserve their source bytes. The source/report hashes are identities, '
            'not evidence of scientific truth.</p></div>'
            '<p><a href="../data/status-2026-10-06.json" download>Machine-readable status and report hashes</a> '
            '· <a href="https://github.com/majieddd/new-ai-dashboard/blob/main/source/status_update.py">Renderer and hash gate</a></p></section>')
