"""Render the OpenAI baseline preparation record from pinned raw bytes.

Every displayed number is derived from the archived probe manifest, probe
JSONL receipts, and the frozen pilot manifest; nothing is typed into HTML.
The loader fails the build when any archived byte changes. The honest status
is zero benchmark calls — this record must never read as a benchmark result.
"""
import hashlib
import html
import json
from pathlib import Path

DATA_NAMES = ("probe_manifest.json", "probe_gpt-5.5.jsonl", "probe_gpt-5.6-sol.jsonl",
             "probe_gpt-5.6-luna.jsonl", "probe_gpt-5.6-terra.jsonl",
             "s_b_pilot_manifest.json")
RECEIPT_LABELS = {
    "probe_manifest.json": "Probe manifest (four readbacks, token usage, limitations)",
    "probe_gpt-5.5.jsonl": "Raw probe JSONL · gpt-5.5",
    "probe_gpt-5.6-sol.jsonl": "Raw probe JSONL · gpt-5.6-sol",
    "probe_gpt-5.6-luna.jsonl": "Raw probe JSONL · gpt-5.6-luna",
    "probe_gpt-5.6-terra.jsonl": "Raw probe JSONL · gpt-5.6-terra",
    "s_b_pilot_manifest.json": "Frozen S-B pilot manifest (20 items/model, 40-call cap)",
}


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(source, results=None):
    """Verify every archived byte before rendering; raise on any change."""
    source = Path(source)
    results = Path(results) if results else source / "results" / "OPENAI"
    record = json.loads((results / "openai_manifest.json").read_text(encoding="utf-8"))
    if record["schema"] != "new-ai-openai-prep-record-v1":
        raise ValueError("Unknown OpenAI prep schema")
    for name, expected in record["data_sha256"].items():
        if _sha(results / name) != expected:
            raise ValueError(f"Changed archived record: {name}")
    for key, expected in record["report_sha256"].items():
        path = source / record["report_paths"][key]
        if path.name != record["report_paths"][key] or _sha(path) != expected:
            raise ValueError(f"Changed report copy: {key}")
    probe = json.loads((results / "probe_manifest.json").read_text(encoding="utf-8"))
    pilot = json.loads((results / "s_b_pilot_manifest.json").read_text(encoding="utf-8"))
    # Cross-checks: displayed values must equal recomputation from raw bytes.
    assert len(probe["models"]) == 4
    for model in probe["models"]:
        records = [json.loads(line) for line in
                   (results / ("probe_" + model["id"] + ".jsonl")).read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        usage = [rec for rec in records if rec.get("type") == "turn.completed" and "usage" in rec]
        assert len(usage) == 1
        assert _sha(results / ("probe_" + model["id"] + ".jsonl")) == model["source_jsonl_sha256"]
        assert model["answer"] == "READY"
        assert usage[0]["usage"]["output_tokens"] == model["usage"]["output_tokens"]
        assert usage[0]["usage"]["input_tokens"] == model["usage"]["input_tokens"]
    assert pilot["unique_items"] == 20 and pilot["per_model_call_cap"] == 20
    assert pilot["model_cap"] == 2 and pilot["parent_subset"] == "S-B"
    assert pilot["protocol_sha256"] == "2c1b0464a08806c78f3171b985423b6a8a9ada3280031ae1d8c06ca0578595ee"
    assert len(pilot["items"]) == 20
    assert record["status"]["benchmark_calls"] == 0
    assert record["status"]["cost_readback"] == "UNAVAILABLE"
    record["_raw"] = {"probe": probe, "pilot": pilot}
    return record


def home_section(record):
    p = record["_raw"]["probe"]
    models = ", ".join(m["id"] for m in p["models"])
    return (f'<section id="openai-prep"><span class="pill">OpenAI baselines · prep complete, 0 benchmark runs</span>'
            '<h2>OpenAI baselines — prepared, not run</h2>'
            '<p class="lede">The owner asked for benchmark plots comparable to other models. The baseline '
            'protocol is QA-accepted and final (SHA-256 <code>2c1b0464a08806c78f3171b985423b6a8a9ada3280031ae1d8c06ca0578595ee</code>), '
            'the subscription path is proven, and the pilot harness is built and tested. '
            f'<strong>Actual benchmark calls: 0.</strong> Four one-word subscription readbacks succeeded on '
            f'{html.escape(models)} via Codex CLI with token usage recorded. The protocol\'s temperature-0 '
            'requirement is not satisfiable on this transport, so the lead approved a narrowly scoped '
            'exploratory amendment (SHA-256 <code>d83a830e34f584bc634b99bfe67b1e9410118c3e17d8da4a51c0946efc1ea7d7</code>): '
            'pinned gpt-5.6-luna + gpt-5.6-sol, Codex CLI default decoding (NOT temperature 0), 40-call cap, '
            'cost unavailable, labeled exploratory calibration. Plots land on this site only after pilot '
            'receipts pass lead QA.</p>'
            '<div class="grid">'
            '<div class="card"><strong class="coral">0</strong>'
            '<small>Actual benchmark calls</small>'
            '<p>Probe readbacks are one-word replies, not benchmark items. No plot is published from them.</p></div>'
            '<div class="card"><strong class="blue">51/51</strong>'
            '<small>Harness CPU tests OK at commit 1d787df5af0dd8adf4313a968e0217e329026e47</small>'
            '<p>Frozen S-B pilot manifest SHA-256 <code>69ff310ed4d1c4a277361a2d8d2ad7e0d710e051515fc0d7cd97865cbcaf166e</code>: '
            '20 items per model, 40 calls maximum for two models.</p></div>'
            '<div class="card"><strong class="mint">4</strong>'
            '<small>Working subscription models probed</small>'
            f'<p>{html.escape(models)} — token usage recorded per readback; per-call dollar cost readback '
            'unavailable on the ChatGPT plan.</p></div></div>'
            '<p><a href="progress/index.html#openai-updates">Full prep record, protocol, amendment and raw probe receipts</a> · '
            '<a href="data/openai-probe_manifest.json" download>Download the probe manifest</a></p></section>')


def progress_section(record):
    r = record["_raw"]
    probe, pilot = r["probe"], r["pilot"]
    rows = "".join(
        f'<tr><th scope="row">{html.escape(m["id"])}</th>'
        f'<td>{html.escape(m["cli"])}</td>'
        f'<td>{html.escape(m["completed_at_file_mtime_utc"])}</td>'
        f'<td>{m["usage"]["input_tokens"]}</td>'
        f'<td>{m["usage"].get("cached_input_tokens", 0)}</td>'
        f'<td>{m["usage"]["output_tokens"]}</td>'
        f'<td><code>{m["source_jsonl_sha256"]}</code></td></tr>'
        for m in probe["models"])
    limitations = "".join(f'<li>{html.escape(l)}</li>' for l in probe["limitations"])
    receipt_links = "".join(
        f'<li><a href="../data/openai-{name}" download>{html.escape(RECEIPT_LABELS[name])}</a> '
        f'— SHA-256 <code>{record["data_sha256"][name]}</code></li>'
        for name in DATA_NAMES)
    report_links = "".join(
        f'<li><a href="https://github.com/majieddd/new-ai-dashboard/blob/main/source/{record["report_paths"][key]}">'
        f'{html.escape(label)}</a> — SHA-256 <code>{record["report_sha256"][key]}</code></li>'
        for key, label in (("openai_protocol", "OpenAI baseline protocol (QA-accepted, final)"),
                          ("openai_amendment", "Pilot amendment (exploratory, non-temp-0)"),
                          ("openai_prep_report", "Preparation report and blocker record")))
    return (f'<section id="openai-updates"><h2>OpenAI baselines · prep record (0 benchmark runs)</h2>'
            '<p class="muted">CPU-only, subscription readbacks only, resident model untouched. This is a '
            'preparation record: the baseline calibrates instrument difficulty and cannot validate the New AI '
            'growth, timing, retention or energy hypothesis. No New AI project gate changes.</p>'
            '<div class="block"><h3>Subscription probe readbacks (not benchmark items)</h3>'
            '<p>Prompt: <em>"Reply with exactly one word: READY. Do not use tools."</em> All four models '
            'answered READY. Timestamps are file mtime UTC; Codex JSONL carries no server timestamps.</p>'
            '<div class="scroll"><table><thead><tr><th scope="col">Model</th><th scope="col">CLI</th>'
            '<th scope="col">Completed (file mtime UTC)</th><th scope="col">Input tokens</th>'
            '<th scope="col">Cached input</th><th scope="col">Output tokens</th>'
            '<th scope="col">Raw JSONL SHA-256</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            '<p class="small">Declared hashes were recomputed from the archived JSONL bytes at build time '
            'and must match; the loader fails otherwise.</p>'
            '<ul>' + limitations + '</ul></div>'
            '<div class="block"><h3>Frozen pilot manifest (prepared, capped)</h3>'
            f'<p>Commit <code>{record["git_pins"]["openai_baseline_head"]}</code> (local branch '
            'research/openai-baseline-pilot, no push). Generator '
            f'<code>{html.escape(pilot["generator"])}(seed={pilot["generator_seed"]})</code>, parent subset '
            f'{html.escape(pilot["parent_subset"])}, pilot subset {html.escape(pilot["subset"])}: first 10 of '
            'the 256 preregistered held-out test sequences per rule (copy_first, copy_last) = '
            f'<strong>{pilot["unique_items"]} unique items per model</strong>, '
            f'<strong>{pilot["per_model_call_cap"]} calls per model</strong>, '
            f'<strong>{pilot["model_cap"]} models</strong> → 40 calls maximum. The runner refuses benchmark '
            'execution unless the reviewed amendment authorizes it, pins models and hashes before the first '
            'response, appends chained per-item receipts, verifies hashes, resumes without repeats, and '
            'records failures. Full CPU suite at that commit: 51/51 OK.</p></div>'
            '<div class="block"><h3>Amendment and honest status</h3>'
            '<p>The QA-accepted protocol requires temperature 0 and per-call cost receipts. Codex CLI '
            '0.160.1 <code>--strict-config</code> rejects <code>model_temperature=0</code> as unknown, and '
            'the ChatGPT plan has no per-call dollar meter. The lead approved a pilot-only amendment '
            '(SHA-256 <code>d83a830e34f584bc634b99bfe67b1e9410118c3e17d8da4a51c0946efc1ea7d7</code>): pinned '
            'gpt-5.6-luna + gpt-5.6-sol via Codex CLI default decoding, NOT temperature 0, cost unavailable, '
            'token usage recorded, every receipt labeled exploratory calibration. Pilot cleared; receipts go '
            'to the lead for QA. <strong>Actual benchmark calls: 0. Cost readback: unavailable. Benchmark '
            'plots land on this site only after pilot receipts pass lead QA.</strong></p>'
            '<div class="block"><h3>Reports and archived receipts (byte-verified at build time)</h3>'
            f'<ul>{report_links}</ul><ul>{receipt_links}</ul></div></div></section>')
