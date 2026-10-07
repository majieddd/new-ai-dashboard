---
title: "Pilot-only amendment: Codex CLI decoding, cost unavailable"
tags: [new-ai, openai, benchmark, amendment]
status: active
created: 2026-10-07
---

# Orchestrator-approved pilot amendment (scoped, exploratory)

Authorizes, for the S-B pilot ONLY, execution through Codex CLI 0.160.1 default decoding (not temperature 0) with cost unavailable (token usage recorded per call, estimated_cost_usd stays null).

- Models: pinned gpt-5.6-luna and gpt-5.6-sol, fixed from the probe receipts; no post-run swap.
- Items: frozen S_B_PILOT_MANIFEST.json, SHA-256 69ff310ed4d1c4a277361a2d8d2ad7e0d710e051515fc0d7cd97865cbcaf166e; cap 20 items/model, 40 calls total.
- Status label: exploratory calibration. Results are NOT protocol-compliant temperature-0 comparisons; plots and receipts must carry that label.
- Owner authorization basis: in-thread request (event 626cf87e19f16cf21b626456670897a4c2b437333f70fde9d8680752b4c7300c) to use the OpenAI subscription and continue until tests are done.
- Constraints unchanged: no GPU, resident model untouched, no site publication without Orchestrator QA, receipts chained and hash-verified, failures recorded, no cherry-picking.
- S-A/S-C/S-D remain gated on a verified temperature-0 API path; this amendment does not extend to them.
