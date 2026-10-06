---
title: "E21 public contract v0.2 exercised handoff and unresolved adversarial findings"
tags: [new-ai, e21, cpu, public-contract, findings]
status: draft
created: 2026-10-06
revision: "1.0.0"
---

# Verdict and producing state

**Public proposal/software checks exercised; independent adoption/review OPEN. E21 language scientific verdict NOT RUN.** No new experiment/checkpoint training, language/GPU study, model/tokenizer/corpus download, final content/key, scientific gate change, or production site operation occurred. The inherited unit suite does perform its existing two-step synthetic optimizer assertions; those are not a new training battery or model result.

Assignment: Orchestrator `16b8a29d50f18afe85294921cfb7b1b3509f8fa32c1f3d5dd07908a76a88fe8b`, owner continuation `4e68e00977e07f928ccaf238e8b373246b87ef529b6f9cd2be18097353c758ce`, existing E21 issue `0e554492d915f3f04ea51986245d8cc8b321ef9d647e152a19e2407565dd6fb7`. Implementer: Energy Model Engineer. Lead: Cloud AI Generalist. Evaluation Scientist owns independent contract/difficulty/gauge review; this report is not that review.

Isolated worktree `C:/Users/Majied/.kr8/REPOS/new-ai-e21-public-contract`, branch `research/e21-public-contract-v02`. The reviewed historical worktree stays at `3f1be602cf1d8cfbd6bbf8dae7ee1d736611c5f1` with its pre-existing untracked public preparation/site directories. No duplicate review worker was spawned.

- Declared public check/proposal scope before execution: `6d5b59b`.
- Adversarial probe code producing the retained first receipt: `6334b655e3833c5ee803d12154209f1a635a3848`.
- v0.2 parser/tests/check runner producing the test/command receipt: `12d86de2c6c94334f237c12fad02883e414598c1`.
- Proposal: `E21_PUBLIC_CONTRACT_V02_PROPOSAL.md`, SHA-256 `2796256bc540cc27005c4b47d9b71ff8d6706745db9137521c5ff5504a56c5f1`.
- Parser: `public_contract_v02.py`, SHA-256 `23f5cc062e60731389f1dcb4e091dccd705177d7691285568071e460d908724b`.
- Raw receipts/logs: `public_checks/v02-run-001/`; exclusive creation, no overwrite.

# Actual commands and results

All ran in the isolated worktree with `CUDA_VISIBLE_DEVICES=''`, explicit existing project interpreter `C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe`, `-B` and inherited profile-owned scratch `TMPDIR`. No dependencies were installed. Default editor Pyright cannot resolve Torch; runtime used the established project venv and succeeded. Deliberately invalid type/immutability test cases can trigger editor diagnostics but are executable negative tests.

1. `python.exe -B e21_public_adversarial.py --out public_checks/v02-run-001/ADVERSARIAL_RECEIPT.json`: exit 0. Five public synthetic seed contexts; mathematical Jacobians and preserved failure observations; 15 existing checkpoint byte/hash inventory entries, **not reconstruction or training**. Receipt SHA-256 `172786043a1c48acf30ddd3ed47c2abf8b7c49a4f7063928c695b91f8992f3e0`.
2. `python.exe -B run_e21_public_checks.py --out public_checks/v02-run-001/COMMAND_RECEIPT.json`: exit 0. Its exact subprocess argv/stdout/stderr are saved, not reconstructed from this prose:
   - `python.exe -B -m unittest -v test_public_contract_v02 test_e21_public_adversarial`: **31 discovered, 31 passed, 0 skipped**. Process wall 1.7600842999963788 seconds including imports/startup; unittest reports 0.244 seconds.
   - `python.exe -B -m unittest discover -v`: **62 discovered, 62 passed, 0 skipped**. Process wall 4.262572100000398 seconds. These are 31 inherited plus 31 additive tests, not 93 independent tests across both runs.
   - `python.exe -B public_contract_v02.py --out public_checks/v02-run-001/PUBLIC_PROBE.json`: exit 0; 12 invented public parser cases plus graph/gauge fixture.
   - Command receipt SHA-256 `3935007aa8f4e624d09eb51aaa4b6a3f5ddeba1fb9f70ab5702eb0649b13e1e1`.

Pre/post byte inventories preserve **148 existing protected files** (baseline tracked files present on disk plus v0.1 source/test/proposal). New source bytes also stayed unchanged during checks. `git diff --exit-code 3f1be602cf1d8cfbd6bbf8dae7ee1d736611c5f1 -- e21_mechanism.py e21_scoring.py run_e21_dev.py verify_e21_dev.py test_e21.py PROTOCOL_E21_V1.md e21_dev_config.json results` exited 0. Full suite generated only an untracked local `research-site/`; it was not staged, uploaded or deployed.

# Severity-ordered implementer adversarial findings

These are newly exercised findings, not the missing independent review's verdict. Severity is scoped to the software contract; none demonstrates corruption of historical predictions or failure of the scientific hypothesis.

## Medium, unresolved: nonfinite K0 prediction accepted

`e21_mechanism.py:116–125` validates finite context then returns bypass/base logits at `:122–123` without a logits-finiteness check. A copied model with entirely finite decoder entries 2.0 and finite context entries 1e308 returns nonfinite K0 logits; the same copied model at K1 raises `ValueError: Nonfinite logits`. This violates the universal reject-nonfinite-logits promise in `PROTOCOL_E21_V1.md:66` for the bypass path. Historic weights/source/results are untouched. Ask the existing reviewer/lead to disposition a versioned boundary fix after snapshot release; do not silently retrofit recorded runs.

## Medium, unresolved: radial projection silently collapses under finite norm overflow

`e21_mechanism.py:14–21` checks candidate entries but not the derived norm. CPU float64 `[1e308,1e308]` has an overflowing naive norm and projects to `[0,0]` rather than approximately `[1.4142135623730951,1.4142135623730951]` on radius 2. It remains bounded/finite, but no longer implements Euclidean radial projection for this input. A stable norm/projection or explicit derived-norm rejection is a candidate remedy, not adopted here. Not observed in the saved ordinary fixture. Passing the characterization test reproduces the defect; it does not clear it.

## Medium, corrected only in unadopted v0.2: bare stop can gain correctness

v0.1 `public_contract.py:26–47` accepted `stop_reason='stop'` and exact answer without receiving any bound completion policy. Its prose warned about this but the API could not enforce the warning. v0.2 requires an immutable CompletionPolicy carrying an exact lower-case 64-hex source locator, Boolean EOS permission and explicit distinct nonempty stop strings, plus an exactly matching observed stop string. Missing policy, unmatched stop, truncation/error/unknown receipt and inconsistent EOS/stop metadata fail. Policy/alias malformation is an instrument error. An engine receipt can still lie: policy hash/type validation proves neither owner approval nor actual tokenizer/engine stopping. The result explicitly records `engine_completion_authenticated=false`. Real integration must independently bind policy/tokenizer/EOS/stop IDs/token budget and inspect raw generated tokens. This public fixture is not custody or final-evaluator adoption.

## Low, corrected only in unadopted v0.2: integer ranks lose distinctions

v0.1 `public_contract.py:110–116,134–147` converted every numeric value to float before ranking. Distinct integers `[9007199254740992,9007199254740993,9007199254740994]` became ranks `[1.5,1.5,3]` instead of `[1,2,3]`. v0.2 preserves exact integer values through ordering/tie assignment, including huge integer annotations, while computing the resulting ranks/correlation in floating arithmetic. Nonfinite/missing/Boolean inputs still reject and constant/too-short vectors remain INVALID. Mean-energy reduction rejects floating-conversion overflow. No real difficulty annotations or correlation outcome were changed.

# Additive mechanism/control diagnostics

Seeds 101,103,107,109,113 here are existing public SOFTWARE fixture contexts, not final seeds. Across them:

- Scalar-energy Hessian maximum antisymmetry: **2.7755575615628914e-17**.
- Independent central finite-difference maximum Hessian error: **7.90089105251468e-11**.
- Direct-update Jacobian antisymmetry range: **0.052615806630370666–0.13032267317063553**.
- Both have 293 trainable head scalars; no-grad logits identical; all parameters/frozen buffers unchanged; no accumulated parameter gradients.

This checks the actual conservative scalar-gradient versus a direct field not constrained conservative at these nondegenerate fixtures. It does not equate their expressivity or compute. Separate one-step training/frozen readout/target isolation/full-unroll gradient checks are inherited tests and original raw checkpoint lineage at training revision `973914722c16967b1a219e329e7df231afe48278`; no new checkpoints were trained. Historical CPU exposure comparison remains **not matched measured compute**; its original mixed/negative results stand.

# Difficulty/gauge limits retained

DAG depth validation rejects cycles/padding/malformed parents and handles a 4,000-edge chain without recursion. It deliberately does **not** certify the truth, minimality, essentiality or semantic difficulty of a structurally valid redundant chain. Independent blinded annotators, shorter-solution adjudication, arity/rule/length/template/nuisance balancing and shortcut tests remain required; no hard cutoff was picked.

Energy is reduced on identical teacher-forced scored-token contexts, not incomparable free-running contexts. Offsets reverse the invented raw rho from +1 to -1 while preserving energy drop. Raw absolute energy therefore remains gauge/convention-dependent; source pinning makes it reproducible, not calibrated. Energy drop is diagnostic, not a replacement acceptance statistic. Master M1 and all prior thresholds remain unchanged. This proposal is not a density model/novelty trigger, EBT replication, competitive LM or self-evolving system.

# Review and owner dependencies

The existing independent code/control review issue `0f25c2e33f4107dffe176021b236409f385bf69ca917764607dbb27b485e63cc` has no checked returned report in this handoff; liveness/disposition belongs to Cloud AI Generalist's owning session. No independent endorsement is claimed. Route the two unresolved historic-mechanism findings there; independent evaluator may adopt, reject or amend this v0.2 candidate prospectively.

Language execution remains blocked at its explicit scope/budget/gate/rights/QA/profile/fresh-seed/uncertainty/custody dependencies. Nominated 4h total/<=1h dev is not approved. A separately accepted principal/off-host custodian with actual denied-read probes is required; another worktree/agent under Majied is not isolation. No final keys/answers may be sent here. Evaluator owns the consolidated decision sheet; implementer does not choose those decisions. E19 FAILED and E21 language NOT RUN stand. Lead owns scoped website publication after independent review; no site operation performed here.

# Additive commit-attribution erratum

The code commit `12d86de2c6c94334f237c12fad02883e414598c1` has correct Energy Model Engineer author/committer identity but an incorrectly transcribed Agent-Owner trailer token: `844d344115ac6b7717969528a7b3c3e31bb45acf823b49247e6cec8ba9fc34`. The verified project-owner coordinate is `844d344115ac6b7717969528a7b3c3e31bb45acf82383b49247e6cec8ba9fc34` (context/repository assignment). This additive erratum corrects the ownership record without amending history or changing the producing revision/bytes. Subsequent commit trailers use the exact verified coordinate. This is a metadata transcription defect, not a scientific-source/outcome change.
