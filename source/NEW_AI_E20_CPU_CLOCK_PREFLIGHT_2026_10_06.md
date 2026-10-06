---
title: "E20 bounded CPU clock preflight on the approved-preparation path"
tags: [new-ai, e20, cpu, development, profiling]
status: active
created: 2026-10-06
---

# Scope and result

At the unchanged `REPOS/new-ai-e20-integrated` commit `f9e3a7ad82916ef158397c2c42396201f32b4913`, I independently reran the *synthetic* full-vocabulary audit clock in two fresh serial processes: pinned reference and integrated candidate. This is neither pretrained SmolLM2 fit nor E20 language acquisition, operational cost, or a scientific outcome. CUDA was hidden; no weights, tokenizer, corpus, final examples, or GPU were accessed. The committed development worktree remained clean, and four protected source files retained their byte hashes.

The candidate's one-window timed span was **9.251519400 s** versus **24.727551100 s** for the reference (**2.67281×** in this one pair). The generated audit JSONL bytes were *identical* (`cd424608c3e2e0cc47a795115435ca6aa0db9b0f7e09fc0c5a6ae4968afaf4e8`); an independent **read-only offline** reconstruction from the saved files checked all **775 audit events**, eight persisted snapshot files, and **329 actually scored masked targets** for each arm. It verified event order, snapshot byte hashes, per-target loss/count and before/after identity. The timed span excludes fixture construction, audit emission and reconstruction. A single pair is not a reliable speed estimate; the earlier three-pair synthetic profile is in `REPOS/new-ai-e20-integrated/E20_FASTPATH_PROFILE.md` and is not replaced here.

## Exact local execution

Venv: `C:/Users/Majied/jev-alt-bench/envs/main/Scripts/python.exe` with `-B`, `CUDA_VISIBLE_DEVICES=''`, `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=C:/Users/Majied/AppData/Local/hermes/profiles/cloudaigeneralist/cache/scratch/E20_CPU_PREFLIGHT_2026_10_06`. Working directory: `REPOS/new-ai-e20-integrated`.

1. `-m unittest -q test_e20_stream test_e20_fastpath`: first attempt discovered 46 tests, **45 passed / one environment error** because the first subprocess lacked `TMPDIR`; the code directly indexes `os.environ['TMPDIR']` at `test_e20_fastpath.py:200`. No source edits or skips followed. With the scratch `TMPDIR` set, the exact suite returned **46/46 passed**, exit 0, 15.212 s outer process wall (suite's own timing retained in the raw command output).
2. `profile_e20_fastpath.py --arm reference --case full_vocab --measurement timing --out <scratch>/reference`: exit 0; measured timed span 24.727551100 s.
3. The same command with `--arm candidate --out <scratch>/candidate`: exit 0; measured timed span 9.251519400 s.
4. Fresh read-only Python reconstruction of both saved `audit.jsonl` files and eight content-addressed snapshots each: exact SHA-256, tick sequence, complete stream, rebuilt `system_loss`/`active_loss`, and equality across arms. No rerun of a model or optimizer.

Raw artifacts: `C:/Users/Majied/AppData/Local/hermes/profiles/cloudaigeneralist/cache/scratch/E20_CPU_PREFLIGHT_2026_10_06/`:
- `PREFLIGHT_RECEIPT.json` SHA-256 `58d49f9cd9384606433ebdbfd9b800ce2d4b00f03ecb979df8226c96b7ba93a2` (both test attempts and both arm commands, exits and raw stdout/stderr, source hashes and paired metrics);
- `OFFLINE_READBACK.json` SHA-256 `2736f4b630bfb58a515bedac7d2b3b10eeee20a4a213e4cba14d42db346c402d` (independent saved-file reconstruction);
- `reference/` and `candidate/` retain measured JSON, audit JSONL and snapshots.

## Budget interpretation and next gate

The exact proposed stream contains 64 blocks × eight windows per arm, with eight arms × ten seeds. **Arithmetic only:** multiplying this one candidate CPU clock time by those counts gives 1.31577 hours per arm-seed or 105.26173 serial clock hours for all 80 arm-seeds, *if the same unbatched repeated-distribution clock were used unchanged*. This is **not** a measured GPU-hours forecast, lower bound, production memory estimate, or evidence the approved 24-hour GPU ceiling has been consumed or will necessarily be exceeded. The synthetic adapter uses eight repeated distributions, cheap scalar fingerprints and no real inference, tensor transfer, routing/GMM, QA or optimizer. A batched, validated audit backend could behave differently. The useful conclusion is narrower: the full E20 battery has **not been shown to fit** the approved ceiling; a genuine model-development fit and measured-work test must precede outcome execution, with changes independently proven causally equivalent and within the already approved ≤1h-development allowance. No extra GPU allocation or change to E19, gates, final custody or the website is inferred here. This CPU milestone adds **zero GPU seconds**; project-wide cumulative GPU use was not audited.
