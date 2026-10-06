---
title: "E21 approved preparation: exercised public alignment/stationarity and pinned metadata"
tags: [new-ai, e21, public-checks, license, preparation]
status: draft
created: 2026-10-06
revision: "1.0.1"
---

# Verdict

**Owner-approved preparation advanced; E21 pretrained fit/language outcomes remain NOT RUN.** This is not a new training experiment, released defect correction, final evaluator/custody seal, EBT replication, or scientific gate revision. Approval is now verified and must not be described as absent. The evaluator has since specified the previously missing study fields as r0.1 proposals; their technical/curation disposition and the historical review-release boundary remain separate prerequisites.

Producing source: `eedfb0928e3a3fb4a1cbd501a652238f06645c26`, branch `research/e21-approved-preparation`, isolated worktree `REPOS/new-ai-e21-approved-prep`, from protected archive `b7e3c6656d4ead02d81c523431a5df34fcdf0315`. The scope was committed before execution. Authority/limits: `E21_APPROVED_PREPARATION_SCOPE_2026_10_06.md`, SHA-256 `d3aada32d07c19c039afd31078fb114565dc03c7648a081136fe7e3219f3cbc4`.

## Actual command and scope

Working directory `C:/Users/Majied/.kr8/REPOS/new-ai-e21-approved-prep`:

`CUDA_VISIBLE_DEVICES='' HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe -B run_e21_approved_preparation.py --out preparation_checks/approved-run-001 --append-master C:/Users/Majied/.kr8/NEW_AI/master-plan.md`

Exit **0**. Raw receipt: `preparation_checks/approved-run-001/RECEIPT.json`, SHA-256 `2c48802e7c8ca609008157cf3b3847bd86e0a337a25f298254ef7cb153ada96b`. Runner uses an explicit public metadata URL allowlist; offline HF/Transformers flags prevent library downloads, while Python retrieves only those metadata/license URLs. No model weights, tokenizer artifacts, corpus, final examples/answers/keys or custodian material was downloaded or accessed.

Actual observed environment, separately queried with the same explicit interpreter: Torch `2.11.0+cu128`, Transformers `5.17.0`, PEFT `0.21.0`, huggingface_hub `1.32.0`. These are installed versions, not replication of the publisher's training runtime or a pretrained compatibility/fit result.

## Exercised CPU software checks

- Full discovery: **71 tests discovered, 70 passed, 1 explicit scope skip, zero failures/errors**. The skipped `test_e19.E19Tests.test_corpus_hash_counts_and_disjoint_splits` deliberately avoids historic AG News corpus/test-text reads. It was skipped in the in-memory runner, not by editing historical tests.
- Nine new public checks cover exact keyed joins, independently shuffled annotations, missing/duplicate/foreign/invalid IDs, copy/no-mutation behavior, constrained boundary stationarity, nonstationary interior/wrong boundary, interior gradient mapping, small-step K8 nonconvergence, and invalid-input rejection. No difficulty annotation, QA quota, hard cutoff or scientific convergence tolerance is adopted by these fixtures.
- Public alignment counterexample: unjoined reverse ordering changes Spearman rho from `+1` to `-1`; keyed joining restores `+1` for the exact same invented item records. This proves an interface hazard, not genuine difficulty, energy calibration or M1 performance.
- On invented E(z)=(z-2)^2/2 constrained to [-1,1], z=1 has gradient -1 but zero projected-gradient mapping, while the wrong boundary/interior is nonstationary. Eight sufficiently small steps remain nonstationary. These are analytic public CPU cases; a supplied software tolerance is not the study's missing convergence lock.
- Known invalid aggregate rows, nonfinite K0 logits and overflowing radial projection **remain unresolved in historical mechanism/scorer source**. Existing characterization tests reproduce the latter defects and do not clear them. The new one-dimensional diagnostic is not a substitute fix to the historical multidimensional projection.
- Inherited synthetic optimizer assertions are unit checks, not fresh experimental training, checkpoint reconstruction, equal-work training or language evidence. The inherited static-site unit compiler wrote only an untracked `research-site/` fixture inside this isolated worktree; nothing was deployed or changed at the lead's production site.

CPU-suite measured wall: **1.1844289000000572 seconds**, excluding imports. Whole runner wall: **3.4437169000011636 seconds**, excluding initial script imports. These are software-preparation timings, not E21 GPU fit or model-training costs. **This milestone consumed 0 GPU allowance seconds**, launched no GPU model/profile job and reserved no window. Cumulative project allowance/reservation remains the lead's ledger responsibility. Approved E21 ceiling is **4 exclusive GPU-hours total including <=1 development/profile hour**, with E20 first/no overlap; no new blanket approval is sought.

Log: `preparation_checks/approved-run-001/CPU_SUITE.log`, SHA-256 `50ed223fb8d5be073defc90db770688501fede857c0d1c29b2b8dc38b70e06bc`. Different execution scopes are explicit: earlier implementer public run 62/62; independent evaluator 61 passes + one no-corpus-read skip; this additive no-corpus-read run 70 passes + one skip. None contradicts the others.

## Exact model metadata and license review

Read model identity **exactly** `HuggingFaceTB/SmolLM2-360M` at `f8027fd0eaeea54caa13c31d31b9fdc459c38b49`. API `sha` matched; complete returned sibling metadata enumerated **10 files** without retrieving the weights/tokenizer.[1][2][4]

The pinned model card declares `license: apache-2.0` and links Apache 2.0 in its License section.[1] The exact revision's `/LICENSE` request returned **HTTP 404**, and the complete returned sibling list contains no license/copying filename.[3][4] This is a missing standalone file, not evidence that the declared model license is absent. The canonical Apache-2.0 text was retrieved for notice/license preservation review.[5] The engineering conclusion is a **publisher-declared Apache-2.0 model candidate**; preserve the card, source revision, applicable license/notices with any permitted redistribution, and review third-party claims/rights separately. This is not legal advice, independent ownership proof, corpus QA reuse clearance or authorization to launch/download/run anything simply from this receipt.

Raw source hashes:

| Source | HTTP | SHA-256 |
|---|---:|---|
| Model card | 200 | `631f842e4a02262e07fc522ede86c816114541319dea53dbf86bac4539a24ac9` |
| Model config | 200 | `34f7801487078de7e434e19162c497e5cc6ff397080e40e8586627cb68a5168a` |
| Exact revision API metadata | 200 | `cba8f38aaef199c4fb1a59899dfc0b6f53fbf6cadfbcc274aa9ee4313acea9be` |
| Missing standalone license response | 404 | `f36668ddf22403a332f978057d527cf285b01468bc3431b04094a7bafa6aba59` |
| Canonical Apache license | 200 | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

Pinned config is `LlamaForCausalLM`, hidden width **960**, vocabulary **49152**, **32** layers, **15** attention/**5** KV heads, tied embedding/readout, no attention bias/dropout, `bos_token_id=0` and `eos_token_id=0`, max positions **8192**, declared `bfloat16`, and recorded publisher Transformers `4.40.1`.[2] A prospective real-model bridge therefore needs exact frozen readout/tied-weight handling, explicit dtype/numerical validation, and an engine/tokenizer-bound completion policy: BOS/EOS sharing an ID is not a receipt of a completed answer. This metadata check does not establish installed-version compatibility or measured fit. Do not cite the card's advertised memory footprint as this machine's measured memory or extrapolate the approved cap from it.

## Historical preservation and master append

All **158 existing protected archive files** had unchanged before/after SHA-256 in the runner. Separate `git diff --exit-code b7e3c6656d4ead02d81c523431a5df34fcdf0315 -- e21_mechanism.py e21_scoring.py run_e21_dev.py verify_e21_dev.py test_e21.py PROTOCOL_E21_V1.md e21_dev_config.json results public_contract_v02.py test_public_contract_v02.py e21_public_adversarial.py test_e21_public_adversarial.py` exited **0**. The reviewed v0.2 candidate and historical source/outcomes remain pinned; no reviewer was replaced or duplicated.

Authorized additive master record is `NEW_AI/master-plan.md:224`. `MASTER_APPEND_RECEIPT.json` verifies the then-current **75,752-byte** prefix, SHA-256 `2d32dd36f8d7b15cfc0a863d53752f4189b0c6d8a0b61623c78c3d5517a9daa2`, was preserved. Immediately after this append, master had **77,324 bytes**, SHA-256 `a548d3bc8d26318a223a093ea2cfd6f6ff2f0dcb9952b27c5c39165d5c3a2485`. An independent reread verified that original prefix hash again. Later lead/evaluator appends may legitimately change the full-file hash; this receipt binds only this append and its preceding bytes.

## Remaining specific dependencies / handoff

1. Existing review `0f25c2e33f4107dffe176021b236409f385bf69ca917764607dbb27b485e63cc` must return/disposition and release its snapshot before the focused new-version software correction. Release request event `5c30186a5ca0fbd9207c13a6d72b73df1ba8246cf6e42e352e2c5485826ce055` was read back exactly. No generic study/budget approval is repeated.
2. Evaluation Scientist's subsequently returned candidate r0.1 now specifies E21 QA/difficulty quantities/hard cutoff, convergence tolerance, generation/retention comparators and aggregation as **proposals**, not adopted fields. Exact candidate SHA-256 is `db2e3341411f569271920e16fe526941286c005d21eb8650d024c632c7a9a2f7`; see the readback/disposition below. The new 704-item human-curation workload still needs owner disposition; do not ask again for the approved study/compute ceilings. Keep the five-seed design exploratory; retain existing M1 and historical gates/results.
3. Actual separately reviewed development data/QA rights/lineage, pretrained bridge numerical/compute controls and measured development fit/cost must precede corresponding downloads/runs. E20 has window priority.
4. Approval accepts a separate-principal/off-host requirement but names no custodian. Smallest unresolved owner custody action: nominate/accept a specific custodian/access arrangement. Evaluator must verify actual denied-read canaries and privilege/key/mount boundaries for every learner/tool principal before final release. No final information or keys belong in the thread.

This milestone is eligible public preparation, not substituted model results. Lead retains execution/publication, evaluator retains language/custody QA, and Engineer retains E21 implementation. E19 FAILED/M1 unchanged; E21 language NOT RUN.

## Subsequent candidate r0.1 readback and technical boundary

Evaluation Scientist's event `dd3904c8d1894b729acfec0fe04f36c4203f4c1ba05abee6f3a5d437b2eb7bb5` returned `RESEARCH/NEW_AI_E20_E21_APPROVED_CANDIDATE_LOCK_2026_10_06.md`. I read the complete candidate and verified the exact returned hash; this does not adopt its proposed quantities or assert custody/fit. Its newly specified 128 train / 64 dev / 256-new+256-old final QA, essential-depth >=3 hard cutoff, residual criterion at each k6/7/8, comparator definitions and keyed within-seed/paired-mean aggregation are now explicit proposals, rather than missing numbers. Human annotation, shortcut/essentiality validation and practical-control feasibility remain unexercised.

Actual fresh **CPU-only** readback at unchanged source `eedfb0928e3a3fb4a1cbd501a652238f06645c26` used the explicit project interpreter with `CUDA_VISIBLE_DEVICES='' HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`, called the committed runner's `cpu_checks()` into NEW directory `preparation_checks/handoff-readback-001`, and asserted the original receipt, source hashes, five saved metadata response hashes, original test-log hash and candidate hash. Result: exit **0**, **70 passed / 71 discovered, one explicit no-corpus-read skip**, zero failures/errors, suite wall **1.1873071000009077s** excluding imports. All **158** protected archive files were unchanged during this fresh suite. Historical master prefixes of **75,752** and **77,324 bytes** also matched their earlier receipt hashes. Readback receipt: `preparation_checks/handoff-readback-001/READBACK_RECEIPT.json`, SHA-256 `a1bc04b18c81ab9a0413cf58b3aca0a0fbdb7c97febc9fe35c93d4c280461948`; fresh log SHA-256 `81b9c3760e9d6aacb8d630ba22fdae0ba4cb457d38e44d9f4cb3c065cec8edb0`. This adds **0 GPU seconds**; no second metadata retrieval, model/tokenizer/corpus/final access, checkpoint reconstruction or scientific experiment was performed.

Technical disposition is **PREPARATION ONLY / NOT FINAL-LOCKED**. The public 1D helper validates a supplied absolute software tolerance; it does NOT implement the candidate's vector relative criterion `1e-3 * max(1, ||z||)` at each k6/7/8, every-token/item coverage or across-seed M1 rule. Nor does the keyed item helper bind model/tokenizer/checkpoint/seed/arm/depth receipt identities or authenticate actual engine stopping. Those integrations require a separate reviewed implementation and representative development checks, charged to the allowed budget. The proposed all-context stationarity rule may make M1 unevaluable; no feasibility claim or tolerance change is inferred. Three historical defects remain untouched pending the existing review snapshot release. No duplicate review, new custodian or GPU reservation was created.

## Sources

[1] https://huggingface.co/HuggingFaceTB/SmolLM2-360M/raw/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/README.md
[2] https://huggingface.co/HuggingFaceTB/SmolLM2-360M/raw/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/config.json
[3] https://huggingface.co/HuggingFaceTB/SmolLM2-360M/raw/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/LICENSE
[4] https://huggingface.co/api/models/HuggingFaceTB/SmolLM2-360M/revision/f8027fd0eaeea54caa13c31d31b9fdc459c38b49
[5] https://www.apache.org/licenses/LICENSE-2.0.txt

Authority: original consolidated decision sheet SHA-256 `4aa92eda05be3bfd6e5c9d6ff2717207f1339996a6f93293bdbb5fec6e9a3b31`, owner approval event `875101f24904db17a0c2b5f9bb0592d3a9077e01ce5be85590fb77dd5dcd7bd3`, routed event `e450a2cb00a94431f16da7245bee4e49c70033ba516f0e46dfa4cdc9c3fec019`; independent contract r1.1 SHA-256 `6457c4de49ea0ad8bd98d4cb9dc1f9bd78e79354c800cf82a8edc4fb6d02a036`. Public source ledger: `preparation_checks/citations.json`. All metadata response bytes/request records and command receipts reside beside the raw receipt.
