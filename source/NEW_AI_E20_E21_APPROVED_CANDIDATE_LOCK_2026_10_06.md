---
title: "E20/E21 approved preparation and prospective candidate language lock"
tags: [new-ai, e20, e21, evaluation, prospective-lock, custody]
status: draft
created: 2026-10-06
revision: "0.1"
---

# Approval is recorded; outcome execution is not yet released

Author: Evaluation Scientist. Delegator: Orchestrator; execution/publication lead: Cloud AI Generalist. This is a NEW additive document in the existing independent worktree, `research/e20-independent-design`, historical base `0cdc379b2cd43d24780318becf9cae55af26c814`. No historical protocol, result, reviewer snapshot or readiness checker is replaced. Candidate fields are prospective, not a completed seal or a language result.

## 1. Authority and exact approved inputs

Owner event `875101f24904db17a0c2b5f9bb0592d3a9077e01ce5be85590fb77dd5dcd7bd3`, 2026-10-06 11:53:13 UTC, author `3bdc8e034a4b43aa89608e225f64222b9769d20405bf1b0d80ab7f86cb2b9c40`, says `@Orchestrator approved, continue`. Routed implementation brief `e450a2cb00a94431f16da7245bee4e49c70033ba516f0e46dfa4cdc9c3fec019` expressly interprets the approved packet and preserves the missing-custodian boundary. Exact relay events are retained in the public-only audit receipt. The approval is NOT an appointment of a person/service or proof of resource use, rights or custody.

Original decision sheet r1.0 remains byte-pinned: `RESEARCH/NEW_AI_E20_E21_OWNER_DECISION_SHEET_2026_10_06.md`, SHA-256 `4aa92eda05be3bfd6e5c9d6ff2717207f1339996a6f93293bdbb5fec6e9a3b31`. Its prior undecided wording is historical; this additive record changes the preparation state without rewriting the original request.

| Field | Approved candidate-lock input |
|---|---|
| E20 scope | Full pretrained `HuggingFaceTB/SmolLM2-1.7B` at `effd688a12921b4cc83e3312b6feb579f70f9c71`, fresh English Wikipedia prose plus grounded QA; language/QA proxy, NOT FiUni/TRACE reproduction. NLL-only remains a fallback requiring explicit pre-outcome disposition, not a full-study PASS. |
| E20 allowance | 24 exclusive GPU-hours TOTAL, with development/profile at most 1 hour INSIDE that total; no additional 1-hour grant. No borrowing from E21. |
| E20 curation | 192 train / 64 dev / 512 final human-verified QA and the original fresh-prose/date/lineage quotas. Permission to prepare these is not completed annotation or per-article rights clearance. |
| E20 protocol | Original design SHA-256 `54c92dc486639830711307cb4f00710639440a9ba21b396ef3ee49c08ef8bf7f`; ten paired seeds and eight arms F/L8/L24/R24/S3/U3/B3/D3. Adopt the sheet's exact V/A/T/D/C/E nominations as candidate inputs, including its separate reranking annex. No numerical rewriting. |
| E21 scope | `HuggingFaceTB/SmolLM2-360M` at `f8027fd0eaeea54caa13c31d31b9fdc459c38b49`; frozen-readout scalar-gradient versus matched direct recurrence, independently trained one-step and frozen controls; clean-room adaptation, NOT EBT reproduction. |
| E21 allowance | 4 exclusive GPU-hours TOTAL, with at most 1 development/profile hour INSIDE that total. E20 first; no overlapping GPU windows. |
| E21 prospective thresholds | Unchanged M1: hard K8–K0 accuracy gain ≥5 percentage points AND raw converged-energy/difficulty Spearman rho≥0.6. Candidate additional thresholds: ≥0.02 nats/token versus BOTH direct controls, positive paired NLL gain in ≥4/5 seeds, ≥2-point generation gain, ≤2-point old-domain loss. Five paired seeds are exploratory; no significance/power claim. |
| Final custody | Accepted REQUIREMENT: named separate principal or off-host custodian with actual denied-read canaries and privilege/key/mount review. No accepted custodian/access arrangement retrieved; no final content/keys opened or created. |

## 2. Newly specified E21 fields — evaluator proposal, not implied owner choices

The approved packet expressly left these fields unspecified. They are now concrete PRE-OUTCOME nominations for curation/implementer/lead review. They are not retroactively owner-approved facts, not newly implemented software, and not excuses to drop a control or extend 4 hours. In particular, the NEW human-curation workload below needs the owner's specific disposition; do not ask again for generic study or compute approval.

### Quantities, domain and independence

Nominate **128 new-domain training QA**, **64 development QA (32 new + 32 old)**, and **512 final QA (256 new + 256 old)**; one QA per independently grouped page/source lineage. Of the 256 new final items, nominate 128 essential-hard and 128 lower-depth items. Total new E21 human-verified QA workload is 704 items. These are quotas to commission, NOT collected items or an annotation-time estimate. Train on the new-domain pool only; the old stratum measures change versus the frozen pretrained readout on a separately held-out matched English-prose distribution. This old stratum is an operational proxy, not proof of retention on the full pretraining distribution.

Use fresh English grounded short-answer questions, authored from independently rights-reviewed prose. Exclude all E19/E20/train/dev page/QID/import/near-duplicate lineage, including PRIVATE E20 final lineage through a custodian-to-custodian comparison. Never reveal those private IDs to the training principal. Topic/source-family assignment and length/arity bins must be fixed before selection; balance hard/lower-depth within new-domain source families and report residual confounds. Do not silently substitute E22 synthetic rule tasks or previously generated fixture answers. If genuine language items cannot meet these quotas/essentiality requirements, the instrument is blocked; return a narrowly specified amendment before outcomes.

### Difficulty and hard cutoff

Two human annotators blinded to every model output/energy/loss specify evidence spans, true grounded relations, the minimal essential dependency DAG and shorter valid derivations. Premises have depth 0; essential inference depth is 1+maximum essential parent depth. **Hard = adjudicated minimum essential serial depth ≥3**, not merely authored graph depth; lower-depth = 1 or 2. Record distinct evidence facts/arity separately. Redundant identity chains, conclusions explicitly restated in the source, nuisance labels and arithmetic compression do not manufacture difficulty. Disagreements and shorter alternatives must be resolved BEFORE freeze; unresolved items never enter final scoring. A third independent adjudicator or accepted custodian resolves disagreement, with reviewer identities retained privately. Do not nominate a nonexistent human.

Answer-changing essential-premise and answer-preserving nuisance checks are required on public DEVELOPMENT examples, along with retrieval-only/query-only shortcut controls, length/template/topic balance and an annotation audit. This is a protocol for semantic review, not proof of a universal minimum reasoning complexity. No performance-based filtering or hard-cutoff selection from model accuracy.

### Answer/generation and retention comparators

Common short-answer prompt, NFC + collapsed whitespace whole-answer normalization; preserve case/punctuation/units/signs. Lock aliases privately before model scores. Same tokenizer, exact prompt, greedy decoding and maximum 32 new tokens for all arms; zero temperature, no reranking, no per-arm demonstrations. Raw token/EOS/stop traces must be bound to engine outputs; v0.2's caller-provided policy hash alone is insufficient. Empty/error/truncated/invalid completion is incorrect and remains in the denominator.

For each seed, compute new-domain QA EM separately for energy K8, frozen K0, cost-matched direct recurrence and the separately trained one-step control. Nominate the ≥2-point generation threshold against EACH of those three comparators, not whichever loses. Old-domain loss is frozen K0 EM minus energy K8 EM, on the same committed old items; nominate ≤2-point FIVE-SEED MEAN loss. Report every seed and both direct controls' old loss, not frozen-core hashes as retention. More restrictive per-seed retention thresholds are not introduced here. Fixed LoRA and same-data replay remain required practical-control feasibility questions; omission restricts claims and requires a specific pre-outcome disposition.

### Convergence and gauge

Pin the original potential formula with NO added context-only offset, z0=0, exact checkpoint/lift/readout/features, alpha, radius, restoring term, head precision and normalization. Alpha/radius/training hyperparameters must be fixed using development BEFORE final access; CPU defaults are not language-fit evidence. For each common teacher-forced scored answer-token context, define projected mapping `r_k = ||z_k - project(z_k - alpha*grad E)||_2 / alpha` using the same alpha/radius. Nominate numerical stationarity when `r_k <= 1e-3 * max(1, ||z_k||_2)` at EACH of k=6,7,8. This is a finite numerical stationarity criterion, not proof of global convergence or good answers. Compute the extra gradients honestly and include them in telemetry cost. No extra K, adaptive stopping, final-based line search or restart is added.

M1 correlation uses the per-item MEAN raw E at z8 on those SAME teacher-forced answer-token contexts, ONLY if every required context in the committed new-domain set meets that criterion. Any unmet/nonfinite context makes that seed's M1 correlation UNEVALUABLE; do not drop the item or replace raw E with energy drop. The criterion can be too strict for a fixed-eight-step language system; test it on DEVELOPMENT and disposition before lock, not after final energy. K8–K0 generated EM remains an independent fixed-depth metric. Pinning a gauge makes raw E reproducible; `E+c(h)` can still reverse energy/difficulty ranks without changing predictions. This is not calibrated evidence of reasoning.

### Aggregation, seed handling and work matching

Nominate five fresh paired seed IDs, to be allocated and published by the evaluator AFTER feasible development configuration is committed; none selected from a successful model score. Within a seed, token NLL is total CE / actual shifted scored-token count (never mean example PPL); QA EM is correct / all committed items. Compare identical item IDs/masks and reject duplicate/missing/extraneous rows. Generation gain, old loss and hard accuracy gain aggregate as arithmetic means of the five paired seed deltas. The hard K8–K0 threshold stays ≥5 points. Spearman uses tied average ranks and keyed joins within each seed/checkpoint on ALL 256 new items; nominate arithmetic mean of five valid seed rhos ≥0.6. Constant vectors, missing annotations, or an unevaluable seed mean M1 UNEVALUABLE, not rho=0 or PASS. Report all five rhos and each hard/easy/source stratum; do not pool raw potentials across trained seeds.

The ≥0.02 nats/token criterion must hold in five-seed paired mean against EACH trained direct control, with ≥4/5 positive paired deltas for EACH. Thresholds are conjunctive; do not select the best checkpoint/depth/seed after outcomes. Descriptive paired-seed SD/range and document-cluster sensitivity are conditional on this dataset, not confirmatory significance. Five-seed consistency remains exploratory. M1 and added quality/retention/cost views receive separate labels; a secondary win cannot repair failed/unevaluable M1.

Retain equal-exposure diagnostics AND a development-measured equal-work comparison: base encoding, nested derivatives, train steps, extra telemetry, warmup, calibration/search and full autoregressive latency. Match training/inference points using measured wall/CUDA-event time with a prospectively fixed matching rule from development, not equal K/parameters. Unmeasured comparability is a dependency, not an advantage. The lead must return a whole-battery bound, charging all arms/seeds/evaluator work and reserving stop/serialization margin within the separate ceilings. No control removal, seed reduction, precision switch or cap extension by inference.

## 3. Custody discovery and smallest owner action

Public relay searches for `custodian`, `custody` and `separate principal`, and the existing public research/issue evidence, were inspected. Their archived raw query outputs and returned/deduplicated counts are in `RESEARCH/E20_E21_APPROVAL_AUDIT_2026_10_06/RUN_01/`. This bounded discovery found requirements/options but NO accepted named person/service plus access arrangement. It cannot rule out an undisclosed arrangement elsewhere. The routed approval brief itself confirms that approval names no custodian. An independent code reviewer, another agent or another worktree under Majied is not final-data custody.

**Smallest concrete owner action:** name one real human/service who accepts E20/E21 final custody, and state the off-host or separate-principal store AND key/access holder unavailable to Majied-side training/tool credentials. If selecting the already offered human-held off-host option, explicitly accept who holds that store/key; don't send a password/key, final examples or answers in chat. The accepted custodian then prepares only nonsensitive canaries and public denial receipts; actual final material is not released during preparation. No account, ACL, mount or network permission is changed by this document.

Before final release: enumerate every training/tool principal and token/elevation identity; run real denied-read probes against custodian-owned NONSENSITIVE canaries; verify separately that the custodian can read; distinguish permission denial from missing path/timeout; audit inherited ACL/group/admin/backup privileges, remote credentials, keys, mounts and shared session access. Off-host inaccessibility to one process is not proof against another mounted/saved-key path. Record public evidence hashes, no keys/content. Repeat probes after any relevant access change. Custodian privately verifies rights/lineage/annotation commitments, freezes all-arm checkpoints/config/seeds, and performs one fixed read-only scoring transaction after training. Learners get no final feedback for tuning.

## 4. License and development-fit boundary

Review only model-card/config/file metadata at the exact nominated revisions; no model/tokenizer weights or corpus collection in this evaluator audit. Both pinned model cards declare Apache-2.0 and link the upstream license. Missing standalone LICENSE at a model repository is recorded as missing, not fabricated. Preserve license notices/attribution and change notices with any permitted redistribution. This metadata review is not an audit of every pretraining source's rights, nor automatic clearance for independent prose/QA or downstream adapter release.

Wikimedia Terms of Use §7 is a general licensing framework, not a per-article clearance. For each selected development/training article, verify revision/creation/import/copy lineage, attribution/history, notices and quoted third-party exceptions before corresponding corpus retrieval/use; separately review release of derived text/adapters. Final articles require the custodian's private review. No source corpus has been cleared or collected here. Model-card memory and analytical BF16 bytes are NOT fit measurements.

Eligible next step for the lead is a bounded development-fit plan AFTER corresponding metadata/rights review: exact model/tokenizer hashes, installed environment/attention backend, real 1.7B warm-up/adapter/common-start, causal shifted-mask/count checks, full-vocabulary predictions, learnability V, allocated AND reserved peaks ≤22 GiB, representative all-arm costs including QA/reranking, and stopping before the ≤1h development allowance or any known invalid instrumentation. No final custody is required to test public development data, but final access remains prohibited. Lead owns scheduling and cost ledger; evaluator does not launch a competing model job. E21 waits behind E20 and its existing code/control reviewer snapshot release and three defect dispositions.

## 5. Completion labels and audit scope

This artifact is a PREPARATION milestone: approval-bound candidate input plus newly specified prospective E21 proposals and custody procedure. E20/E21 language outcomes remain NOT RUN; E19 FAILED and M1/history unchanged. Original E20 checker/manifest are preserved; its earlier 41-predicate BLOCKED record is historical receipt completeness, not 41 scientific failures or an assertion that approval is still missing. This audit consumes NO GPU allowance; project-wide prior development consumption requires the lead's reconciled ledger and is not assumed zero.

The public CPU audit below checks exact approval/brief IDs and event hashes, sheet/design/report hashes, candidate-field arithmetic, public search receipts, metadata and unchanged protected files. It does NOT set `run_authorized=true`, certify rights/custody, execute canary denials, read final material, train or generate model answers. The candidate is NOT FINAL-LOCKED until actual software/data/profile/rights/custody and the new curation/comparator/convergence fields have explicit pre-outcome disposition.

Sources: original sheet :17–46; E20 design :64–108,168–201,229–250; E21 protocol :74–86; evaluator r1.1 :77–89; owner/brief event IDs above; pinned cards at `https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B/raw/effd688a12921b4cc83e3312b6feb579f70f9c71/README.md` and `https://huggingface.co/HuggingFaceTB/SmolLM2-360M/raw/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/README.md`; `https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content`.
