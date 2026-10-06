---
title: "Original model goal and October 6 requirements-to-evidence trace"
tags: [new-ai, requirements, e8, e20, e21, public-status]
status: draft
created: 2026-10-06
---

# The requested bot is not yet delivered

**As of 2026-10-06T17:38:19Z, there is no runnable real-language bot meeting the owner's original specification.** This is a requirements trace, not a revised gate or authorization to spend GPU time. The primary intent is the owner's root channel event `47ff4515b673e26334f26fba90af389fb3ff266d96e38ff961414709af5953f0`, `NEW_AI/master-plan.md` §§1–3 (notably lines 29–47 and 103–107), and `NEW_AI/sources/framework.md`. The owner reiterated the original task at event `4f494a7e8ff42fb335a5ec53732e7fb48f4c1963ce7006f39070650a82682791` on October 6.

| Requirement | What the retained evidence establishes | Status / existing workstream |
|---|---|---|
| Frozen small language core and pretrained adaptation/control | E20 code/preflight was exercised on tiny synthetic tokens and random-weight models. A SmolLM2-1.7B base revision was pinned in metadata; no pretrained weights or article text were loaded. | **NOT RUN** on the language core. E20 owns measured fit then adaptation/control. |
| Learned iterative energy refinement | E21 synthetic CPU mechanism/contract tests and public preparation QA exist; independent code/control review is still separate. | **NOT RUN** as a pretrained-language test. E21 owns the isolated comparison. |
| Novelty causes new trainable parameters | E18's input-only detector fails the same-input/changed-label counterexample; E20 growth path is a synthetic software check. | No causal language demonstration; E20/E21 controls remain necessary. |
| Older skills remain after growth | Historical E19 real-text linear-classifier gate **FAILED**; toy retention checks cannot establish language retention. | Not met; independently scored old/new held-out checks are required. |
| Better capability at matched compute | The E20 one-pair CPU synthetic timing measures neither capability nor complete compute. | E8 composition **NOT STARTED**; matched measured-compute control remains ahead. |
| Ternary CPU efficiency and tiered VRAM/RAM/NVMe memory | E4 substrate and E5 paging are separate system requirements, not substitutes for the bot. | No validated real-bot efficiency/paging result. |

**Next model-delivery checkpoint:** measured development fit for the pinned pretrained core and an independently reviewable frozen-core adaptation/control run, only after the rights, final-data custody and sole-controller GPU reservation/opening-balance decisions. E20 approved cap remains 24 exclusive GPU-hours, including ≤1 development hour; E21 separate 4, including ≤1 development hour. The approved caps are not reopened. Chargeable remaining balance is **UNKNOWN**; GPU booking **HELD**. No article entry was rights-cleared or selected for TRAIN/DEV. The separate E21 code/control reviewer has not released its snapshot. Official nine-lane benchmarks and E20/E21 language trials are **NOT RUN**.

**Public evidence on this revision:** `NEW_AI_E20_CPU_CLOCK_PREFLIGHT_2026_10_06.md`, `NEW_AI_E20_E21_GPU_RESERVATION_RIGHTS_RECONCILIATION_2026_10_06.md`, and `NEW_AI_E20_E21_GPU_COMMAND_ENVELOPE_RECOVERY_2026_10_06.md`; their exact source/receipt SHA-256 values are in `data/status-2026-10-06.json`. `E21_APPROVED_PREPARATION_REPORT_2026_10_06.md` and `data/e21-approved-preparation-readback.json` carry the separately bounded E21 public-preparation result. The site generator tests pin and verify the newly copied raw bytes before building.
