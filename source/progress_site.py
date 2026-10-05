"""Render public preparation status without promoting CPU checks to model results."""
import html
import math
from statistics import mean


def verify(snapshot):
    if snapshot["schema"] != "new-ai-public-development-progress-v1":
        raise ValueError("Unknown progress snapshot schema")
    if snapshot["scientific_verdict"] != "NO_CONFIRMED_LLM_RESULT":
        raise ValueError("A confirmed LLM result needs its own EXX publication")
    e20, e21, e22 = (snapshot[key] for key in ("e20", "e21", "e22"))
    if (e20["status"], e20["run_authorized"]) != ("BLOCKED", False):
        raise ValueError("E20 gate is not the reviewed blocked state")
    if e21["status"] != "LANGUAGE_CONFIRMATION_NOT_RUN" or len(e21["seeds"]) != 5:
        raise ValueError("E21 language status or five-seed fixture changed")
    if len(e21["paired_direct_minus_energy_k4_nll"]) != len(e21["seeds"]):
        raise ValueError("E21 paired records are incomplete")
    if not all(math.isfinite(v) for v in e21["paired_direct_minus_energy_k4_nll"]):
        raise ValueError("E21 nonfinite paired result")
    if (e22["status"], e22["model_outcome"]) != ("PUBLIC_DEVELOPMENT_INSTRUMENT_ONLY", None):
        raise ValueError("E22 model outcome or status changed")
    if e22["factor_cells"] != len(e22["per_cell_groups"]) or e22["variants"] != 3 * e22["base_examples"]:
        raise ValueError("E22 cell or variant count changed")
    return e20, e21, e22


def paired_chart(e21):
    """Plot *within-fixture* NLL differences only; no cross-task score axis."""
    seeds = e21["seeds"]
    deltas = e21["paired_direct_minus_energy_k4_nll"]
    bound = max(0.01, max(abs(v) for v in deltas) * 1.15)
    positives = sum(v > 0 for v in deltas)
    zero, span = 430, 270
    label = lambda value: f"{value:+.4f}"
    bits = ['<svg class="chart" viewBox="0 0 850 380" role="img" '
            'aria-labelledby="pair-title pair-desc" xmlns="http://www.w3.org/2000/svg">',
            '<title id="pair-title">E21 synthetic CPU fixture: paired direct minus energy K4 negative-log-likelihood</title>',
            '<desc id="pair-desc">Five paired synthetic fixture seeds. Positive means lower energy-head NLL, '
            f'negative means lower direct-head NLL; {positives} positive, {len(deltas)-positives} non-positive. '
            'Not a language-model test, a matched-compute comparison, or statistical confirmation.</desc>',
            f'<path d="M {zero} 45 V 313" stroke="#d6deef" stroke-width="2"/>',
            f'<text x="{zero}" y="34" fill="#d6deef" text-anchor="middle">0</text>']
    for i, (seed, delta) in enumerate(zip(seeds, deltas)):
        yy = 78 + 48 * i
        end = zero + (delta / bound) * span
        color = "#71d7bf" if delta >= 0 else "#f4a393"
        bits.append(f'<text x="83" y="{yy+5}" fill="#eef3ff">seed {seed}</text>')
        bits.append(f'<path d="M {zero} {yy} H {end:.1f}" stroke="{color}" stroke-width="8"/>')
        bits.append(f'<circle cx="{end:.1f}" cy="{yy}" r="7" fill="{color}">'
                    f'<title>Seed {seed}: {label(delta)} nats/token direct minus energy</title></circle>')
        bits.append(f'<text x="{745 if delta >= 0 else 315}" y="{yy+5}" '
                    f'fill="#eef3ff" text-anchor="end">{label(delta)}</text>')
    bits += [f'<text x="{zero}" y="350" fill="#eef3ff" text-anchor="middle">'
             'Paired direct minus energy NLL (nats/token; positive favors energy)</text>', '</svg>']
    return "".join(bits)


def home_section(snapshot):
    e20, e21, e22 = verify(snapshot)
    deltas = e21["paired_direct_minus_energy_k4_nll"]
    positives = sum(delta > 0 for delta in deltas)
    return (f'<section id="progress"><h2>Current work · preparation, not a model win</h2>'
            f'<p class="lede">Status snapshot {html.escape(snapshot["as_of_utc"])}. '
            'E19 remains the latest completed outcome and failed its causal timing gate. '
            'E20–E22 below are different CPU preparation tracks, not three new language-model results.</p>'
            f'<div class="grid"><div class="card"><strong class="coral">BLOCKED</strong>'
            f'<small>E20 language benchmark readiness</small><p>{e20["missing_evidence_predicates"]} '
            'missing <em>evidence predicates</em> in a public-receipt checklist; not 41 failed trials. '
            'No approved budget or independent final custody.</p></div>'
            f'<div class="card"><strong class="blue">{positives}/{len(deltas)}</strong>'
            '<small>E21 synthetic fixture · paired NLL sign</small><p>Mixed CPU software result '
            'against a matched-parameter direct control, with equal token exposure but unequal measured compute. '
            'No language-model result or significance claim.</p></div>'
            f'<div class="card"><strong class="mint">{e22["variants"]}</strong>'
            '<small>E22 public development variants</small><p>Independent arithmetic checks of a candidate '
            'geometry instrument, not model predictions or a held-out benchmark. Its shortcut audit is pending.</p>'
            '</div></div><p><a href="progress/index.html">See the evidence, paired CPU chart and next gates</a> · '
            '<a href="data/progress.json" download>Download the public status projection</a></p></section>')


def render(snapshot):
    e20, e21, e22 = verify(snapshot)
    diffs = e21["paired_direct_minus_energy_k4_nll"]
    positives = sum(x > 0 for x in diffs)
    per_cell = e22["base_examples"] // e22["factor_cells"]
    if per_cell * e22["factor_cells"] != e22["base_examples"]:
        raise ValueError("Unequal E22 cell quota")
    tiles = []
    for cell, count in sorted(e22["per_cell_groups"].items()):
        if not 0 <= count <= per_cell:
            raise ValueError("E22 structural group count outside cell quota")
        description = cell.replace("depth", "depth ").replace("_arity", " · arity ").replace("_distractors", " · distractors ")
        tiles.append(f'<div class="tile"><span>{html.escape(description)}</span><b>{count}/{per_cell}</b>'
                     f'<div class="track"><i style="width:{100*count/per_cell:.1f}%"></i></div></div>')
    scores = e21["mean_fixture_scores"]
    fixture_rows = "".join(f'<tr><th scope="row">{label}</th>'
                           f'<td>{scores[key]["nll_nats_per_token"]:.4f}</td>'
                           f'<td>{100*scores[key]["accuracy"]:.2f}%</td></tr>'
                           for key, label in (("frozen_k0", "Frozen K0"), ("energy_k4", "Energy K4"),
                                              ("direct_k4", "Direct K4")))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">
<title>New AI — development progress, not a model outcome</title>
<meta name="description" content="Auditable E20–E22 preparation status, CPU-only checks and pending scientific gates.">
<style>
:root{{color-scheme:dark;--bg:#0b1020;--panel:#151d32;--line:#35415a;--ink:#f3f6ff;--muted:#b3bfd4;--mint:#71d7bf;--coral:#f4a393;--blue:#88a9fb}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(ellipse at 80% 0,#213151 0%,transparent 45%),var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}}
a{{color:#a9c0ff}}a:focus-visible{{outline:3px solid var(--mint);outline-offset:3px}}.wrap{{width:min(1060px,calc(100% - 32px));margin:auto}}
header{{border-bottom:1px solid var(--line);padding:16px 0}}nav{{display:flex;gap:20px;flex-wrap:wrap}}h1{{font-size:clamp(2rem,4.4vw,4rem);line-height:1.1;margin:25px 0 12px}}h2{{margin:0 0 10px;font-size:1.8rem}}section{{padding:42px 0;border-bottom:1px solid var(--line)}}p{{max-width:920px}}.muted{{color:var(--muted)}}.pill{{display:inline-block;border-radius:20px;background:#443528;color:#ffcf92;padding:6px 12px;font-weight:700}}
.cards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}.card,.block,.tile{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px}}.card b{{font-size:1.8rem;display:block}}.coral{{color:var(--coral)}}.blue{{color:var(--blue)}}.mint{{color:var(--mint)}}.block{{margin-top:18px}}.chartbox{{overflow-x:auto}}.chart{{display:block;min-width:730px;width:100%;height:auto}}.tilegrid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}}.tile{{padding:13px;font-size:.83rem}}.tile b{{float:right;font-size:.95rem}}.track{{clear:both;height:9px;background:#35415a;border-radius:9px;overflow:hidden;margin-top:8px}}.track i{{display:block;background:var(--mint);height:100%}}table{{width:100%;border-collapse:collapse}}td,th{{padding:9px;text-align:left;border-bottom:1px solid var(--line)}}td{{text-align:right}}.scroll{{overflow-x:auto}}.note{{border-left:3px solid var(--coral);padding:12px 16px;background:#30283a}}footer{{padding:30px 0 55px;color:var(--muted)}}code{{overflow-wrap:anywhere}}@media(max-width:800px){{.cards{{grid-template-columns:1fr}}.tilegrid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media(max-width:450px){{.tilegrid{{grid-template-columns:1fr}}}}
</style></head><body>
<header><nav class="wrap" aria-label="Sections"><a href="../index.html">Results home</a><a href="#e20">E20</a><a href="#e21">E21</a><a href="#e22">E22</a><a href="#evidence">Evidence</a></nav></header>
<main class="wrap"><section><span class="pill">No confirmed LLM result</span><h1>Progress, without a premature PASS.</h1>
<p class="muted">As of {html.escape(snapshot["as_of_utc"])}. The <a href="../index.html#text-pilot">latest completed outcome, E19</a>, failed its feedback-versus-scheduled gate. E20–E22 have CPU preparation evidence, not a trained language-model verdict. None has a reserved GPU window or independently sealed final set.</p>
<div class="cards"><div class="card"><b class="coral">E20 · blocked</b><p>{e20["missing_evidence_predicates"]} missing public-receipt predicates; <strong>0 model trials inferred</strong>.</p></div>
<div class="card"><b class="blue">E21 · CPU fixture</b><p>{positives}/{len(diffs)} paired NLL signs favor energy against direct K4 on synthetic tokens, not a statistical or compute-matched language win.</p></div>
<div class="card"><b class="mint">E22 · instrument</b><p>{e22["factor_cells"]} cells · {e22["base_examples"]} base items · {e22["variants"]} public variants; <strong>no model predictions</strong>.</p></div></div></section>
<section id="e20"><h2>E20 · language-study readiness</h2><p>The public-receipt checker returned <strong>BLOCKED</strong> with {e20["missing_evidence_predicates"]} enumerated <em>missing-evidence predicates</em>. They are not model failures or independent annotations. Its own output says <code>run_authorized=false</code>; a syntactically complete form alone would not prove security or approve a run.</p><p class="note">Pending: owner decisions on scope, proposed compute and human QA/rights; reviewed implementation and real-model profile; independent final-test custody with access-denial evidence. The proposed 24 exclusive GPU-hour E20 cap (up to 1 development hour) is a request, not an allocation.</p></section>
<section id="e21"><h2>E21 · scalar energy versus direct update</h2><p>Five paired <strong>synthetic CPU software-fixture</strong> seeds, not language generation. Energy K4 and direct K4 both trained with the same token exposure and matched functional parameter count, but measured training compute differs. The independent outcome scorer uses token NLL, not energy decrease. The positive bars below mean lower energy-head NLL; one seed goes the other way. A 4/5 sign is practical consistency only, not confirmatory statistical significance.</p>
<div class="block"><h3>Five paired seeds · direct minus energy K4 NLL</h3><p class="muted">Horizontal chart uses its own synthetic-token NLL axis. On a narrow screen, swipe horizontally for every seed. No proposed threshold is shown as adopted.</p><div class="chartbox">{paired_chart(e21)}</div></div>
<div class="block"><h3>Software-fixture means, not LLM accuracy</h3><div class="scroll"><table><thead><tr><th>Arm</th><th>NLL nats/token</th><th>Exact token accuracy</th></tr></thead><tbody>{fixture_rows}</tbody></table></div>
<p class="muted">Measured CPU training wall time across these seeds: energy {e21["training_wall_seconds_by_arm"]["energy"]:.3f}s, direct {e21["training_wall_seconds_by_arm"]["direct"]:.3f}s. Equal token exposure is <em>not</em> equal measured compute; these timings are not GPU or model-fit estimates. M1 gates have not changed. Language-model scope, independent scorer/code review, rights, custody, difficulty calibration, uncertainty design, cap and GPU slot remain unresolved.</p></div></section>
<section id="e22"><h2>E22 · oracle-backed geometry candidate</h2><p>This standard-library CPU instrument produced {e22["variants"]} public development prompts across {e22["factor_cells"]} factor cells and {e22["distinct_structural_groups"]} distinct numeric-free structural groups overall. Forward arithmetic and a separately encoded rational-equation solver agreed on the emitted answers; <strong>that is not a model accuracy score</strong>. A changed-given partner and a nuisance partner accompany each base. Both directions are represented ({e22["counterfactual_directions"]["1"]} increases / {e22["counterfactual_directions"]["-1"]} decreases).</p>
<div class="block"><h3>Distinct structures within each cell</h3><p class="muted">Bars count structural groups among {per_cell} bases in each cell; repeated groups across cells mean these bars do not add to the {e22["distinct_structural_groups"]} overall total. This is generator coverage, not reasoning difficulty or model performance.</p><div class="tilegrid">{"".join(tiles)}</div></div>
<p class="note">Not benchmark-ready: construction depth can be algebraically compressed; arity is confounded with operation family and prompt length; nuisance labels reveal the condition; depth-1 cells have only two templates. Independent validity/shortcut review, human semantics, model learnability, approved gates and fresh final custody are still pending.</p></section>
<section id="evidence"><h2>Inspect the status evidence</h2><p><a href="../data/progress.json" download>Download public status projection (JSON)</a> · <a href="../source/PROGRESS_STATUS.md">Read provenance and unresolved decisions</a> · <a href="../source/prepare_progress_snapshot.py">Projection code</a> · <a href="../source/progress_site.py">Page renderer</a>.</p>
<p class="muted">The downloadable projection includes SHA-256 identities of the original E20 readiness JSON, E21 CPU summary and E22 development receipt. It omits local execution identities and final data. Results here are a time-stamped preparation snapshot; original failed gates and E19 raw records remain on the home page. No E20/E21/E22 confirmatory model outcome has been published.</p></section></main>
<footer class="wrap">New AI research ledger · measured preparation stays separate from scientific outcome.</footer></body></html>'''
