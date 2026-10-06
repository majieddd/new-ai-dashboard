"""Pinned October 6 goal/evidence readback; never promote preparation to a bot result."""
import hashlib
import html
import json
from pathlib import Path

STYLE = ".goal-table td{text-align:left;vertical-align:top;overflow-wrap:anywhere}.goal-table th{white-space:normal}.goal-table{min-width:690px}.goal-note{background:#151d32;border:1px solid #35415a;border-radius:14px;padding:20px}.goal-links{overflow-wrap:anywhere;word-break:break-word}"
CPU_REPORT = "NEW_AI_E20_CPU_CLOCK_PREFLIGHT_2026_10_06.md"
GPU_REPORT = "NEW_AI_E20_E21_GPU_RESERVATION_RIGHTS_RECONCILIATION_2026_10_06.md"
ENVELOPE_REPORT = "NEW_AI_E20_E21_GPU_COMMAND_ENVELOPE_RECOVERY_2026_10_06.md"
GOAL_TRACE = "NEW_AI_ORIGINAL_GOAL_REQUIREMENTS_TRACE_2026_10_06.md"
RECEIPT_KEYS = ("profile", "stream", "recheck", "integrated")


def _pinned(parent, item):
    path = parent / item["path"]
    if path.name != item["path"] or not path.is_file():
        raise ValueError("Missing or unsafe public evidence path")
    if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
        raise ValueError(f"Changed public evidence: {path.name}")
    return path


def verify(record, source, data):
    """Return derived test values only after checking exact report and receipt bytes."""
    goal = record["original_goal"]
    if (goal["runnable_real_language_bot_meeting_spec"], goal["e8_composition"],
            goal["e20_pretrained_language"], goal["e21_pretrained_language"]) != (
            False, "NOT_STARTED", "NOT_RUN", "NOT_RUN"):
        raise ValueError("The original bot goal cannot be promoted by this status update")
    e20 = record["e20_verified_preparation"]
    if (e20["source_revision"], e20["gpu_chargeable_balance"],
            e20["rights_cleared_articles"], e20["gpu_booking"]) != (
            "f9e3a7ad82916ef158397c2c42396201f32b4913", "UNKNOWN", 0, "HELD"):
        raise ValueError("E20 scope, accounting or rights changed")
    if set(e20["reports"]) != {"cpu", "gpu_accounting", "gpu_envelopes", "goal_trace"} or {
            v["path"] for v in e20["reports"].values()} != {CPU_REPORT, GPU_REPORT, ENVELOPE_REPORT, GOAL_TRACE}:
        raise ValueError("Missing October 6 report")
    for item in e20["reports"].values():
        _pinned(Path(source), item)
    cpu = json.loads(_pinned(Path(data), e20["cpu_receipt"]).read_text(encoding="utf-8"))
    readback = json.loads(_pinned(Path(data), e20["cpu_readback"]).read_text(encoding="utf-8"))
    if cpu["source_commit"] != e20["source_revision"] or readback["source_commit"] != e20["source_revision"]:
        raise ValueError("CPU source revision differs")
    commands = cpu["commands"]
    if (len(commands), [x["exit_code"] for x in commands]) != (4, [1, 0, 0, 0]):
        raise ValueError("CPU test/profile execution envelope changed")
    if not ("Ran 46 tests" in commands[0]["stderr"] and "FAILED (errors=1)" in commands[0]["stderr"]
            and "Ran 46 tests" in commands[1]["stderr"] and commands[1]["stderr"].rstrip().endswith("OK")):
        raise ValueError("CPU pass and initial environment error not demonstrated")
    rows = readback["rows"]
    if (not readback["all_hashes_and_counts_match"] or not readback["exact_before_after_audit_bytes"]
            or [r["arm"] for r in rows] != ["reference", "candidate"]
            or any((r["audit_events"], r["snapshots_checked"], r["reconstruction"]["scored_targets"])
                   != (775, 8, 329) for r in rows)
            or rows[0]["audit_sha256"] != rows[1]["audit_sha256"]):
        raise ValueError("Saved CPU audit readback does not establish the claimed reconstruction")
    measurements = cpu["measurements"]
    if any(measurements[r["arm"]]["audit_sha256"] != r["audit_sha256"] for r in rows):
        raise ValueError("CPU receipt and offline audit disagree")
    if set(e20["gpu_receipts"]) != set(RECEIPT_KEYS):
        raise ValueError("Four named GPU development receipts required")
    gpu = {}
    for key in RECEIPT_KEYS:
        gpu[key] = json.loads(_pinned(Path(data), e20["gpu_receipts"][key]).read_text(encoding="utf-8"))
        if not gpu[key]["scope"].startswith("DEV_SYNTHETIC_GPU") or gpu[key]["total_wall_seconds"] <= 0:
            raise ValueError("GPU receipt no longer a bounded synthetic development run")
    if any(gpu[key]["test_count"] != 41 for key in ("stream", "recheck", "integrated")):
        raise ValueError("Synthetic GPU development test counts changed")
    return {"reference_seconds": measurements["reference"]["wall_seconds"],
            "candidate_seconds": measurements["candidate"]["wall_seconds"],
            "audit_hash": rows[0]["audit_sha256"], "gpu": gpu,
            "source_revision": cpu["source_commit"]}


def _report(item, label):
    path = html.escape(item["path"], quote=True)
    return (f'<a href="https://github.com/majieddd/new-ai-dashboard/blob/main/source/{path}">'
            f'{html.escape(label)}</a> <code>SHA-256 {html.escape(item["sha256"])}</code>')


def home_section(record, derived):
    e20, goal = record["e20_verified_preparation"], record["original_goal"]
    rows = (
        ("Frozen small language core", "E20 tiny random-model CUDA/CPU stream and pinned SmolLM2-1.7B metadata only; pretrained adaptation NOT RUN.", "Not built as a real-language bot", "Cloud AI Generalist + Evaluation Scientist: verified model fit and frozen-core control"),
        ("Learned iterative energy refinement", "E21 five-seed synthetic CPU fixture and 70/71 public preparation suite (one no-corpus-read skip); independent code/control review and language study open.", "Not validated in language", "Energy Model Engineer + existing independent reviewer: close review, then eligible language test"),
        ("Novelty-triggered new parameters", "E18 input-only novelty fails on same-input/changed-label rules; E20 growth software is synthetic and tiny.", "No causal language demonstration", "Cloud lead + Evaluation Scientist: matched random/scheduled trigger control"),
        ("Retain old skills", "E19 real-text linear-classifier timing/accuracy gates FAILED; toy adapter retention does not prove LM retention.", "Not met", "Evaluation Scientist: fresh old/new held-out retention after a real adaptation run"),
        ("Matched-compute capability advantage", "E8 composition NOT STARTED; CPU synthetic one-window speed is not LM cost/capability.", "Not measured", "Generalist: E8 after viable components, with matched measured compute"),
        ("Ternary CPU + tiered memory", "Separate E4 substrate and E5 paging requirements; no validated real-bot efficiency/paging result.", "Separate, unmet", "Cloud lead: isolate kernel/memory benchmarks after core model path"),
    )
    body = "".join(f'<tr><th scope="row">{html.escape(spec)}</th><td>{html.escape(evidence)}</td>'
                   f'<td><strong>{html.escape(status)}</strong></td><td>{html.escape(next_step)}</td></tr>'
                   for spec, evidence, status, next_step in rows)
    return (f'<section id="goal"><span class="pill">Original model goal · delivery check</span>'
            f'<h2>Are we building the requested self-evolving language bot?</h2>'
            f'<p class="lede">As of {html.escape(record["as_of_utc"])}: <strong>No runnable real-language bot meeting the specification exists.</strong> '
            'The target is a frozen small language core whose learned energy is refined iteratively; sustained novelty '
            'instantiates trainable new parameters while older skills persist. The full system must beat a fine-tuning '
            'control at matched measured compute. Ternary CPU speed and VRAM/RAM/NVMe paging are separate engineering requirements.</p>'
            '<p class="small">On a narrow screen, swipe the table sideways to see every status and owner.</p>'
            '<div class="scroll"><table class="goal-table"><thead><tr><th>Specification</th><th>Implementation / test evidence</th>'
            f'<th>Status</th><th>Next milestone / owner</th></tr></thead><tbody>{body}</tbody></table></div>'
            f'<p class="goal-note"><strong>Next model-delivery checkpoint:</strong> {html.escape(goal["next_checkpoint"])}. '
            'Core model work: E20 actual pretrained-language adaptation/control, E21 learned-energy descent, and E8 composition. '
            'Rights, final custody, GPU accounting, software checks and website publication are prerequisites or supporting work—not the bot itself.</p>'
            '<p class="goal-links"><a href="progress/index.html#oct6-results">October 6 test results and source bytes</a> · '
            f'{_report(e20["reports"]["goal_trace"], "Original-goal source/requirements trace")} · '
            '<a href="progress/index.html#updates">Earlier preparation ledger</a> · '
            '<a href="data/status-2026-10-06.json" download>Current status manifest</a></p></section>')


def results_section(record, derived):
    e20 = record["e20_verified_preparation"]
    gpu = derived["gpu"]
    names = {"profile": "Two-layer profile", "stream": "4×2 stream", "recheck": "4×2 recheck", "integrated": "Integrated fastpath"}
    gpu_rows = "".join(
        f'<tr><th scope="row">{names[key]}</th><td>October 5 · tiny random/synthetic</td>'
        f'<td>{gpu[key]["total_wall_seconds"]:.3f}s in-process</td>'
        f'<td><a href="../data/{html.escape(e20["gpu_receipts"][key]["path"], quote=True)}">Raw JSON</a> · '
        f'<code>{html.escape(e20["gpu_receipts"][key]["sha256"])}</code></td></tr>'
        for key in RECEIPT_KEYS)
    return (f'<section id="oct6-results"><h2>October 6 · verified test results, not a language outcome</h2>'
            f'<p class="muted">As of {html.escape(record["as_of_utc"])}: a complete real-language bot is not runnable. '
            'Results below are public development checks. '
            'The E20 CPU test and saved-audit readback ran on synthetic token distributions at pinned source '
            f'<code>{html.escape(derived["source_revision"])}</code>; they do not load the pretrained model.</p>'
            '<div class="goal-note"><strong>E20 CPU stream + fastpath:</strong> 46/46 passed, zero skipped, after '
            'an initial 45-pass/one-environment-error attempt caused by missing TMPDIR. No source edits. '
            'Reference/candidate one-window timed spans: '
            f'<strong>{derived["reference_seconds"]:.9f}s / {derived["candidate_seconds"]:.9f}s</strong> '
            '(one pair, not a throughput claim). Identical saved audit SHA-256 '
            f'<code>{html.escape(derived["audit_hash"])}</code>; independent read-only reconstruction '
            'checked 775 events, eight snapshots and 329 scored targets per arm, exact saved bytes. '
            f'<a href="../data/{html.escape(e20["cpu_receipt"]["path"])}">Raw command/test receipt</a> '
            f'<code>{html.escape(e20["cpu_receipt"]["sha256"])}</code> · '
            f'<a href="../data/{html.escape(e20["cpu_readback"]["path"])}">Offline readback</a> '
            f'<code>{html.escape(e20["cpu_readback"]["sha256"])}</code>. '
            f'{_report(e20["reports"]["cpu"], "CPU preflight report")}</div>'
            '<div class="goal-note"><strong>E20 bounded GPU development receipts:</strong> four separate October 5 '
            'tiny random-model/synthetic executions, before the later study approval. Their clocks exclude portions '
            'of launch/tests or other reruns; the command-envelope recovery finds additional attempts. No pretrained '
            'language fit or chargeable exclusive GPU interval can be inferred. '
            '<p class="small">On a narrow screen, swipe sideways for the exact artifact hashes.</p>'
            '<div class="scroll"><table class="goal-table"><thead><tr><th>Run</th><th>Scope</th><th>Clock</th>'
            f'<th>Exact artifact</th></tr></thead><tbody>{gpu_rows}</tbody></table></div>'
            f'<p>{_report(e20["reports"]["gpu_accounting"], "Receipt/rights reconciliation")} · '
            f'{_report(e20["reports"]["gpu_envelopes"], "Command-envelope recovery")}</p></div>'
            '<div class="goal-note"><strong>E21:</strong> approved public preparation 70 passed / 71 discovered, '
            'one explicit no-corpus-read skip; independent nine new public tests 9/9, no skips. The pinned full '
            'suite log was parsed by QA, not independently rerun in that QA; 158 protected archive paths were '
            'unchanged. The separate code/control review remains with its existing reviewer; no snapshot release or '
            'pretrained-language result. <a href="../data/e21-approved-preparation-readback.json">Raw CPU readback</a> · '
            '<a href="https://github.com/majieddd/new-ai-dashboard/blob/main/source/E21_APPROVED_PREPARATION_REPORT_2026_10_06.md">Preparation report</a>.</div>'
            '<p class="goal-note"><strong>Current blockers:</strong> zero article entries rights-cleared; named '
            'independent final custodian and denied-read arrangement absent; new E21 704-QA proposal undecided; '
            'chargeable E20/E21 GPU balance <strong>UNKNOWN</strong> and booking <strong>HELD</strong> pending '
            'owner controller/opening-history decision. Approved caps are not being reopened. Next model checkpoint: '
            'measured E20 pretrained development fit and an independently reviewable frozen-core adaptation/control '
            'run after these prerequisites. Historical E19 <strong>FAILED</strong>; E20/E21 language and all nine '
            'official benchmark lanes <strong>NOT RUN</strong>; candidate r0.1 <strong>NOT FINAL-LOCKED</strong>.</p></section>')
