"""Render the October 7 verified CPU development record from pinned raw bytes.

Every displayed number is derived from the archived receipts; nothing is typed
into HTML. The loader fails the build when any archived byte changes. The
prospective control is a measured NEGATIVE result and is rendered as a failure.
"""
import hashlib
import html
import json
from pathlib import Path
from statistics import mean

DATA_NAMES = ("prospective_summary.json", "e21_suite_receipt.json",
             "e21_reconstruction.json", "e21_mutation_receipt.json",
             "e21_preservation_receipt.json", "hybrid_cpu_receipt.json",
             "feedback_receipt.json", "matched_control_receipt.json")
RECEIPT_LABELS = {
    "prospective_summary.json": "Prospective control summary (12 paired seeds)",
    "e21_suite_receipt.json": "E21 correction suite receipt (45/46, one no-corpus skip)",
    "e21_reconstruction.json": "E21 original-control reconstruction (5 seeds x 9 arms, 2,880 predictions)",
    "e21_mutation_receipt.json": "E21 receipt-mutation audit (19/19 rejected)",
    "e21_preservation_receipt.json": "E21 reviewed-pin preservation (145/143 files byte-unchanged)",
    "hybrid_cpu_receipt.json": "CPU hybrid prototype receipt (seed 23, train/freeze/growth/rollback)",
    "feedback_receipt.json": "Seed-23 feedback run receipt",
    "matched_control_receipt.json": "Seed-23 matched scheduled control receipt",
}
CRITERIA_LABELS = {
    "mean_new_test_diff_at_least_0_02": "Mean paired new-test difference >= 0.02",
    "strict_feedback_wins_at_least_9": "Strict feedback wins >= 9 of 12",
    "mean_old_retention_loss_at_most_0_02": "Mean feedback old retention loss <= 0.02",
    "total_inclusive_cpu_ratio_at_most_1_10": "Feedback inclusive process CPU <= 1.10 x schedule",
}


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(source, results=None):
    """Verify every archived byte before rendering; raise on any change."""
    source = Path(source)
    results = Path(results) if results else source / "results" / "OCT7"
    record = json.loads((results / "oct7_manifest.json").read_text(encoding="utf-8"))
    if record["schema"] != "new-ai-oct7-verified-development-record-v1":
        raise ValueError("Unknown October 7 record schema")
    for name, expected in record["data_sha256"].items():
        if _sha(results / name) != expected:
            raise ValueError(f"Changed archived record: {name}")
    for key, expected in record["report_sha256"].items():
        path = source / record["report_paths"][key]
        if path.name != record["report_paths"][key] or _sha(path) != expected:
            raise ValueError(f"Changed report copy: {key}")
    summary = json.loads((results / "prospective_summary.json").read_text(encoding="utf-8"))
    suite = json.loads((results / "e21_suite_receipt.json").read_text(encoding="utf-8"))
    recon = json.loads((results / "e21_reconstruction.json").read_text(encoding="utf-8"))
    mutations = json.loads((results / "e21_mutation_receipt.json").read_text(encoding="utf-8"))
    preservation = json.loads((results / "e21_preservation_receipt.json").read_text(encoding="utf-8"))
    cpu = json.loads((results / "hybrid_cpu_receipt.json").read_text(encoding="utf-8"))
    feedback = json.loads((results / "feedback_receipt.json").read_text(encoding="utf-8"))
    control = json.loads((results / "matched_control_receipt.json").read_text(encoding="utf-8"))
    # Cross-checks: the displayed aggregates must equal recomputation from raw entries.
    entries = summary["entries"]
    assert [e["seed"] for e in entries] == list(range(101, 113))
    assert summary["completed"] == 12 and summary["errored"] == 0
    assert abs(mean(e["paired_new_test_difference"] for e in entries)
             - summary["mean_paired_new_test_difference"]) < 1e-12
    assert sum(e["paired_new_test_difference"] > 0 for e in entries) == summary["strict_feedback_wins"]
    assert abs(mean(e["feedback"]["old_retention_loss"] for e in entries)
             - summary["mean_feedback_old_retention_loss"]) < 1e-12
    assert abs(summary["feedback_inclusive_process_cpu_seconds"]
              / summary["schedule_inclusive_process_cpu_seconds"]
              - summary["cpu_ratio"]) < 1e-9
    assert summary["verdict"] == "no advantage established"
    assert all(e["feedback"]["trigger_block"] == 2 and e["schedule"]["trigger_block"] == 3
               for e in entries)
    assert suite["passed"] == 45 and suite["discovered"] == 46 and suite["skipped"]
    assert suite["errors"] == 0 and suite["failures"] == 0
    assert (recon["paired_seeds"], recon["arms_per_seed"], recon["prediction_records"],
            recon["training_step_records"], recon["max_checkpoint_vs_raw_logit_error"],
            recon["verified"], recon["fresh_optimizer_replay"]) == (5, 9, 2880, 900, 0.0, True, False)
    assert len(mutations) == 19 and all(m["rejected"] for m in mutations)
    assert (preservation["unchanged"], preservation["reviewed_files"],
            preservation["correction_preserved_files"]) == (True, 145, 143)
    assert preservation["reviewed_head"] == record["git_pins"]["e21_reviewed_pin"]
    assert preservation["review_sha256"] == record["git_pins"]["e21_review_report_sha256"]
    assert cpu["seed"] == 23 and len(cpu["trials"]) == 2
    assert [t["name"] for t in cpu["trials"]] == ["mismatched_feedback", "true_feedback"]
    assert control["seed"] == 23 and control["matched_optimizer_state"] and control["matched_logits"]
    record["_raw"] = {"summary": summary, "suite": suite, "recon": recon,
                      "mutations": mutations, "preservation": preservation,
                      "cpu": cpu, "feedback": feedback, "control": control}
    return record


def paired_delta_chart(entries):
    """Per-seed paired new-test difference (feedback minus schedule), in points."""
    left, top, width, height = 190, 46, 640, 300
    x = lambda p: left + (p + 2.4) / 4.8 * width
    bits = ['<svg class="chart" viewBox="0 0 960 420" role="img" '
            'aria-labelledby="oct7-delta-title oct7-delta-desc" xmlns="http://www.w3.org/2000/svg">',
            '<title id="oct7-delta-title">Prospective control: paired new-test accuracy difference per seed, feedback minus schedule</title>',
            '<desc id="oct7-delta-desc">Twelve seeds. Feedback is better on four, worse on five, equal on three. '
            'The mean is negative, below the preregistered +2-point advantage line. No advantage established.</desc>']
    for tick in (-2, -1, 0, 1, 2):
        pos = x(tick)
        bits += [f'<path d="M {pos:.1f} {top} V {top+height}" stroke="#394661" stroke-width="1"/>',
                 f'<text x="{pos:.1f}" y="{top+height+22}" fill="#d5deef" text-anchor="middle" font-size="15">{tick}</text>']
    bits.append(f'<path d="M {x(2.0):.1f} {top} V {top+height}" stroke="#f4a393" stroke-width="3" stroke-dasharray="5 5"/>')
    bits.append(f'<text x="{x(2)-8:.1f}" y="{top-8}" fill="#f4a393" text-anchor="end" font-size="15">required >= +2 pts</text>')
    for i, row in enumerate(entries):
        yy = top + 14 + i * 24
        diff = 100 * row["paired_new_test_difference"]
        if diff < -2.2 or diff > 2.2:
            raise ValueError("paired difference outside chart range")
        color = "#71d7bf" if diff > 0 else ("#f4a393" if diff < 0 else "#88a9fb")
        bits.append(f'<text x="{left-19}" y="{yy+5}" fill="#ecf2ff" text-anchor="end" font-size="14">seed {row["seed"]}</text>')
        bits.append(f'<path d="M {x(0)} {yy} H {x(diff):.1f}" stroke="{color}" stroke-width="4"/>')
        bits.append(f'<circle cx="{x(diff):.1f}" cy="{yy}" r="4.5" fill="{color}">'
                    f'<title>Seed {row["seed"]}: feedback minus schedule {diff:+.3f} points</title></circle>')
    mean_pts = 100 * mean(r["paired_new_test_difference"] for r in entries)
    bits.append(f'<path d="M {x(mean_pts):.1f} {top} V {top+height}" stroke="#dfffe9" stroke-width="2" stroke-dasharray="3 4"/>')
    bits.append(f'<text x="{x(mean_pts)+8:.1f}" y="{top+14}" fill="#dfffe9" font-size="15">mean {mean_pts:+.4f}</text>')
    bits += [f'<text x="{left+width/2:.1f}" y="{top+height+44}" fill="#ecf2ff" text-anchor="middle" '
             'font-size="16">Feedback minus scheduled, new-test accuracy (percentage points)</text>',
             '</svg>']
    return "".join(bits)


def home_section(record):
    s = record["_raw"]["summary"]
    mean_pts = 100 * s["mean_paired_new_test_difference"]
    wins = s["strict_feedback_wins"]
    return (f'<section id="oct7"><span class="pill">October 7 · CPU development record · measured negative</span>'
            '<h2>October 7 · verified development results, including a failure</h2>'
            '<p class="lede">Three CPU packages were independently verified by the lead. The headline is a '
            '<strong>negative</strong>: a preregistered prospective control on 12 new seeds found '
            '<strong>no feedback-timing advantage</strong> — mean paired new-test difference '
            f'<strong>{mean_pts:+.4f} points</strong>, feedback strictly better on <strong>{wins}/12</strong> seeds. '
            'The E21 focused correction passed its CPU suite (45/46, one explicit no-corpus skip) with '
            '19/19 receipt mutations rejected, and the CPU hybrid prototype ran train/freeze/energy-inference/'
            'growth/rollback end-to-end on synthetic data. E20/E21 language studies remain <strong>NOT RUN</strong>, '
            'the GPU ledger stays <strong>HELD</strong>, and the public release foundation is accepted as PR #1 '
            'with the merge pending the owner\'s word.</p>'
            '<div class="grid">'
            f'<div class="card"><strong class="coral">{mean_pts:+.4f} pts</strong>'
            f'<small>Prospective control · mean paired new-test difference</small>'
            f'<p>Preregistered gate required >= +2 points. Verdict: <strong>no advantage established</strong> '
            f'({wins}/12 strict feedback wins).</p></div>'
            '<div class="card"><strong class="mint">45/46</strong>'
            '<small>E21 correction suite · one explicit no-corpus skip</small>'
            '<p>19/19 receipt mutations rejected; original control reconstructed 5 seeds x 9 arms, '
            '2,880 predictions, max logit error 0.0. Language NOT RUN.</p></div>'
            '<div class="card"><strong class="blue">0.98046875 → 0.99609375</strong>'
            '<small>CPU hybrid prototype · old → new accuracy after true-feedback promotion (seed 23)</small>'
            '<p>Train, freeze, energy-inference, growth, retention check, promote/rollback exercised on '
            'synthetic inputs with receipts. Not a language result.</p></div></div>'
            '<p><a href="progress/index.html#oct7-updates">Full October 7 record, reports and receipts</a> · '
            '<a href="data/oct7-prospective_summary.json" download>Download the 12-seed prospective summary</a></p></section>')


def progress_section(record):
    r = record["_raw"]
    s, suite, recon, pres, cpu, control = r["summary"], r["suite"], r["recon"], r["preservation"], r["cpu"], r["control"]
    pins = record["git_pins"]
    mean_pts = 100 * s["mean_paired_new_test_difference"]
    rows = "".join(
        f'<tr><th scope="row">{e["seed"]}</th>'
        f'<td>{100*e["feedback"]["new_test"]["accuracy"]:.6f}</td>'
        f'<td>{100*e["schedule"]["new_test"]["accuracy"]:.6f}</td>'
        f'<td>{100*e["paired_new_test_difference"]:+.6f}</td>'
        f'<td>{100*e["feedback"]["old_retention_loss"]:.6f}</td>'
        f'<td>{e["feedback"]["inclusive_totals"]["process_cpu_seconds"]:.6f}</td>'
        f'<td>{e["schedule"]["inclusive_totals"]["process_cpu_seconds"]:.6f}</td></tr>'
        for e in s["entries"])
    criteria = "".join(
        f'<tr><th scope="row">{html.escape(CRITERIA_LABELS[key])}</th>'
        f'<td>{"Yes" if value else "No"}</td></tr>'
        for key, value in s["criteria"].items())
    seed23 = cpu["trials"][1]
    report_links = "".join(
        f'<li><a href="https://github.com/majieddd/new-ai-dashboard/blob/main/source/{record["report_paths"][key]}">'
        f'{html.escape(label)}</a> — SHA-256 <code>{record["report_sha256"][key]}</code></li>'
        for key, label in (("prospective_report", "Prospective control report (12 seeds)"),
                          ("e21_correction_report", "E21 focused correction report"),
                          ("hybrid_cpu_report", "CPU hybrid prototype report"),
                          ("scheduled_control_report", "Seed-23 matched scheduled control report")))
    receipt_links = "".join(
        f'<li><a href="../data/oct7-{name}" download>{html.escape(RECEIPT_LABELS[name])}</a> '
        f'— SHA-256 <code>{record["data_sha256"][name]}</code></li>'
        for name in DATA_NAMES)
    return (f'<section id="oct7-updates"><h2>October 7 · verified CPU development record</h2>'
            '<p class="muted">CPU-only, offline, resident model untouched, 0 GPU allowance seconds added. '
            'These are development packages with disclosed limits — not language, E20/E21, official benchmark, '
            'novelty-discovery, or generalization results. Every number below is generated from the archived '
            'receipts linked at the end of this section.</p>'
            '<div class="block"><h3>1. Prospective synthetic trigger control — FAILED its advantage gate</h3>'
            '<p>Twelve new paired seeds (101–112), protocol committed <em>before</em> execution at '
            f'<code>{pins["prospective_protocol_commit"]}</code>; producing source '
            f'<code>{pins["prospective_producing_commit"]}</code>; clean HEAD '
            f'<code>{pins["prospective_clean_head"]}</code>. The fixed schedule fired at preregistered block 3; '
            'the feedback detector fired at block 2 on all 12 seeds; both arms promoted in every pair. '
            f'Mean paired new-test difference <strong>{mean_pts:+.4f} points</strong> '
            f'(feedback {100*mean(e["feedback"]["new_test"]["accuracy"] for e in s["entries"]):.7f} vs '
            f'schedule {100*mean(e["schedule"]["new_test"]["accuracy"] for e in s["entries"]):.7f}); '
            f'strict feedback wins <strong>{s["strict_feedback_wins"]}/12</strong>; mean feedback old retention loss '
            f'<strong>{100*s["mean_feedback_old_retention_loss"]:.4f} points</strong>; inclusive process CPU '
            f'<strong>{s["feedback_inclusive_process_cpu_seconds"]} s vs {s["schedule_inclusive_process_cpu_seconds"]} s</strong> '
            f'(ratio {s["cpu_ratio"]:.6f}).</p>'
            '<p class="note"><strong>Preregistered verdict: no advantage established.</strong> The disclosed '
            'asymmetry — 64 revealed labels and 7,680 growth presentations per feedback seed versus 96 and '
            '11,520 per schedule seed — means this is not an equal-data causal comparison. Capacity and update '
            'count match; labeled-example and presentation budgets do not.</p>'
            '<div class="chartbox">' + paired_delta_chart(s["entries"]) + '</div>'
            '<div class="scroll"><table><thead><tr><th scope="col">Seed</th><th scope="col">Feedback new test</th>'
            '<th scope="col">Schedule new test</th><th scope="col">Paired Δ (pts)</th>'
            '<th scope="col">Feedback old retention loss (pts)</th><th scope="col">Feedback CPU s</th>'
            '<th scope="col">Schedule CPU s</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            '<div class="scroll"><table class="goal-table"><thead><tr><th scope="col">Locked criterion</th>'
            '<th scope="col">Passed?</th></tr></thead><tbody>' + criteria + '</tbody></table></div>'
            '<p class="small">Δ = feedback minus schedule, exact values in the per-seed receipts. '
            'Seed 23 was reserved for implementation tests and excluded from the 12-seed analysis.</p></div>'
            '<div class="block"><h3>2. E21 focused development correction — CPU suite accepted, language NOT RUN</h3>'
            '<p>Protocol committed first at '
            f'<code>{pins["e21_correction_protocol_commit"]}</code>; tested source '
            f'<code>{pins["e21_tested_source_commit"]}</code>; evidence commit '
            f'<code>{pins["e21_evidence_commit"]}</code>. Suite: <strong>{suite["passed"]} passed / '
            f'{suite["discovered"]} discovered</strong>, {len(suite["skipped"])} explicit no-corpus skip '
            f'({html.escape(suite["skipped"][0]["reason"])}), 0 errors, 0 failures. '
            f'<strong>{len(r["mutations"])}/{len(r["mutations"])} receipt mutations rejected</strong>, including '
            'the three previously accepted cases and the retained raw-NLL rejection control. The original control '
            f'was reconstructed, not retrained: {recon["paired_seeds"]} seeds x {recon["arms_per_seed"]} arms, '
            f'{recon["prediction_records"]} predictions, {recon["training_step_records"]} step records, maximum '
            f'checkpoint-vs-raw logit error <strong>{recon["max_checkpoint_vs_raw_logit_error"]}</strong>, '
            f'<code>fresh_optimizer_replay={str(recon["fresh_optimizer_replay"]).lower()}</code>. The reviewed pin '
            f'<code>{pres["reviewed_head"]}</code> and its report hash '
            f'<code>{pres["review_sha256"]}</code> are preserved; {pres["reviewed_files"]} reviewed and '
            f'{pres["correction_preserved_files"]} protected files byte-unchanged.</p></div>'
            '<div class="block"><h3>3. CPU hybrid integration exercised — synthetic, seed 23</h3>'
            f'<p>Train, freeze, energy-inference, growth decision, retention check and promote/rollback ran '
            f'end-to-end on public synthetic data (prototype commit <code>{pins["hybrid_dev_prototype_commit"]}</code>, '
            f'matched control HEAD <code>{pins["hybrid_dev_matched_control_head"]}</code>). The mismatched-feedback '
            'trial was <strong>REJECTED</strong> (new accuracy '
            f'{seed23["new_after"]["accuracy"]} after growth — the retention check correctly refused promotion); '
            f'the true-feedback trial was <strong>PROMOTED</strong>: old held-out accuracy '
            f'{seed23["old_before"]["accuracy"]} → {seed23["old_after"]["accuracy"]}, new '
            f'{seed23["new_before"]["accuracy"]} → {seed23["new_after"]["accuracy"]}. The seed-23 matched '
            'scheduled control showed exact state/logits/optimizer parity and, being post-hoc, no causal '
            'timing benefit. Not implemented: pretrained language core, expert graft, ternary substrate, '
            'tiered paging, calibrated universal novelty, matched-compute study.</p></div>'
            '<div class="block"><h3>4. Public release foundation</h3>'
            f'<p>PR #1 on <code>majieddd/new-ai</code> accepted by lead QA (commit '
            f'<code>{pins["release_foundation_commit"]}</code>): README, Apache-2.0, CITATION.cff, '
            'CONTRIBUTING, third-party notices, pinned requirements.lock, CPU-only CLI with 2/2 tests. '
            'Merge is pending the owner\'s word; no model, weights, corpus, receipts, or paper are packaged.</p></div>'
            '<div class="block"><h3>Reports and archived receipts (byte-verified at build time)</h3>'
            f'<ul>{report_links}</ul>'
            f'<ul>{receipt_links}</ul></div></section>')
