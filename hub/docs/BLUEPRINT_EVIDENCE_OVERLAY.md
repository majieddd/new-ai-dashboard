---
title: "New AI blueprint — scientific validation and evidence overlay"
tags: [new-ai, blueprint, evaluation, evidence, architecture]
status: draft
created: 2026-10-05
---

# Blueprint validation overlay for the New AI hub

**Author:** Evaluation Scientist. **Requested by:** Cloud AI Generalist, event `3312ebde2eb2245b926d7f9d412844ca9c5066b26c2220aa253d05cf618412e9`, New AI thread `47ff4515b673e26334f26fba90af389fb3ff266d96e38ff961414709af5953f0`.

**Scope:** authored-graph content and scientific validation rules only. No website/Archify code, model outcome run, GPU action, historical experiment edit, or master-plan gate change. E20 design was completed and posted first. This overlay does not certify a live site or an operating deployment.

**Headline for the hub:** **E19 measured a failed classifier timing gate. E20 is a proposed real-language benchmark. E21 is a separate proposed latent-energy mechanism test. No result here establishes a self-evolving LLM, guaranteed retention, or cheaper-than-fine-tuning computation.**

## 1. Evidence maturity is not a pass/fail verdict

Keep separate fields `maturity`, `verdict`, `model_class`, `experiment`, `evidence_ref`, `protocol_lock_ref` and `runtime_state`. A built component can have a negative scientific result; a published plan is not a running component.

| Allowed maturity | Exact rendering rule | Current application |
|---|---|---|
| **measured E19** | An E19 raw record backs the specified signal; include the classifier class and scientific verdict. This is not a claim of a serving production model. | Linear classifier, centroid router, residual adapter and head-training timing. M2 timing verdict is **FAIL**, not green. |
| **preregistered-unrun** | The exact protocol/implementation/config/model/data commitments and genuine test-custody record are locked before outcomes; no outcome has run. Link that lock. A draft file or its hash alone is insufficient. | **Do not assign this to E20/E21 yet.** The supplied E20 design explicitly says proposed/unsealed. Historical E18/E19 are already measured, not unrun. |
| **proposed** | Design exists, but approval, implementation, fit/data validity or sealed-test commitments are incomplete. Show static/dashed edges and no activity pulse. | SmolLM2 E20, richer density routing, feedback growth controls, sealed language evaluator and E20 energy-scoring annex; E21 latent-energy/direct-control pair. |
| **long-term** | Outside the next bounded experiment; no claimed implementation or validated outcome in the sources used here. | Serving two-model freeze/swap, automatic promotion/rollback, cold graft/paging, unbounded growth, ternary composition, observer/self-play orchestration. |

E18 has its own **measured diagnostic** evidence, not the “measured E19” badge: its paired-input detector audit informs the monitor tooltip. Its calibration caveat remains visible. If the renderer must use only the four maturity values, attach E18 as a separately labelled historical evidence item, not as a language-model result.

For every claim use `PASS / FAIL / INVALID / INCOMPLETE / NOT TESTED` independently of maturity. For unrun designs, numeric gate values are **targets**, not attained scores. Do not substitute zero for absent measurements. Source: `NEW_AI/master-plan.md:17-25,115-141,155-161`; `RESEARCH/NEW_AI_E20_EVAL_DESIGN_2026_10_05.md:10-16,168-184,229-254`.

## 2. Claim-by-claim validation matrix

### M1 — learned energy helps inference, not merely scoring

- **Current status:** **proposed / NOT TESTED in the language experiments reviewed here.** E19 has no learned scalar energy or latent-gradient inference. E18's free-energy/entropy scores are fixed classifier proxies. The lead placed true latent energy-versus-direct refinement in the separate, unrun E21 track.
- **Measurable signal:** full-vocabulary conditional token NLL and generated-answer quality at locked inference depths, old-domain/system retention, measured training/inference cost and latency. Energy decline, gradient norm and energy–difficulty association are diagnostics, not independent success targets that can replace answer quality.
- **Matched counterfactual:** frozen LM/K=0; same functional/trainable-capacity direct recurrent updater; separately trained one-step updater; zero-gradient/bypass and frozen-random-energy checks; practical LoRA/replay references. Equal inner-step count is not equal compute: the direct arm needs a development-locked comparable measured budget, with any extra training exposures reported.
- **Sealed test:** a fresh, licensed, group-disjoint language/QA final split; target/answer isolation; immutable tokenizer/readout and predeclared depths/selection rule. The evaluator alone may see references. Never pass answer targets to latent initialization, energy candidate features or inference-depth choice.
- **Failure verdict:** energy falls without better NLL/answer quality; advantage disappears versus direct control at comparable compute; longer refinement hurts quality/retention; extra weights/candidates or an oracle explain gains. A positive readout-latent result is still a new adaptation, not reproduction of EBT or proof of general reasoning.
- **Original gate preserved:** master-plan M1/E1 asks >=5-point hard-instance improvement and energy–difficulty Spearman >=0.6 on its stated toy tasks. E21's suggested language thresholds are **not** adopted replacements. They need a separate authorized lock.
- **Graphic warning:** do not draw a solid “energy minimizes → correct answer” guarantee, mark the refiner as running, or turn the E20 finite-pool reranker into an iterative latent loop.
- **Evidence:** `NEW_AI/master-plan.md:39,64-67,135,141,161`; `REPOS/new-ai-e19/PROTOCOL_E19.md:3-4,21`; `REPOS/new-ai-e19/PROTOCOL_E18.md:12`; `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md:45-55,76-102,165-223`; E20 design §8.

### M2 — stress/feedback timing causes useful growth

- **Current status:** **measured E19 / FAIL** for the specified classifier timing claim; **proposed / NOT TESTED** for E20 language adaptation. E20 feedback is pre-update observed next-token loss, **not a trained-energy growth signal**.
- **Measurable signal:** paired final acquisition/retention deltas against scheduled and rate-matched random triggers; event count, observed-label-token delay, false events, distinct/processed training tokens, actual system routing decisions and oracle-route gap. All trigger attempts and never-trigger seeds count.
- **Matched counterfactual:** E20 F/L8/L24/R24/S3/U3/B3/D3. U3 receives B3's addition count only, never its timing or scores, under a random order committed before labels; all chronological clone/train ordering is identical. Capacity, active trainable weights, exposure and compute remain distinct accounting dimensions.
- **Sealed test:** A/B/C/G page-lineage/near-duplicate-disjoint final prose and QA; no category, date, task ID, onset or oracle route reaches the learner. Body meaning is an implicit cue, so “task-free” does not mean “no information in the input.” Threshold calibrated on old development only; future suffixes and post-update losses forbidden.
- **Failure verdict:** tie with schedule; only frozen is beaten; random/capacity/replay explains the gain; no useful new learning; useful experts need oracle routing; expansion fires on harmless novelty or missed shifts are forced into late events. A/T/D/C are separate E20 gates; a quality-only result at excess cost is not efficiency.
- **Measured evidence:** E19 feedback and scheduled both 74.6605% balanced accuracy; paired timing edge **0.00 points in every seed**; random mean 74.1132%; new accuracy 59.1526% misses the locked 65%; event after 32 labels in every seed. Thresholds remain >=2-point timing edge and >=4/5 positive paired seeds for that historical protocol.
- **Proposed E20 thresholds:** new-domain H gain >=0.0512932944 nats/token versus frozen; final A/B/C macro H advantage >=0.03 nats/token over **each** S3/U3/L24/R24, >=9/10 positive pairs and Holm-corrected sign tests. These are language-design thresholds, **not rewritten E19/master M2 accuracy gates**.
- **Graphic warning:** “Novelty detected” may route to **investigate**, not imply “capacity needed” or “growth improved capability.” E18 identical-X label changes have input-only AUROC 0.5; its nuisance density alert can be high while accuracy remains 100%. A scalar absolute energy is not automatically a calibrated alarm.
- **Evidence:** `NEW_AI/master-plan.md:40,69-76,128,157-159`; `REPOS/new-ai-e19/PROTOCOL_E19.md:9-18`; `REPOS/new-ai-e19/E19_REPORT.md:13-19`; `REPOS/new-ai-e19/E18_REPORT.md:7-19`; E20 design §§5-7; `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md:55`.

### Retention — unchanged weights are not unchanged capabilities

- **Current status:** **measured E19 / narrow low-interference observation**, not a full successful growth result. The language/no-catastrophic-forgetting claim is **proposed / NOT TESTED**.
- **Measurable signal:** old A and broader G H/QA deterioration from each seed's immutable A0; worst scored checkpoint loss; recurrence behavior and router-induced errors; core/parent tensor hashes and clone birth identity as separate engineering checks.
- **Matched counterfactual:** same starting A0/F, fixed LoRA and replay; naive FT is an informative historical comparator, not an equally sized modular inference system. Evaluate automatic routing, not an old-domain oracle.
- **Sealed test:** old and general guard pages/QA never trained or placed in replay; fixed checkpoints 0/24/48/64 scored together without test-selected checkpoint choice. G is broader prose/comprehension only, not a comprehensive reasoning/code/safety battery.
- **Failure verdict:** old/G damage exceeds gate; baseline never solved old task; no new acquisition (vacuous retention); output changes through routing despite unchanged base weights; final checkpoint recovers while severe intermediate losses are hidden.
- **Observed/proposed thresholds:** E19 feedback old drop 0.1895 points, full FT 5.8421 points, but feedback failed timing/new-task gates. E20 proposed final mean old/G PPL increase <=2% and any seed <=5%; QA mean EM drop <=2 points and any seed <=5. These do not guarantee lifelong retention.
- **Graphic warning:** label frozen weights **“backbone not updated”**, not “old skills guaranteed.” Cloned E20 slots are not zero-init sprouts; birth identity says nothing about outputs after thawing or route-key changes.
- **Evidence:** `NEW_AI/master-plan.md:31,41,75-76,138`; `REPOS/new-ai-e19/E19_REPORT.md:5-17`; E20 design §§4,6,7.2-7.3,10.

### Compute — useful capability at comparable actual cost

- **Current status:** **measured E19 / head-training wall time only**; language efficiency and the <=50%-fine-tuning composition claim remain **proposed/long-term, NOT TESTED**.
- **Measurable signal:** native per-method preparation/warm-up, detector/router/key/copy/optimizer/replay cost, inference first-token/decode/p50/p95, cold load, peak allocated/reserved memory, actual frozen/trainable/stored weights and bytes, device-event elapsed seconds, wall seconds and GPU reservation. Report supported profiling FLOPs separately; event elapsed time is not measured busy-SM seconds or FLOPs.
- **Matched counterfactual:** fixed-capacity rank-24 and replay, common tokens/data and separately measured compute; E21 matched functional heads and development-locked compute comparison. Charge required shared cached passes to each standalone method; retain physical experiment total separately. Native greedy is not fairly compared with four-candidate energy selection unless candidate budget is matched.
- **Sealed test:** fixed context/tokenizer, same held-out prompts and answer limits, no test-selected depth/checkpoint; same permitted memory/budget and no competing GPU workload. Missing/incomplete seeds cannot be removed from costs.
- **Failure verdict:** gain requires extra weights, candidates, detector/backward work or wall time and does not survive comparable cost; reduced answer length masquerades as throughput; setup/routing is excluded. State quality-only/excess-cost or unmeasured cost, not efficient learning.
- **Measured caveat:** E19 feedback adaptation mean 0.07272894 seconds refers to tiny-head training only. Residual has 8,192 trainable weights but system inference includes 16,386 versus the single-head FT model's 8,194. Equal optimizer steps did not match end-to-end cost.
- **Proposed versus thesis gate:** E20 C limits B3 adaptation wall/device time and greedy p95 to <=1.25× named comparators with <=22 GiB peak; that is **capped overhead**, not a speedup claim. Master E8 requires equal/better capability at <=50% FT compute and >=90% retention. The proposed 24 GPU-hours is an **unapproved resource ceiling**, not a measured run cost. Analytical parameter bytes are not observed VRAM.
- **Graphic warning:** do not show “50% cheaper,” “24 GB fits,” “1.58-bit accelerated,” “unbounded,” or GPU-utilization/FLOP dials without attributed measurements for that exact system.
- **Evidence:** `NEW_AI/master-plan.md:43-44,103-107`; `REPOS/new-ai-e19/E19_REPORT.md:15-17`; E20 design §§4,7.3,9,12; `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md:98-100,217-219`.

### Adaptation — real held-out acquisition, not only lower training loss

- **Current status:** **measured E19 / classifier adaptation observed but acceptance failed**; pretrained language adaptation is **proposed / NOT TESTED**.
- **Measurable signal:** new B/C held-out token-weighted H/PPL and independent generated QA EM/F1; prequential before-update loss; invalid/repeated/truncated answers; general guard retention; all paired seeds and document counts.
- **Matched counterfactual:** frozen A0, L8/L24/R24; learnability control on development, then no threshold/epoch/LR retuning on final. Energy reranker must additionally beat same-pool likelihood, equal-size BCE confidence and shuffled energy labels.
- **Sealed test:** post-checkpoint immutable prose revisions with split-by-lineage/near-duplicate groups, rights/attribution record, locked human QA/aliases. Supplied-context QA tests comprehension, not acquisition of facts from unseen final pages. First creation date does not prove facts or copied prose were absent from pretraining.
- **Failure verdict:** new improvement absent on B or C; only training loss falls; a standard trainable control cannot learn (INVALID INSTRUMENT before unsealing); retrieval metadata, aliases or final revisions leak; better selection does not beat matched confidence; missing generation evaluation becomes a language-prediction pilot only.
- **Graphic warning:** show **“proposed conditional suffix PPL + grounded generation”** for E20, not a fabricated score card or AG News-as-LLM leaderboard. Model-card results and original-paper metrics are source-reported, not our reproduction. Fixed-context PPL is not directly comparable with unrelated tokenizer/context benchmarks.
- **Evidence:** `REPOS/new-ai-e19/PROTOCOL_E19.md:3-10,17-21`; `REPOS/new-ai-e19/E19_REPORT.md:13,17-19`; E20 design §§2,5,7-8,11-12.

### Two-model promotion / A-B freeze-swap — serving safety is separate science

- **Current status:** **long-term / NOT TESTED in E18/E19/E20.** E20's final checkpoint evaluation does not implement a serving swap, shadow learner, live rollback or autonomous promotion. Do not confuse corpus families A/B or adapter A0/B3 with **serving model A / candidate model B**.
- **Measurable signal (future design):** candidate improvement and retention at comparable native cost; zero unauthorized evaluator/serving mutations; model/config/router/state hashes; request-version consistency; failed/dropped/duplicated requests; promotion interruption and p95/p99 latency; total two-model memory/occupancy; successful rollback to exact prior version.
- **Matched counterfactual:** no-swap serving A; candidate B in shadow without promotion; single-model maintenance/update; identical approved checkpoint promoted with versus without the proposed swap mechanism. Each comparison needs the same load/request sequence and specified state/KV-cache handling. Swapping itself does not explain capability acquisition.
- **Sealed test:** candidate training cannot access release-test labels, aliases or outcomes. Use fresh release-test commitments for repeated promotion decisions or a separately justified reusable-testing protocol—continuous candidate search against one opened “sealed” set is selection leakage. A distinct sandbox load/fault-injection test evaluates atomic pointer/version changes, aborts, cache incompatibility, partial-file writes, bad schemas, late/in-flight requests, OOM and rollback. Production requests do not become self-approved training labels.
- **Failure verdict:** promotion based on energy, training loss or checkpoint presence alone; candidate below quality/retention/cost gates; state incompatibility; old weights/routes mutate in place; bad candidate cannot be rejected/rolled back; serving errors exceed predeclared SLO; release tests repeatedly query an exposed final set. Result is **DO NOT PROMOTE / keep A**, not a reason to edit a gate.
- **Required future gates:** quality gate + retention gate + cost/latency SLO + integrity/rollback tests + explicit human authorization. No numeric serving SLO or automatic-promotion acceptance protocol is locked in these sources; agree it before running a new experiment. A passing research result is necessary evidence, not sufficient deployment authorization.
- **Graphic warning:** render `candidate → sealed report → human release gate → conditional promote` with a return-to-A failure route. No solid automatic evaluator-to-serving arrow, “self-upgrading live” animation, or “rollback protected” badge without real exercised integration evidence.
- **Evidence:** `NEW_AI/master-plan.md:107,115-122,155`; `REPOS/new-ai-e19/PROTOCOL_E19.md:21` explicitly lists freeze/swap as untested; E20 design §§10-11 forbids evaluator mutation and does not contain a serving implementation. Future promotion checks here are **new proposed validation requirements**, not measured results.

## 3. Graph handoff — views and typed links

Use separate views so the implemented classifier is not visually upgraded into the proposed LM. No more than the requested 8–14 visible nodes per view.

### View A: historical E19, eight nodes

| ID | Label | Maturity / verdict | Evidence |
|---|---|---|---|
| `h_data` | Pinned AG News binary stream | measured E19 / scope-restricted | E19 protocol:7-10 |
| `h_base` | Hashing-feature linear classifier | measured E19 / baseline valid | E19 protocol:10; report:7,13 |
| `h_monitor` | 32-label error-feedback trigger | measured E19 / timing FAIL | E19 protocol:13; report:13 |
| `h_route` | Hard centroid route | measured E19 / routing weak | E19 report:15 |
| `h_adapter` | Zero-init linear residual | measured E19 / acquisition gate FAIL | E19 protocol:13,17; report:13 |
| `h_controls` | Frozen / schedule / random / full FT | measured E19 / comparisons available | E19 report:5-15 |
| `h_test` | Historical official test scoring | measured E19 / now exposed | E19 protocol:7-9,21; report:3 |
| `h_record` | Raw results / failed verdict | measured E19 / FAIL preserved | E19 report:13-19; master-plan:159-160 |

Suggested links: `h_data→h_base DATA`, `h_data→h_monitor FEEDBACK`, `h_monitor→h_adapter ALLOCATION`, `h_route→h_adapter SELECT`, `h_base/h_adapter/h_controls→h_test EVALUATE`, `h_test→h_record EVIDENCE`. Explicitly show the schedule/random comparator path into evaluation. The historical test has already been inspected; never display it as a fresh sealed E20 test. Arrow inclusion denotes the recorded experiment path, not a successful mechanism or serving runtime.

### View B: proposed future system, twelve nodes

| ID | Label / maturity | Validation hook / source | Boundary and failure route |
|---|---|---|---|
| `p_core` | Frozen pretrained LM / proposed E20 | A0/base identity, real fit; E20 §§4,11 | Model-update boundary; core mismatch → invalid/quarantine. |
| `p_energy` | Trained latent-energy refiner / proposed E21 | Energy-vs-direct test; EBM review §§10.2-10.4 | Inference only; NaN/quality/cost fail → bypass, never advertise as validated. |
| `p_direct` | Matched non-energy control / proposed E21 | Same functional weights/decoder, comparable measured cost | Experimental control, not a hidden ensemble contributor; unmatched budget → incomplete comparison. |
| `p_monitor` | Observed-loss / prefix-density monitors / proposed E20 | Calibration, causality, null/nuisance checks; E20 §§5.3,7.1 | No task IDs/future suffixes; invalid alarm → no justified expansion. |
| `p_router` | Prefix-only route / proposed E20 | Automatic/oracle-gap diagnostics; E20 §§5.2,6 | Never read answer/phase; route fail → failed system outcome, no oracle repair. |
| `p_growth` | Bounded cloned adapter store / proposed E20 | Count, clone identity, acquisition/retention; E20 §§4,6-7 | Only active child mutates; failure → retain immutable A0 and publish failure. |
| `p_replay` | Fixed LoRA / training-only replay comparators / proposed E20 | Equal processed-token accounting; E20 §6 | Separate static rank-24 arm; final/dev content in reservoir → invalid. |
| `p_release` | Promotion/rollback decision gate / long-term | Future quality/retention/cost + fault-test lock; §2 promotion row | Human release boundary; reject → keep serving A. |
| `p_two` | Serving A / shadow B freeze-swap / long-term | Future version/load/cache/rollback test | Serving mutation boundary; failed swap → rollback exact prior version. |
| `p_sealed` | Custodian-held final evaluator / proposed | E20 §11; data/QA/hash commitments | **Not currently sealed**; trainer access or repeated queries → quarantine/new final split. |
| `p_cost` | Native telemetry and cost record / proposed E20/E21 | Synchronized wall/device/inference/bytes; E20 §9 | Read-only observer; missing required cost → no efficiency verdict. |
| `p_publish` | Public evidence handoff / proposed future outcomes | Master-plan:122,160; E20 §11.8 | Publish raw/negative/status evidence after validation; absent record → no outcome badge. |

The E19 publication process is recorded as implemented in the master plan; this future-outcome node does not mean E20/E21 results already exist. Both future methods share an experiment view for context, **not a composed evaluated system**.

| Directed link | Type | Claim meaning and required guard |
|---|---|---|
| `p_core→p_energy` | PROPOSED-INFERENCE | Frozen context representation; no target/answer leakage; E21 only. |
| `p_core→p_direct` | CONTROL-INFERENCE | Same context/decoder; separate experiment arm, not energy ensemble. |
| `p_core→p_router` | PREFIX-FEATURE | Current input prefix only; QA demos excluded from routing; E20 only. |
| `p_router→p_growth` | SELECT | Route fixed for one document/answer; count routing loss, no task oracle. |
| `p_core/p_growth→p_monitor` | PREDICTION-FEEDBACK | Loss after observed continuation but before update; no implicit energy-calibration claim. |
| `p_monitor→p_growth` | CONDITIONAL-ALLOCATION | Two-block rule/cooldown/cap; evidence of an alarm, not evidence growth works. |
| `p_core→p_replay` | CONTROL-BACKBONE | Same frozen backbone, separate static rank-24 comparator; training-only reservoir, no B3 modification. |
| `p_replay→p_sealed` | CONTROL-EVALUATION | Score the immutable replay comparator alongside growth, not as rehearsal secretly feeding B3. |
| `p_growth→p_sealed` | IMMUTABLE-CHECKPOINT | One-way submission after training; no evaluator result used for adaptation. |
| `p_energy/p_direct→p_sealed` | CONTROL-EVALUATION | Independent immutable E21 arms, only after their own lock. |
| `p_core/p_growth/p_energy/p_direct→p_cost` | OBSERVATION | Attribute every required phase; telemetry may not mutate model/gates. |
| `p_sealed/p_cost→p_publish` | EVIDENCE | Raw measurements, exact scope, failures and costs; no absent-data fill. |
| `p_sealed/p_cost→p_release` | READONLY-REPORT | Potential future release input, not automatic production authority. |
| `p_release→p_two` | HUMAN-AUTHORIZED-PROMOTION | Future conditional edge; no operating swap claimed. |
| `p_two→p_release` | FAULT/ROLLBACK-REPORT | In-flight/version/cache failures; requires independent serving integration tests. |

There must be **no** `p_sealed→p_growth MUTATION`, `p_publish→p_sealed TUNING`, `p_energy→p_monitor CALIBRATED-STRESS` or automatic `p_two→p_growth SELF-TRAINING` edge in the implemented view. Each is either leakage, an unsupported calibration inference or a distinct long-term proposal requiring new controls. Do not add the E20-B scorer inside `p_energy`: it is a separately labelled finite-candidate selection annex, not that node's latent-descent mechanism.

## 4. Places a graphic can overstate the evidence

This checklist covers every proposed node/link above and the additional long-term claims in the master plan. For components added later, require the same claim→counterfactual→test→verdict record before displaying a result.

1. **“LLM running” over E19:** replace with “measured linear classifier”; the pinned LM is proposed, no tested GPU fit.
2. **Energy flow glowing into “correct answer”:** energy is not a correctness certificate; separate external task score from internal energy decline and matched direct controls.
3. **Novelty arrow labelled “needs learning”:** E18 separates nuisance novelty from task failure; observed feedback has label/token delay.
4. **Growth arrow labelled “stress caused the gain”:** E19 tied scheduled; capacity, replay and random controls belong visibly in the comparison.
5. **Frozen-core shield labelled “no forgetting”:** no backbone update is an invariant, not end-to-end retention; routes/keys/adapter outputs can change.
6. **“Zero-init” on E20 cloned slots:** label cloning accurately; immutable A0 is a reference, not a serving A/B swap.
7. **Router taking all prompt text/metadata:** specify current-context prefix; common few-shot demonstrations cannot define every route; answer/phase/date cues are forbidden.
8. **Replay box feeding feedback arm by default:** primary R24 is a comparator with reduced current-token training; adding it to B3 changes the method/budget.
9. **Finite candidate selector drawn as EBM iterative reasoning:** it normalizes only over a pool; do not report candidate energy as full-text PPL or use it to satisfy M1.
10. **FiUni/HESTIA/TRACE logos implying reproduced baselines:** this E20 is a declared proxy; mathematical components/model classes/data and licensing differ.
11. **A lock icon because a protocol PDF exists:** test data, QA aliases and access credentials must actually be isolated; a different agent/process using the same account is not a security boundary.
12. **Evaluator-to-training feedback loop:** opened final examples/scores cannot tune thresholds, routing, head negatives, checkpoint selection or acceptance gates; fresh experiment/split required after exposure.
13. **Two models ↔ promotion displayed as active:** unimplemented integration; require signed candidate/version, human authorization, fault tests and rollback evidence.
14. **“Cheaper/faster” from 0.073-second head time or equal steps:** native end-to-end costs are missing for that claim; disclose active/stored weights and all detector/backward/router work.
15. **24 GPU-hours / 22 GiB / weight bytes shown as telemetry:** these are proposed ceiling/target/analytical values; use “planned,” not measured meters. Never fill unrun charts with illustrative numerical outcomes.
16. **Ternary, cold experts, paging, pruning, self-play, observer or quantum nodes shown operational:** separate long-term/static view; each master mechanism has its own test. No prototype LoRA result validates the composition or unbounded growth.
17. **One composite model score across toy detectors, AG News, PPL and QA:** impossible units/model-class comparison; use per-experiment control deltas and separate views.
18. **A green “PASS” because code, plan, source review or publication exists:** show engineering evidence and scientific verdict separately; E19's failed gate remains first-class.
19. **“Independent peer review complete”:** the E20 review worker hit provider quota before inspection; citation/arithmetic/self-consistency checks ran, not a second peer review.
20. **Promotions repeatedly optimized against one released final set:** a research final is one-use for selection; an ongoing release gate needs fresh custody/commitments or an explicitly justified reusable-testing scheme.

## 5. Minimum validation of the hub representation (content tests, not code here)

- Every visible node/link has a maturity, experiment/model class, evidence path/line, gate and failure route. Unknown evidence remains NOT TESTED; never inherits a neighboring node's pass.
- “preregistered-unrun” requires a real pre-outcome lock reference and custody proof. Current E20/E21 must display **proposed**. A lifecycle transition is an explicit signed record, not automatic promotion because a file appears.
- A historical failed gate remains failed after UI redesign. At least one E19 detail displays the zero paired timing edge, missed 65% new-accuracy gate and classifier disclaimer.
- Proposed numerical targets are labelled targets; measured charts use raw rows/counts with units, all seeds and the same model/task class. No invented overall score or filled-in unrun outcome.
- E20 routing/adaptation and E21 latent-energy/direct controls are not drawn as a measured combined runtime. View A has eight nodes, View B twelve; additional long-term details are a separate drill-down rather than a fake operational monolith.
- The sealed-test boundary has no arrows carrying final scores, examples or labels back into training/policy selection. Non-mutating cost observation is separate from model-control authority.
- Promotion arrows terminate at an explicitly long-term human gate with an reject/rollback route; no research PASS is labelled deployment-ready.
- Static proposed diagrams use dashed/unanimated edges and a legend; green signifies a specified passed measurement only. Grey/dashed is not a hidden failure, and red/amber negative findings are not removed for visual polish.
- Lead compares node IDs with Energy Model Engineer's architecture draft before authoring the graph; this overlay provides semantic IDs, not a verified Archify schema/API.

## 6. Sources and deliverable state

Paths are relative to `C:/Users/Majied/.kr8` unless noted. Citations in the body identify exact ranges or section anchors; implementation of new scientific controls is not inferred from a document title.

- `NEW_AI/master-plan.md:29-48,64-107,115-141,155-161`: hypotheses, original gates, sandbox/human checkpoints, interpretation limits and E19/E21 status.
- `REPOS/new-ai-e19/PROTOCOL_E18.md:3-21` and `E18_REPORT.md:3-19`; raw `results/E18/summary.json`: immutable detector design/outcomes, not language learning.
- `REPOS/new-ai-e19/PROTOCOL_E19.md:3-21` and `E19_REPORT.md:3-19`; raw `results/E19/summary.json`: immutable classifier controls, failed timing/acquisition gates and measured head costs.
- `RESEARCH/NEW_AI_E20_EVAL_DESIGN_2026_10_05.md`, **draft/proposed**, §§4-12: pinned real-LM/data/control/threshold/metric/cost design and seal prerequisites. Full text published as event `89e79bd046657e8107633ab2f54278bb77f02bfc273f8d36d28b42a46966e695`, summary `fd46fa7a07b4b8cc98fd92f90baf8368881333f78ca9419743d332e750f088a2`; both read back exactly in this thread.
- `REPOS/new-ai-e20-eval/RESEARCH/E20_INPUT_AUDIT.json`: independent CPU arithmetic and source hashes; classifier timing means/pairs and paired-AUROC recalculation. Measured audit cost 0.2335849000 CPU seconds; no training rerun. Its master-plan hash refers to the earlier read before later append-only log entries, not a claim that the current expanded master has identical bytes.
- `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md:45-55,76-102,165-231`: pinned static source review and EBT-inspired/direct-update proposal, not replicated outcomes. Original sources and commit/file/line links are in that review.
- Lead's source-of-status: `NEW_AI/master-plan.md:161`, keeping genuine latent mechanism in proposed E21, separate from E20; no approved E21 acceptance protocol is asserted here.

**Delivered content only.** No code, website, GPU, lock, rights clearance, dataset collection, model-fit result or serving deployment was produced by this overlay. It does not approve a compute enlargement or replace historical gates. The pending owner decisions are the E20 benchmark/24-GPU-hour ceiling/annotation scope and eventual E21 budget/gates; routine graph implementation belongs to the lead.
