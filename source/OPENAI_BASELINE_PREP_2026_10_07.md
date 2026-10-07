---
title: "OpenAI subscription baseline pilot preparation and blocker"
tags: [new-ai, openai, benchmark, cpu, probe]
status: active
created: 2026-10-07
---

# OpenAI baseline pilot: prepared, not run

The QA-accepted protocol is `RESEARCH/NEW_AI_OPENAI_BASELINE_PROTOCOL_2026_10_07.md` (SHA-256 `2c1b0464a08806c78f3171b985423b6a8a9ada3280031ae1d8c06ca0578595ee`). It requires two or more pinned models, temperature 0, and per-call receipts. The baseline calibrates instrument difficulty; it **cannot** validate the New AI growth, timing, retention or energy hypothesis. No New AI project gate changes.

## Subscription probe (readback, not benchmark)

- Installed Codex CLI 0.130.0-alpha.5 had a config parse error (`service_tier=priority`). With `--ignore-user-config`, `gpt-5.5` returned `READY`; candidate `gpt-5` and bundled 5.2/5.3-codex/5.4/5.4-mini were rejected for ChatGPT-account access.
- `gpt-5.6-luna` on the installed CLI returned “requires a newer version of Codex.” A scratch-only npm install of `@openai/codex@0.160.1` succeeded; `gpt-5.6-luna`, `gpt-5.6-sol`, and `gpt-5.6-terra` then each returned `READY` with JSONL token usage. Neither user-installed CLI nor config/auth files were modified.
- Probe receipts and usage are in `RESEARCH/NEW_AI_OPENAI_PROBE_2026_10_07.json` and `RESEARCH/NEW_AI_OPENAI_PROBE_2026_10_07/*.jsonl`; their archived byte hashes match the manifest. Timestamps are **file mtime UTC**, not server event timestamps; Codex JSONL does not include server timestamps.
- ChatGPT subscription tokens have no verified per-call dollar cost from this interface. `codex exec --strict-config -c 'model_temperature=0'` rejects the field as unknown, and the CLI has no verified temperature-zero switch. **Do not treat these probes as temperature-zero benchmark calls.**
- OpenAI's [billing guidance](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform) separates ChatGPT and API billing. Its [Codex plan guidance](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) says CLI work counts against the plan's allowance/credits, so API token prices cannot be presented as the subscription's per-call cost. The [API Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) describes a `temperature` field for API requests, not for this CLI transport.

## Frozen pilot preparation

- Local-only branch `research/openai-baseline-pilot`, commit `1d787df5af0dd8adf4313a968e0217e329026e47`, worktree `C:/Users/Majied/.kr8/REPOS/new-ai-openai-baseline` (no remote push).
- `openai_baseline.py` imports the existing `tasks_v2.make_stream(seed=31)`, selects the first 10 test sequences for each of `copy_first` and `copy_last` from the preregistered first 256 held-out sequences, and pins templates and item hashes in `S_B_PILOT_MANIFEST.json` (SHA-256 `69ff310ed4d1c4a277361a2d8d2ad7e0d710e051515fc0d7cd97865cbcaf166e`). Total 20 items/model, 40 calls maximum for two models. The same 10 underlying sequences appear in both rule tasks.
- The runner refuses benchmark execution unless a reviewed protocol amendment explicitly authorizes “Codex CLI decoding” and “cost unavailable”; it pins models and hashes before first response, appends chained per-item receipts with response and token counts, verifies hashes, resumes without repeats, and records failures. An amendment must be reviewed by Orchestrator before use; code's phrase check is not itself authorization.
- At committed source, full CPU unittest discover: **51 tests OK** (including 5 new offline harness tests); `CUDA_VISIBLE_DEVICES=-1`, project Python at `C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe`. The mock-transport test emits *synthetic mock answers* solely to test receipt handling and is **not a benchmark result**. A first attempt with Hermes Python 3.14 failed import because it lacked torch; rerun under the project venv passed.
- Actual benchmark items called: **zero**; real pilot receipt files: **none**; cost readback: unavailable; no site publication, GPU work, or resident-model changes. Inherited site tests produced an untracked `research-site/` build artifact in this isolated worktree; it was not staged or committed.

## Lead decision requested

Orchestrator to review an explicit pilot-only amendment for pinned `gpt-5.6-luna` and `gpt-5.6-sol` through Codex CLI 0.160.1 default decoding (not temperature 0), unknown monetary cost with token usage recorded, and exploratory/non-publishable-as-temperature-zero status. Without that amendment or a supported API route with verified temperature 0, pilot execution remains blocked.
