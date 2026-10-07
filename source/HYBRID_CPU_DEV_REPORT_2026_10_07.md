---
title: "New AI bounded hybrid CPU prototype — verified synthetic development receipt"
tags: [new-ai, hybrid, energy, growth, cpu, synthetic]
status: draft
created: 2026-10-07
---

# Scope and provenance

Local worktree `REPOS/new-ai-hybrid-dev`, branch `research/hybrid-cpu-dev`, base `f9e3a7a`; uncommitted additions: `hybrid_dev/{__init__.py,core.py,run.py}`, `test_hybrid_dev.py`, `HYBRID_DEV_README.md`. The code is isolated from E21 and is not a public or accepted benchmark result. The full runner emits `receipt.json`, `pre_growth.pt`, `promoted.pt`; permanent copies are alongside this report in `RESEARCH/NEW_AI_HYBRID_CPU_DEV_2026_10_07/`. Source references are the worktree paths and the receipt's per-stage trace/metrics.

## Verified execution

`C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe -B -m unittest -v test_hybrid_dev` reported **4/4 passing**, run on the CPU with CUDA hidden. The single full seed-23 run (`python -B -m hybrid_dev.run --out .../NEW_AI_HYBRID_CPU_2026_10_07_02`) reported `REJECT`, `PROMOTE`. The runner independently reloaded the pre-growth state after rejection and the promoted model/optimizer from disk after acceptance. Its output was parsed and both checkpoint hashes checked against the saved bytes after copying to RESEARCH.

| Synthetic development measure | Before growth | After true-feedback promotion |
|---|---:|---:|
| Old held-out accuracy | 0.9921875 | 0.98046875 |
| New held-out accuracy | 0.51953125 | 0.99609375 |

Detection fired after block 2 with threshold 0.106703125206548 and block-2 observed NLL 4.92893227439775; 64 observed feedback examples entered growth and 448 later training examples remained excluded. The mismatched-feedback trial fell to new accuracy 0.005859375, was rejected, and full-state rollback was verified. Frozen-core fingerprint remained unchanged in both trials. The saved receipt is SHA-256 `b4241df90c39dbe91d813ee9c628761be327547513c9d49a99cb30da05d7a547`; pre-growth checkpoint `3fbd4b155d31cb33a37ebf226c749ff03588655e6a2b5640b737941189a0055c`; promoted checkpoint `9a341a9f1e978ecc7fe20b83a1718bf75fd9cecd146a817ebfa7d4f6c2a5c1a0`.

## Limits and next engineering question

This is a deliberately simple 2-feature classifier with a hard-coded known-shift gate, supervised feedback-NLL detector, and one residual sprout. No language model, resident GPU, benchmark data, expert graft, ternary weights, novelty discovery or E20/E21 outcome is involved. It tests wiring of train→freeze→scalar-energy descent→growth decision→retention gate→promote/rollback and checkpoint integrity only. Held-out old/new development examples govern promotion, so these are not independent final test claims. The next defensible comparison would keep the same revealed data, capacity and compute with a scheduled trigger control before attributing any advantage to feedback timing; it has **not** been run here.
