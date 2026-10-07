---
title: "Prospective synthetic CPU hybrid trigger comparison"
tags: [new-ai, synthetic, cpu, prospective-control]
status: active
created: 2026-10-07
---

# Prospective control — no feedback advantage established

**Scope.** Engineering comparison on a public, constructed two-feature label shift, not language, E20/E21, learned domain discovery, or open-ended novelty. GPU hidden, one PyTorch CPU thread, no resident-model access. No publication, push, PR or merge. Protocol `REPOS/new-ai-hybrid-dev/PROSPECTIVE_HYBRID_PROTOCOL.md` was committed **before** execution at `6e8d71b`; SHA-256 `82821f72ad1429a40c9e14f95817ef8c9f250d3587cfdffabcdde769e174cf2a`. Producing source/test commit: `307c02884538d4ddf1481dd06d972e49c36b297c`; subsequent documentation-only commit `86610ff3935009ecb204310b955a3402e651ca0c` is the current clean HEAD of `research/hybrid-cpu-dev` (not pushed).

## Design and execution

Twelve new paired seeds, 101–112, all complete and none omitted. Shared base is trained and frozen, then reloaded from one checkpoint (including RNG state) for each arm. Feedback calibrates on separate old examples, computes labeled batch NLL, and fires on two consecutive exceedances within four blocks. The preregistered schedule fires at block **3** without feedback-NLL computation or detector consultation. Promotion depends only on development labels and a frozen-parameter check. Both arms' decisions and final model/optimizer reloads precede **independent** old/new test scoring. Training, development and test feature sets were checked for overlap. Per-seed receipts and checkpoint hashes are in the numbered subdirectories here; `progress.json` and `summary.json` index them. The tests use only public synthetic data.

All 12 feedback alerts occurred at block **2** and both arms promoted in every pair. That uniform timing is an *observed* outcome, not a retrospective choice of the fixed block; block 3 was locked first. Feedback had 64 revealed labels and 7,680 growth example presentations per seed; schedule had 96 and 11,520. Both had one sprout and 120 growth optimizer steps per seed. **Capacity and update count match, but labeled-example and presentation budgets do not.**

| Seed | Feedback new test | Schedule new test | Paired Δ | Feedback old retention loss | Feedback CPU s | Schedule CPU s |
|---:|---:|---:|---:|---:|---:|---:|
| 101 | 0.986328 | 0.968750 | +0.017578 | 0.011719 | 0.968750 | 0.984375 |
| 102 | 0.962891 | 0.982422 | -0.019531 | 0.009766 | 0.281250 | 0.265625 |
| 103 | 0.984375 | 0.994141 | -0.009766 | 0.017578 | 0.375000 | 0.328125 |
| 104 | 0.964844 | 0.968750 | -0.003906 | 0.011719 | 0.343750 | 0.312500 |
| 105 | 0.996094 | 0.978516 | +0.017578 | 0.019531 | 0.343750 | 0.328125 |
| 106 | 0.970703 | 0.990234 | -0.019531 | 0.003906 | 0.343750 | 0.328125 |
| 107 | 0.990234 | 0.978516 | +0.011719 | 0.009766 | 0.328125 | 0.328125 |
| 108 | 0.984375 | 0.984375 | +0.000000 | 0.011719 | 0.328125 | 0.312500 |
| 109 | 0.986328 | 1.000000 | -0.013672 | 0.017578 | 0.312500 | 0.312500 |
| 110 | 0.988281 | 0.988281 | +0.000000 | 0.017578 | 0.328125 | 0.328125 |
| 111 | 0.980469 | 0.980469 | +0.000000 | 0.013672 | 0.343750 | 0.328125 |
| 112 | 0.982422 | 0.978516 | +0.003906 | 0.013672 | 0.328125 | 0.328125 |

Δ = feedback minus schedule, exact values in receipts (table rounded to six places). Both arms' mean new-test accuracy: **0.9814453125** feedback versus **0.9827473958333334** schedule. Mean paired Δ **−0.0013020833333333333**, feedback strictly better on **4/12** seeds. Mean feedback old-test retention loss **0.01318359375** (schedule **0.013020833333333334**).

## Locked comparison rule, applied as written

| Criterion for evidence of a feedback advantage | Observed | Passed? |
|---|---:|---|
| Mean paired new-test Δ ≥ 0.02 | −0.0013020833 | No |
| Strict feedback wins ≥ 9/12 | 4/12 | No |
| Mean feedback old retention loss ≤ 0.02 | 0.01318359375 | Yes |
| Feedback inclusive process CPU ≤ 1.10 × schedule | 4.625 / 4.484375 = 1.031358885 | Yes |

**Verdict: no advantage established.** This is not proof the detector can never help on other streams. Here it fired earlier but its final accuracy was slightly lower on average than a later schedule with more examples.

## Work and overhead accounting

Per-seed receipts include phase wall and process-CPU seconds, model forward calls/examples, candidate-gradient steps/example-steps, optimizer steps/presentations, calibration/observation examples, and checkpoint write/read bytes. The same measured base generation/training/development/checkpoint plus independent base-test cost is allocated to each arm; all detection overhead is charged to feedback. Across all 12 pairs, inclusive feedback versus schedule: **4.625 vs 4.484375 process-CPU seconds**; **4.802110 vs 4.752792 wall seconds**; **3,600 vs 3,600 optimizer steps** including both arms' allocated 180 shared base steps per seed; **299,520 vs 345,600 optimizer example presentations**; **3,864 vs 3,720 forwards**, **365,568 vs 407,040 forward examples**; **3,840 vs 0 calibration examples**, **768 vs 1,152 observed/revealed examples**; **276,564 vs 275,796 checkpoint-write bytes** and the same read bytes. Shared CPU allocation totals 2.609375 s per arm. Seed 101 includes framework warmup and carries much larger shared cost (0.828125 CPU s); process-time values are coarse/quantized on this Windows run, so the ratio is not a portable performance estimate. Single-run sequential timings, alternating first-arm order by seed parity.

## Verification and limits

`python -B -m unittest -v test_hybrid_dev test_prospective_hybrid`: **6 tests OK** before the run and again at clean HEAD `86610ff` after the README-only edit. Independent post-run parser read every receipt and all **36 checkpoints** (shared/feedback/schedule for each seed), verified declared SHA-256 bytes, 12/12 seed coverage, CPU/work arithmetic, paired differences and the summary comparison rule. `summary.json` SHA-256 `6d29bb01c4b581e17a5cf1b7d509515f94378c90f2277fe1791a7a6e7edfa957`. These checks validate consistency of produced artifacts, not external scientific replication. No alternative threshold, seed selection, or rerun was used. Seed 23 was reserved for implementation tests and excluded from the 12-seed analysis.

The shift gate (`x[:, 0] > 2`) was authored into the model; the detector uses observed labels. The schedule was a single locked block, not a sweep. The observed budget mismatch prevents an equal-training-data causal interpretation, and a seed sweep on one synthetic distribution does not establish language or real-world utility. CPU package only; E20/E21 language experiments remain **NOT RUN** here, their GPU ledger remains HELD, and E21 correction work is an independent lane pending its own review.
