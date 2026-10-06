---
title: "E20/E21 chargeable GPU receipt reconciliation and public TRAIN/DEV rights screen"
tags: [new-ai, e20, e21, gpu-budget, rights, preparation]
status: draft
created: 2026-10-06
revision: "0.1"
---

# Bounded reconciliation — October 6, 2026

**Scope:** exact owner approval event `875101f24904db17a0c2b5f9bb0592d3a9077e01ce5be85590fb77dd5dcd7bd3` is 2026-10-06 11:53:13 UTC; the approved packet is E20 24 exclusive GPU-hours total with ≤1 development hour INSIDE it, E21 separate 4h total with ≤1 development hour INSIDE it, E20 first. This report inventories **named public/local receipts**, not all historical machine processes or reservations. It performs no GPU work or model training, makes no budget debit or final-data access, and does not treat local file modification time as a signed exclusive start/end. Remaining chargeable balance is **UNKNOWN** until the gaps below are reconciled.

## Exact earlier E20 GPU development receipts

All four saved GPU receipt files below have filesystem modification times on **October 5**, before the October 6 approval. They document tiny random-model/synthetic-token development work, **not** the approved 1.7B language study. The in-process wall figures explicitly exclude process launch and, for the profile, other test reruns; they are neither exclusive GPU reservations nor exhaustive GPU time. The output hashes below were freshly computed from retained bytes. Producing commits/reports identify Cloud AI Generalist as the development implementer, but these receipt JSONs carry no signed controller identity or UTC exclusive intervals; charging them retroactively against the later approval is **not presumed**.

| Retained receipt and SHA-256 | Observed file mtime UTC (not run end proof) | Scope and measured in-process time | Missing accounting |
|---|---|---|---|
| `REPOS/new-ai-e20-gpu-profile/results/E20_DEV_GPU/receipt.json` `45d5d5b6dd4530db6c46c46ce0147d66d027d62429a3e054345ebe1e86ec128f` | 2026-10-05 15:27:30 | Random two-layer GPU profile: 0.7446302s script in-process; independent integration-test rerun 0.7797139s reported separately in `RESEARCH/NEW_AI_E20_GPU_DEV_PROFILE_2026_10_05.md:16-24` | Controller-signed start/end, exclusive reservation, launch/import/test envelope and test-rerun receipt |
| `REPOS/new-ai-e20-gpu-adapter/results/E20_DEV_GPU_STREAM/receipt.json` `af193b81c28be1be7a76c596a66ea0f11ae510defce55717eba0229532532988` | 2026-10-05 18:21:52 | Tiny random 4×2 stream, 5.4802652s in-process including imports/tests, 0.2045452s demo subset | Exclusive start/end, failed-attempt/controller receipt and any additional review rerun |
| `REPOS/new-ai-e20-gpu-adapter/results/E20_DEV_GPU_STREAM_RECHECK/receipt.json` `958c34dddd724a6a65c14cacde9fd7485b1e02982d5021b96ff395a8530038d7` | 2026-10-05 19:30:01 | Same tiny stream recheck, 5.7256686s in-process, 0.2170197s demo subset | Same missing reservation/controller/accounting evidence; distinct physical execution despite same audit hash |
| `REPOS/new-ai-e20-integrated/results/E20_DEV_GPU_FASTPATH_INTEGRATED/receipt.json` `b128cac0b775e400f4828cc045d2f51c10d6f5e010a9cfb158118d95e6e3ee9c` | 2026-10-05 19:35:34 | Integrated tiny stream, 5.4691007s in-process, 0.2190969s demo subset | Same missing reservation/controller/accounting evidence; same audit hash is **not** evidence of zero new compute |

Sources: each exact JSON above; `REPOS/new-ai-e20-gpu-profile/RESEARCH/NEW_AI_E20_GPU_DEV_PROFILE_2026_10_05.md:8-26`; `REPOS/new-ai-e20-gpu-adapter/RESEARCH/NEW_AI_E20_GPU_STREAM_2026_10_05.md:8-24`; `REPOS/new-ai-e20-integrated/RESEARCH/NEW_AI_E20_DEV_INTEGRATION_2026_10_05.md:8-28`. No unverified sum of event intervals or extrapolation to real model fit is credited.

## Postapproval evidence inspected, and exact gap

A bounded `buzz messages get` in the New AI channel from `2026-10-06T11:53:13Z` returned **37 events** at inspection; the scoped local worktree and report inventory contains E21 approved public metadata/CPU checks (`REPOS/new-ai-e21-approved-prep/E21_APPROVED_PREPARATION_REPORT_2026_10_06.md:15-36`) and our E20 CPU audit (`RESEARCH/NEW_AI_E20_CPU_CLOCK_PREFLIGHT_2026_10_06.md`) plus metadata ledger (`RESEARCH/NEW_AI_E20_RIGHTS_FIT_LEDGER_2026_10_06.md`). Each of these named milestones explicitly reports **zero GPU seconds**. The four named GPU receipts above all predate the approval. This is **not proof** that no unreported GPU process/window ran in another session, worktree or user account. E21 original CPU fixture's `REPOS/new-ai-e21/e21_dev_config.json:4` specifies CPU; that does not certify every project process. No signed exclusive-window ledger, complete process/NVML historical trace, or previous development usage ledger was located in these scoped sources.

| Allowance | Evidence-supported debit from the three named postapproval milestones | Project-wide chargeable cumulative | Remaining |
|---|---:|---|---|
| E20 24h total / ≤1h dev inside | 0 GPU seconds | **UNRECONCILED** | **UNKNOWN** |
| E21 4h total / ≤1h dev inside | 0 GPU seconds | **UNRECONCILED** | **UNKNOWN** |

**Exact missing entry/owner/evidence:** Cloud AI Generalist (execution lead) must recover or establish a signed chronological exclusive-GPU-window ledger from the owner/controller of *each* GPU run, covering UTC start/end, GPU ID, process/controller, failures/retries and overlap, source/config/model/checkpoint, hashes and receipt. For the four October 5 synthetic runs above, classify their preapproval status and any later test/reviewer GPU reruns explicitly; do not silently debit or erase them. For October 6 onward, reconcile all sessions/worktrees/accounting rather than inferring global zero from channel posts. If historic reservations are irretrievable, label the interval **unknown** and surface the specific proof deficit for a prospective baseline/owner decision before new GPU booking. No signed exclusive window means no positive balance claim and **no E20/E21 GPU scheduling yet**; no new cap or generic approval is requested.

## Versioned public TRAIN/DEV-only article-rights manifest v0.1

Machine-readable artifact: `RESEARCH/NEW_AI_E20_PUBLIC_TRAIN_DEV_ARTICLE_RIGHTS_MANIFEST_V01.json`, SHA-256 `79b61a7d40fb9ff7e2fe474010c7b295579e8a303d42c4ec58aed3669f235e97`. It points to ten raw public metadata-only API response files with SHA-256 readback in profile scratch (`E20_RIGHTS_LEDGER_20261006`). The manifest has **four entries, zero rights-cleared, zero TRAIN/DEV selections, no article bodies and no FINAL IDs/salt**. All four proposed first revisions fall in the date window, but that fact is insufficient:

- **Exclude:** `Fulham Municipal Orchestra` page `84284287`, revision `1375932739` is a 39-byte redirect to the older Fulham Symphony Orchestra. A new *title* is not fresh prose.
- **Exclude pending older-copy lineage:** `Ranchhodraiji Temple` page `84284087`, first revision `1375930456` explicitly says information was copied from `Dakor`. Its pre-cutoff revision `1377067824` has a comment about reverting likely LLM usage. No novelty, copy/attribution or content rights are presumed.
- **Hold:** `Retrotink` page `84284047`, first `1375929885`, pre-cutoff `1375937494`, nonredirect; bounded title logs return a creation event. Category B technology is only a proposal; full page/source and near-duplicate/rights review is missing.
- **Hold with incomplete archival metadata:** `Artists' Union England` page `84284093`, first `1375930602`; one live cutoff query reported `1375934463` before the archival batch hit **HTTP 429** on its cutoff request. The raw first metadata response is saved; cutoff/log raw responses are missing. Category C is only a proposal. We did not hammer the API or substitute invented evidence.

The first three entries' first/cutoff/title-log queries and fourth's first query were saved; a bounded offline check confirmed all **ten** raw file hashes and zero cleared/selected flags. The retrieval script and the partial failed attempt remain in the same scratch directory; the 429 is a recorded limitation. The source is the public English Wikipedia revision/log API, not a licensed development corpus; Wikimedia Terms §7's general licensing/attribution rules do not clear an individual page or its donor. **Next right-specific step:** identify/train-dev pages by creation and complete redirect/move/import/deletion/donor lineage, inspect article-body quotation/license/exception notices manually, review attribution and group near duplicates/QIDs, then record each selected revision/content hash and rights disposition **before** any development-content retrieval/training. Final content and private lineage remain with an independent custodian. Neither this metadata screen nor the publisher-declared Apache-2.0 model card authorizes full study execution.

**No gate or released software was changed.** E20/E21 language NOT RUN, E19 FAILED, candidate r0.1 NOT FINAL-LOCKED; E21 recovery worker owns its separate read-only CPU review and the reviewed source remains untouched. Named custodian/access holder and disposition of the new 704-QA proposal still need owner choice.
