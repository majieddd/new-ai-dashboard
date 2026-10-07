---
title: "New AI synthetic CPU matched scheduled-trigger control"
tags: [new-ai, hybrid, energy, growth, cpu, synthetic, control]
status: draft
created: 2026-10-07
---

# Disposition

**Engineering control passed; no trigger-timing advantage was shown.** This is not a language, E20/E21, official benchmark, novelty-discovery, or generalization result. The known-shift residual gate and observed-label feedback remain disclosed. The scheduled block 2 was selected **after** the seed-23 feedback alert was known, so the comparison is post-hoc, not a prospective causal study.

Source worktree: `REPOS/new-ai-hybrid-dev`, branch `research/hybrid-cpu-dev`, clean HEAD `990f6ad855aec7fdacb8b138f76c5cd29284f1df` (initial verified prototype commit `c394fc11d370ff49df82dfe95627ec9c9022313e`). No remote is configured, no push/PR/merge or site publication occurred. GPU visibility was empty, both runners set offline mode, and the resident model was not loaded, stopped or changed. Full test and runner stdout are in `TEST_HYBRID_DEV_OUTPUT.log`, `FEEDBACK_RUN_OUTPUT.log`, `SCHEDULED_RUN_OUTPUT.log` beside this report.

## Paired execution

The full `test_hybrid_dev` suite passed **4/4** at exact HEAD above. Re-ran seed 23 on that committed source in two separate CPU processes:

1. `python -B -m hybrid_dev.run --out <fresh>/feedback` issued a saved feedback receipt and pre/promoted checkpoints; its two trials rejected mismatched feedback (rollback) then promoted true feedback.
2. `python -B -m hybrid_dev.control --out <fresh>/scheduled --receipt <feedback>/receipt.json --pre <feedback>/pre_growth.pt --promoted <feedback>/promoted.pt --expected-receipt-sha256 156df16327d9d1d2b80a7d71171dc8eb7920e8850fced1e600c8652180df253c --schedule-block 2` rebuilt all five synthetic data splits, checked their hashes and source-checkpoint bytes, loaded pre-growth state/RNG, and trained a fresh sprout **without consulting the feedback detector**. Its checkpoint and optimizer state were reloaded before issuing its receipt. The test patches `FeedbackDetector.observe` to fail if the scheduled arm calls it, and separately rejects wrong receipt/checkpoint hashes, a mismatched block and an existing output directory.

Both arms used exactly 64 revealed examples, one zero-entry sprout, 120 Adam steps at LR 0.06, effective batch 64 (96 sampling ceiling), and 7,680 example presentations. They matched full model tensor hash `250684c8292081b20e5a0114675234cb92dc379e51a940c1a27c6b5d319f21b2`, optimizer moments, loss-trace values and held-out old/new logits **exactly**.

| Seed-23 synthetic development accuracy | No growth | Feedback trigger, block 2 | Fixed schedule, block 2 |
|---|---:|---:|---:|
| Old split | 0.9921875 | 0.98046875 | 0.98046875 |
| New split | 0.51953125 | 0.99609375 | 0.99609375 |

The arms match **optimizer work**, not total process wall time or detection overhead. This identity comparison supplies no evidence that feedback timing improved performance; it also cannot generalize to untested seeds, schedules, language, or an independent final test set. The next causal question requires a prospective fixed schedule/control over new seeds with independent evaluation and matched complete compute accounting. Those runs were not done.

## Archived receipts (exact byte copies from executed run)

- `FEEDBACK_RECEIPT.json` SHA-256 `156df16327d9d1d2b80a7d71171dc8eb7920e8850fced1e600c8652180df253c`
- `PRE_GROWTH.pt` SHA-256 `3fbd4b155d31cb33a37ebf226c749ff03588655e6a2b5640b737941189a0055c`
- `PROMOTED.pt` SHA-256 `9a341a9f1e978ecc7fe20b83a1718bf75fd9cecd146a817ebfa7d4f6c2a5c1a0`
- `MATCHED_CONTROL_RECEIPT.json` SHA-256 `c3c9e57fdea251120280ba597e1004dc16f33f35635b11b5f7cc2db050596d95`
- `SCHEDULED.pt` SHA-256 `2a30f3e4daa49cb50194c759f99d91d5d69bb7d7d3b935692ed024dd82a2fc90`

Do not load checkpoints from untrusted sources. The earlier seed-23 archive at `RESEARCH/NEW_AI_HYBRID_CPU_DEV_2026_10_07/` remains unmodified: its `batch_size: 96` meant the sampling ceiling despite only 64 available examples. The new paired receipt distinguishes effective batch 64 from ceiling 96; no training arithmetic changed.
