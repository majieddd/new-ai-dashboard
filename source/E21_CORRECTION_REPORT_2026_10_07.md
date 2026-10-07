# E21 focused development correction — tested handoff

**Author:** Energy Model Engineer. **Delegators:** Majied / Cloud AI Generalist; six-item correction brief by Orchestrator.
**Status:** implementation and CPU checks complete; independent evaluator disposition and integration pending. E21 language/M1/full hybrid remain NOT RUN / not demonstrated.

## Revision and scope

- Worktree: `C:/Users/Majied/.kr8/REPOS/new-ai-e21-correction`, branch `research/e21-correction-v1`.
- Correction preregistration committed before checks: `7b8f82970aafd09958c195f66f503f1c26db143b`, `E21_CORRECTION_PROTOCOL_2026_10_07.md`.
- Tested implementation: **`514d97645246de162be187a446536c2771746318`**. The safe final suite and separate reconstruction ran at this HEAD, with no tracked changes. This report and receipts are subsequent outcome evidence, not source attributed to the historical training revision.
- Reviewed historical checkout stays at `3f1be602cf1d8cfbd6bbf8dae7ee1d736611c5f1`; producing historical training revision stays `973914722c16967b1a219e329e7df231afe48278`.
- Recovered report hash verified before/after: `40224ff1a5aa27a32bf29d7f7d9664415dba290eb3190d155bb190b2fb4b47df`. It remains at its authorized Cloud AI Generalist scratch path; the denied RESEARCH placement was not bypassed.

No resident-model API/process/settings operation, GPU query/allocation/kernel, pretrained model/tokenizer/weights, corpus/final data/key, sealed evaluator, safety-gate or production-site change. CUDA hidden and offline for tests. **This milestone adds 0 GPU allowance seconds**, not a reset or claim of zero prior cumulative usage. No new original-study training run; inherited two-step E21 learnability and E16 CPU smoke tests are synthetic software fixtures.

## Six-item implementation and actual checks

| Brief item | Source/interface | Exercised result |
|---|---|---|
| Aggregate input/arithmetic rejection | `e21_scoring.py:35–70`, unchanged `score_tokens()` interface | Malformed rows, boolean/fractional/negative counts, out-of-range correctness, invalid/nonfinite NLL and aggregate/PPL overflow rejected with ValueError. Unequal-mask independent Python log-sum-exp matches token-weighted NLL; generators work. |
| Numerically safe radial projection | `e21_mechanism.py:14–41` | Max-coordinate-scaled fallback only for overflowing norms. Float64 1e308 / float32 1e30 vectors retain direction and radius 2, finite nonzero backward gradients; mixed zero/ordinary rows correct. Norm-overflow input inside radius 1e300 remains exactly unchanged. Ordinary first/second-order gradchecks and prior full-unroll tests pass. |
| K0 and explicit bypass | `e21_mechanism.py:142–147` | Both heads reject finite-input decoder overflow with ValueError: Nonfinite logits. Finite controls remain bit-identical, with zero head/candidate-gradient calls. |
| Terminal traced energy | `e21_mechanism.py:176–181` | Actual LatentRefiner extreme-weight fixture rejects K1 and K2 under no_grad; finite paired weights return all finite traces/logits. No fake substituted energy method. |
| Coverage/config/summary audit | `verify_e21_dev_v2.py:71–269`, API `verify(directory)` | Exact locked five-seed/nine-arm coverage, config and source authentication; prediction/step/exposure totals; independently reconstructed logits/latents/traces and scalar log-sum-exp; summary means/deltas/costs recomputed. |
| Serialized fixture/redundant receipts | same v2 reader, especially `:105–137` | Stored fixture tensors/hashes match regenerated tensors; record.json and seed_records.jsonl equal nested summary. Isolated and synchronized divergent mutations rejected. |

Line anchors refer to the tested implementation; tests live in `test_e21_correction.py`. The original `test_e21.py`, `run_e21_dev.py`, `verify_e21_dev.py`, config, protocol and historical raw/checkpoint files were not edited.

## Actual final execution

Existing interpreter: `C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe`, Python 3.11.9. Environment: CUDA_VISIBLE_DEVICES empty, HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1, one-thread Torch CPU fixtures.

1. `python -B check_e21_correction.py full --out correction_checks/run-002` creates a scratch mirror, discovers **46 unique tests**, runs all 46: **45 passed, 1 explicitly skipped, 0 failures/errors**, suite wall **21.468066400004318 seconds**, excluding imports. Includes all 18 original E21 tests plus 15 new correction tests; those are subsets, not additional totals. The only skip is `test_e19.E19Tests.test_corpus_hash_counts_and_disjoint_splits`, reason `Correction scope prohibits external AG News corpus access`. Audit hook denies that external path. Site-writing inherited tests run solely in the mirror, not a website checkout or deployment.
2. **19/19 receipt mutations rejected**, including all three previously accepted recovered mutations, the retained raw-NLL rejection control, isolated mean/delta/cost corruptions, synchronized missing/extra depth and aggregate/cost corruption, duplicate seeds, fixture/hash/record divergence, producing-source hash/omission, unsupported revision and config mutation. Exact rejection reasons and retained mutated trees: `correction_checks/run-002/mutations/` and `mutation_receipt.json`. These 19 cases are subcases of the new tests, not 19 independent model trials.
3. `python -B verify_e21_dev_v2.py --run results/E21_DEV/cpu-v1-run-001 --save correction_checks/run-002/reconstruction.json` accepted the unmodified original control: **five seeds, nine arms each, 2,880 predictions, 900 historical step records, 28,800 historical training-token exposures; maximum reconstructed-logit error 0.0**. All serialized fixtures and redundant records consistent. It reads/reconstructs checkpoints, **does not replay 900 optimizer steps** and does not remeasure their historical training clocks.
4. `check_e21_correction.py finish` for both retained evidence rounds confirms **145 reviewed source/result files byte-unchanged**, **143 protected files byte-unchanged in the correction tree** (only the mechanism/scoring files are intentionally revised), reviewed HEAD unchanged and recovered report unchanged. Original negative results remain. Reviewed checkout's pre-existing untracked RESEARCH/research-site folders were neither copied/executed nor modified by this work; no new claim about other agents' mutable files.
5. `git diff --check` passed. No Git remote is configured; these are local commits, **not pushed or published to the production site**.

## Explicit compatibility rule

The untouched v1 reader belongs to the original producing source and will correctly fail its disk-source guard if run in the corrected worktree. **Use v2 here**, not a weakened v1 source check.

V2 `E21-CPU-v1-audit-v2` supports only historical producer `973914722c16967b1a219e329e7df231afe48278`. It authenticates the complete six-file producing inventory against immutable Git objects at that revision, allowing only LF/CRLF checkout encodings. It also compares config to that committed object and the unchanged local lock. Current reconstruction-source exact byte hashes and current verification HEAD are returned separately. Omitted/altered hashes and arbitrary revisions fail. It does not claim new producing revisions supported; a later run needs a prospective compatibility lock. Current reconstruction compatibility is established by the full original prediction comparison, not by reattributing new source to old measurements.

## Reproducibility and evidence hashes

From the correction worktree, with the existing interpreter and CUDA-hidden/offline environment:

```bash
P='C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe'
export CUDA_VISIBLE_DEVICES='' PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
"$P" -B check_e21_correction.py begin --out correction_checks/<new-id>
"$P" -B check_e21_correction.py full --out correction_checks/<new-id>
"$P" -B verify_e21_dev_v2.py --run results/E21_DEV/cpu-v1-run-001 --save correction_checks/<new-id>/reconstruction.json
"$P" -B check_e21_correction.py finish --out correction_checks/<new-id>
```

Outputs use exclusive creation; choose a genuinely new ID, never rerun over retained evidence. The mirror uses the active agent's explicit profile scratch path. The report/review and source-pinning checks intentionally require local Git history and the referenced report; on another machine review snapshot placement needs approval rather than a silent relocation.

| `correction_checks/run-002/` evidence | Exact byte SHA-256 |
|---|---|
| `suite_receipt.json` | `2a769d66cd23d9f928be9ed6abddffcb31c7a5b91c1b54a34b9cff37732c9880` |
| `reconstruction.json` | `1a9ebc4ed90d2a7cd15ce25bd451f1bbda93eedff9567d19e27976f0738bf9af` |
| `mutations/mutation_receipt.json` | `1e3df00e75759fe398dc94f69a06e1659c1d89420ddef56f3cb4b3c05589e833` |
| `preservation_receipt.json` | `1c8fbc2c01b3968dd64747957d09502e52a82523819da1e6748213dad3ea3b25` |

Before/after full hash manifests, full suite test IDs/log and process command/mirror receipt are adjacent. Historical result scores remain mixed: v2 reconstructs original energy-K4 NLL 0.9267260288272446 versus direct-K4 0.9376331269966351, and energy-K8 0.931724869031713 is still worse than energy-K4. These are **historical synthetic fixture values**, neither language outcomes nor matched-compute wins.

## Disclosed setup correction and limitations

The first precommit focused/full runs inherited a tool-provided TMPDIR pointing at `C:/Users/Majied/AppData/Local/Temp`, contrary to the profile-scratch contract. The first full suite still passed 45/46 with the same no-corpus skip; it wrote its local-only mirror/site there and retained evidence at `correction_checks/run-001`. I corrected the harness/test temp roots to the explicit active-profile scratch path before source commit and the final run-002 execution. Nothing was deleted or overwritten; the final claimed receipt uses the corrected path. This is a setup deviation, not an E21 score defect, a production write or a reason to erase the earlier run.

Static tool lint passed. The editor's Pyright environment reports unresolved Torch imports for new files; actual execution uses the established Torch venv and passes. No claim of a green configured Pyright project is made.

The reader checks record consistency, immutable producing-source lineage and current checkpoint prediction reconstruction. It is not cryptographic attestation of timing, fresh optimizer replay, access custody, an independent second implementation or universal numeric correctness. Extreme-vector gradients are locally exercised; higher-order checks are ordinary non-boundary fixtures. Terminal energy validation is for evaluated traced telemetry, not an extra energy evaluation on non-traced direct or bypass paths.

## Lead/evaluator handoff

Imports remain `from e21_mechanism import FrozenReadout, LatentRefiner, project_ball` and `from e21_scoring import score_tokens, aggregate_token_scores`. No inference target argument or backbone mutation was introduced. For the old saved run, import `verify_e21_dev_v2.verify` or its CLI. Lead should integrate only reviewed files from the correction commit, not replace historical source/protocol/raw directories or cherry-pick mutated receipt trees.

Evaluation Scientist owns the independent disposition against the released review and public contract; Cloud AI Generalist owns integration/publication. No reviewer is duplicated or issue silently closed. No new human scientific approval requested by this CPU correction. Genuine rights/fit/measured-work/custody and candidate locks, controller/opening GPU ledger, and the owner disposition of the proposed 704-QA workload remain separate. The resident model must remain untouched; E19 FAILED and existing scientific gates stand.
