"""Build a candid, self-contained New AI results site from raw experiment files.

No network, templates, JS frameworks, or hand-entered outcome numbers. The site
has one rounds-by-configuration graph; other observations are cards and tables.
"""
import argparse
import html
import json
import shutil
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
ARMS = (("self_assembly", "Readout-only (historically named self-assembly)", "#71d7bf"),
        ("full_finetune", "Full fine-tune", "#f4a393"),
        ("frozen_baseline", "Frozen", "#88a9fb"))


def load_results(source=HERE):
    e15 = json.loads((source / "results/E15/summary.json").read_text(encoding="utf-8"))
    e16 = json.loads((source / "results/E16/summary.json").read_text(encoding="utf-8"))
    e17 = json.loads((source / "results/E17/summary.json").read_text(encoding="utf-8"))
    e14 = [json.loads(p.read_text(encoding="utf-8"))
           for p in sorted((source / "results/E14").glob("*_e14.jsonl"))]
    assert len(e15["history"]) == 10 and len(e14) == 5
    assert len(e16["runs"]) == len(e17["runs"]) == 5
    assert set(r["seed"] for r in e16["runs"]).isdisjoint(r["seed"] for r in e17["runs"])
    assert [r["round"] for r in e15["history"]] == list(range(1, 11))
    return e14, e15, e16, e17


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


def summarise(e14, e15, e16, e17):
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
                    for arm in ("frozen", "scheduled_adapter", "full_finetune")}}


def render(e14, e15, e16, e17):
    s = summarise(e14, e15, e16, e17)
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
@media(max-width:800px){.grid,.twocol{grid-template-columns:1fr}.hero{padding-top:42px}.block{padding:18px}.top nav{gap:12px}}
</style></head><body>
<header class="top wrap"><div class="brand">NEW AI <span class="small">/ research ledger</span></div><nav aria-label="Sections"><a href="#rounds">Rounds</a><a href="#corrected">Corrected test</a><a href="#roadmap">Next gates</a><a href="#data">Data</a></nav></header>
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
<section id="roadmap"><h2>What would count as progress?</h2><ol class="steps"><li><strong>Mechanism test:</strong> train and validate an explicit energy function. Measure descent and held-out accuracy independently; reject stable-but-wrong answers.</li><li><strong>Causal trigger test:</strong> compare stress-triggered, random-triggered (matched event count), scheduled/fixed adapters, frozen, and full fine-tune under held-out novelty. Report false alarms, detection delay, retention, parameters, GPU-seconds and transfer cost.</li><li><strong>Real evolution:</strong> inherit trained weights/modules across rounds; select the top 80% on validation only; breed compatible survivors, seal tests and confirm champions on independent seeds. Scaling size alone is a separate ablation.</li><li><strong>Language and systems:</strong> only after toy causal gates pass, test actual text generation and unmodified external benchmarks. Separately validate two-model freeze/swap rollback, compressed ternary kernels and tiered paging. Keep the model unable to edit its evaluator.</li></ol><p class="note">The announced target—at least +15 composite points versus <em>both</em> frozen and fine-tuned controls at matched compute, with ≤2-point old-task loss—remains a target. It has not been met.</p></section>
<section id="data"><h2>Check the numbers yourself</h2><p>Download the exact records behind this page: <a href="data/e15.json" download>E15 ten rounds</a> · <a href="data/e16.json" download>E16 five seeds</a> · <a href="data/e17.json" download>E17 five fresh seeds</a> · <a href="data/e14.json" download>E14 five seeds</a>. <a href="source/PROTOCOL_E16_E17.md">Read the E16/E17 protocol</a> and <a href="source/run_e17.py">runner source</a>; their JSON records include exact source-file hashes and a dirty-tree warning. E15's embedded commit hash predates its runner, so that old record is not independently reproducible from the cited commit alone.</p><p class="small">Generated from raw files by <a href="source/build_research_site.py"><code>build_research_site.py</code></a>; no results are manually entered into the page. The source benchmark names refer to synthetic analogues; original papers: Hendrycks et al. (MMLU, arXiv:2009.03300), Zellers et al. (HellaSwag, arXiv:1905.07830), Chollet (ARC, arXiv:1911.01547), Cobbe et al. (GSM8K, arXiv:2110.14168). <a href="data/method.html">Method and limitations</a>.</p></section>
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
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    assert "__" not in template
    assert template.count("<svg") == 1
    return template


def build(source=HERE, out=None):
    source = Path(source)
    dest = Path(out) if out else source / "research-site"
    dest.mkdir(parents=True, exist_ok=True)
    data = dest / "data"
    data.mkdir(exist_ok=True)
    e14, e15, e16, e17 = load_results(source)
    page = render(e14, e15, e16, e17)
    (dest / "index.html").write_text(page, encoding="utf-8")
    for key in ("E15", "E16", "E17"):
        shutil.copyfile(source / "results" / key / "summary.json", data / (key.lower() + ".json"))
    (data / "e14.json").write_text(json.dumps(e14, indent=2), encoding="utf-8")
    public_source = dest / "source"
    public_source.mkdir(exist_ok=True)
    for filename in ("PROTOCOL_E16_E17.md", "tasks_v2.py", "run_e16.py", "run_e17.py",
                     "test_e16.py", "test_site.py", "build_research_site.py"):
        shutil.copyfile(source / filename, public_source / filename)
    method = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Method and limitations</title>'
              '<body style="font:1.2em/1.6 system-ui;max-width:850px;margin:40px auto;padding:18px;background:#0b1020;color:#f3f6ff">'
              '<h1>Method and limitations</h1><p>E15 is a historical single-seed pilot with independent new models in each round;'
              ' selection occurred on test and its embedded git commit does not contain the runner. It does not prove evolution.'
              '</p><p>E14 is a task-specific no-replay comparison, not a general guarantee. E16/E17 use toy categorical rules with an explicit'
              ' task cue; E17 was tuned after inspecting E16. Neither tests learned energy or stress-triggered growth. All scores'
              ' come from raw JSON linked on the home page.</p><p>Current scientific protocol: test learned energy against held-out correctness,'
              ' stress trigger against matched random/scheduled controls, inheritance across rounds and then real language tasks.'
              '</p><a style="color:#a9c0ff" href="../index.html">Back to results</a></body></html>')
    (data / "method.html").write_text(method, encoding="utf-8")
    print(f"Built {dest / 'index.html'} ({len(page)} chars; one chart)")
    return page


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=HERE)
    ap.add_argument("--out", type=Path)
    opts = ap.parse_args()
    build(opts.source, opts.out)
