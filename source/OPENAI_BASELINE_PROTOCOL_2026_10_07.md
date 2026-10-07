---
title: "Preregistered benchmark-comparison protocol: OpenAI-model baselines on project instruments"
tags: [new-ai, benchmark, openai, protocol, preregistered]
status: draft
created: 2026-10-07
author: "Researcher"
---

# OpenAI-baseline comparison protocol v0.1 (preregistered, pre-run)

**Scope:** protocol design only. No runs performed by Researcher. Cloud AI Generalist executes after Orchestrator QA. CPU-only on the project side; OpenAI arms are external API calls (no GPU on this machine, resident model untouched). Publication follows `SITE_PUBLICATION_CHECKLIST.md` exactly.

## 0. What this comparison is and is not

OpenAI baselines **calibrate task difficulty** on instruments the project already measures. They **do not validate the New AI hypothesis**: an OpenAI model has no frozen core, no growth trigger, no retention measurement, and no energy inference. A gap between an OpenAI arm and a project arm is evidence about task difficulty, never about growth, timing, or energy mechanisms. No gate on any project instrument is changed by this protocol; OpenAI arms have **no gates** (they cannot pass or fail the hypothesis).

## 1. Baseline arms (pinned before first response)

- Model set: exactly **4 models**, chosen by the Generalist's subscription probe, pinned as exact API model-ID strings recorded in the probe receipt. Candidate IDs (confirm availability, do not assume): `gpt-4.1`, `gpt-4o-mini`, `o4-mini`, `gpt-5`. If fewer than 4 are available on the subscription, pin the available set (minimum 2) and record the shortfall; never substitute a model after the first response.
- Decoding: `temperature=0` for all arms; for reasoning models pin `reasoning_effort` at one fixed level for the whole run; fixed max-token budget per subset stated in the runner.
- Prompt: **one fixed template per subset**, committed in the runner before any call; template SHA-256 recorded in every receipt. No prompt edits after the first response; a template change requires a new subset ID.
- Endpoint: chat/responses API with logprobs enabled where the metric needs NLL.

## 2. Task subsets (exact counts, from instruments already measured)

**S-A: E19-style binary topic transfer (AG News, SetFit/ag_news pinned revision `ca5ba619eb034211db5f70932b6702efd21e7c73`).**
- Items: seed 31 cleaned selection, **200 items per stage** (100 per class), Stage A World→0/Sports→1, Stage B Business→0/Sci/Tech→1, fixed order, item SHA-256 list committed before calls. Total 400 items per model.
- Metric: exact class accuracy (n/N per stage) and sequence NLL over the two class tokens from logprobs.
- Project arms: E19 frozen base A, feedback adapter, scheduled adapter (existing E19 arms, seeds 31,37,41,43,47; E19 **FAILED** gates stand).
- Licensing: items are sent as bounded API requests only; corpus stays uncommitted; no redistribution.

**S-B: E16/E17-style rule copy (synthetic, generated, no licensing).**
- Items: **256 unique six-symbol sequences per task** (8^6 space, drawn without replacement, pinned generator seed), `copy_first` and `copy_last`, same sequence set for both tasks, split rule as E16/E17. Total 512 items per model.
- Metric: 8-class accuracy per task; retention delta (old-task accuracy after learning the second rule) is project-side only — OpenAI arms see both rules cued and cannot be measured for retention.
- Project arms: E17 scheduled adapter, full fine-tune, frozen (seeds 13,17,19,23,29).

**S-C: E18-style detector audit (synthetic).**
- Items: **512 unique test X** (first symbol 0–3, five uniform 0–7), concept shift = same X with `copy_first` labels.
- OpenAI arms see the rule explicitly in the prompt (cue-present accuracy, calibration ceiling). Project arms: input-only density score (AUROC, expected 0.5 by invariance), block-error feedback alarm (delay, false alarms). The OpenAI cue-present accuracy and the project AUROC 0.5 are the published contrast.
- Metric: cue-present accuracy per model; AUROC/FPR/TPR project-side.

**S-D: small public reasoning subset (self-authored, rights-clean).**
- Items: **32 original items authored in the protocol commit** — 8 per band (easy/medium/hard/expert), deterministic gold answers, no third-party dataset. Total 32 items per model.
- Metric: exact-match accuracy per band, answer rate.
- Project arms: none runnable today (hybrid_dev is toy-scalar; E22 candidate has open validity defects). S-D is OpenAI-only calibration; state that in the section.

## 3. Preregistered comparison rule and plot spec

- One figure per subset; **one metric per axis** — never mix accuracy and NLL, never mix toy accuracy and text accuracy on one axis (checklist rule).
- Bars per arm with n/N denominators printed; project arms show per-seed bars + mean; OpenAI arms show single bars (temperature 0 is deterministic per item; no seeds, no significance test claimed on OpenAI arms).
- Paired per-item scatter only where items are identical across arms (S-A, S-B, S-C).
- Gate thresholds stated before running: project arms keep their existing gates (E19 gate 2: feedback ≥65% new, ≤5 pt old drop, ≥2 pt advantage over scheduled in ≥4/5 seeds; E18 gates 1–3). OpenAI arms: no gate. Verdict language: "calibration reference", never "beaten" or "outperformed" as a hypothesis claim.
- Negative results publish as failures, unchanged.

## 4. Cost discipline and receipts

- Cap: **≤1,500 items per model** (400+512+512+32 = 1,456), **≤4 models**, **≤6,000 total calls**. Stop before running if the probe shows subscription quota below the cap; state the shortfall.
- Per-call receipt: model ID, prompt-template SHA-256, item SHA-256, full response text, token usage (prompt/completion/reasoning), logprobs payload SHA-256, cost, timestamp, endpoint. Receipts append-only, one JSONL per model.
- No GPU on this machine, resident model untouched; project arms run in the established project venv CPU-only.

## 5. Publication path

Raw JSON (per-item responses, receipts, per-seed project records) under `data/`, generator reads them, `check_publication()` + full unittest discover pass, PR to the dashboard repo, lead QA, merge, deployed-byte verification. Site states explicitly: OpenAI baselines calibrate; they do not validate growth.

## 6. Stop condition

Protocol delivered to @Orchestrator for QA; **no runs performed by Researcher**. Execution is Cloud AI Generalist's, only after QA.
