# NEW AI — Master Plan & Experiment Log

**Project:** New AI (channel `49e9dd8f`, repo `new-ai`)
**Owner:** majied5090 · **Plan author:** Generalist
**Created:** 2026-09-29 · **Status: ACTIVE — E19 real-text classifier timing gate failed; full thesis not demonstrated**

This is the running master document. Every decision, result, and status change gets appended to §8 (Log). The experiment battery in §3 is **pre-registered**: thresholds are fixed before runs; changing a threshold means a new experiment ID, never a silent edit.

---

## 0. Status board

| Item | State |
|---|---|
| Source absorption (framework paper, RSI conversation log, EBM+quantum guide) | DONE 2026-09-29 |
| Master plan + pre-registered experiment battery | DONE 2026-09-29 (this document) |
| Phase 0: repo scaffold + harness + toy task suite | BUILT, but original T2 fails learnability gate; corrected synthetic instrument in E16 |
| E1–E4 (core mechanism tests) | RUN; mixed/negative, see raw repo results and independent audit |
| E5–E7 (memory, pruning, observer) | NOT STARTED |
| E8 (composition / headline test) | NOT STARTED |
| E15 ten-round claim | RUN; one seed, 0/10 wins against frozen, 0/10 retention-gate passes; see independent audit |
| E16/E17 corrected synthetic diagnostic | RUN locally on five seeds each; E16 adapter failed, E17 exploratory LR correction worked on fresh seeds; not EBM/LLM |
| E18 input-only trigger audit | RUN on five fresh seeds; paired label-only shift AUROC 0.5, harmless input shift AUROC 1.0; validation false-alarm gate missed 5.078% > 5%; outcome feedback alerts after 32 labels. No adapter training in this round |
| E19 real-text causal-timing pilot | RUN on five AG News seeds: feedback vs scheduled timing advantage 0.00 pts; new-topic 59.15% < 65% gate; **FAILED**. Real text, but hashing-feature linear classifier, not LLM/EBM/FiUni. Raw/report in `REPOS/new-ai-e19/` |
| Publication | Corrected GitHub Pages site at `https://majieddd.github.io/new-ai-dashboard/`; E19 results via PR #4 (`e627574`) and measured visualizations via PR #5 (`3a416b5`), deployed bytes verified. Site generator now fails if a new EXX summary lacks its own entry; every future EXX must ship raw outcomes, source, pass/fail, and same-class visuals. Research branch `research/e19-visuals` through `9c674ec`; relay source push remains unavailable. E20 needs new held-out task and strong routing/replay controls |

---

## 1. What we are building (thesis, one paragraph)

A **self-assembling model**: a small frozen "cortical core" whose inference is iterative energy minimization (EBM phase-locking) rather than a single feed-forward pass; whose persistent high energy on novel inputs triggers the physical instantiation of new parameters (zero-initialized sprouts or grafted frozen expert layers from cold storage); which then thaws only the new parameters until system energy drops. The substrate is 1.58-bit ternary ({-1,0,1}) so forward passes are integer additions — fast, tiny, CPU-runnable — and a tiered VRAM/RAM/NVMe memory topology with autonomic paging supports unbounded logical growth. The claim to be tested: **this system gains capability over time without retraining the core, retains old capabilities (no catastrophic forgetting), and does so at lower compute cost than fine-tuning equivalents.**

## 2. Mechanism inventory — paper claim → testable prediction

The framework paper mixes metaphor with mechanism. Each row separates the measurable content from the analogy. "Metaphor-only" rows are flagged, not tested as stated.

| ID | Paper claim (paraphrased) | Testable prediction | Verdict if it fails |
|---|---|---|---|
| M1 | EBM phase-locking: iterative energy minimization finds answers a single forward pass misses | On hard instances, K iterations of latent refinement beat K=0 by ≥5 pts; converged energy correlates with instance difficulty (Spearman r≥0.6) | Energy-as-reasoning is not better than feed-forward on these tasks → drop M1 or restrict to task class where it wins |
| M2 | Persistent high energy triggers growth that adds capability without retraining | After OOD shock: grown model beats frozen-core-only by ≥10 pts on new data AND beats a random-trigger control at matched trigger rate (rules out "just more parameters") | Growth-as-learning is dead as specified; keep only grafting or abandon |
| M3 | Zero-init makes new layers enter mathematically invisible (function-preserving) | Property test: output identity at t=0 for additive residual injection (trivially true by construction — verified, not hypothesized). Real hypothesis M3′: thawing recovers new capability with ≤2 pt drop on old tasks | Catastrophic interference kills the growth approach → need isolation architecture (separate heads/routing) |
| M4 | Grafting frozen expert layers from cold storage lowers energy in their domain | Correct-domain graft beats random-layer, zero-init, and no-layer controls by ≥5 pts in-domain with ≤1 pt cross-domain degradation; stream latency measured, not assumed | Knowledge grafting is dead; sprouting-only remains |
| M5 | Ternary 1.58-bit substrate: INT8-add forward pass → speedup + ~90% compression at acceptable quality | On our hardware: ≥2× throughput vs FP32 at ≤2 pt accuracy loss (post-hoc ternarization, then QAT if time); weight bytes ≈ ⅛ of FP32 | Substrate claim overstated for this scale; keep FP16 core and revisit at larger scale |
| M6 | Tiered VRAM/RAM/NVMe memory with utility-based placement keeps accuracy stable when working set > VRAM | Accuracy within 1 pt of all-in-VRAM baseline under a >VRAM working-set stream; p95 latency bounded; beats naive OS allocation on fragmentation/latency | Engineering problem, not science — iterate implementation |
| M7a | Autonomic self-pruning: exact zeros let the model sever connections and shrink without losing intelligence | Pruning sweep finds ≥30% size reduction at ≤1 pt loss somewhere on the Pareto curve | Ternary sparsity is too coarse to prune usefully |
| M7b | SAT/combinatorial search over ternary configs beats gradient descent (the "FPGA" claim) | **Metaphor-heavy — exploratory only.** On a small discrete task objective, exhaustive/SAT search over a tiny sprouted layer finds a config ≥ gradient-descent result. Labeled exploratory; failure is expected and informative, not fatal | Claim stays metaphorical |
| M7c | Synthetic self-play: model generates its own training data via parallel rollouts | Self-generated data improves held-out accuracy vs no-self-play control at matched compute, with diversity gate preventing distribution collapse | Data RSI dead without external grounding |
| M7d | Frozen observer evolves the growth hyperparameters (threshold, window τ) | Adaptive threshold policy has lower regret than best-fixed-threshold across a difficulty ramp; VRAM thrash rate not worse | Keep fixed thresholds; observer is overhead |

## 3. Pre-registered experiment battery

**Environment:** Windows 11, RTX 5090 Laptop GPU (24 GB), torch 2.11.0+cu128 (`C:/Users/Majied/jev-alt-bench/envs/main`), Python 3.14 system. All toy experiments fit on CPU or one GPU; total Phase 1–2 cost ≈ a few GPU-hours, not days.

**Toy task suite (built in Phase 0):**
- **T1 — 2D cluster mapping:** circle/square/triangle point clouds → label. The paper's own validation protocol (nurture on circle, shock with square).
- **T2 — sequence rule learning:** small-alphabet rules (parity, copy, +1 mod n) as a "language-like" task; OOD = new rule family. This is where the system must actually *learn something useful*, not just fit geometry.
- **T3 — combinatorial puzzles:** small constraint-satisfaction instances with known difficulty ordering, for testing iterative refinement (M1).

**Arms and controls are fixed per experiment below. Seeds: 5 per arm (E1–E4), report mean ± std. Every run logs seed, config hash, hardware, wall-clock, all metrics to `results/` in the repo.**

### E0 — Harness & baselines (Phase 0)
Build: task suite T1–T3 with fixed train/test splits; logging harness (JSONL per run); baseline models (frozen core only, static fine-tuned same-size). **Exit:** all three tasks solvable by the frozen core at >90% on in-distribution data; baselines recorded.

### E1 — M1: iterative energy refinement vs single pass
- **Design:** T3 + hard subset of T2. Arms: K=0 (single forward), K=4, K=8 latent-refinement iterations (gradient/Hopfield-style updates on z given x).
- **Metrics:** accuracy@K; Spearman(converged energy, instance difficulty); wall-clock per answer.
- **PASS:** K=8 beats K=0 by ≥5 pts on hard set AND r≥0.6. **FAIL-FALSIFIED:** no iteration advantage beyond noise → M1 dead for these task classes. **INCONCLUSIVE:** advantage only on one task class → restrict claim to that class, name it.

### E2 — M2/M3′: seed-organism distribution shift (headline mechanism test)
- **Design:** T1 and T2. Nurture core on cluster/rule A until energy stabilizes; freeze core; shock with B. Arms:
  - **A** frozen core only (no growth)
  - **B** growth + localized thawing (the paper's protocol)
  - **C** random-trigger control — same number of sprouts, triggered by noise at matched rate (isolates "more parameters" from "stress-timed parameters")
  - **D** static model fine-tuned on A+B with equal parameter budget (upper-bound reference)
- **Metrics:** post-shock accuracy on B per arm; retention = pre-shock accuracy on A minus post-shock accuracy on A (catastrophic interference); trigger precision/recall against true OOD events.
- **PASS:** B > A by ≥10 pts on B AND B's retention drop ≤2 pts AND C ≈ A. **FAIL-FALSIFIED:** B ≈ C → the timing is not doing work; growth alone explains it (still interesting, but M2 as specified is dead). **INCONCLUSIVE:** B < D by a wide margin with poor retention → growth helps but forgets; route to isolation-architecture redesign.

### E3 — M4: knowledge grafting
- **Design:** T2 with domain-specific experts (expert trained only on rule family R). Arms: correct-domain graft, random layer same size, zero-init layer, no layer. Graft inserted mid-stack per the paper's interleaving scheme.
- **Metrics:** in-domain energy/loss; cross-domain degradation; measured stream latency per layer at toy scale (extrapolation to real sizes stated explicitly as extrapolation).
- **PASS:** correct graft beats all controls by ≥5 pts in-domain with ≤1 pt cross-domain cost. **FAIL-FALSIFIED:** random layer ≈ correct graft → the *content* of the expert isn't being used; only capacity matters.

### E4 — M5: ternary substrate on our hardware
- **Design:** train T2 model FP32 → (a) post-hoc ternarization (round to {-1,0,1} + per-layer rescale), (b) quantization-aware training if time permits. Measure GPU and CPU throughput.
- **Metrics:** accuracy delta vs FP32; wall-clock throughput ratio (GPU, CPU); weight file bytes.
- **PASS:** ≥2× throughput at ≤2 pt loss AND ≈90% weight compression verified by file size. **FAIL-FALSIFIED:** >2 pt loss post-hoc → substrate claim doesn't hold at this scale with post-hoc quantization; QAT result decides whether it's a training-time problem (retry) or a capacity problem (M5 dead at small scale).

### E5 — M6: tiered memory under working-set pressure
- **Design:** T1/T2 stream whose active parameter set exceeds VRAM. Arms: utility-based placement vs naive OS allocation vs all-in-RAM fallback.
- **Metrics:** accuracy stability vs all-resident baseline; p95 latency; fragmentation events.
- **PASS (engineering):** within 1 pt accuracy, bounded p95, fewer stalls than naive. This is an implementation test — iterate freely, no pre-registration beyond metrics.

### E6 — M7a: self-pruning sweep
- **Design:** on E4's ternary model, prune fractions of exact-zero weights (0/25/50/75% of zeros), re-measure T1+T2.
- **Metrics:** size–accuracy Pareto curve; inference speedup at each point.
- **PASS:** some point with ≥30% size reduction at ≤1 pt loss.

### E7 — M7d: observer threshold adaptation
- **Design:** difficulty ramp on T2 (easy→hard rule families). Arms: adaptive frozen observer adjusting (threshold, τ) vs grid of fixed thresholds; oracle-threshold policy as reference.
- **Metrics:** regret = gap to oracle policy across the sweep; thrash rate (growth events per unit time).
- **PASS:** adaptive beats best-fixed by ≥5% relative regret without worse thrash.

### E8 — Composition: is this a better way to think? (headline)
- **Design:** T2 task stream with growing difficulty, fixed total compute budget. Arms: (i) standard feed-forward + fine-tune on new data as it arrives; (ii) full system (EBM inference + stress-growth + ternary where E4 passed). 
- **Metrics:** capability curve over the stream at matched cumulative compute; retention; cost per capability point (GPU-seconds per accuracy pt gained).
- **PASS:** arm (ii) reaches equal-or-better final capability at ≤50% of the fine-tuning compute, with retention ≥90%. This is the test that decides whether the *paradigm* — not just one mechanism — is worth scaling.
- **Safety framing (fixed before runs):** all self-modification confined to sandboxed parameter space; the observer cannot modify its own code, the evaluation harness, or the metrics pipeline; human checkpoint between stream segments; no network access from any model component.

### E9 — M7b: SAT search over ternary configs (exploratory)
- **Design:** tiny sprouted layer on a discrete task objective; exhaustive/SAT search vs gradient descent. Labeled exploratory; expected to be informative, not decisive.

### E10 — Optional: quantum annealer cross-check (from the EBM+quantum guide)
D-Wave Leap free tier (≤1 min QPU/month): sample our energy function's landscape on a small T3 instance via QUBO mapping and compare found states vs classical relaxation. Cheap, optional, clearly separated from the core battery — it tests whether annealing finds lower-energy answers than our iterative refinement, not whether the model works.

## 4. Pre-registration rules (fixed before any run)

1. Thresholds in §3 are frozen at Phase 0 completion. Any change = new experiment ID with a note in §8; old results stand as-is.
2. Seeds: 5 per arm for E1–E4, fixed seed list published in the harness config. Report mean ± std; single-seed runs are labeled pilot and never count toward PASS/FAIL.
3. Every run writes `results/<exp>/<seed>_<arm>.jsonl`: seed, config hash, hardware string, wall-clock, all metrics, git commit of the code that produced it.
4. Negative results are first-class outcomes: each experiment's FAIL-FALSIFIED branch is a valid, publishable conclusion — "mechanism X does not work as specified" is exactly what we need to know.
5. No post-hoc metric selection: metrics listed per experiment above are the only ones that count for PASS/FAIL; anything else is labeled exploratory.
6. **Publication operation (added 2026-10-05; does not alter a preregistered outcome gate):** every new EXX session gets a separate result section and raw/source/protocol downloads on the live website, a within-task control visualization showing capability, retention, paired seeds, and actual compute/weight costs where measured, then desktop/mobile and live-byte verification before announcing publication. The generator's `check_publication()` rejects unrepresented new `results/EXX/summary.json` files. Do not combine unlike tasks or model classes on a common performance axis; see `REPOS/new-ai-visuals/SITE_PUBLICATION_CHECKLIST.md`.

## 5. Interpretation ladder (what outcomes mean)

- **PASS on E1+E2** → energy-based reasoning + stress-growth both work in isolation → proceed to composition (E8) with confidence; scale task difficulty.
- **E1 fails, E2 passes** → growth works but iteration doesn't add value → system becomes "feed-forward core + stress-growth"; M1 shelved.
- **E2 fails on the C-control comparison** → more parameters explain everything → the *timing* claim (M2) is dead; only capacity matters. This is a genuinely important negative result: it means the Free-Energy-Principle framing adds nothing measurable over "add layers when you see OOD data."
- **E4 fails post-hoc but passes QAT** → substrate works, needs training-time commitment → keep ternary as a Phase 2 decision.
- **E8 passes** → the paradigm is real at toy scale; next step is scaling T2 to genuine language-like tasks and reporting cost-per-capability honestly.
- **E8 fails** → mechanisms work in isolation but don't compose → the architecture, not the parts, is wrong; redesign integration (routing/isolation) before any further mechanism work.

## 6. Risks & known failure modes (honest list)

1. **Energy-head gaming:** E can be minimized without task success (output collapse). Mitigation: calibrate E against a ground-truth proxy on held-out data *before* it is used as a trigger; monitor for degenerate solutions every run.
2. **Hopfield capacity limits:** classical associative memory stores ~0.14N patterns; modern variants improve this but "phase-locking = the answer" needs empirical validation — that is exactly what E1 measures, and its failure mode is bounded (we find out on toy tasks, cheaply).
3. **BitNet quality gap at small scale** is documented in the literature; post-hoc ternarization loses more than QAT. If E4 fails on accuracy it is a real finding about the substrate claim, not an implementation bug — do not "fix" it by silently switching to FP16.
4. **Catastrophic forgetting** is the classic killer of continual growth; E2's retention metric exists specifically to catch it early.
5. **Self-play distribution collapse (M7c):** generated data can degenerate into a narrow distribution; diversity gate + held-out validation are mandatory before any self-generated data counts as training signal.
6. **Metaphor contamination:** the paper uses "phase-locking," "crystallization," and "metabolism" as if they were mechanisms. This battery deliberately separates each metaphor from its measurable content (§2) so a failed test tells us something specific instead of "the biology analogy didn't work."
7. **Scale gap (the big one):** everything in Phase 1–2 is toy-scale. A PASS at toy scale licenses *more testing*, never the claim that this works for real LLMs. The plan says so explicitly wherever it extrapolates.

## 7. Hardware & environment

- Windows 11, Intel Core Ultra 9 275HX, RTX 5090 Laptop GPU (24 GB VRAM), 64 GB RAM
- torch 2.11.0+cu128 at `C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe` (CUDA verified)
- System Python 3.14; node available for any JS-side tooling
- Repo: relay-hosted `new-ai` (`https://latechllc.communities.buzz.xyz/git/844d.../new-ai`) — **push from agent session currently blocked** (git credential helper returns no credentials); deliverables flow via canvas + chat attachments until that is fixed
- Local working copy: `C:/Users/Majied/.kr8/NEW_AI/`

## 8. Log (append-only)

- **2026-09-29** — Plan authored by Generalist from three sources: framework paper ("A Theoretical Framework for Dynamic Architecture Expansion via Ternary Energy-Based Models"), the full RSI conversation log (the Google Doc; 27 pages, absorbed in full), and the EBM+quantum integration guide. Mechanism inventory M1–M7d, experiment battery E0–E10, pre-registration rules, interpretation ladder, risk list all drafted. Awaiting owner approval to start Phase 0.
- **2026-09-29** — Environment verified: torch 2.11.0+cu128 + CUDA on RTX 5090 confirmed in `jev-alt-bench/envs/main`. Git push from agent session blocked (credential helper no-op); flagged to owner.
- **2026-10-03** — Independent audit posted in the New AI thread and saved to `OUTBOX/NEW_AI_INDEPENDENT_AUDIT_2026_10_03.md`. E15 ten-round claims are unsupported; old results retained. Corrected instrument created in `REPOS/new-ai-e16/` (new branch/worktree, not original master): sequence-position one-hots, explicit rule cue, unique sequence-disjoint train/val/test, oracle and isolation tests, plus E16 and E17 raw five-seed GPU results. E16 100/12.01% old/new for scheduled adapter (failure); E17, after changing adapter LR post-inspection and running five fresh seeds, 100/100% (exploratory), vs naive full fine-tune 14.16/100%. Equal optimizer steps, not matched measured compute; simple task cue hard-routes the adapter. Protocol and caveats in `REPOS/new-ai-e16/PROTOCOL_E16_E17.md`. No claim that energy-triggered growth, ternary inference, two-model swap, or a language model works. Next gate: E18 calibrated trigger versus matched random/scheduled controls with held-out data, then a separate trained-energy test.
- **2026-10-03** — Corrected research website published from `majieddd/new-ai-dashboard` PR #1 (Pages commit `0854c9e`). One rounds-by-configuration SVG; E15 0/10 wins and 0/10 retention gate plainly shown, E16 failure and E17 exploratory correction separate, E14 carefully scoped; raw JSON and runner/test source downloadable. Six repository tests pass. Helium browser verified the live URL at desktop/mobile widths with zero new runtime errors; fetched live `index.html`, `data/e15.json`, `data/e17.json`, and `source/run_e17.py` are byte-identical to Pages commit. Commits carry Agent-Name, Agent-ID and Agent-Owner trailers; agent email is the non-deliverable `.invalid` address derived from its public ID, not the owner's personal email. This closes the website/instrument milestone, **not** the self-evolving-LLM research goal.
- **2026-10-04** — Targeted original-paper review recorded in `RESEARCH/NEW_AI_PRIOR_ART_AND_TRIGGER_LIMITS_2026_10_04.md` and source `REPOS/new-ai-e18/PRIOR_ART_E18.md`: SEMA (2025), MaRS (2026), SCALE (2026), Meta-UCF (2026), Li et al. energy-based continual learning, and Nalisnick et al. OOD likelihood limitations already cover significant proposed components. E18 was preregistered before its outcome run in `REPOS/new-ai-e18/PROTOCOL_E18.md`, executed across seeds 31,37,41,43,47, and committed at `28779f9`. Exactly paired X with changed labels yielded input-only AUROC 0.5; a harmless covariate shift got categorical-NLL AUROC 1.0 with 100% classifier accuracy; error-feedback alerts the actual rule shift after 32 observed labels. **Calibration gate miss:** validation FPR 5.078% against ≤5%, though held-out old test mean was 4.727%. No growth, trained EBM, or language model was tested. Nine unit tests passed; full results in `results/E18/summary.json` and `E18_REPORT.md`. E18 isolates a necessary detector limitation; the earlier planned trigger-versus-random/scheduled causal comparison is deferred as E19, not silently counted as passed. Website PR #2 merged to Pages commit `ddfe739`; six live artifacts were byte-identical to that commit and Helium desktop/mobile checks showed zero runtime errors or horizontal overflow.
- **2026-10-04 (post-E18 literature update)** — Found especially close task-free LLM prior art *after* E18 finished: FiUni (Han et al., August 2026, Fisher/K-FAC-guided detection and LoRA subspace reuse/expansion), Le et al. UAI 2026 density-guided adapter routing, and AgentCL controlled transfer streams. These did not influence the locked E18 protocol; they must shape E19 baselines/streams. Source update `ee885bd`, website PR #3 / Pages commit `33bbeec`; live HTML, raw E18, prior-art notes and generator byte-identical to the commit. Helium desktop/mobile checks passed without overflow or runtime errors.
- **2026-10-05** — E19 preregistered as a *linear real-news-text pilot*, not an LLM or FiUni reproduction (`REPOS/new-ai-e19/PROTOCOL_E19.md`, protocol commit `4f23317`). Dataset-only duplicate discovery added before outcome code ran; 10 train/test collisions and 151 repeated train texts removed before split. Runner/tests at `ad1aa2d`; five locked AG News seeds ran on RTX 5090, raw record `results/E19/summary.json`, interpretation `E19_REPORT.md`, source/report commit `0cdc379`. Feedback fired after 32 labels on every seed and exactly tied scheduled on balanced accuracy (74.66% vs 74.66%, required ≥2-point edge); feedback new-task accuracy 59.15%, below ≥65%; random 74.11% and full fine-tune 78.65% balanced. The preregistered causal timing gate **FAILED**. 13 tests green. Website PR #4 merged at `e627574`, live HTML/raw JSON/report/runner byte-identical to that Pages commit. Still no competitive LLM; E20 must address the weak input router, a strong replay comparator and a *new* held-out task before further model-size claims. Researcher model-update draft requested but remains owner-review-only; no delegation assumed.
- **2026-10-05 (website visualization iteration)** — Owner requested that each EXX session update the actual site with meaningful visuals of model performance. Branch `research/e19-visuals` at `9c674ec` adds an E19 five-seed old/new accuracy versus retention scatter, a paired timing-advantage chart and a data-driven routing-coverage graphic, plus observed adaptation time and weight counts; all derive from the published raw JSON. Feedback still ties scheduled, so the failed gate remains visible. The historical E15 synthetic round chart stays separate rather than making an invalid cross-task model score. Added `SITE_PUBLICATION_CHECKLIST.md` and a build guard to reject any future EXX summary lacking a site entry. 15 tests pass; local and live Helium desktop/mobile checks show three SVGs, no body overflow and no runtime errors. Website PR #5 merged to `3a416b5`; live `index.html`, E19 raw JSON, generator and checklist matched that commit byte-for-byte after Pages built. This is a publication/interpretability improvement, not a new model result.
- **2026-10-05 (original-source EBM review, no outcome)** — Energy Model Engineer inspected pinned original code and produced `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md` plus `NEW_AI_EBM_SOURCE_MANIFEST_2026_10_05.json` (five repositories, 26 source records; artifact existence and key EBT/mini-AGI call paths independently checked). mini-AGI's inspected predictor uses recurrence/token CE/halting, not explicit candidate energy descent; EBT implements a scalar energy and candidate-gradient updates, while IBC/JEM use distinct conditional/density constructions. Three source trees are Apache-2.0, mini-AGI MIT; Du–Mordatch's release has no tracked license. Proposed frozen-pretrained-LM scalar-energy versus equally sized direct-update head is **new method-inspired work**, not EBT replication or proof. Kept it as a separate, unrun E21 mechanism track (`buzz://issue?id=0e554492d915f3f04ea51986245d8cc8b321ef9d647e152a19e2407565dd6fb7&owner=844d344115ac6b7717969528a7b3c3e31bb45acf82383b49247e6cec8ba9fc34&d=new-ai`) rather than mixing it into E20's task-free routing gate. Protocol, dataset, fresh sealed test, compute budget and owner-approved thresholds remain open; E20 outcomes have not begun.
