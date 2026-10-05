---
title: "New AI development progress snapshot — October 5, 2026"
tags: [new-ai, progress, provenance, pre-outcome]
status: draft
created: 2026-10-05
---

# Preparation, not a language-model result

`data/progress.json` is a **public projection** generated at 2026-10-05T13:01:46Z from three local source records. It is not an EXX `summary.json`, a preregistration, final-test custody, a model-run receipt or a GPU reservation. `prepare_progress_snapshot.py` checks source status and numerical consistency before exporting, and `progress_site.py` derives every displayed progress number and chart position from that projection. Original E19's failed feedback-versus-scheduled gate and all prior results remain unchanged on the home page.

| Track | Exact input in the New AI workspace | SHA-256 of original bytes | Interpretation |
|---|---|---|---|
| E20 | `REPOS/new-ai-e20-eval/RESEARCH/E20_PREPARATION_AUDIT_2026_10_05_02/BLOCKED_READINESS.json` | `bbe16e5a76b2c83386e664e580320aa44d62a04575768c775ebd4a14d8da9d34` | Public receipt checklist: exit 2/BLOCKED, 41 missing predicates, `run_authorized=false`; **not 41 model failures**. Evaluation Scientist's report is `RESEARCH/NEW_AI_E20_E21_PREOUTCOME_EVIDENCE_2026_10_05.md` in that worktree. |
| E21 | `REPOS/new-ai-e21/results/E21_DEV/cpu-v1-run-001/summary.json` | `2a95f1dcbefb76ab29e4e1f65179656fc55ad5c1978769a3a1e89a19f725a2ff` | Five paired, synthetic CPU fixture seeds, not language generation. Full source/protocol and reconstruction report: `REPOS/new-ai-e21/E21_CPU_REPORT.md` and `PROTOCOL_E21_V1.md`. The lead reran 31 CPU tests and reconstructed 2,880 predictions with max logit error 0.0 at `3f1be60`. |
| E22 | `REPOS/new-ai-e22-candidate/e22_candidate/dev_runs/SWEEP_2026_10_05_B/RECEIPT.json` | `cfa24e4ef129aa4e0a657848fca21234d71c0455e04794fe86e4f47d476573c0` | 16 cells, 256 bases / 768 public development variants and 117 numeric-free groups. Independent arithmetic checks, **no model predictions**. Full report/source posted in the New AI thread and recorded at `RESEARCH/NEW_AI_E22_CPU_CANDIDATE_AND_SOURCE_STATUS_2026_10_05.md`. The lead reran the full inherited-plus-candidate 40-test CPU suite and the read-back auditor. |

The source records are separate development/worktree artifacts. Their original hashes above permit byte-level checking; the public projection intentionally omits an OS security principal, executable path and all final examples/keys. The site does **not** redistribute full third-party philosophy papers or unlicensed benchmark content. E21's fixture mean NLL/accuracy and paired bars are descriptive about that tiny synthetic token task; equal token exposure is not equal measured compute. E22's cell bars represent distinct generated structures within each cell, not a model score; structures can recur across cells. E20's checklist counts missing evidence categories and related predicates, not scientific attempts.

## Pending decisions and gates

- E20: explicit owner choice for language/grounded-QA scope, the proposed 24 exclusive GPU-hours (including at most 1 development hour), human-verified QA/rights and gate binding. A real model-run profile, an approved implementation, and independent final custody with denied-read checks do not yet exist. See E20 issue `b662a6767df9fe4ac6e83c7830a2c6f10cbcd1097eec2cdb1457b4efca7e22de`.
- E21: proposed separate 4h/1h ceiling, thresholds and uncertainty design need explicit approval; independently reviewed language scoring, difficulty/energy reference, fresh final lineage and custody are still needed. Master M1 is unchanged. See E21 issue `0e554492d915f3f04ea51986245d8cc8b321ef9d647e152a19e2407565dd6fb7`.
- E22: independent validity/shortcut review issue `98f12c74468fc414b113bc20432b0811411b71cf5a2b505edbdffc9b706f5a57` is assigned; its result remains pending. The construction depth is not minimum proof depth, arity is confounded with rule family/length, nuisance labels reveal the condition, and depth-1 structural diversity is only two groups per cell. Owner scope/gates and future model compute/custody are separate decisions. The exposed development examples cannot become a fresh final test.
- Reasoning source coverage: three replacement full-reading packages for archived Attractor, archived Principia and recovered Rule-v3 text have not yet been verified as completed. Current Attractor v5 is not proven identical to the archived file. An inspected v3 first-page CC BY-NC-SA notice does not license a commercial product or all components.

A shared Windows account or a differently named agent is not an independent final-data boundary. No E20/E21/E22 language-model scientific PASS, GPU confirmation or live new model result is asserted by this page. The New AI master document is `NEW_AI/master-plan.md` §8 in the project workspace; this public snapshot is deliberately narrower and time-stamped.
