# E16/E17 corrective instrument — October 3, 2026

This is a new, synthetic diagnostic. It does not replace any E0–E15 data or demonstrate an energy-based or self-evolving LLM.

## Hypothesis and protocol

An explicitly task-cued, frozen-core adapter can retain a previously learned rule while learning a second rule without replay; compare with a frozen model and a naive full fine-tune. This is an established, simple architectural control, **not** evidence for novel stress timing or energy minimization.

- `tasks_v2.py`: 2,048 unique six-symbol sequences drawn without replacement from 8⁶ possibilities; six position-specific one-hots and a two-way rule cue. `copy_first` and `copy_last` are deterministic eight-class tasks. Split once by sequence into 70% train / 15% validation / 15% sealed test. The same sequence stays in the same split across the two tasks. Old and new tasks deliberately use different rule cues.
- Train a 50→64→8 MLP on the first rule (140 steps). Freeze it. On the second rule only, compare frozen-only, full-model fine-tune, and a 400-weight, zero-initialized additive adapter applied only for the explicitly cued second rule. The adapter's old-task path is asserted bit-identical before and after training. No replay; all arms use exactly the same 140 new-task optimizer steps and minibatch index sequence. This is **not** equal FLOPs, trainable parameters or compute time; measure and report both. No validation selection is implemented yet; no test selection.
- E16: fixed LR .01 for both adapting arms; five seeds 1,7,42,123,999. E16 failed for the adapter on new-task learning: mean old/new test accuracy 100/12.01%, versus full fine-tune 12.01/100%, frozen 100/12.01%. Do not discard this negative run.
- E17: after inspecting E16 (including its test outcomes), choose an adapter LR of .15, keep full fine-tune LR .01, and evaluate on **fresh** seeds 13,17,19,23,29. E17 is exploratory, not preregistered confirmatory. On those five seeds the scheduled adapter achieves 100/100%, full fine-tune 14.16/100%, frozen 100/14.16% mean old/new test accuracy. This does not isolate learning rate fairness or stress-triggering. All five per-seed records and timing/parameter counts are in the raw JSON. The tasks are deliberately simple.

## Reproduce

From a checkout of this worktree, with PyTorch + NumPy available:

```text
python -m unittest discover -p "test_*.py" -v
python run_e16.py --seeds 1,7,42,123,999 --device cuda --old-steps 140 --new-steps 140 --out <NEW_EMPTY_DIRECTORY>/e16.json
python run_e17.py --device cuda --out <NEW_EMPTY_DIRECTORY>/e17.json
```

The runners refuse to overwrite their historical result paths. Each JSON includes the base commit, a dirty-working-tree warning, SHA-256s of the exact runner/task source bytes, software/hardware, counts, time and per-seed outcomes. The source changes are not committed yet; this is a provenance deficit to fix before calling the experiment independently reproducible. `test_e16.py` tests the encoding, deterministic oracle, disjoint train/validation/test sequence keys, task-cue isolation and zero-initialized adapter identity.

## Go/no-go and next causal test

E16/E17 only validate the corrected instrument and show a no-replay *fixed scheduled adapter* can outperform naive fine-tuning on retention for this deliberately task-cued split. A conditional-growth E18 should register threshold/selection **before** any new run, include a stress/energy-triggered adapter, a random trigger at matched event count, a scheduled/fixed-capacity adapter, frozen and full fine-tune, plus a competent adapter baseline; test on new datasets where a task cue does not trivially route old versus new. Calibrate novelty using held-out training-domain validation and report AUROC/delay/false alarms. Report equalized FLOPs/GPU time and independently held-out seeds. E18 failure versus scheduled/random means the stress trigger does not add value, even if a fixed adapter retains knowledge. Then separately test trained energy descent, adaptive growth, real text generation, and memory/ternary engineering. No model may alter its evaluator, data split or promotion gate.

Evidence: `tasks_v2.py`, `run_e16.py`, `run_e17.py`, `test_e16.py`, `results/E16/summary.json`, `results/E17/summary.json`. Original goals: `NEW_AI/master-plan.md` and `NEW_AI/sources/framework.md`.
