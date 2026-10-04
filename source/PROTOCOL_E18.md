# E18 pre-registration: input-only trigger identifiability (2026-10-04)

**Status:** locked before running outcome-producing code. This is a toy *detector* audit, not an expansion or LLM result. Prior work and rationale: `RESEARCH/NEW_AI_PRIOR_ART_AND_TRIGGER_LIMITS_2026_10_04.md` in the kr8 workspace.

## Question and non-claims
Can an input-only novelty/energy proxy determine that a new rule needs learning when the input distribution is exactly unchanged? Can it distinguish a visible but harmless covariate shift from a true label-rule change? This tests a necessary condition for an autonomous grow-on-stress trigger; it does **not** train a joint energy model, instantiate parameters, or use language data.

## Fixed design
- Fresh seeds: **31,37,41,43,47**. For each: 2,048 train, 512 validation and 512 test **unique** six-symbol sequences; first symbol restricted to 0–3, five others drawn uniformly from 0–7, split *before* labels. Classifier: 48→8 linear softmax model trained on `copy_last` for 160 Adam steps (batch 128, LR .05, no replay) from seed-dependent initial weights. The output is the last symbol, so a first-symbol shift is task-irrelevant.
- Test **concept shift**: *the exact same 512 test X* with `copy_first` labels. Input-only scores on old versus concept test are perfectly paired. No task cue and no feedback before scoring.
- Test **covariate shift**: 512 unique first-symbol 4–7 examples (other five uniform 0–7), with the **same** `copy_last` rule. Compare matched old test versus nuisance covariate test. Test examples do not overlap train/validation/test.
- Scores: (i) empirical per-position categorical negative log likelihood with Laplace +1 counts learned on old train (a strong input-density control); (ii) fixed classifier free energy `-logsumexp(logits)`, using the conventional high-energy = novelty direction fixed here; (iii) predictive entropy. The latter two are *logit proxies*, NOT a trained EBM. For concept shift, all input-only scores should achieve **exact AUROC .5** for paired inputs, including any other deterministic input-only score.
- Calibration: one-sided high-score alarm at the 95th percentile of held-out old validation; compare FPR and TPR for nuisance/concept test. AUC uses mid-ranks/tie handling; no tuning on test. For feedback, prequential *error* is observed **after a label arrives**. Divide ordered validation/test streams into non-overlapping blocks of 32; set error-count threshold to the maximum old-validation block, alarm only when a block exceeds it. Report earliest alerted block as detection delay (32,64,… labels), false-alarm blocks, and classification accuracy before any adaptation. No adaptation is permitted in E18.
- This is a synthetic stress test with domain-shift simplicity; no FLOP/compute equality claim. Report per-seed raw metrics, source SHA-256, git commit, software/hardware and dirty-tree state. Do not overwrite historical E0–E17.

## Primary acceptance and fail criteria
1. Paired concept AUROC of **0.5 for every input-only score** (an invariance check, not a win). If not, treat it as a code/data leak, not a discovery.
2. Input-density score should detect nuisance shift (at least **90% TPR**, at most **5% FPR** averaged over seeds) while old and nuisance accuracy stay at least **95%**. If so, novelty alone would trigger unnecessary expansion.
3. With label feedback, block-error alarm should detect concept shift within **64 observed labels** on all five seeds with at most **5%** false-alarm blocks in old validation and old/nuisance test. If classifier baseline or calibration does not meet these gates, record the failure and do not silently retune.

Regardless of outcome, **no** E18 score supports model growth or learned EBM claims. Next study must include matched random/scheduled/SEMA-like triggers and a nontrivial cue-free adaptation task; preregister before looking at its test set.
