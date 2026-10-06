"""Build a candid, self-contained New AI results site from raw experiment files.

No network, templates, JS frameworks, or hand-entered outcome numbers. Charts
compare only arms on the same test; historical experiments stay separate.
"""
import argparse
import html
import json
import shutil
from pathlib import Path
from statistics import mean
from progress_site import home_section, render as render_progress
from status_update import home_section as home_review_update, load as load_review_update, progress_section as review_progress_section
from goal_status import STYLE as GOAL_STYLE, home_section as goal_home_section, results_section as goal_results_section
from benchmark_preview import build as build_benchmark

HERE = Path(__file__).resolve().parent
ARMS = (("self_assembly", "Readout-only (historically named self-assembly)", "#71d7bf"),
        ("full_finetune", "Full fine-tune", "#f4a393"),
        ("frozen_baseline", "Frozen", "#88a9fb"))
E19_ARMS = (("frozen", "Frozen", "#88a9fb"),
            ("random", "Random timing", "#f5cc86"),
            ("scheduled", "Scheduled adapter", "#71d7bf"),
            ("feedback", "Feedback adapter", "#c9f6d8"),
            ("full_finetune", "Full fine-tune", "#f4a393"))
PUBLISHED_SUMMARIES = ("E15", "E16", "E17", "E18", "E19")


def load_results(source=HERE):
    e15 = json.loads((source / "results/E15/summary.json").read_text(encoding="utf-8"))
    e16 = json.loads((source / "results/E16/summary.json").read_text(encoding="utf-8"))
    e17 = json.loads((source / "results/E17/summary.json").read_text(encoding="utf-8"))
    e18 = json.loads((source / "results/E18/summary.json").read_text(encoding="utf-8"))
    e14 = [json.loads(p.read_text(encoding="utf-8"))
           for p in sorted((source / "results/E14").glob("*_e14.jsonl"))]
    assert len(e15["history"]) == 10 and len(e14) == 5
    assert len(e16["runs"]) == len(e17["runs"]) == 5
    assert [r["seed"] for r in e18["runs"]] == [31, 37, 41, 43, 47]
    assert set(r["seed"] for r in e16["runs"]).isdisjoint(r["seed"] for r in e17["runs"])
    assert [r["round"] for r in e15["history"]] == list(range(1, 11))
    return e14, e15, e16, e17, e18


def chart(rounds):
    # One chart with one scale; plotted composite accuracy from raw E15 summary.
    W, H, left, top, pw, ph = 980, 420, 66, 42, 878, 304
    x = lambda i: left + i * pw / 9
    y = lambda p: top + ph * (1 - p / 40)
    bits = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" '
            'aria-labelledby="chart-title chart-desc" xmlns="http://www.w3.org/2000/svg">',
            '<title id="chart-title">E15 composite accuracy by trial round and model configuration</title>',
            '<desc id="chart-desc">Ten rounds, three configurations. Frozen exceeds the readout-only and full fine-tune arms in all ten rounds. This single-seed pilot does not show progressive improvement.</desc>']
    for t in range(0, 41, 10):
        yy = y(t)
        bits += [f'<path d="M {left} {yy:.1f} H {left+pw}" stroke="#35415a" stroke-width="1"/>',
                 f'<text x="{left-13}" y="{yy+5:.1f}" fill="#aeb9d1" font-size="15" text-anchor="end">{t}</text>']
    for i in range(10):
        bits.append(f'<text x="{x(i):.1f}" y="{top+ph+29}" text-anchor="middle" fill="#aeb9d1" font-size="14">{i+1}</text>')
    for key, label, color in ARMS:
        values = [r["arms"][key]["composite"] * 100 for r in rounds]
        coords = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
        bits.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
        for i, v in enumerate(values):
            bits.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="5" fill="{color}"><title>{html.escape(label)} round {i+1}: {v:.2f}%</title></circle>')
    bits += [f'<text x="{left+pw/2:.1f}" y="{H-10}" fill="#aeb9d1" text-anchor="middle" font-size="15">Trial round</text>',
             '<text transform="translate(17,209) rotate(-90)" fill="#aeb9d1" text-anchor="middle" font-size="15">Composite test accuracy (%)</text>',
             '</svg>']
    return "".join(bits)


def summarise(e14, e15, e16, e17, e18):
    rounds = e15["history"]
    wins = sum(r["arms"]["self_assembly"]["composite"] > r["arms"]["frozen_baseline"]["composite"] for r in rounds)
    retention_pass = sum(r["arms"]["self_assembly"]["retention_drop_pts"] <= 2 for r in rounds)
    means = {key: 100 * mean(r["arms"][key]["composite"] for r in rounds) for key, _, _ in ARMS}
    ret = {key: mean(r["arms"][key]["retention_drop_pts"] for r in rounds) for key, _, _ in ARMS}
    def score(d, arm, metric):
        return 100 * mean(r["arms"][arm][metric] for r in d["runs"])
    def seconds(d, arm):
        return mean(r["arms"][arm].get("adapt_seconds", 0) for r in d["runs"])
    E14 = {"self_old_drop": mean(r["metrics"]["arm_self_assembly"]["retention_drop_pts"] for r in e14),
           "fine_old_drop": mean(r["metrics"]["arm_full_finetune"]["retention_drop_pts"] for r in e14),
           "self_new": 100 * mean(r["metrics"]["arm_self_assembly"]["acc_f2"] for r in e14),
           "fine_new": 100 * mean(r["metrics"]["arm_full_finetune"]["acc_f2"] for r in e14)}
    return {"wins": wins, "retention_pass": retention_pass, "means": means, "ret": ret,
            "params_first": rounds[0]["arms"]["self_assembly"]["nparams"],
            "params_last": rounds[-1]["arms"]["self_assembly"]["nparams"],
            "E14": E14,
            "E16": {arm: {"old": score(e16, arm, "old_test"), "new": score(e16, arm, "new_test"), "seconds": seconds(e16, arm)}
                    for arm in ("frozen", "scheduled_adapter", "full_finetune")},
            "E17": {arm: {"old": score(e17, arm, "old_test"), "new": score(e17, arm, "new_test"), "seconds": seconds(e17, arm)}
                    for arm in ("frozen", "scheduled_adapter", "full_finetune")},
            "E18": {"concept_auc": mean(r["metrics"]["input_nll"]["old_vs_concept_auc"] for r in e18["runs"]),
                    "nuisance_auc": mean(r["metrics"]["input_nll"]["old_vs_nuisance_auc"] for r in e18["runs"]),
                    "nuisance_tpr": 100 * mean(r["metrics"]["input_nll"]["nuisance_tpr"] for r in e18["runs"]),
                    "val_fpr": 100 * mean(r["metrics"]["input_nll"]["old_val_fpr"] for r in e18["runs"]),
                    "test_fpr": 100 * mean(r["metrics"]["input_nll"]["old_test_fpr"] for r in e18["runs"]),
                    "nuisance_accuracy": 100 * mean(r["feedback"]["nuisance"]["accuracy_before_adaptation"] for r in e18["runs"]),
                    "concept_accuracy": 100 * mean(r["feedback"]["concept"]["accuracy_before_adaptation"] for r in e18["runs"]),
                    "feedback_delay": [r["feedback"]["concept"]["first_alert_after_labels"] for r in e18["runs"]]}}


def render(e14, e15, e16, e17, e18):
    s = summarise(e14, e15, e16, e17, e18)
    def row(label, old, new, seconds):
        return f'<tr><th scope="row">{html.escape(label)}</th><td>{old:.1f}%</td><td>{new:.1f}%</td><td>{seconds:.3f}s</td></tr>'
    table15 = "".join(
        '<tr><th scope="row">R{}</th>{}</tr>'.format(r["round"], "".join(
            f'<td>{r["arms"][key]["composite"]*100:.1f}%</td>' for key, _, _ in ARMS))
        for r in e15["history"])
    table16 = "".join(row(label, **s["E16"][key]) for key,label in
                      (("frozen", "Frozen"), ("scheduled_adapter", "Scheduled adapter"),
                       ("full_finetune", "Full fine-tune")))
    table17 = "".join(row(label, **s["E17"][key]) for key,label in
                      (("frozen", "Frozen"), ("scheduled_adapter", "Scheduled adapter"),
                       ("full_finetune", "Full fine-tune")))
    legend = "".join(f'<span><i style="background:{color}"></i>{html.escape(label)}</span>'
                     for _, label, color in ARMS)
    template = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">
<meta name="description" content="New AI research ledger: real measured toy experiments, negative results, provenance and next scientific gates.">
<title>New AI — research results, not hype</title>
<style>
:root{color-scheme:dark;--bg:#0b1020;--panel:#151d32;--line:#35415a;--ink:#f3f6ff;--muted:#b3bfd4;--mint:#71d7bf;--coral:#f4a393;--blue:#88a9fb}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse at 80% 0,#213151 0%,transparent 48%),var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
a{color:#a9c0ff}a:hover{color:white}a:focus-visible,summary:focus-visible{outline:3px solid var(--mint);outline-offset:3px}
.wrap{width:min(1120px,calc(100% - 36px));margin:auto}.top{padding:18px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap}
.brand{font-weight:800;letter-spacing:.04em}.top nav{display:flex;gap:20px;font-size:.91rem}.hero{padding:72px 0 30px}.eyebrow{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--mint);font-weight:800}h1{font-size:clamp(2.1rem,5vw,4.5rem);line-height:1.05;letter-spacing:-.045em;max-width:900px;margin:12px 0 23px}h2{font-size:clamp(1.5rem,3vw,2rem);letter-spacing:-.025em;margin:0 0 10px}h3{margin:0 0 12px;font-size:1.16rem}.lead{font-size:1.18rem;color:var(--muted);max-width:900px}.lede{font-size:1rem;color:var(--muted);margin:0 0 24px}.pill{display:inline-block;background:#443528;color:#ffcf92;padding:7px 12px;border-radius:100px;font-weight:800;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card,.block{border:1px solid var(--line);border-radius:16px;background:var(--panel)}.card{padding:23px}.card strong{display:block;font-size:2.25rem;letter-spacing:-.045em;line-height:1.1}.card small{display:block;color:var(--muted);margin-top:7px}.card p{margin:8px 0 0;color:var(--muted)}.mint{color:var(--mint)}.coral{color:var(--coral)}.blue{color:var(--blue)}section{padding:48px 0}.block{padding:26px;margin-top:18px}.small{font-size:.91rem;color:var(--muted)}.legend{display:flex;gap:14px 24px;flex-wrap:wrap;font-size:.91rem;color:var(--ink);margin:6px 0 20px}.legend span{display:inline-flex;gap:8px;align-items:center}.legend i{width:13px;height:13px;border-radius:4px;display:inline-block}.chart{width:100%;height:auto;display:block;min-width:520px}.chartbox{overflow-x:auto}.note{border-left:3px solid var(--coral);padding:12px 16px;background:#30283a;color:var(--ink);margin:20px 0 0}table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}td,th{text-align:left;border-bottom:1px solid var(--line);padding:10px 9px}thead th{color:var(--muted);font-size:.82rem}td{text-align:right}tbody th{font-weight:600}details{margin-top:16px}summary{cursor:pointer;font-weight:700}.scroll{overflow-x:auto}.twocol{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.steps{padding-left:23px}.steps li{padding-left:8px;margin:12px 0}.footer{border-top:1px solid var(--line);padding:30px 0 60px;color:var(--muted)}code{font-size:.86em;background:#202c44;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}
.route{max-width:680px;margin:30px auto 4px}.route strong{display:block;font-size:1.07rem}.meter-label{display:flex;justify-content:space-between;margin:12px 0 4px;color:#e6eeff;font-size:.92rem}.meter{width:100%;height:14px;border-radius:8px;background:#33415a;overflow:hidden}.meter span{display:block;height:100%;min-width:2px;border-radius:8px}.top nav{flex-wrap:wrap}
@media(max-width:800px){.grid,.twocol{grid-template-columns:1fr}.hero{padding-top:42px}.block{padding:18px}.top nav{gap:12px}}
</style></head><body>
<header class="top wrap"><div class="brand">NEW AI <span class="small">/ research ledger</span></div><nav aria-label="Sections"><a href="#rounds">Rounds</a><a href="#corrected">Corrected test</a><a href="#trigger">Trigger audit</a><a href="#roadmap">Next gates</a><a href="#data">Data</a></nav></header>
<main class="wrap">
<section class="hero"><div class="eyebrow">Transparent experiments · synthetic scale</div><h1>Can a model add a new skill without erasing an old one?</h1>
<p class="lead">We are testing a self-assembling, energy-guided language-model hypothesis. What exists today is a small classifier and several toy experiments—not a self-evolving LLM. The 10-round pilot did <strong>not</strong> meet its win condition.</p><span class="pill">Current verdict: hypothesis not established</span></section>
<section id="rounds"><h2>The ten-round trial</h2><p class="lede">E15 · one seed · four synthetic task families · test composite (mean accuracy). Each round starts with a newly initialized host; weights are not inherited and no new sprout is instantiated. This is not continuous model evolution. The family names in the old code reference MMLU, HellaSwag, ARC and GSM8K by analogy only: no official datasets were evaluated.</p>
<div class="grid"><div class="card"><strong class="coral">__WINS__/10</strong><small>Readout-only wins vs frozen</small><p>A large capability advantage was not observed.</p></div><div class="card"><strong class="coral">__RET_PASS__/10</strong><small>Retention drop ≤2 points</small><p>The announced retention gate was not met.</p></div><div class="card"><strong>__SIZE_FIRST__ → __SIZE_LAST__</strong><small>Actual parameters, first → last</small><p>Not the advertised 8 million.</p></div></div>
<div class="block"><h3>One graph · rounds × configuration type</h3><div class="legend">__LEGEND__</div><div class="chartbox">__CHART__</div>
<p class="small">Mean composite over ten rounds: readout-only __MEAN_SA__%, full fine-tune __MEAN_FF__%, frozen __MEAN_FB__%. Mean first-task retention drop: readout-only __RET_SA__ points, full fine-tune __RET_FF__ points. These are ten different model sizes, one seed, and unpaired compute paths; the horizontal axis does <em>not</em> prove learning over time.</p>
<details><summary>See exact scores by round</summary><div class="scroll"><table><thead><tr><th scope="col">Round</th><th scope="col">Readout-only</th><th scope="col">Fine-tune</th><th scope="col">Frozen</th></tr></thead><tbody>__E15_TABLE__</tbody></table></div></details></div>
<p class="note"><strong>Why the old verdict changed:</strong> freezing old weights does not preserve their rank against newly updated logits. Labels overlap across E15 families; the “self-assembly” arm updates existing readout rows rather than growing a new organ. Its apparent retention advantage over naive fine-tuning is not the proposed mechanism.</p></section>
<section id="corrected"><h2>A cleaner instrument, with both failure and follow-up</h2><p class="lede">E16 and E17 use position-specific one-hots, an explicit rule cue, and sequence-disjoint train/validation/test splits. Five seeds each. The easy task is “copy first symbol,” then “copy last symbol,” with no replay. A scheduled 400-weight adapter is added only for the cued second task; the first task's output path stays exactly unchanged. This is an established fixed adapter control, not autonomous growth, energy descent, or text generation.</p>
<div class="twocol"><div class="block"><h3>E16 · negative result</h3><p>At the same 0.01 learning rate, the adapter preserved the old rule but failed to learn the new one. Keep the failure visible; it motivated the follow-up.</p><div class="scroll"><table><thead><tr><th scope="col">Arm</th><th scope="col">Old test</th><th scope="col">New test</th><th scope="col">Adapt time*</th></tr></thead><tbody>__E16_TABLE__</tbody></table></div></div>
<div class="block"><h3>E17 · exploratory correction</h3><p>After inspecting E16, the adapter learning rate was raised to 0.15. On five <em>fresh</em> seeds it reached <strong>__E17_OLD__% old / __E17_NEW__% new</strong> test accuracy. Full fine-tuning reached __E17_FINE_OLD__% / __E17_FINE_NEW__%. This is a toy, task-cued control and a post-E16 hyperparameter choice, <em>not</em> a preregistered mechanistic win.</p><div class="scroll"><table><thead><tr><th scope="col">Arm</th><th scope="col">Old test</th><th scope="col">New test</th><th scope="col">Adapt time*</th></tr></thead><tbody>__E17_TABLE__</tbody></table></div></div></div>
<p class="small">*GPU seconds are observed adaptation wall time averaged over five seeds, not equalized compute. Arms used the same examples, minibatch order and 140 optimizer steps, but have different trainable parameter counts and learning rates in E17. There is no stress-triggered growth arm here.</p>
<div class="block"><h3>Prior narrow result: E14</h3><p>In a separate, favorable no-replay geometry task with disjoint classes, the localized arm averaged __E14_SA_OLD__ points old-task drop and __E14_SA_NEW__% new-task accuracy; naive full fine-tune averaged __E14_FF_OLD__ points old-task drop and __E14_FF_NEW__% new-task accuracy across five seeds. Its core was frozen and new rows were already allocated. This supports a narrow retention observation, not an open-ended no-forgetting guarantee.</p></div></section>
<section id="trigger"><h2>E18 · can novelty tell us when to grow?</h2><p class="lede">Five fresh-seed detector audit, no task cue. A fixed classifier faces two held-out changes: (1) the <em>same exact inputs</em> with the answer rule switched from last symbol to first; (2) new first-symbol values, but the original last-symbol rule still works. No model expands or learns a new rule in this round.</p>
<div class="grid"><div class="card"><strong class="coral">__E18_CONCEPT_AUC__</strong><small>Input-only AUROC on label-only change</small><p>Exact input pairing forces chance-level detection for <em>any</em> fixed input-only score. Logit free energy and entropy also measured 0.500.</p></div><div class="card"><strong class="blue">__E18_NUISANCE_TPR__%</strong><small>Input-density alarm on harmless shift</small><p>Categorical input NLL detected it with AUROC __E18_NUISANCE_AUC__; old-rule accuracy remained __E18_NUISANCE_ACC__%.</p></div><div class="card"><strong class="mint">__E18_DELAY__ labels</strong><small>Feedback-based alert on true rule change</small><p>Errors after seeing outcomes signalled it on all five seeds. Concept-rule accuracy before adaptation was __E18_CONCEPT_ACC__%.</p></div></div>
<p class="note"><strong>Pre-registered calibration miss:</strong> 95th-percentile input-density alarm exceeded its ≤5% old-validation false-alarm gate: __E18_VAL_FPR__% (held-out old test mean __E18_TEST_FPR__%). Input novelty alone would call for growth when no new skill is needed. A feedback alert is not proof an adapter would help. These are synthetic detector measurements, not an energy-trained model or an autonomous LLM.</p>
<p class="small">Read the <a href="source/PROTOCOL_E18.md">pre-registered protocol</a>, <a href="source/E18_REPORT.md">full outcome and gate accounting</a>, and <a href="source/PRIOR_ART_E18.md">prior-art comparison with primary papers</a>. Published SEMA and MaRS already study dynamic adapter/slot expansion; SCALE studies frozen-base growth; Meta-UCF studies constant-memory LLM adapters. An August 2026 FiUni paper goes further: task-free batch-level detection and adaptive LoRA subspaces. It and other post-E18 discoveries are marked in the review; none influenced E18. The next causal round must beat these kinds of baselines, not relabel them as new.</p></section>
<section id="roadmap"><h2>What would count as progress?</h2><ol class="steps"><li><strong>Mechanism test:</strong> train and validate an explicit energy function. Measure descent and held-out accuracy independently; reject stable-but-wrong answers.</li><li><strong>Causal trigger test:</strong> compare stress-triggered, random-triggered (matched event count), scheduled/fixed adapters, frozen, and full fine-tune under held-out novelty. Report false alarms, detection delay, retention, parameters, GPU-seconds and transfer cost.</li><li><strong>Real evolution:</strong> inherit trained weights/modules across rounds; select the top 80% on validation only; breed compatible survivors, seal tests and confirm champions on independent seeds. Scaling size alone is a separate ablation.</li><li><strong>Language and systems:</strong> only after toy causal gates pass, test actual text generation and unmodified external benchmarks. Separately validate two-model freeze/swap rollback, compressed ternary kernels and tiered paging. Keep the model unable to edit its evaluator.</li></ol><p class="note">The announced target—at least +15 composite points versus <em>both</em> frozen and fine-tuned controls at matched compute, with ≤2-point old-task loss—remains a target. It has not been met.</p></section>
<section id="data"><h2>Check the numbers yourself</h2><p>Download the exact records behind this page: <a href="data/e15.json" download>E15 ten rounds</a> · <a href="data/e16.json" download>E16 five seeds</a> · <a href="data/e17.json" download>E17 five fresh seeds</a> · <a href="data/e18.json" download>E18 five-seed trigger audit</a> · <a href="data/e14.json" download>E14 five seeds</a>. <a href="source/PROTOCOL_E16_E17.md">Read the E16/E17 protocol</a>, <a href="source/PROTOCOL_E18.md">E18 protocol</a> and <a href="source/run_e18.py">E18 runner source</a>; JSON records include source-file hashes and a dirty-tree warning. E15's embedded commit hash predates its runner, so that old record is not independently reproducible from the cited commit alone.</p><p class="small">Generated from raw files by <a href="source/build_research_site.py"><code>build_research_site.py</code></a>; no results are manually entered into the page. The source benchmark names refer to synthetic analogues; original papers: Hendrycks et al. (MMLU, arXiv:2009.03300), Zellers et al. (HellaSwag, arXiv:1905.07830), Chollet (ARC, arXiv:1911.01547), Cobbe et al. (GSM8K, arXiv:2110.14168). <a href="data/method.html">Method and limitations</a>.</p></section>
</main><footer class="footer"><div class="wrap">New AI · a research log, not a product claim. Historical negative results remain public.</div></footer></body></html>"""
    replacements = {
        "__WINS__": str(s["wins"]), "__RET_PASS__": str(s["retention_pass"]),
        "__SIZE_FIRST__": f'{s["params_first"]:,}', "__SIZE_LAST__": f'{s["params_last"]:,}',
        "__LEGEND__": legend, "__CHART__": chart(e15["history"]),
        "__MEAN_SA__": f'{s["means"]["self_assembly"]:.2f}',
        "__MEAN_FF__": f'{s["means"]["full_finetune"]:.2f}',
        "__MEAN_FB__": f'{s["means"]["frozen_baseline"]:.2f}',
        "__RET_SA__": f'{s["ret"]["self_assembly"]:.2f}',
        "__RET_FF__": f'{s["ret"]["full_finetune"]:.2f}',
        "__E15_TABLE__": table15, "__E16_TABLE__": table16, "__E17_TABLE__": table17,
        "__E17_OLD__": f'{s["E17"]["scheduled_adapter"]["old"]:.1f}',
        "__E17_NEW__": f'{s["E17"]["scheduled_adapter"]["new"]:.1f}',
        "__E17_FINE_OLD__": f'{s["E17"]["full_finetune"]["old"]:.1f}',
        "__E17_FINE_NEW__": f'{s["E17"]["full_finetune"]["new"]:.1f}',
        "__E14_SA_OLD__": f'{s["E14"]["self_old_drop"]:.1f}',
        "__E14_FF_OLD__": f'{s["E14"]["fine_old_drop"]:.1f}',
        "__E14_SA_NEW__": f'{s["E14"]["self_new"]:.1f}',
        "__E14_FF_NEW__": f'{s["E14"]["fine_new"]:.1f}',
        "__E18_CONCEPT_AUC__": f'{s["E18"]["concept_auc"]:.3f}',
        "__E18_NUISANCE_AUC__": f'{s["E18"]["nuisance_auc"]:.3f}',
        "__E18_NUISANCE_TPR__": f'{s["E18"]["nuisance_tpr"]:.0f}',
        "__E18_NUISANCE_ACC__": f'{s["E18"]["nuisance_accuracy"]:.0f}',
        "__E18_CONCEPT_ACC__": f'{s["E18"]["concept_accuracy"]:.1f}',
        "__E18_DELAY__": str(max(s["E18"]["feedback_delay"])),
        "__E18_VAL_FPR__": f'{s["E18"]["val_fpr"]:.3f}',
        "__E18_TEST_FPR__": f'{s["E18"]["test_fpr"]:.3f}',
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    assert "__" not in template
    assert template.count("<svg") == 1
    return template


def e19_accuracy_chart(runs):
    """Old/new held-out accuracy trade-off; all five seeds remain visible."""
    left, top, width, height = 94, 52, 742, 365
    x = lambda p: left + (p - 80) / 15 * width
    y = lambda p: top + (80 - p) / 32 * height
    old_floor = 100 * mean(r["old_before_test"] for r in runs) - 5
    bits = ['<svg class="chart" viewBox="0 0 960 510" role="img" '
            'aria-labelledby="e19-accuracy-title e19-accuracy-desc" xmlns="http://www.w3.org/2000/svg">',
            '<title id="e19-accuracy-title">E19 old versus new test accuracy, five paired seeds per arm</title>',
            '<desc id="e19-accuracy-desc">The upper right passes the two absolute accuracy gates. '
            'The feedback and scheduled markers coincide on every seed; full fine-tuning learns the new topic '
            'better but drops old accuracy below the retention threshold. This chart cannot show the separate '
            'two-point timing-advantage requirement.</desc>',
            f'<rect x="{x(old_floor):.1f}" y="{y(80):.1f}" width="{x(95)-x(old_floor):.1f}" '
            f'height="{y(65)-y(80):.1f}" fill="#173e38" opacity=".52"/>']
    for tick in (50, 55, 60, 65, 70, 75, 80):
        pos = y(tick)
        bits += [f'<path d="M {left} {pos:.1f} H {left+width}" stroke="#394661" stroke-width="1"/>',
                 f'<text x="{left-13}" y="{pos+5:.1f}" fill="#d5deef" text-anchor="end" font-size="15">{tick}</text>']
    for tick in (80, 85, 90, 95):
        pos = x(tick)
        bits += [f'<path d="M {pos:.1f} {top} V {top+height}" stroke="#394661" stroke-width="1"/>',
                 f'<text x="{pos:.1f}" y="{top+height+25}" fill="#d5deef" text-anchor="middle" font-size="15">{tick}</text>']
    bits += [f'<path d="M {x(old_floor):.1f} {top} V {top+height}" stroke="#b6edce" stroke-dasharray="6 5" stroke-width="2"/>',
             f'<path d="M {left} {y(65):.1f} H {left+width}" stroke="#b6edce" stroke-dasharray="6 5" stroke-width="2"/>',
             f'<text x="{x(old_floor)+8:.1f}" y="{top+20}" fill="#daf5e5" font-size="15">old loss ≤ 5 pts</text>',
             f'<text x="{left+width-8}" y="{y(65)-10:.1f}" fill="#daf5e5" text-anchor="end" font-size="15">new ≥ 65%</text>']
    for arm, label, color in E19_ARMS:
        if arm == "feedback":
            continue  # Exactly coincident with scheduled; draw one marker, not two misleading dots.
        vals = [(100*r["arms"][arm]["old_test"], 100*r["arms"][arm]["new_test"], r["seed"])
                for r in runs]
        for old, new, seed in vals:
            bits.append(f'<circle cx="{x(old):.1f}" cy="{y(new):.1f}" r="4" fill="{color}" '
                        f'opacity=".52"><title>{label}, seed {seed}: old {old:.2f}%, new {new:.2f}%</title></circle>')
        old, new = mean(v[0] for v in vals), mean(v[1] for v in vals)
        bits.append(f'<circle cx="{x(old):.1f}" cy="{y(new):.1f}" r="9" fill="{color}" '
                    f'stroke="#0b1020" stroke-width="2"><title>{label} mean: old {old:.2f}%, new {new:.2f}%</title></circle>')
        if arm == "scheduled":
            bits.append(f'<circle cx="{x(old):.1f}" cy="{y(new):.1f}" r="12" fill="none" '
                        'stroke="#c9f6d8" stroke-width="2"/>'
                        f'<text x="{x(old)-14:.1f}" y="{y(new)-17:.1f}" fill="#dfffe9" '
                        'text-anchor="end" font-size="15">scheduled = feedback</text>')
    bits += [f'<text x="{left+width/2:.1f}" y="490" text-anchor="middle" fill="#ecf2ff" font-size="17">Old-topic test accuracy (%)</text>',
             '<text transform="translate(20,235) rotate(-90)" text-anchor="middle" fill="#ecf2ff" font-size="17">New-topic test accuracy (%)</text>',
             '</svg>']
    return "".join(bits)


def e19_timing_chart(runs):
    """Paired per-seed timing effect in accuracy points, not raw arm score."""
    left, top, width = 196, 50, 638
    x = lambda value: left + value / 2.2 * width
    bits = ['<svg class="chart" viewBox="0 0 960 350" role="img" '
            'aria-labelledby="e19-timing-title e19-timing-desc" xmlns="http://www.w3.org/2000/svg">',
            '<title id="e19-timing-title">E19 feedback advantage over scheduled and random timing, paired by seed</title>',
            '<desc id="e19-timing-desc">Feedback versus scheduled is zero on all five seeds; versus random '
            'is positive on four but under one percentage point on all five. Neither reaches the preregistered '
            'two-point mean advantage.</desc>']
    for tick in (0, .5, 1, 1.5, 2):
        xx = x(tick)
        bits += [f'<path d="M {xx:.1f} {top-8} V 278" stroke="#394661" stroke-width="1"/>',
                 f'<text x="{xx:.1f}" y="301" fill="#d5deef" text-anchor="middle" font-size="15">{tick:g}</text>']
    bits.append(f'<path d="M {x(2):.1f} {top-8} V 278" stroke="#f4a393" stroke-width="3" stroke-dasharray="5 5"/>')
    for i, row in enumerate(runs):
        yy = top + i * 46
        bits.append(f'<text x="{left-19}" y="{yy+9}" fill="#ecf2ff" text-anchor="end" font-size="15">seed {row["seed"]}</text>')
        for arm, color, offset in (("scheduled", "#71d7bf", -6), ("random", "#f5cc86", 8)):
            diff = 100 * (row["arms"]["feedback"]["balanced_test"] - row["arms"][arm]["balanced_test"])
            if diff < -1e-8 or diff > 2.2:
                raise ValueError("E19 timing effect outside chart range")
            ypos = yy + offset
            bits.append(f'<path d="M {left} {ypos} H {x(diff):.1f}" stroke="{color}" stroke-width="5"/>')
            bits.append(f'<circle cx="{x(diff):.1f}" cy="{ypos}" r="5" fill="{color}">'
                        f'<title>Seed {row["seed"]}, feedback minus {arm}: {diff:.3f} percentage points</title></circle>')
    bits += [f'<text x="{x(2)-8:.1f}" y="29" fill="#f4a393" text-anchor="end" font-size="15">required ≥2 pts</text>',
             f'<text x="{left+width/2:.1f}" y="330" fill="#ecf2ff" text-anchor="middle" font-size="16">Feedback balanced-accuracy advantage (percentage points)</text>',
             '</svg>']
    return "".join(bits)


def e19_section(record):
    """Derive all E19 display values from five pinned raw seed records."""
    runs = record["runs"]
    assert record["experiment"] == "E19"
    assert [r["seed"] for r in runs] == [31, 37, 41, 43, 47]
    arms = (("frozen", "Frozen"), ("scheduled", "Scheduled adapter"),
            ("random", "Random-timed adapter"), ("feedback", "Feedback-triggered adapter"),
            ("full_finetune", "Full fine-tune"))
    def metric(arm, key):
        return mean(r["arms"][arm][key] for r in runs)
    router_old = 100 * metric("feedback", "router_old_rate")
    router_new = 100 * metric("feedback", "router_new_rate")
    router_new_range = [100 * r["arms"]["feedback"]["router_new_rate"] for r in runs]
    rows = "".join(
        f'<tr><th scope="row">{html.escape(label)}</th>'
        f'<td>{100*metric(arm, "old_test"):.2f}%</td>'
        f'<td>{100*metric(arm, "new_test"):.2f}%</td>'
        f'<td>{100*metric(arm, "balanced_test"):.2f}%</td>'
        f'<td>{metric(arm, "old_drop_points"):.2f} pts</td>'
        f'<td>{metric(arm, "adapt_seconds"):.3f}s</td>'
        f'<td>{metric(arm, "total_params"):,.0f}</td></tr>'
        for arm, label in arms)
    versus_scheduled = 100 * (metric("feedback", "balanced_test") - metric("scheduled", "balanced_test"))
    versus_random = 100 * (metric("feedback", "balanced_test") - metric("random", "balanced_test"))
    assert [r["arms"]["feedback"]["trigger_after_labels"] for r in runs] == [32] * 5
    assert versus_scheduled == 0
    legend = "".join(f'<span><i style="background:{color}"></i>{html.escape(label)}</span>'
                     for arm, label, color in E19_ARMS if arm != "feedback")
    return (f'<section id="text-pilot"><h2>E19 · real text, but no timing win</h2>'
            f'<p class="lede">Five-seed AG News binary-transfer pilot: topic A (World/Sports) then topic B '
            f'(Business/Science). A hashed-word <strong>linear classifier</strong>, not a language model, '
            f'processes English articles without an explicit task cue. The feedback alarm sees outcome labels '
            f'and creates a zero-initialized adapter; scheduled and random-timed controls use the same '
            f'adapter and training-step budget.</p>'
            f'<div class="grid"><div class="card"><strong class="coral">{versus_scheduled:.2f} pts</strong>'
            f'<small>Feedback vs scheduled · balanced accuracy</small><p>Both triggered after 32 labels '
            f'on every seed. Required advantage: at least 2 points; timing gate failed.</p></div>'
            f'<div class="card"><strong class="coral">{100*metric("feedback", "new_test"):.2f}%</strong>'
            f'<small>Feedback new-topic test accuracy</small><p>Below the locked 65% minimum. '
            f'Router activates on only {min(router_new_range):.0f}–{max(router_new_range):.0f}% of new-topic test examples across seeds.</p></div>'
            f'<div class="card"><strong class="blue">{versus_random:.2f} pts</strong>'
            f'<small>Feedback vs random timing</small><p>Below the locked 2-point advantage.</p></div></div>'
            f'<div class="block"><h3>Capability versus retention</h3>'
            f'<p class="small">Each faint dot is one seed; large markers are five-seed means. '
            f'Scheduled and feedback overlap exactly. Green region is only the absolute old/new '
            f'accuracy gates; passing it would <em>not</em> establish a timing advantage. '
            f'Axes are cropped and labelled, not zero-based. On a phone, swipe the charts '
            f'horizontally to inspect every marker and threshold.</p>'
            f'<div class="legend">{legend}<span><i style="border:2px solid #c9f6d8;background:none"></i>Feedback = scheduled</span></div>'
            f'<div class="chartbox">{e19_accuracy_chart(runs)}</div></div>'
            f'<div class="block"><h3>Does the trigger actually help?</h3>'
            f'<p class="small">Paired balanced-accuracy difference on the <em>same</em> seed. '
            f'Zero for scheduled on all five seeds; random timing is slightly worse. '
            f'The coral line is the locked +2-point mean threshold.</p>'
            f'<div class="legend"><span><i style="background:#71d7bf"></i>Versus scheduled</span>'
            f'<span><i style="background:#f5cc86"></i>Versus random</span></div>'
            f'<div class="chartbox">{e19_timing_chart(runs)}</div>'
            f'<div class="route"><strong>Why does the adapter learn so little?</strong>'
            f'<p class="small">The unsupervised route activates on only {router_new:.1f}% of new-topic '
            f'articles; it also misroutes {router_old:.1f}% of old-topic articles (five-seed means). '
            f'Coverage is a diagnosis, not a task accuracy score.</p>'
            f'<div class="meter-label">New-topic routing <b>{router_new:.1f}%</b></div>'
            f'<div class="meter"><span style="width:{router_new:.1f}%;background:#71d7bf"></span></div>'
            f'<div class="meter-label">Old-topic false routing <b>{router_old:.1f}%</b></div>'
            f'<div class="meter"><span style="width:{router_old:.1f}%;background:#f4a393"></span></div>'
            f'</div></div>'
            f'<div class="block"><h3>Same-class classifier controls · official held-out test</h3>'
            f'<div class="scroll"><table><thead><tr><th>Arm</th><th>Old accuracy</th>'
            f'<th>New accuracy</th><th>Balanced mean</th><th>Old drop</th>'
            f'<th>Adapt time*</th><th>Total weights</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div><p class="small">Five-seed means, no test tuning. '
            f'Full fine-tuning learns more on the new topic but forgets more of the old one. '
            f'*Observed adaptation wall time excludes detector, routing and base training. '
            f'Equal optimizer steps are not equal total compute or latency. This custom binary topic '
            f'transfer is not the standard four-class AG News leaderboard task.</p>'
            f'<p><a href="source/PROTOCOL_E19.md">Locked protocol</a> · '
            f'<a href="source/E19_REPORT.md">Interpretation and limits</a> · '
            f'<a href="data/e19.json">All five raw seed records</a> · '
            f'<a href="source/run_e19.py">Runner source</a> · '
            f'<a href="source/SITE_PUBLICATION_CHECKLIST.md">Future-round publication gate</a>'
            f'</p></div></section>')

def check_publication(source, page):
    """Fail the build when a new EXX summary lacks a site entry/download."""
    observed = {path.parent.name for path in (source / "results").glob("E*/summary.json")
                if path.parent.name[1:].isdigit()}
    expected = set(PUBLISHED_SUMMARIES)
    if observed != expected:
        raise ValueError(f"update site for experiment summaries before publishing: "
                         f"missing={sorted(observed-expected)}, unavailable={sorted(expected-observed)}")
    for exp in PUBLISHED_SUMMARIES:
        if f'data/{exp.lower()}.json' not in page:
            raise ValueError(f"{exp} has no discoverable raw-data link")


def build(source=HERE, out=None):
    source = Path(source)
    dest = Path(out) if out else source / "research-site"
    dest.mkdir(parents=True, exist_ok=True)
    data = dest / "data"
    data.mkdir(exist_ok=True)
    e14, e15, e16, e17, e18 = load_results(source)
    page = render(e14, e15, e16, e17, e18)
    e19 = json.loads((source / "results/E19/summary.json").read_text(encoding="utf-8"))
    page = page.replace('<section id="rounds">', e19_section(e19) + '<section id="rounds">')
    page = page.replace('<a href="#rounds">Rounds</a>',
                        '<a href="#text-pilot">Latest · E19</a><a href="#rounds">Rounds</a>')
    page = page.replace('a small classifier and several toy experiments—not a self-evolving LLM.',
                        'small classifiers on synthetic rules and a real news-text pilot—not a self-evolving LLM.')
    page = page.replace('Transparent experiments · synthetic scale',
                        'Transparent experiments · real text pilot + historical synthetic tests')
    page = page.replace('The 10-round pilot did <strong>not</strong> meet its win condition.',
                        'The latest real-text timing gate and the historical ten-round pilot both <strong>failed</strong> their win conditions.')
    progress = json.loads((source / "results/PROGRESS/status.json").read_text(encoding="utf-8"))
    page = page.replace('<section id="text-pilot">', home_section(progress) + '<section id="text-pilot">')
    review = load_review_update(source, source.parent / "data")
    historical_home = home_section(progress).replace(
        'No approved budget or independent final custody.',
        'October 5 snapshot; budget later approved, independent custody still open.')
    historical_home = historical_home.replace('Current work · preparation, not a model win',
                                              'October 5 evidence snapshot · not a model win')
    historical_home = historical_home.replace('E20 language benchmark readiness', 'E20 October 5 checklist')
    page = page.replace(home_section(progress), historical_home)
    page = page.replace('<section id="progress">', home_review_update(review) + '<section id="progress">')
    page = page.replace('<section id="review-update">',
                        goal_home_section(review, review['_goal_evidence']) + '<section id="review-update">')
    page = page.replace('</head>', f'<style>{GOAL_STYLE}</style></head>')
    page = page.replace('<a href="#text-pilot">Latest · E19</a>',
                        '<a href="#progress">Progress</a><a href="#text-pilot">Result · E19</a>')
    page = page.replace('<a href="#progress">Progress</a>',
                        '<a href="#review-update">Latest review</a><a href="#progress">Progress</a>')
    page = page.replace('<a href="#review-update">Latest review</a>',
                        '<a href="#goal">Original goal</a><a href="#review-update">Preparation</a>')
    page = page.replace('<a href="#progress">Progress</a>',
                        '<a href="#progress">Progress</a><a href="benchmarks/index.html">Benchmarks · proposal</a>')
    assert '<section id="text-pilot">' in page and page.count('<svg') == 3
    check_publication(source, page)
    build_benchmark(dest / "benchmarks")
    (dest / "index.html").write_text(page, encoding="utf-8")
    progress_dir = dest / "progress"
    progress_dir.mkdir(exist_ok=True)
    progress_page = render_progress(progress)
    progress_page = progress_page.replace(
        'Pending: owner decisions on scope, proposed compute and human QA/rights;',
        'October 5 snapshot: owner scope/compute approvals were pending then; the October 6 '
        'preparation approval below supersedes that part. Still pending: human QA/rights;')
    progress_page = progress_page.replace(
        'The proposed 24 exclusive GPU-hour E20 cap (up to 1 development hour) is a request, not an allocation.',
        'The E20 24-hour/at-most-1-hour ceiling was approved for preparation on October 6; '
        'no GPU window is reserved.')
    progress_page = progress_page.replace(
        'Language-model scope, independent scorer/code review, rights, custody, difficulty calibration, uncertainty design, cap and GPU slot remain unresolved.',
        'October 5 snapshot: language scope/cap were pending then and were approved for preparation '
        'October 6; independent scorer/code review, rights, custody, difficulty calibration, '
        'uncertainty design and GPU slot remain unresolved.')
    progress_page = progress_page.replace('<b class="coral">E20 · blocked</b>',
                                          '<b class="coral">E20 · October 5 checklist</b>')
    progress_page = progress_page.replace('<h2>E20 · language-study readiness</h2>',
                                          '<h2>E20 · October 5 readiness snapshot</h2>')
    progress_page = progress_page.replace('<main class="wrap">',
                                          '<main class="wrap">' + goal_results_section(review, review['_goal_evidence']), 1)
    progress_page = progress_page.replace('</head>',
        '<style>#updates li{overflow-wrap:anywhere;word-break:break-word}' + GOAL_STYLE + '</style></head>')
    progress_page = progress_page.replace('</main>', review_progress_section(review) + '</main>')
    progress_page = progress_page.replace('<a href="#evidence">Evidence</a>',
                                          '<a href="#evidence">Evidence</a><a href="#updates">October 6 update</a>')
    (progress_dir / "index.html").write_text(progress_page, encoding="utf-8")
    shutil.copyfile(source / "results/PROGRESS/status.json", data / "progress.json")
    shutil.copyfile(source / "status_update_2026_10_06.json", data / "status-2026-10-06.json")
    for name in ("e21-public-v02-command.json", "e21-independent-pinned-suite.json",
                 "e21-approved-preparation-readback.json"):
        shutil.copyfile(source.parent / "data" / name, data / name)
    e20_public = review["e20_verified_preparation"]
    for item in (e20_public["cpu_receipt"], e20_public["cpu_readback"],
                 *e20_public["gpu_receipts"].values()):
        shutil.copyfile(source.parent / "data" / item["path"], data / item["path"])
    for key in PUBLISHED_SUMMARIES:
        shutil.copyfile(source / "results" / key / "summary.json", data / (key.lower() + ".json"))
    (data / "e14.json").write_text(json.dumps(e14, indent=2), encoding="utf-8")
    public_source = dest / "source"
    public_source.mkdir(exist_ok=True)
    for filename in ("PROTOCOL_E16_E17.md", "tasks_v2.py", "run_e16.py", "run_e17.py",
                     "test_e16.py", "test_site.py", "build_research_site.py",
                     "PROTOCOL_E18.md", "E18_REPORT.md", "PRIOR_ART_E18.md",
                     "run_e18.py", "test_e18.py", "PROTOCOL_E19.md", "E19_REPORT.md",
                     "run_e19.py", "test_e19.py", "SITE_PUBLICATION_CHECKLIST.md",
                     "prepare_progress_snapshot.py", "progress_site.py", "test_progress.py",
                     "PROGRESS_STATUS.md", "benchmark_preview.py",
                     "benchmark_preview_template.html", "benchmark_suite_v0_1.json",
                     "BENCHMARK_PREVIEW_PROTOCOL.md", "test_benchmark_preview.py",
                     "status_update.py", "status_update_2026_10_06.json", "test_status_update.py",
                     "goal_status.py", "test_goal_status.py",
                     "NEW_AI_E20_CPU_CLOCK_PREFLIGHT_2026_10_06.md",
                     "NEW_AI_E20_E21_GPU_RESERVATION_RIGHTS_RECONCILIATION_2026_10_06.md",
                     "NEW_AI_E20_E21_GPU_COMMAND_ENVELOPE_RECOVERY_2026_10_06.md",
                     "NEW_AI_ORIGINAL_GOAL_REQUIREMENTS_TRACE_2026_10_06.md",
                     "NEW_AI_ATTRACTOR_FULL_READING_2026_10_05.md",
                     "NEW_AI_PRINCIPIA_FULL_READING_2026_10_05.md",
                     "NEW_AI_ARXIV_2609_00006_KR8_APPLICATION_REVIEW_2026_10_05.md",
                     "E21_PUBLIC_CONTRACT_V02_REPORT.md",
                     "NEW_AI_E21_INDEPENDENT_CONTRACT_REVIEW_2026_10_06_PUBLIC.md",
                     "NEW_AI_E20_E21_APPROVED_CANDIDATE_LOCK_2026_10_06.md",
                     "E21_APPROVED_PREPARATION_REPORT_2026_10_06.md"):
        shutil.copyfile(source / filename, public_source / filename)
    method = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Method and limitations</title>'
              '<body style="font:1.2em/1.6 system-ui;max-width:850px;margin:40px auto;padding:18px;background:#0b1020;color:#f3f6ff">'
              '<h1>Method and limitations</h1><p>E15 is a historical single-seed pilot with independent new models in each round;'
              ' selection occurred on test and its embedded git commit does not contain the runner. It does not prove evolution.'
              '</p><p>E14 is a task-specific no-replay comparison, not a general guarantee. E16/E17 use toy categorical rules with an explicit'
              ' task cue; E17 was tuned after inspecting E16. E18 pairs identical X with different labels to show that fixed'
              ' input-only scores cannot detect this concept shift. Its density alarm slightly misses the 5% validation'
              ' false-alarm gate. E19 uses genuine news text in a linear classifier but its feedback-triggered adapter'
              ' matches scheduled timing and fails its new-task accuracy gate. None tests learned energy'
              ' or competitive language generation. All scores come from raw JSON'
              ' linked on the home page.</p><p>Current scientific protocol: test learned energy against held-out correctness,'
              ' stress trigger against matched random/scheduled controls, inheritance across rounds and then real language tasks.'
              '</p><a style="color:#a9c0ff" href="../index.html">Back to results</a></body></html>')
    (data / "method.html").write_text(method, encoding="utf-8")
    print(f"Built {dest / 'index.html'} ({len(page)} chars; three separate, measured charts)")
    return page


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=HERE)
    ap.add_argument("--out", type=Path)
    opts = ap.parse_args()
    build(opts.source, opts.out)
