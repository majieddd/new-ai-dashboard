# E18 result — input-only triggers do not identify a label-only rule shift

Executed 2026-10-04 under the locked `PROTOCOL_E18.md`; raw per-seed scores, thresholds, input hashes and environment/source hashes are in `results/E18/summary.json`. Five previously unused seeds: 31, 37, 41, 43, 47. Nine repository unit tests passed. This is a toy detector audit, not an EBM training, expansion, or language experiment.

| Metric | Five-seed result | Interpretation |
|---|---:|---|
| Old vs exactly paired concept input-only AUROC (categorical NLL, logit free energy, entropy) | 0.5000 each, every seed | The input X is identical; no fixed input-only score can tell which rule supplies its labels. |
| Old vs *harmless* covariate shift: categorical input-NLL AUROC / TPR | 1.000 / 100% | Detects a strong out-of-support first-symbol shift even though the old last-symbol rule still works. |
| Input-NLL old validation alarm rate (95th-percentile quantile) | 5.078% | **Misses** literal preregistered ≤5% FPR by 0.078 percentage point due to finite 512-example calibration and strict `>`; do not silently revise the run. |
| Input-NLL old test alarm rate | 4.727% mean (3.125–7.227% across seeds) | Aggregate held-out FPR passes 5%; two individual seeds exceed it. |
| Logit free-energy / entropy AUROC on nuisance | 0.481 / 0.499 mean | These fixed classifier proxies do not detect this shift; they are not trained EBMs. |
| Old / nuisance task accuracy | 100% / 100%, all seeds | Novel input != needed adaptation. |
| Concept task accuracy before adaptation | 12.344% mean | The old rule fails when the answer changes from last to first symbol. |
| Error-feedback alert on concept | after 32 observed labels, all five seeds | Labels provide information absent from input-only scores. No model learns a new rule in this experiment. |
| Feedback false alarm on old validation, old test, nuisance | 0/16 blocks each per seed | The pre-registered maximum-validation-error threshold was zero, and the old classifier made no errors on old/nuisance data. |

**Gate accounting:** paired-AUROC invariant passes; nuisance detection and accuracy gates pass on held-out mean FPR, but the old-validation FPR narrowly fails the literal ≤5% constraint; feedback gate passes. Report that calibration caveat, not an unqualified success. Finite-sample uncertainty and intentionally stark shifts make these numbers a diagnostic, not a real-world operating characteristic.

The core result is structural, not a claim about all autonomous learning: input-only novelty cannot see an identical-X label flip *until* a task cue, outcome feedback, or correlated temporal/context signal arrives. A later growth experiment must distinguish a novelty alert from evidence that adding parameters improves held-out performance over scheduled/random and SEMA/MaRS-like controls under a comparable budget. The next round should preregister a 5%-target finite-sample calibration with explicit quantile/tie handling, use a harder cue-free task, measure adaptation and retention, and preserve the E18 mismatch as a negative result.
