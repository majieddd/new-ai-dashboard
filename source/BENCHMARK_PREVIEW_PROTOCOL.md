---
title: "New AI benchmark-program preview, inspired by Luke's Dev Lab"
tags: [new-ai, evaluation, benchmark, proposal]
status: draft
created: 2026-10-05
---

# A benchmark format to review, not an approved model test

The owner's reference is [Luke's Dev Lab video, “Swift 1.5 Qwen3.8-27B · GSQ-RCO tested”](https://www.youtube.com/watch?v=aNOUkWk9piU). I checked its public chapter list and YouTube storyboard frames and inspected the creator's [public benchmark interface](https://lukesdevlab.com/) on October 5, 2026. The video groups throughput, long-context memory, reasoning, Python coding and practical agent-built Kanban/Sand Physics/Dungeon Crawler/Blender/Godot artifacts. The public interface presents model configuration, matched side-by-side reports, denominators and category-level results. YouTube playback/caption retrieval was rate-limited in this session; I did **not** transcribe the full video or assert its exact private prompts and scoring.

`benchmark_suite_v0_1.json` translates those categories into **original New AI proposal descriptions**, not borrowed questions, numerical results, or logo/branding. `benchmark_preview.py` renders the static dashboard at `benchmarks/index.html` on the website, generated from `source/research-site/benchmarks/index.html`, with benchmark/agent-task filters, method/grade/control disclosures, and an intentionally locked comparison. The JSON file copied next to the page is byte-identical to the input, and the page displays its SHA-256.

## Proposed reporting contract

For each real model run, publish: model and tokenizer IDs plus hashes; quantization/adapter and framework revisions; hardware/VRAM; prompt template and decode settings; rights basis and split lineage; exact task/run IDs; trial-level responses and grader versions; wall time, memory and failures; aggregate numerators/denominators and uncertainty; score receipt and review status. Performance needs fixed cache conditions and GPU synchronization; long-context memory needs controlled position bins and decoys; reasoning needs declared strata and locked grading; coding needs a sandbox, answer-rate accounting and a task-rights/contamination check. Agent-built artifacts must actually build, reopen and run: source alone or a screenshot cannot pass Kanban, Sand, Dungeon, Blender or Godot.

The existing E19 failed outcome must remain what it was. These optional practical-capability lanes **do not amend E20/E21/E22 confirmatory gates or approve a run**. A current synthetic GPU optimization receipt, a synthetic CPU fastpath timing or a toy fixture cannot be imported as an official model score. `benchmark_preview.py` rejects any nonempty `official_results` or any test status other than `not_run`; a later scored-results renderer must be separately designed, reviewed and authorized with fresh final-data custody.

## Status and next decision

This is a **proposed** suite and visual preview, now published as a design for review. No tests were run on a New AI language model for this request, no official score exists, and no final data were acquired. Publishing the design does **not** approve the suite or change the research outcomes. Before calling it official, the owner should decide whether these capability lanes belong in the project's public evaluation program and approve a scope, source rights, task set, graders, budgets and independently sealed final split. The dashboard's current no-score state is the honest representation until then.
