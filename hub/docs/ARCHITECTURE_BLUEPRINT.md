---
title: "New AI — evidence-backed architecture blueprint content"
tags: [new-ai, architecture, archify, research-status, trust-boundaries]
status: draft
created: 2026-10-05
---

# Architecture blueprint content for the New AI hub

**Owner of this content:** Energy Model Engineer. **Delegator:** Cloud AI Generalist.
**Scope:** an authored graph/content draft, not website code, a running system, an execution protocol, a seal certificate or a model result. No model/GPU/site changes. Every proposed safeguard below is a design requirement unless its historical implementation is separately cited.

## 1. Truth labels and the story the hub must tell

- **E19 / IMPLEMENTED HISTORICAL PILOT / FAILED:** hashing-feature binary news classifier, linear residual adaptation, centroid routing and observed-error feedback were implemented and measured. Feedback tied scheduled timing; the new-task accuracy gate also failed. It is not a pretrained LM, an EBM or a running production service. See S03, S04:3–21 and S06:13–19.
- **E20 / PROPOSED, NOT LOCKED OR RUN:** independent SmolLM2-1.7B task-free LoRA/replay/routing design. Data, approval, software/profile and custodian lock are prerequisites, not completed artifacts. Its optional answer-energy reranking annex is NOT latent energy descent. See S05:10–16,186–201,229–254.
- **E21 / PROPOSED, UNRUN MECHANISM TRACK:** frozen SmolLM2-360M with a genuinely trained scalar-energy latent update versus a functional-capacity-matched direct update. This is a new EBT-inspired adaptation, not an EBT reproduction. It is separate from E20; the readout-loss thresholds in S02:221 are suggestions, NOT accepted project gates. See S01:161 and S02:165–223.
- **LONG TERM / UNIMPLEMENTED COMPOSITION:** safe candidate promotion, whole-state rollback, A/B freeze-swap and tiered expert placement have not been demonstrated as this composed system. Neither a passing pilot nor unchanging core weights proves retained system competence. See S01:31–48,103–107,141 and S04:21.

All nodes have `running_now: false` in this static draft. Do not turn a proposed node green, animate traffic as measured activity, imply live model telemetry, or use “self-evolving LLM” as an achieved status. Parent must refresh statuses from actual evidence before any future deployment of the hub. An E19 historical analogue must retain its per-view label; never relabel its linear classifier as the proposed pretrained LM.

The canonical components are logical responsibilities, not claimed deployed microservices. In E19, router and residual adapter are methods/fields of the same Python `Adapter`, not separate services (S03:98–113).

## 2. Evidence catalog

Paths are workspace-relative. `Sxx:a-b` means the exact path below, inclusive line range. Source ranges are checked against the fetched/read snapshots. Proposals cite the documents that specify them; citations do not turn a requirement into a completed implementation.

| ID | Evidence path / revision | Use and limits |
|---|---|---|
| S01 | `NEW_AI/master-plan.md` | Master mechanism inventory, immutable scientific gates and E21 separation. Unversioned running document; snapshot hash recorded by validation. |
| S02 | `RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md` | Pinned original papers/code and the proposed energy-vs-direct readout mechanism; no local model run. |
| S03 | `REPOS/new-ai-e19/run_e19.py` @ `0cdc379b2cd43d24780318becf9cae55af26c814` | Historical actual implementation, inspected statically; not executed for this task. |
| S04 | `REPOS/new-ai-e19/PROTOCOL_E19.md` @ same E19 commit | Historical scope, data/controls and acceptance gates. |
| S05 | `REPOS/new-ai-e20-eval/RESEARCH/NEW_AI_E20_EVAL_DESIGN_2026_10_05.md` | Independent E20 candidate design. Untracked draft in `research/e20-independent-design`, not a committed seal or peer-reviewed approval. |
| S06 | `REPOS/new-ai-e19/E19_REPORT.md` @ same E19 commit | Failed historical verdict and routing/compute limitations. |
| S07 | `NEW_AI/sources/rsi_benchmarks.txt:47–52` | Original user intent for alternating frozen/editable models. It is not implementation evidence; do not cite the surrounding generated literature claims as replication. |
| S08 | `REPOS/new-ai-visuals/SITE_PUBLICATION_CHECKLIST.md` @ `9c674ec9679e4bdad99210535dcbb114c9c6436e` | Human-reviewed, per-EXX publication and live verification contract. |
| S09 | `REPOS/new-ai-e19/test_e19.py` @ same E19 commit | Existing historical identity/freeze/feedback/feature tests; not rerun here. |

Archify source inspected at `3c4e4a50b0ebba92ffc0859ae12f34d90de523ae`: native fields/types are in `archify/schemas/architecture.schema.json:7–26,73–150` and `common.schema.json:71–73,100–102,148–179`.[1][2]

Retired views and verified source/ownership constraints are in `schemas/README.md:54–55,207–218,228–239`; bounded authored source and separate validation are in `docs/authoring-cookbook.md:41–65`.[3][4]

## 3. Authored content model

This JSON is the **hub content ledger**, not native Archify IR. Preserve its stable IDs for detail cards, typed relation labels and provenance. Registry references (`gate`, `boundary`, `failure`) expand to explicit contracts in the same object, so every node and edge has its own evidence and review/failure path. `failure` describes the nominated route to implement or the research handling rule; it does NOT certify that an automatic rollback exists in E19.

```json
{
  "content_schema": "new-ai-blueprint-draft-1",
  "scientific_status": "full thesis not demonstrated",
  "source_catalog": {
    "S01": "NEW_AI/master-plan.md",
    "S02": "RESEARCH/NEW_AI_EBM_CODE_REVIEW_2026_10_05.md",
    "S03": "REPOS/new-ai-e19/run_e19.py",
    "S04": "REPOS/new-ai-e19/PROTOCOL_E19.md",
    "S05": "REPOS/new-ai-e20-eval/RESEARCH/NEW_AI_E20_EVAL_DESIGN_2026_10_05.md",
    "S06": "REPOS/new-ai-e19/E19_REPORT.md",
    "S07": "NEW_AI/sources/rsi_benchmarks.txt",
    "S08": "REPOS/new-ai-visuals/SITE_PUBLICATION_CHECKLIST.md",
    "S09": "REPOS/new-ai-e19/test_e19.py"
  },
  "status_labels": {
    "historical": "IMPLEMENTED HISTORICAL E19 PILOT; FAILED",
    "analogue": "E19 HISTORICAL ANALOGUE; NOT THE PROPOSED LM/SEAL",
    "e20_proposed": "E20 PROPOSED; NOT LOCKED/RUN",
    "e21_proposed": "E21 PROPOSED; UNRUN",
    "unimplemented": "LONG-TERM UNIMPLEMENTED",
    "human_gate": "PROPOSED HUMAN REVIEW; NOT AUTO-PROMOTION"
  },
  "gates": {
    "G_inputs": {"rule": "Pinned/licensed/group-disjoint allowed data only; no task/source IDs or future outcomes in routing; E20 suffix revealed only after saved prefix decisions.", "evidence": ["S03:34-95", "S04:6-10", "S05:82-116", "S05:229-239"]},
    "G_core": {"rule": "Hash/freeze base tensors; preserve common-start outputs; no model code, tokenizer, evaluator or safety-gate edits. E19 freezing starts after A training, not pretrained initialization.", "evidence": ["S03:98-105", "S09:36-44", "S05:66-80", "S02:175-175", "S01:107-107"]},
    "G_energy": {"rule": "E21 protocol/compute/data lock first; scalar E and real grad_z update; CE must train the energy through the update; finite-difference/nonzero-gradient/bypass tests; independent quality and equal measured-compute controls. Energy decrease alone fails the capability claim.", "evidence": ["S02:177-223", "S01:39-39", "S01:115-122", "S01:161-161"]},
    "G_control": {"rule": "Same functional head capacity, initial conditions, restoring drift, decoder and permitted data; independently verify real tensor counts; report equal-data and equal-compute views without conflating them.", "evidence": ["S02:177-219"]},
    "G_detector": {"rule": "Causal observed feedback and development-only thresholds; no oracle onset or final-score calibration; E19 strict timing gate stays failed. E20 B3/D3 candidate rules are not approval or a universal false-alarm guarantee.", "evidence": ["S03:139-150", "S04:13-21", "S06:13-15", "S05:143-149", "S05:176-182"]},
    "G_router": {"rule": "Prefix/input-only routing, no true task/answer/test identity; log selections and independent oracle gap only as a diagnostic. If learned capability is accessible only with oracle routing, the autonomous system fails.", "evidence": ["S03:106-113", "S06:15-19", "S05:135-137", "S05:215-227"]},
    "G_adapt": {"rule": "Approved allocation cap and method-specific identity test; train only allowed new weights with logged causal exposure. E19 zero-init residual differs from E20 cloning; no claim that core freezing proves retention.", "evidence": ["S03:183-201", "S09:36-44", "S05:70-80", "S05:118-137", "S05:237-238"]},
    "G_replay": {"rule": "Training-only bounded reservoir; log repeats, bytes and fresh-data tradeoff; charge replay work. Never replay development/final examples or silently add extra updates.", "evidence": ["S05:125-133", "S05:203-213"]},
    "G_promotion": {"rule": "Human review of a precommitted candidate and independent validity/quality/retention/cost verdict; PASS licenses the stated next test, not automatic deployment. Reject/incomplete/invalid retains the accepted baseline; Majied approves budget or project-gate changes.", "evidence": ["S01:107-122", "S01:124-141", "S02:225-231", "S05:229-250"]},
    "G_swap": {"rule": "Long-term prerequisite: immutable A/B manifests, atomic whole-state pointer change, only the authorized candidate editable, frozen side hashes unchanged, interruption/failure restore drills. This new engineering gate is proposed, not measured or already preregistered.", "evidence": ["S07:47-52", "S01:107-107", "S04:21-21"]},
    "G_eval": {"rule": "Separate custodian, real access isolation, immutable all-arm artifacts, one locked final transaction, no adaptive final queries, no post-hoc checkpoint/threshold choice. E19 official-test scoring was not a demonstrated ACL-enforced custodian seal.", "evidence": ["S03:133-136", "S04:20-21", "S05:151-184", "S05:229-240"]},
    "G_cost": {"rule": "Cost collector outside candidate write authority; count data, detector, routing, training and generation; reject NaN/missing/zero counts; equal steps do not prove equal compute. E19 records limited adaptation wall time, not full LLM/GPU cost.", "evidence": ["S03:116-130", "S03:241-260", "S06:15-17", "S02:217-219", "S05:203-213", "S05:237-240"]},
    "G_publish": {"rule": "Per-EXX raw/protocol/source/verdict; preserve failures; separate task/model classes; sanitize licensed corpus/test content; human website PR and desktop/mobile/live-byte verification. A proposed graph is not a measured EXX result.", "evidence": ["S01:119-122", "S08:3-12"]},
    "G_tiers": {"rule": "Long-term development tests: accurate cold/resident expert identity, bounded p95 paging latency, state/optimizer integrity and full resident comparison; no unbounded-growth or ternary-speed claim without its own tests. Budget enlargement needs owner approval.", "evidence": ["S01:42-44", "S01:78-91", "S02:66-74", "S02:225-231"]}
  },
  "boundaries": {
    "B_ingress": "Untrusted corpus/user text -> approved, provenance-checked input; source metadata kept out of model decisions.",
    "B_runtime": "Sandbox model/latent computations; read-only frozen base, no network or code/safety/evaluator mutation authority.",
    "B_training": "Trainable candidate, bounded replay and causal keys only; no development/final data access.",
    "B_feedback": "Observed outcomes from the allowed stream only -> detector; no final-test or oracle phase feedback.",
    "B_eval": "Independent custodian owns final data/evaluator; model artifacts cross read-only, never trainer-accessible final text or adaptive score queries.",
    "B_governance": "Human protocol/release authorization separated from learned detector/model output; no autonomous acceptance-gate rewriting.",
    "B_metrics": "Protected measurement/record collector can observe candidates but candidates cannot rewrite measurement or outcome records.",
    "B_public": "Reviewed export -> public log; no raw sealed/licensed text, credentials or model-control channel.",
    "B_tiers": "Content-addressed resident/cold expert artifacts; checked identity and approved storage/I/O budget; not a memory tier deployed by this draft."
  },
  "failures": {
    "R_quarantine": "Deny suspect input/metadata, quarantine offending record and stop the relevant arm; preserve evidence. Exposed-final integrity correction requires a fresh experiment/test, not test repair.",
    "R_baseline": "Retain the immutable reference/core state; mark the candidate or router failure. In a preregistered run, do not silently replace a failing arm with baseline output and call it success.",
    "R_abort_arm": "Stop unsafe/nonfinite/over-budget candidate work, preserve partial logs and report failed/incomplete seed. No replacement seed or score-driven tuning.",
    "R_no_growth": "No allowed causal trigger -> no allocation; score the unchanged system. False alarms, wrong routes and cap saturation remain recorded failures/diagnostics.",
    "R_no_promotion": "Reject promotion on failed/incomplete/invalid evidence; keep last accepted version and publish the narrow verdict, including negatives.",
    "R_restore_state": "Proposed whole-state rollback: restore base/hash, adapter/expert weights, router keys, active-slot pointer, replay/optimizer lineage and compatible version manifest. Do not restore weights while retaining incompatible routing state.",
    "R_restore_pair": "Proposed A/B rollback: atomically restore both manifests and active/frozen roles; quarantine interrupted candidate; neither side may edit evaluator/code/safety controls.",
    "R_incomplete": "Mark missing/malformed cost or scoring evidence INCOMPLETE; do not invent estimates or publish a pass.",
    "R_keep_public": "Keep prior verified result release; correct/version the new export through review. A deployment failure means not live; old negative records remain visible.",
    "R_resident": "Stop paging/grafting test; use the predeclared all-resident or no-graft comparator for diagnosis, not as a relabeled success; owner decides any enlarged budget."
  },
  "nodes": [
    {"id":"stream","label":"Allowed stream / delayed outcomes","type":"external","running_now":false,"view_labels":{"e19":"E19 news text + observed labels","e20":"E20 licensed prose / causal suffixes","e21":"E21 allowed language train/dev data","future":"Approved input + feedback ingress"},"view_status":{"e19":"historical","e20":"e20_proposed","e21":"e21_proposed","future":"unimplemented"},"evidence":["S03:34-95","S05:82-116","S02:213-213"],"gate":"G_inputs","boundary":"B_ingress","failure":"R_quarantine","note":"Curator labels assemble cohorts; they are never model routing inputs. Sealed final remains with evaluator."},
    {"id":"core","label":"Frozen pretrained LM","type":"backend","running_now":false,"view_labels":{"e19":"E19 frozen linear base (NOT LM)","e20":"Proposed frozen SmolLM2-1.7B","e21":"Proposed frozen SmolLM2-360M","future":"Frozen cortical-core candidate"},"view_status":{"e19":"analogue","e20":"e20_proposed","e21":"e21_proposed","future":"unimplemented"},"evidence":["S03:98-113","S05:66-78","S02:171-175"],"gate":"G_core","boundary":"B_runtime","failure":"R_baseline","note":"Original weights stay unchanged after designated warm-up/freeze; changed routing/residuals can still change competence."},
    {"id":"energy","label":"Trained scalar-energy latent refiner","type":"backend","running_now":false,"view_labels":{"e21":"E21 scalar E + grad_z update","future":"Candidate energy-descent inference"},"view_status":{"e21":"e21_proposed","future":"unimplemented"},"evidence":["S02:177-191","S02:201-223","S01:161-161"],"gate":"G_energy","boundary":"B_runtime","failure":"R_abort_arm","note":"Continuous latent only; CE through updates trains E. Lower E is diagnostic, not task-quality evidence or a calibrated detector."},
    {"id":"direct","label":"Matched direct-update control","type":"backend","running_now":false,"view_labels":{"e21":"E21 same-capacity direct U update","future":"Non-energy recurrent comparator"},"view_status":{"e21":"e21_proposed","future":"unimplemented"},"evidence":["S02:177-209","S02:217-223"],"gate":"G_control","boundary":"B_runtime","failure":"R_abort_arm","note":"Separate experimental arm, not an online fallback relabeled as energy; one-step and K=0 controls also required."},
    {"id":"detector","label":"Novelty / observed-feedback detector","type":"backend","running_now":false,"view_labels":{"e19":"E19 error feedback + density probe","e20":"E20 proposed B3/D3 monitors","future":"Causal monitor; fixed approved policy"},"view_status":{"e19":"historical","e20":"e20_proposed","future":"unimplemented"},"evidence":["S03:139-177","S06:13-15","S05:143-149"],"gate":"G_detector","boundary":"B_feedback","failure":"R_no_growth","note":"Input-only novelty cannot resolve identical-input label-only shifts. No E21 absolute-energy-to-growth connection is authorized."},
    {"id":"router","label":"Router / expert-key store","type":"backend","running_now":false,"view_labels":{"e19":"E19 two-centroid gate (weak route)","e20":"E20 proposed prefix GMM + slots","future":"Verified prefix router + expert registry"},"view_status":{"e19":"historical","e20":"e20_proposed","future":"unimplemented"},"evidence":["S03:106-113","S06:15-19","S05:135-137"],"gate":"G_router","boundary":"B_runtime","failure":"R_baseline","note":"E19 has two centroids and a linear residual, not a tiered expert library. E20 keys use frozen unadapted-prefix features, not task IDs."},
    {"id":"adapter","label":"Adapter / bounded growth","type":"backend","running_now":false,"view_labels":{"e19":"E19 zero-init linear residual","e20":"E20 proposed rank-8 clone / child","future":"Sandbox localized parameter growth"},"view_status":{"e19":"historical","e20":"e20_proposed","future":"unimplemented"},"evidence":["S03:98-113","S03:183-201","S05:70-80","S01:40-41"],"gate":"G_adapt","boundary":"B_training","failure":"R_abort_arm","note":"Clone != zero-init sprout. Training uses active chronological slot; proposed E20 inference uses router-selected slot."},
    {"id":"replay","label":"Rehearsal / bounded replay","type":"database","running_now":false,"view_labels":{"e20":"E20 R24 training-only reservoir","future":"Bounded rehearsal memory"},"view_status":{"e20":"e20_proposed","future":"unimplemented"},"evidence":["S05:125-133","S05:203-213"],"gate":"G_replay","boundary":"B_training","failure":"R_quarantine","note":"A separate R24 arm, not free replay added to B3; no E19 replay was implemented in its primary adaptation."},
    {"id":"promotion","label":"Human promotion / rollback gate","type":"security","running_now":false,"view_labels":{"e21":"Human protocol / verdict handoff","future":"Reviewed promote-or-rollback gate"},"view_status":{"e21":"human_gate","future":"unimplemented"},"evidence":["S01:107-122","S02:225-231","S05:229-250"],"gate":"G_promotion","boundary":"B_governance","failure":"R_no_promotion","note":"Human authorization, not a model-run service. Whole-state rollback is a proposed safeguard; E21 PASS does not auto-promote a generator."},
    {"id":"freeze_swap","label":"A/B freeze-swap coordinator","type":"security","running_now":false,"view_labels":{"future":"Unimplemented atomic A/B role swap"},"view_status":{"future":"unimplemented"},"evidence":["S07:47-52","S04:21-21","S01:107-107"],"gate":"G_swap","boundary":"B_governance","failure":"R_restore_pair","note":"Design intent only. No coding the other model's code, evaluator, metrics or safety gate; edits restricted to approved parameter sandbox."},
    {"id":"evaluator","label":"Independent sealed evaluator","type":"security","running_now":false,"view_labels":{"e19":"E19 official-test scorer (NOT ACL seal)","e20":"Proposed independent sealed custodian","e21":"Proposed separate E21 final evaluator","future":"Read-only independent scientific evaluator"},"view_status":{"e19":"analogue","e20":"e20_proposed","e21":"e21_proposed","future":"unimplemented"},"evidence":["S03:133-136","S04:20-21","S05:229-242","S02:213-223"],"gate":"G_eval","boundary":"B_eval","failure":"R_quarantine","note":"E19 test now inspected and cannot become E20/E21's fresh final. Evaluation artifacts return to human/publication, not the learning loop."},
    {"id":"telemetry","label":"Telemetry / measured costs / raw ledger","type":"backend","running_now":false,"view_labels":{"e19":"E19 recorded head-wall time / counts","e20":"Proposed end-to-end cost ledger","e21":"Proposed derivative / generation costs","future":"Protected capability-cost audit trail"},"view_status":{"e19":"historical","e20":"e20_proposed","e21":"e21_proposed","future":"unimplemented"},"evidence":["S03:116-130","S03:241-260","S06:15-17","S02:217-219","S05:203-213"],"gate":"G_cost","boundary":"B_metrics","failure":"R_incomplete","note":"Read-only observation authority; candidate cannot change collector. CUDA-event elapsed is not exact busy-SM time/FLOPs."},
    {"id":"publishing","label":"Public per-EXX result publishing","type":"frontend","running_now":false,"view_labels":{"e19":"Published E19 failed result / raw record","e20":"E20 planned separate result section","e21":"E21 planned separate mechanism section","future":"Human-reviewed research publication"},"view_status":{"e19":"historical","e20":"e20_proposed","e21":"e21_proposed","future":"unimplemented"},"evidence":["S01:24-25","S01:122-122","S08:3-12"],"gate":"G_publish","boundary":"B_public","failure":"R_keep_public","note":"Existing E19 publication is historical evidence. This blueprint task makes no website edit or live-deploy claim; proposed tracks show no synthetic metric cards."},
    {"id":"tiers","label":"Tiered expert residency / cold artifacts","type":"database","running_now":false,"view_labels":{"future":"Unimplemented VRAM / RAM / NVMe tiers"},"view_status":{"future":"unimplemented"},"evidence":["S01:42-44","S01:78-91","S02:66-74"],"gate":"G_tiers","boundary":"B_tiers","failure":"R_resident","note":"Long-term M4/M6. Ternary kernels/pruning/self-play/observer are separate unimplemented roadmap items in this card, not benefits inherited from mini-AGI."}
  ],
  "edges": [
    {"id":"e01","from":"stream","to":"core","type":"data","payload":"Allowed text/prefix; E19 hashed article features, E20/E21 permitted language inputs","views":["e19","e20","e21","future"],"evidence":["S03:92-95","S05:116-116","S02:175-175"],"gate":"G_inputs","boundary":"B_ingress","failure":"R_quarantine"},
    {"id":"e02","from":"stream","to":"detector","type":"feedback","payload":"Observed labels/suffixes after committed prediction; never final labels or true phase","views":["e19","e20","future"],"evidence":["S03:139-150","S05:116-116","S05:145-149"],"gate":"G_detector","boundary":"B_feedback","failure":"R_quarantine"},
    {"id":"e03","from":"stream","to":"router","type":"data","payload":"E19 input-only hashed article features","views":["e19"],"evidence":["S03:92-113"],"gate":"G_router","boundary":"B_ingress","failure":"R_baseline"},
    {"id":"e04","from":"core","to":"router","type":"data","payload":"Read-only frozen unadapted-prefix features, not answer/suffix metadata","views":["e20","future"],"evidence":["S05:135-137"],"gate":"G_router","boundary":"B_runtime","failure":"R_baseline"},
    {"id":"e05","from":"core","to":"detector","type":"data","payload":"E19 base predictions for pre-adaptation observed-error blocks","views":["e19"],"evidence":["S03:139-177"],"gate":"G_detector","boundary":"B_feedback","failure":"R_no_growth"},
    {"id":"e06","from":"adapter","to":"detector","type":"feedback","payload":"E20 current-active-slot pre-update predictions; suffix loss computed only after suffix reveal","views":["e20","future"],"evidence":["S05:116-116","S05:145-145"],"gate":"G_detector","boundary":"B_feedback","failure":"R_no_growth"},
    {"id":"e07","from":"router","to":"detector","type":"data","payload":"D3 diagnostic uses fixed initial A density key, not changing router-selected loss","views":["e20","future"],"evidence":["S05:129-129","S05:135-145"],"gate":"G_detector","boundary":"B_runtime","failure":"R_no_growth"},
    {"id":"e08","from":"detector","to":"adapter","type":"control","payload":"Bounded causal allocation request; E19 block trigger, E20 next-block action","views":["e19","e20","future"],"evidence":["S03:147-150","S03:182-194","S05:116-133"],"gate":"G_adapt","boundary":"B_training","failure":"R_no_growth"},
    {"id":"e09","from":"router","to":"adapter","type":"control","payload":"Inference-only route/gating decision; not permission to train frozen old slots","views":["e19","e20","future"],"evidence":["S03:109-113","S05:135-137"],"gate":"G_router","boundary":"B_runtime","failure":"R_baseline"},
    {"id":"e10","from":"core","to":"adapter","type":"data","payload":"Frozen base outputs/parameters composed with a trainable residual or LoRA candidate","views":["e19","e20","future"],"evidence":["S03:98-113","S05:70-78"],"gate":"G_core","boundary":"B_runtime","failure":"R_baseline"},
    {"id":"e11","from":"stream","to":"replay","type":"training_data","payload":"Revealed training windows into bounded reservoir; no development/final content","views":["e20","future"],"evidence":["S05:131-133","S05:116-116"],"gate":"G_replay","boundary":"B_training","failure":"R_quarantine"},
    {"id":"e12","from":"replay","to":"adapter","type":"training_data","payload":"R24 comparator rehearsal samples under the same processed-token allowance; not B3 free replay","views":["e20","future"],"evidence":["S05:125-133"],"gate":"G_replay","boundary":"B_training","failure":"R_abort_arm"},
    {"id":"e13","from":"adapter","to":"router","type":"artifact","payload":"Versioned slot and causally assigned prefix-key update; parent alias until new key warm-up","views":["e20","future"],"evidence":["S05:76-76","S05:135-137"],"gate":"G_router","boundary":"B_training","failure":"R_restore_state"},
    {"id":"e14","from":"core","to":"energy","type":"data","payload":"Same frozen h, decoder/lift and initial latent z for E21 energy arm","views":["e21","future"],"evidence":["S02:175-191"],"gate":"G_energy","boundary":"B_runtime","failure":"R_abort_arm"},
    {"id":"e15","from":"core","to":"direct","type":"data","payload":"Paired frozen h, decoder/lift and initial z for separate matched direct arm","views":["e21","future"],"evidence":["S02:175-209"],"gate":"G_control","boundary":"B_runtime","failure":"R_abort_arm"},
    {"id":"e16","from":"core","to":"evaluator","type":"evaluation_artifact","payload":"Immutable baseline model/predictions for independent scoring; E19 scorer was in-process","views":["e19","e20","e21","future"],"evidence":["S03:179-181","S05:122-122","S05:238-240","S02:203-223"],"gate":"G_eval","boundary":"B_eval","failure":"R_quarantine"},
    {"id":"e17","from":"adapter","to":"evaluator","type":"evaluation_artifact","payload":"All predeclared arm/checkpoint outputs, including no-growth and failure records","views":["e19","e20","future"],"evidence":["S03:183-213","S05:155-166","S05:238-240"],"gate":"G_eval","boundary":"B_eval","failure":"R_incomplete"},
    {"id":"e18","from":"energy","to":"evaluator","type":"evaluation_artifact","payload":"Locked E21 K settings, output generations and checkpoint hashes; task metric independent of E","views":["e21","future"],"evidence":["S02:201-223"],"gate":"G_energy","boundary":"B_eval","failure":"R_no_promotion"},
    {"id":"e19","from":"direct","to":"evaluator","type":"evaluation_artifact","payload":"Matched direct/one-step controls, same data and reported measured-compute points","views":["e21","future"],"evidence":["S02:201-223"],"gate":"G_control","boundary":"B_eval","failure":"R_incomplete"},
    {"id":"e20","from":"adapter","to":"telemetry","type":"audit","payload":"Allocation/exposure/route events, trained/stored weights and attributable adaptation costs","views":["e19","e20","future"],"evidence":["S03:195-221","S03:241-260","S05:157-166","S05:207-213"],"gate":"G_cost","boundary":"B_metrics","failure":"R_incomplete"},
    {"id":"e21","from":"energy","to":"telemetry","type":"audit","payload":"Input derivatives, higher-order training, generation, latency and finite-state failure traces","views":["e21","future"],"evidence":["S02:191-191","S02:209-219"],"gate":"G_cost","boundary":"B_metrics","failure":"R_incomplete"},
    {"id":"e22","from":"direct","to":"telemetry","type":"audit","payload":"Separate direct-arm training/generation costs; equal K is not compute equivalence","views":["e21","future"],"evidence":["S02:217-219"],"gate":"G_cost","boundary":"B_metrics","failure":"R_incomplete"},
    {"id":"e23","from":"evaluator","to":"publishing","type":"result","payload":"Sanitized locked metrics, protocol/source references, explicit failed/incomplete verdict and scope","views":["e19","e20","e21","future"],"evidence":["S06:13-19","S05:240-242","S08:3-12"],"gate":"G_publish","boundary":"B_public","failure":"R_keep_public"},
    {"id":"e24","from":"telemetry","to":"publishing","type":"audit","payload":"Raw attributable costs/counts/attempts; missing costs remain missing, not estimates","views":["e19","e20","e21","future"],"evidence":["S03:241-260","S02:219-219","S05:207-209","S08:6-10"],"gate":"G_publish","boundary":"B_public","failure":"R_keep_public"},
    {"id":"e25","from":"evaluator","to":"promotion","type":"review","payload":"Independent verdict to human only; no adaptive final-score return to model/trainer","views":["e21","future"],"evidence":["S02:225-231","S05:238-240","S01:107-107"],"gate":"G_promotion","boundary":"B_governance","failure":"R_no_promotion"},
    {"id":"e26","from":"adapter","to":"promotion","type":"artifact","payload":"Candidate manifest and complete model/router/replay lineage for proposed human review","views":["future"],"evidence":["S05:238-240","S01:107-107"],"gate":"G_promotion","boundary":"B_governance","failure":"R_no_promotion"},
    {"id":"e27","from":"promotion","to":"freeze_swap","type":"approval","payload":"Human-approved immutable A/B role/pointer manifest; proposed atomic switch or rejection","views":["future"],"evidence":["S07:47-52","S01:107-107"],"gate":"G_swap","boundary":"B_governance","failure":"R_restore_pair"},
    {"id":"e28","from":"freeze_swap","to":"core","type":"control","payload":"Select approved frozen-role checkpoint; never make unreviewed candidates the accepted base","views":["future"],"evidence":["S07:47-52","S01:107-107","S04:21-21"],"gate":"G_swap","boundary":"B_runtime","failure":"R_restore_pair"},
    {"id":"e29","from":"promotion","to":"router","type":"control","payload":"Proposed versioned accepted core/expert/key pointer set; rollback restores the compatible tuple","views":["future"],"evidence":["S01:107-107","S05:76-76","S05:135-137"],"gate":"G_promotion","boundary":"B_governance","failure":"R_restore_state"},
    {"id":"e30","from":"router","to":"tiers","type":"storage_request","payload":"Approved content-addressed expert load/placement request with storage/I/O budget","views":["future"],"evidence":["S01:42-44","S01:78-91","S02:66-74"],"gate":"G_tiers","boundary":"B_tiers","failure":"R_resident"},
    {"id":"e31","from":"tiers","to":"router","type":"artifact","payload":"Verified resident/cold expert handle and identity; not a permission to fetch arbitrary code","views":["future"],"evidence":["S01:42-44","S01:78-91","S02:66-74"],"gate":"G_tiers","boundary":"B_tiers","failure":"R_resident"},
    {"id":"e32","from":"stream","to":"adapter","type":"training_data","payload":"Allowed adaptation examples and causally revealed targets; chronological active slot only in E20","views":["e19","e20","future"],"evidence":["S03:187-194","S05:116-116","S05:137-137"],"gate":"G_adapt","boundary":"B_training","failure":"R_quarantine"},
    {"id":"e33","from":"stream","to":"energy","type":"training_data","payload":"Allowed next-token targets for CE through E21 latent updates, never final labels","views":["e21","future"],"evidence":["S02:191-191","S02:213-215"],"gate":"G_energy","boundary":"B_training","failure":"R_quarantine"},
    {"id":"e34","from":"stream","to":"direct","type":"training_data","payload":"Paired allowed next-token targets for the separately trained direct control","views":["e21","future"],"evidence":["S02:193-209","S02:213-217"],"gate":"G_control","boundary":"B_training","failure":"R_quarantine"}
  ],
  "views": [
    {"id":"e19","title":"E19 historical classifier pilot — FAILED","nodes":["stream","core","detector","router","adapter","evaluator","telemetry","publishing"],"primary_edges":["e01","e02","e03","e05","e08","e09","e10","e16","e17","e20","e23","e24","e32"],"note":"Eight logical historical responsibilities. No LM, EBM, sealed-custodian service, replay, cold experts or freeze-swap claim."},
    {"id":"e20","title":"E20 proposed causal language adaptation","nodes":["stream","core","detector","router","adapter","replay","evaluator","telemetry","publishing"],"primary_edges":["e01","e02","e04","e06","e08","e09","e10","e11","e12","e17","e20","e23","e24","e32"],"note":"Nine proposed responsibilities; B3 feedback route and separate R24 replay comparator are not one combined arm. Other authored links remain in the relation ledger."},
    {"id":"e21","title":"E21 proposed energy-versus-direct mechanism","nodes":["stream","core","energy","direct","evaluator","telemetry","publishing","promotion"],"primary_edges":["e01","e14","e15","e16","e18","e19","e21","e22","e23","e24","e25","e33","e34"],"note":"Eight responsibilities; parallel experimental arms, independent outcomes and human review. Promotion node is a proposed human handoff, not running automation."},
    {"id":"future","title":"Long-term composition — UNIMPLEMENTED","nodes":["stream","core","energy","direct","detector","router","adapter","replay","promotion","freeze_swap","evaluator","telemetry","publishing","tiers"],"primary_edges":["e01","e02","e04","e08","e09","e11","e12","e14","e15","e23","e24","e25","e27","e28","e30","e31"],"note":"Fourteen unimplemented composition responsibilities. Additional relationships are selectable details, not invented running traffic. No capability/compute win follows from this map."}
  ],
  "forbidden_links": [
    {"from":"energy","to":"detector","reason":"E21 gradient-trained absolute E is not a calibrated novelty/growth score.","evidence":["S02:55-55"]},
    {"from":"evaluator","to":"adapter","reason":"Final outcomes/text/aliases cannot become training data or adaptive gate tuning.","evidence":["S05:234-239"]},
    {"from":"evaluator","to":"detector","reason":"No final ROC/threshold selection or post-test recalibration.","evidence":["S05:147-149","S05:239-239"]},
    {"from":"publishing","to":"core","reason":"Public hub is not a model-control or parameter-training channel.","evidence":["S01:107-107","S08:10-10"]},
    {"from":"freeze_swap","to":"evaluator","reason":"Model-role exchange has no authority to edit evaluator, code, metrics or safety controls.","evidence":["S01:107-107"]}
  ]
}
```

## 4. Archify integration contract — author facts, not operational claims

1. **Separate projections, not `meta.views`.** Archify's schema accepts the legacy view field but the renderer ignores it. Generate four separate native Architecture documents from the view recipes above, or implement hub tabs that select those documents. Each projection has 8–14 visible nodes. Do not assume highlighting hides the other nodes.[3]
2. Native IR uses `schema_version: 1`, `diagram_type: "architecture"`, `meta`, `components`, `boundaries`, `connections` and optionally `cards`; its objects reject unknown fields. `meta.output` must be a portable relative `.html` path even for a prospective render. Map node `id/type`, the **view-specific label**, and status text into `components[].tag/sublabel`; map relation `id/from/to` plus `type: payload` into `connections[].label`. Keep gate/boundary/failure/evidence details in authored cards or the hub content store, not as invented native fields.[1][2]
3. Use `animation: "none"`. Historical E19 links can be solid with an explicit **HISTORICAL / FAILED** caption; E20/E21/future links use `variant: "dashed"`, with no “active” pulse. Use text badges, not color alone. The optional human-review node in E21 says **proposed human handoff**, never “promotion running”. These are editorial rules for this draft, not built-in operational status semantics.
4. Default each projection to its primary edge list; preserve every additional scoped edge as an explicit selectable relation/detail. The long-term graph is an architectural inventory, not one experimental arm: the direct update is a comparator and R24 replay is a separate E20 control. Never draw them as techniques secretly added to the energy/feedback candidate.
5. Suggested trust-boundary boxes: model sandbox (`core`, `energy`, `direct`, `detector`, `router`, `adapter`, `replay`, `tiers` as present); independent evaluator (`evaluator`); human governance (`promotion`, `freeze_swap`); protected costs (`telemetry`); approved external ingress (`stream`); public export (`publishing`). E19 boxes are neutral logical `region` groupings, not hardened ACLs; proposed-view `security-group` boxes must say **PROPOSED / NOT ENFORCED**. Box membership is a proposed permission contract, not a cloud deployment claim. Parent must choose non-overlapping geometry and annotate actual crossing mechanisms when rendering.
6. **Do not fake repository-verified source passports.** This content mixes unversioned project notes, an untracked evaluator draft and separate pinned code trees. Archify's native `sources` requires verified repository metadata/root/commit/blobs. Do not assign the E19 commit to S01/S02/S05 or point all sources at the Archify repository. Use the local evidence catalog/cards until the correct documents are committed or uploaded with genuine links. `engineering_profile: "deployment-ownership"` must remain unset unless real owners/regions/mechanisms are known.[3][4]
7. Content validation covers reference integrity, scope/status, source ranges, view counts and native schema shape. It **does not** certify Archify runtime geometry, browser behavior, aesthetic polish, an implemented seal, a passing scientific gate or a live deployment. Those remain the website owner’s renderer/browser/deploy checks.[3][4]

## 5. Failure and rollback story for reader-facing cards

- **Learning/route failed:** preserve that arm's outcome; retain the frozen reference and disallow promotion. Do not silently emit baseline predictions under the failing arm name. E19's route/timing failures remain visible.
- **Integrity/feedback leakage:** quarantine the offending record and stop; opened final data cannot be “re-sealed” by renaming a folder. New confirmatory work needs untouched final data.
- **Energy decreases without independent quality:** label an energy diagnostic, not intelligence or novelty detection; compare to direct/one-step controls at measured cost.
- **Candidate/paging/swap failure:** proposed recovery restores a compatible versioned state tuple, not just model weights. A/B interruption recovery must preserve both role manifests. This machinery is a future engineering requirement, not an existing executor.
- **Missing measurements or blocked publication:** mark incomplete/not live, keep prior verified public release, and preserve failed/raw records. No synthesized telemetry or capability numbers.

## 6. Handoff and decisions

Cloud AI Generalist owns hub website code/rendering/deployment; Evaluation Scientist owns final acceptance/custodian design. This draft supplies authored content and evidence only. E20's 1.7B design and E21's 360M mechanism remain separate candidates; neither is an approved resource expansion. The numeric E21 effect-size suggestions do not override M1 or any sealed project gate. Majied decides substantive compute/gate changes; lead decides how to integrate these projections with the hub and must verify current status before publication.

Readiness of draft: logical content can be integrated after structural/citation checks. Remaining website work: extract four native IR projections, choose layout, inspect actual Archify validation/render receipts, check desktop/mobile accessibility and hover/detail/edge navigation, then the authorized PR/live verification workflow. No such HTML or site change is produced by this content task.

## 7. Content validation receipt

Validated with `.scratch/blueprint-2026-10-05/validate_blueprint.py`: 14 unique component IDs, 34 unique directed typed relations, gate/trust/failure registry integrity, forbidden-edge absence, all `running_now` flags false, cited source-range bounds and historical Git-blob/content agreement. Four extracted native IR drafts pass the pinned Architecture/Common JSON Schemas; visible node counts are E19 8, E20 9, E21 8, long-term 14. The reproducible receipt with source snapshot hashes is `.scratch/blueprint-2026-10-05/validation.json`; extracted draft IR files are `projection_e19.architecture.json`, `projection_e20.architecture.json`, `projection_e21.architecture.json` and `projection_future.architecture.json` in that scratch directory. The canonical ledger and recipes remain in this durable Markdown if scratch copies expire.

**Verification limit:** this is JSON/schema/content validation, NOT Archify CLI runtime validation or HTML/layout/browser/deployment verification. Proposed boundaries and rollback gates were not implemented or exercised.

## Sources

[1] https://github.com/tt-a1i/archify/blob/3c4e4a50b0ebba92ffc0859ae12f34d90de523ae/archify/schemas/architecture.schema.json
[2] https://github.com/tt-a1i/archify/blob/3c4e4a50b0ebba92ffc0859ae12f34d90de523ae/archify/schemas/common.schema.json
[3] https://github.com/tt-a1i/archify/blob/3c4e4a50b0ebba92ffc0859ae12f34d90de523ae/archify/schemas/README.md
[4] https://github.com/tt-a1i/archify/blob/3c4e4a50b0ebba92ffc0859ae12f34d90de523ae/docs/authoring-cookbook.md
