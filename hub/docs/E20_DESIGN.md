---
title: "New AI E20 — independent pre-outcome language-model evaluation design"
tags: [new-ai, evaluation, preregistration, continual-learning, language-models]
status: draft
created: 2026-10-05
---

# E20: real language adaptation, causal timing, and a bounded energy ablation

**Author:** Evaluation Scientist. **Delegator:** Cloud AI Generalist. **Design only: no E20 model was run.**

**Recommendation:** use a pinned, pretrained SmolLM2-1.7B causal decoder, not another news-classification head. Test task-free adaptation on a fresh, group-disjoint English prose stream, against capacity-matched fixed LoRA, replay, scheduled and rate-matched random expansion. Keep an energy-scoring experiment separate from language-model perplexity. Do not call a conditional scoring head an energy-descent LLM.

**Protocol status:** this is an independent candidate acceptance protocol with numerical decisions specified before E20 outcomes. It is **not yet a runnable, sealed preregistration**: the corpus, human QA, software lock and custodian commitments do not exist yet. The owner must approve the substantive budget/benchmark choices in §12, then the custodian and implementer must complete §11 before any confirmatory outcome run. Publish a signed/hash-identified lock record; never describe this draft as an already sealed test.

Worktree: `C:/Users/Majied/.kr8/REPOS/new-ai-e20-eval`, branch `research/e20-independent-design`, read-only historical base `0cdc379b2cd43d24780318becf9cae55af26c814`. Requested shared copy: `RESEARCH/NEW_AI_E20_EVAL_DESIGN_2026_10_05.md`. No historical protocol, runner, website, or GPU state was changed.

## 1. Inputs independently checked

Read `NEW_AI/master-plan.md:29-47,115-141,155-160`; `REPOS/new-ai-e19/PROTOCOL_E18.md:8-21`; `PROTOCOL_E19.md:6-21`; both reports, both runners and the complete raw JSON through a CPU-only arithmetic audit. Machine-readable recomputation and input SHA-256 hashes are in this worktree's `RESEARCH/E20_INPUT_AUDIT.json`.

| Audit item | Independently recomputed result | Consequence for E20 |
|---|---|---|
| E18 paired input-only AUROC | Exactly 0.5 for all three scores, each of five seeds; old/concept raw arrays identical | A detector cannot identify a changed answer from unchanged input alone. Explicitly disclose the feedback channel. |
| E18 old-validation input-density FPR | 0.05078125 in every seed | Avoid interpolated-quantile ambiguity; specify integer order statistic, strict comparison and ties. |
| E19 feedback delay | 32 labels for every seed | E19 did not establish autonomous timing beyond a first-block schedule. |
| E19 feedback balanced accuracy | 0.7466052294 mean | This is a binary hashing-feature classifier score, not generation or standard four-class AG News. |
| Feedback minus scheduled | 0.000000 points, all seeds | Preserve the failed causal-timing verdict. |
| Feedback minus random | +0.5473679304 mean points | Below the locked +2-point requirement. |
| Feedback minus full fine-tune | -3.9842098951 mean points | No overall classifier win. |
| Feedback new accuracy / old drop | 0.5915262818 / 0.1894712448 points | New accuracy missed 65%; low interference did not imply useful acquisition. |
| Recorded feedback adaptation time | 0.0727289400 mean seconds | Head-training wall time only; not end-to-end GPU cost or LLM throughput. |

Relevant runner paths: `run_e19.py:98-113` hard cosine-centroid route; `:147-150` maximum-old-error trigger; `:169-190` first-block schedule and arm-specific subsequent training slices; `:193-209` identity check/training/scoring. Timing also changed which examples trained the adapter, so E20 must log exposure explicitly rather than attributing every difference to timing. `run_e18.py:121-130` interpolated quantile; `:136-144` feedback; `:169-174` recorded CPU device. In particular, the E18 raw record says **CPU**, not GPU.

Audit elapsed time was **0.2335849000 CPU wall seconds** for loading, hashing and recomputing the recorded quantities; it did not rerun historical training. No GPU runtime was imported for this calculation. E20 training/inference cost remains **unmeasured**.

## 2. Primary-source implications and reproduction labels

| Original work inspected | What matters here | What this E20 would actually be |
|---|---|---|
| FiUni, Han et al., arXiv:2608.27070v1, §§3.1–3.3, 4, C | K-FAC activation/gradient eigenspaces drive reuse/expand/new decisions; frozen left/right bases with trainable core matrices; two-window confirmation. Eq. 9 sums subspace updates into effective weights. Detection uses forward **and backward** work, not a free input-only scalar. Paper reports T5-Large/LLaMA-3.1-8B and SC/LS/TRACE.[20] | **Not a FiUni reproduction.** A scalar loss trigger plus ordinary routed LoRA lacks Fisher-guided construction, geometry and summed-subspace inference. A future full-method port must implement all these components, count frozen bases as stored weights, and declare changed backbone/stream as a replication on new conditions. |
| HESTIA, Le et al., UAI 2026, §§2–4 and parameter appendix | Order-invariant linearized adaptation and sufficient statistics are central; adapter-specific Gaussian-mixture embeddings guide detection and routing. Retrieval guarantees assume density quality and separability; they are not unconditional retention guarantees. Experiments are **vision**, including CIFAR/ImageNet-R/VTAB, not pretrained language generation.[21] | **Density-routing-inspired proxy**, not HESTIA. Frozen-prefix GMMs plus SGD LoRA omit linearized closed-form learning and adapter-specific representations. Never transfer its accuracy or theorem to our LM. |
| Task-Free Continual Learning, Aljundi et al., CVPR 2019 | Streaming, gradual change without known boundaries is an established setting; the original method makes MAS importance updates online in face recognition and navigation.[11] | Task-free experimental **setting**, not an implemented MAS baseline. Ordinary reservoir replay below is our explicit strong comparator. |
| TRACE, Wang et al., 2023, §§3–4 | Eight diverse tasks; separates target-task performance from general ability, instruction following and safety; uses full FT, LoRA, replay and ICL. Published tasks can already occur in model training.[34] | Our new prose/QA stream is **not TRACE** and does not establish multilingual, code, safety or general reasoning retention. A standard TRACE reproduction is a distinct, licensed-data project with its own ID. |
| SmolLM2 original paper and pinned card/config | A genuine 1.7B autoregressive decoder; paper studies data mixing and general benchmarks, not this growth mechanism. Card separately reports base and instruct evaluations.[24][30][31] | Use the **base** checkpoint and its tokenizer consistently. Model-card leaderboard numbers are source claims, not measurements by this project. |
| Li et al., Energy-Based Models for Continual Learning, CoLLAs 2022, §§4.2–4.3 | Conditional input-label energy, sampled negative labels from the current batch, argmin-energy classification; does **not** require MCMC negative images or latent inference descent.[33] | §8 is a **bounded conditional-energy scoring proxy** on generated answers, not their continual image-classification method or a joint generative EBM. |
| Nalisnick et al., ICLR 2019 | High likelihood can favor unrelated inputs; density is not equivalent to task competence.[35] | Measure capability, nuisance alerts, routing mistakes and false expansion separately. |

Public code provenance inspected without executing it: FiUni `2fcc502c8af2fd3c14d92c023bc509b37f6ed503`; HESTIA `2d755f7a06c1da99231fc7f627a4d6457ed57e6d`; TRACE `462e39f616134f4f819efeb3baea8638c03c7db4`. Public FiUni tree retrieval was complete and contained **no LICENSE/COPYING file**; public visibility is not permission to redistribute its implementation.[40] HESTIA root license is MIT and TRACE root code license is Apache-2.0; neither automatically licenses their bundled datasets or third-party components.[38][39] Saved tree records are in `RESEARCH/E20_SOURCES/`. Do not copy FiUni implementation until permission is resolved; independently specified paper-based methods still require attribution. This is a bounded source review, not a novelty certification.

## 3. Questions and scope to lock

**Q1 acquisition:** does adaptation improve held-out conditional next-token prediction and retain old language ability relative to the common starting model?

**Q2 causal timing:** does feedback-timed expansion outperform fixed-time and rate-matched random allocation at the same maximum added-weight capacity and training-token budget? This is a stricter question than “does adding an adapter help?”

**Q3 replay/capacity:** does any advantage survive a single rank-24 adapter and a rank-24 task-free replay comparator? If not, capacity/isolation or rehearsal is a sufficient explanation on this stream.

**Q4 energy component:** does trained answer energy improve selection from an identical candidate pool beyond LM likelihood, an equal-sized confidence scorer and shuffled energy labels? A success is a reranking result only, **not** latent energy reasoning, growth timing or normalized full-language perplexity.

E20 does not test ternary kernels, cold-layer grafting, self-generated training corpora, unbounded growth, model-code self-modification, quantum acceleration, general recursive improvement, or a 50%-compute advantage over full fine-tuning. Do not combine Q1–Q4 into one “overall intelligence score.”

## 4. Model, memory and weights

**Checkpoint:** `HuggingFaceTB/SmolLM2-1.7B`, revision `effd688a12921b4cc83e3312b6feb579f70f9c71`. Public metadata retrieved here reports 1,711,376,384 BF16 parameters, repository creation 2024-10-30 and last modification 2025-02-06.[29] Pinned card declares Apache-2.0; a standalone `LICENSE` at this base revision returned HTTP 404, so retain the pinned card and upstream license reference rather than inventing a file.[30]

Use `AutoModelForCausalLM`, BF16, tokenizer from the exact same revision, no remote custom code, no quantization, no context/tokenizer change between arms. Config has 24 layers, hidden size 2048, 32 attention and 32 KV heads, tied word embeddings and vocabulary 49,152.[31] Raw BF16 weight storage is **3,422,752,768 bytes = 3.1876869202 GiB**, a static parameter calculation, **not** a measured peak memory allocation. Frozen backbone plus short-context LoRA is a realistic candidate for a 24 GB device; actual fit and speed must pass the development-only profile before locking (§11). Never substitute model-card memory for actual optimizer/activation/KV/allocator memory.

**Adapters:** q_proj and v_proj in all 24 layers, bias none, dropout 0, rank 8, alpha 16 (scale 2). Rank-24 capacity controls use alpha 48 to keep the same scale. Standard LoRA freezes pretrained weights and learns low-rank updates; this is an established technique, not a project invention.[32]

Calculated counts: rank-8 q/v adapter = `24 × 2 × 8 × (2048 + 2048)` = **1,572,864** weights; three slots or one rank-24 adapter = **4,718,592**. Count actual tensors before execution and abort on disagreement. Count frozen old adapters, density statistics, random projections, scorer weights, optimizer state and replay bytes separately; “only one active slot trains” is not a total-parameter or FLOP equivalence.

**Common old warm-up:** per seed, train one rank-8 adapter on 131,072 A input tokens (64 optimizer steps of 2,048 input tokens). Preserve an immutable checkpoint A0; each adapting arm receives its own mutable copy, so its pre-expansion updates must not overwrite the retention reference. All arms begin with identical outputs. The rank-24 controls embed the trained first eight ranks and zero the additional B columns with the same scale; verify identity. This avoids giving the capacity control a different starting competence.

**Expansion design:** clone the currently active rank-8 adapter into a new slot, freeze its parent, train only the active child. A clone has the same initial function, but is **not zero-initialized sprouting**. Router initially aliases the parent until the new key has 32 observed prefixes. Log the difference. Three slots maximum including A0; no pruning, offline expert graft or forced late expansion.

**Optimization:** AdamW, learning rate 1e-4, betas (0.9,0.999), epsilon 1e-8, weight decay 0, gradient norm clip 1.0. Sequence length 512; microbatch 2, accumulate 2 for 2,048 input tokens/step. Gradient checkpointing on, training KV cache off, generation cache on. Two updates per stream block, no additional epochs. Fixed LR, no final-test early stopping. Exact library versions, attention backend and deterministic settings are a required implementation lock, not guessed here.

Target measured peak allocated **and reserved** memory at or below 22 GiB. If the machine cannot provide this working margin, abort the profile; do not terminate another agent's job or silently change precision, length or backbone.

## 5. Fresh corpus, rights, leakage and stream

### 5.1 Source selection and freshness

Proposed corpus: **English Wikipedia main-namespace prose first created between 2026-03-01 and 2026-09-30 UTC**, using the last permitted revision at or before `2026-09-30T23:59:59Z`. This is after the pinned checkpoint's recorded modification. MediaWiki provides revision IDs, timestamps, content and hashes; use immutable revision references, not “latest” URLs.[27]

A custodian must verify first creation history, redirects, moves and imports; a new page title with old copied prose is not fresh content. Strip categories, infoboxes, HTML, source URLs, revision dates, edit summaries, references, navboxes and page titles from **model inputs**, preserving ordinary body prose. Keep metadata only in the audit manifest. Prefer local archived retrieval/bulk sources with respectful access; save retrieval failures. Exclude fair-use quotations, disputed copyright/import notices, sensitive personal records, long quoted third-party text, bot-generated list pages and provenance that cannot be verified.

Families defined for the curator only: A geography/history; B science/technology; C arts/sports; G broader politics/economics/biography prose used only as a retention guard. Define a disjoint category/QID assignment table before selection; ambiguous pages are excluded, not reassigned after scores. Body semantics are implicit domain cues: **task-free means no explicit task ID, not absence of all input information**. This narrow same-language prose stream is not a hidden-concept-shift theorem test.

Rights: Wikimedia text generally offers CC BY-SA 4.0/GFDL with attribution and project-specific exceptions; verify footer/history and imported material individually. Modified/released text requires attribution, change notices and the applicable share-alike license; images have separate licenses and are excluded.[26] Archive article/revision/history URLs and rights notes. Do not assume CC licensing determines the legal status of downstream model weights; obtain an explicit release review before publishing adapters. Neither SmolLM2's Apache label nor TRACE's code license licenses our corpus.

**Freshness limitations:** first creation after a frozen checkpoint reduces direct exposure to that exact revision; it does not prove unseen facts, no older web copies, or complete pretraining decontamination. Report exact-text/near-duplicate and sampled web checks plus a residual-uncertainty statement. Wikipedia facts can be known already. This tests new prose/domain adaptation, not first discovery of facts.

### 5.2 Splits and quotas

Group **before splitting** by page lineage/QID, redirect/move lineage and connected near-duplicate clusters. Normalize for audit using Unicode NFKC, case-fold and collapsed whitespace. Exact document/paragraph duplicates are grouped; compare word-five-gram Jaccard >=0.8 and exact contiguous normalized 64-token overlaps across prospective splits. Boilerplate is removed before clustering. Use deterministic connected-component grouping, log thresholds and all removals. Related QA/context/answers and all revisions of a page stay in the same group. A custodian may examine proposed test text for integrity only, never model outcomes.

Use one fixed corpus partition for all model seeds: group hash buckets 00–59 training, 60–79 development/calibration, 80–99 sealed final, salted by the custodian before model work. A corpus manifest commits selection/filter versions, salt commitment, page/revision IDs, per-file SHA-256 and selected byte/token counts. Do **not** reroll the partition to find an easier benchmark.

Minimum training quota: A 131,072 warm-up input tokens plus sufficient disjoint A/B/C documents to construct each 262,144-token stream. No document reuse within one seed's online stream; sharing the same training pool across seeds is allowed and documented. Development needs separate A calibration blocks and B/C learnability windows; no training or replay reads development files. Require at least **199 disjoint A blocks of eight 512-token windows** for threshold calibration and at least 128 development windows each for B, C and G.

Sealed final: **128 distinct-page windows per A/B/C/G**, each 512 tokens, prefix 128 and scored suffix 384: **49,152 scored tokens per family**. Also seal **512 additional distinct-page A windows** for the 64-block stationary detector diagnostic, disjoint from the main final windows. That diagnostic runs frozen A0/initial-density monitors only, with no adaptation, and evaluates the confirmation/cooldown policy without changing trained checkpoints. If quotas or grouped independence cannot be met, stop and ask for a corpus/date-window amendment **before** lock; do not pad by repeating articles or replacing with AG News/WikiText-2. These are proposed quotas, not a claim that those pages have already been collected.

Nuisance diagnostic: precommit a whitespace-only transformation of final QA contexts (replace runs of horizontal spaces by a tab and insert a blank line between existing paragraphs; preserve words/punctuation/questions/aliases). Score prefix-density changes and paired greedy-QA quality on those contexts. No assumption that this is harmless to a tokenizer; report both changes. Treat an increased density alarm rate as an unnecessary-capacity warning only if paired QA deterioration is <=1 point. This is secondary, not an extra opportunity to tune thresholds or claim a guaranteed false-alarm rate.

Generation extension: human-verified grounded short-answer QA, **128 questions per final family** (512 total), each with a source context and accepted answer aliases; at most one question per final page. Separate training-only scorer set 64 questions per A/B/C (192 total); development 16 per A/B/C/G (64 total). Human authors work from the allotted pages, not model guesses. Preserve rights/attribution and lock wording/aliases before model scoring. Three fixed in-context demonstrations from development only; same `Context / Question / Answer` format for every domain and arm. Current context <=384 model tokens, question <=64, each complete demonstration <=96, prompt total <=1,024 and answer <=32 new tokens; lock the exact formatting/demonstration IDs. Author questions answerable from the supplied context, not an omitted suffix. Generation routing uses **only the first 128 tokens of the current source context**, never the shared demonstration prefix, question/answer or metadata, and holds its chosen slot fixed for that answer. Energy prompt features exclude demonstrations as well. Otherwise the same first 128 demonstration tokens could force every QA item onto the same route and silently invalidate the claimed context-based router. Context makes this a comprehension test, **not closed-book acquisition of unseen final-page facts**.

### 5.3 Hidden stream and labels

Ten paired seeds: **101,103,107,109,113,127,131,137,139,149**. These are E20 seeds, not a claim that no historical project run ever used any of them. Derive separate RNG streams for order, minibatch order, LoRA initialization, routing projection and random triggers; persist draws. Swap B/C order on alternating listed seeds (five each).

64 blocks × eight 512-token windows = **262,144 observed input tokens**. Custodian draws first drift onset j1 uniformly from blocks 12–20 and second onset j2 from 36–44. Four transition blocks have new-domain proportions 1/4, 1/2, 3/4, 1. Before j1 use A; between transitions use the first new family; after the second use the other. Every eighth block is A recurrence, overriding the phase mixture; all instances remain new pages. Publish exact draws after final scoring, not to learning policies. Fixed scheduled policy may know block count but not onset draws.

For each block: reveal prefixes; make/save predictions and prefix-only routing decisions; reveal natural continuations; compute pre-update loss; queue any allocation **only for the next block**; perform two updates on the revealed block with its previous active slot; update replay/key statistics causally; then, if queued, clone the now-updated parent and freeze it before the next block. Scheduled/random allocation uses that same end-of-block ordering. Label feedback is the observed suffix from natural text, not an external topic ID. Never route using suffix, answer, source metadata, true phase, future blocks or held-out NLL. Shared frozen feature/monitor caches may be physically reused across arms for convenience, but their standalone computation must still be charged to any method that needs them.

## 6. Arms and routing controls

| Arm | Parameters beyond frozen backbone | Online policy | Purpose |
|---|---|---|---|
| F | One frozen A0 rank-8 slot | No learning | Same-start frozen reference; separately retain untouched base checkpoint metrics. |
| L8 | One rank-8 slot | Train continuously, no replay | Simple sequential PEFT baseline. |
| L24 | One rank-24 slot | Train continuously, no replay | Matches maximum three-slot weight capacity without modular routing. |
| R24 | One rank-24 slot + bounded replay | Train continuously, 25% replay | Strong constant-capacity task-free comparator. |
| S3 | Up to three rank-8 slots + keys | Clone after blocks 16 and 40 | Non-oracle fixed schedule, same architecture as feedback. |
| U3 | Same maximum capacity as B3 | Rate-matched random allocation below | Isolates allocation timing conditional on number of added slots. |
| B3 | Up to three slots + keys + loss monitor | Two consecutive high-loss blocks, cooldown 8, at most two additions | Feedback-driven candidate. No hit means no addition. |
| D3 | Same slot/key budget | Two consecutive high prefix-density scores; same cooldown/cap | Input-only density alarm control, not an energy-trained model. |

R24 reservoir: 128 whole windows (65,536 input-token capacity), initialized from A training only, updated with all revealed stream windows via uniform reservoir sampling. Before inserting current samples, draw one memory window and three current windows per effective batch. Two batches use six of eight current windows selected by a logged uniform draw without replacement; thus R24 sees the same stream but trains on fewer distinct current tokens. This equal-processed-token tradeoff is explicit, not concealed by claiming equal fresh-data training. Log replay repeats and age. A data-exposure-matched replay arm would need extra compute and a new budget; do not silently give it free extra updates.

Every adapting arm processes the same **262,144 training input tokens** in 128 stream updates; F processes none for training. Older slots freeze only after cloning. All slots count as stored weights. For U3, commit a random ordering of eligible blocks 8–56 before seeing stream labels, with an eight-block minimum separation. After B3 finishes streaming but **before any held-out score**, read only its count k of additions, take the first k eligible draws, sort, and rerun U3 on the identical stream. This locked conditional-count procedure controls rate; U3 gets no B3 times or scores. If k=0, there is no causal expansion-timing win to claim. Publish k and the random order. S3 may have more slots if B3 uses fewer; L24 remains a maximum-capacity comparator.

**Router common to S3/U3/B3/D3:** frozen *unadapted* backbone features from each 128-token prefix only; mean last-layer hidden representation, fixed seeded orthonormal projection 2048→64, standardized with A-training means/variances (variance floor 1e-6). Per-slot diagonal GMM with eight components, covariance floor 1e-3, equal slot priors; route to minimum prefix negative log density, deterministic smallest-slot tie break. Initial A key uses 256 training prefixes; new keys warm with the first 32 causally observed active-slot prefixes, then fit/update from a bounded uniform reservoir of 256 active-slot prefix features, ten EM iterations per block with fixed initialization/draws. Freeze a parent's key and feature reservoir together with its adapter. A child is not a selectable route until its 32-prefix key is fit; the parent remains selectable during that warm-up, even though the child's outputs may diverge after learning. No true domain supervision. Include density buffers and fit time/bytes. This is deliberately not HESTIA's adapter-specific feature space. Fix floating-point precision, GMM initialization and failure behavior in the implementation lock; nonfinite density is a recorded numerical failure, never an implicit task-oracle fallback.

Training uses the active chronological slot; inference uses the prefix router. This distinction is fixed and reported. A recurrence is not permission to pass its label to the router or reactivate a frozen expert for training. At final evaluation, save router selections and predictions for each sample. Compare inference against every slot offline and report the gap to a **best-slot oracle**, computed only by the scorer; oracle scores never tune routing. Domain/slot contingency tables are diagnostics, not an assumption that one human family must equal one latent adapter. If useful learning exists only with the oracle route, the autonomous system fails.

Add an oracle-onset scheduled reference only if budget is explicitly extended. Label it privileged and exclude it from task-free superiority claims; it is not one of the eight primary arms.

## 7. Calibration, metrics and acceptance decisions

### 7.1 Thresholds fixed without final data

For B3, block score is mean conditional suffix NLL of the **currently active adapter**, predicted on all eight windows before any updates on that block. Calibration uses A0, and the resulting threshold is fixed thereafter; do not recalibrate new slots. Save the active-slot monitor predictions separately from router-selected system predictions and charge any extra forward pass. A fixed A0-only loss monitor would remain high even after acquiring the new domain and could spend both additions on one persistent shift, so it is not the nominated feedback policy. The adaptive monitor can itself change score distributions; this procedure has no uniform calibration theorem, and its behavior must pass the empirical diagnostics. For D3, block score is mean negative log density under the **fixed initial A key** using prefix-only features; persistent novelty alarms are counted even after the capacity cap.

Sort n=199 old-development block scores. Threshold is the **190th order statistic** (`ceil((n+1)×0.95)`), alarm iff score strictly greater, ties never alarm. A two-consecutive-block confirmation creates an event for the next block; clear the streak after an event; wait eight complete blocks before another event. No multiplier, dynamic threshold or sign switch. Quantile construction yields at most 9/199 = **4.5226130653% calibration exceedances**, absent invalid counts; it does **not** guarantee future <=5% under dependent/nonstationary data. Do not call this a time-uniform false-alarm guarantee.

No scan of final ROC curves for an optimal operating point. Sensitivity plots on development only may accompany the record but do not change the nominated threshold. On the final stationary A diagnostic stream, report both per-block exceedance FPR and actual confirmed expansion events; continuing alarms after two-slot cap still count as detector alarms.

### 7.2 Per-seed raw records

For arm m, family d and checkpoint t, store sum negative log probability and **actual scored target count**. `H(m,s,d,t)=sum_NLL/count`; `PPL=exp(H)`. Use identical tokenizer/windows/prefixes/masks. For a 512-token window, score target positions 128–511 using their causal preceding logits (384 targets). Count from the **shifted valid-label mask**, not `valid_labels - batch_size` unless that identity was actually proved for that mask. Unit-test against explicit token sums. Padding, context and EOS/BOS conventions must not change denominators across arms. This is fixed-context **conditional suffix PPL**, not full-corpus sliding-window WikiText PPL; context and tokenization affect comparability.[37]

Report A/B/C/G individually; macro H = equal-family mean; new H = mean over B and C. Never arithmetic-average example PPLs. Save checkpoints at block 0,24,48,64; final scorer may evaluate those immutable checkpoints in one sealed transaction after training. No checkpoint selection after viewing their scores.

Record:
- Final new-domain gain versus F: `H_F,new - H_m,new`; acquisition separately for B and C.
- A and G retention loss versus **that seed's common A0**; maximum deterioration over scored checkpoints and per-family curves. Frozen-core status is not a retention proof when routing/adapter outputs change.
- Prequential per-block sum/count **before** suffix training; area under cumulative prequential NLL versus observed tokens. This is online training-stream prediction, not the sealed test metric.
- Post-first-exposure learning curves and recurring-A performance; evaluator-known onset used only for analysis/delay calculation.
- Trigger count/time, observed-label-token delay, false events in pre-onset A, event count during recurring A and cooldown/cap saturation. Missed shifts retain null delay, never a forced final event.
- Final grounded-QA greedy EM and token F1, by family and macro; normalize with locked lowercase/punctuation/article/whitespace rules and aliases. Empty/invalid answers score zero. Also report answer lengths, repetition and truncation.
- Router choices, best-slot oracle gap and lost/gained quality for A/B/C/G; no oracle labels in inputs.
- Total/trainable/active/frozen parameter counts, actual serialized bytes, replay/key/projection/scorer/optimizer bytes, number of examples/tokens seen and trained (distinct and repeated).
- Costs defined in §9 and all infrastructure failures; source, checkpoint and manifest hashes.

### 7.3 Gates to nominate before lock

The numbers below are design choices about practical effect size, **not literature-proven guarantees**. Owner may change them before locking, never after an outcome.

**Validity gate V (development only):** exact split/causal/parameter/mask invariants pass; all counts nonzero; actual memory <=22 GiB; common A0 dev grounded-QA macro EM >=30%; fixed R24 on development improves new conditional H by at least 0.02 nats/token on **both B and C** within the nominated token budget. If the stream is not learnable under this control, report INVALID INSTRUMENT and stop before final unsealing. Do not salvage it by silently increasing epochs or switching corpus. No absolute A language perplexity cutoff is guessed across unrelated prose.

**Acquisition/retention gate A:** B3's ten-seed mean new H improvement versus F >= **0.0512932944 nats/token** (a 5% reduction in geometric-mean conditional PPL), with positive new improvement in >=9/10 seeds and neither B nor C mean worse than F. On **each of A and G**, mean final H deterioration versus A0 <= **0.0198026273** (2% PPL increase); no individual seed deterioration > **0.0487901642** (5% PPL increase). Mean greedy-QA EM drop on each A/G <=2 percentage points, no seed drop >5 points. Report checkpoint worst-case losses even when the final gate passes.

**Strict timing/control gate T:** B3 final A/B/C macro H is at least **0.03 nats/token lower** in paired mean than **each** of S3, U3, L24 and R24; each comparison positive in >=9/10 seeds, with four one-sided exact paired sign tests Holm-corrected at familywise 0.05. Ties are non-wins; keep n=10 for the conservative sign test. With 9/10 wins, raw p=0.0107421875 and the largest first Holm multiplier is 4, yielding 0.04296875; no single-seed cherry-picking. Pass also requires k>=1 additions for >=9/10 seeds. If scores tie scheduled, **T FAILS**, even if A passes. Distinct-data and per-step trainable-budget differences remain disclosed; this is not a proof of unique causality in all streams.

**Detector gate D:** on the frozen-reference 64-block stationary-A diagnostic, block FPR mean <=5%, no seed >10%, and <=1 confirmed allocation-policy event per seed. This diagnostic tests the starting monitor, not adaptive-monitor validity. Also require the actual B3 pre-onset A segment to meet mean block FPR <=5%, no seed >10% and <=1 confirmed false expansion per seed; report its smaller denominator and binomial uncertainty. Recurrence/formatting diagnostics are reported separately; novelty need not justify capacity. No conditional/time-uniform guarantee follows for later adapted slots. Failure means the empirical detector gate fails even if adaptation helps.

**Operational efficiency gate C:** B3 standalone end-to-end online-adaptation CUDA-event time AND online-adaptation wall time <=1.25× R24, S3 and U3, using ratios of paired means; final system greedy-QA p95 end-to-end latency <=1.25× R24, actual total added weights <=4,718,592 plus explicitly reported shared key/projection buffers, peak memory <=22 GiB. This is a capped-overhead gate, **not equal FLOPs** and **not the master plan's 50%-compute thesis**. Failure permits a quality-only result, never “more efficient.” Shared warm-up and evaluator costs must still be published separately.

**Overall labels:** V failure → invalid/blocker, no final run. V valid but A/T/D fails → negative result for the relevant claim. A passes, T fails → useful LM adaptation without an established feedback-timing advantage. A/T/D pass, C fails → quality improvement at excess cost. A/T/D/C all pass → narrow task-free small-LM improvement on this stream; still no full thesis/competitive-general-LLM claim. Infrastructure or incomplete seeds → INCOMPLETE, not a statistical pass. Missing generation extension → language-prediction-only pilot, not the full E20 acceptance result.

Report arithmetic mean, sample SD and paired 95% seed-bootstrap CIs (10,000 resamples, analysis RNG 20201005) on H, differences and costs; significance decisions use the locked sign/Holm rule. Same final corpus across seeds means seed uncertainty is conditional on this corpus; document-cluster resampling is a separate sensitivity analysis, not extra independent seeds. Hyperparameter/method selection across repeated experiments consumes evidence: a failed E20 cannot be made confirmatory by renaming a rerun while reusing its opened final data.

## 8. Energy-specific generation ablation (E20-B; separate verdict)

The minimal affordable test is **answer-energy selection**, not a new language generator. Freeze each seed's final B3 model; every selector receives the exact same pool per QA question: one greedy answer plus three answers with temperature 0.7, top_p 0.95, max_new_tokens 32 and committed question/seed RNG. Deduplicate exact answers without replacing them; ties choose candidate creation order. Candidate IDs/probabilities must match across selectors. Report native one-answer greedy cost separately from four-candidate cost.

Use frozen unadapted-backbone features for prompt+context and answer, each projected to 64 dimensions as in §6. Scorer input is concatenated prompt vector, answer vector, elementwise absolute difference (192 features) plus candidate mean conditional LM log probability (one), yielding 193 inputs. `193→128→1` tanh scalar head has **24,961 parameters**. Scorer training uses only the 192 training QA items, correct aliases as positives, length-matched wrong answers from other training questions plus predeclared single-entity corruptions as negatives. A human verifies corruptions really are wrong; no final answers enter negative generation. Train 100 AdamW steps, batch 64 pairs, LR 1e-3, weight decay 0, norm clip 1; loss `softplus(1 + E_positive - E_negative) + 1e-3*(E_positive² + E_negative²)`. All negative draws and optimizer steps are committed; no new synthetic LM-training corpus is generated.

Compare five selectors:
1. **LM likelihood:** largest length-normalized candidate log probability; no scorer.
2. **Energy:** smallest trained E; energy temperature 1. Candidate-set normalized probability is `exp(-E)/sum_pool exp(-E)` only over the available candidates.
3. **Shuffled energy labels:** identical head/updates with fixed permuted positive associations, preserving length/domain distributions; tests useful learning versus extra computation/weights.
4. **Confidence control:** identical head/inputs/updates trained by binary BCE on correct/wrong labels; choose largest confidence. Head size, labels and candidate budget matched.
5. **Random selector:** committed uniform choice from the same pool.

**Critical interpretation:** a scalar energy over a finite candidate set is mathematically equivalent to a negative score; softmax of negative energies is a classifier. A gain over BCE can isolate a loss/negative-sampling choice, not “energy as a uniquely new model class.” Our objective is a stabilized pair-ranking proxy, **not Li et al.'s Eq. 5 reproduction**. There is no gradient descent on latent answers, Langevin reasoning, partition function over all text, or proof that energy correlates with correctness outside this pool. Never compute “EBM PPL” from candidate energies or average it with causal-LM PPL. This experiment tests an energy-specific component honestly while leaving master-plan M1 untested.

**E gate:** mean final macro grounded-QA EM advantage >=2 percentage points versus each LM-likelihood, shuffled-energy and confidence selector, with positive paired advantage in >=9/10 seeds and one-sided sign tests Holm-corrected across those three contrasts at 0.05. Mean A/G EM no worse than the LM selector by >1 point; energy p95 selector-inclusive latency <=1.25× the matched four-candidate LM selector. Report random and best-candidate oracle success as diagnostics. If the pool has little oracle headroom, still report the failure; do not increase candidates after opening final. Candidate scoring success cannot rescue failed growth timing. A genuine latent-refinement EBM proposal from Energy Model Engineer needs its own K=0/K>0, random-gradient, equal-compute and same-weight controls **before** an additional run, not a post-result substitution here.

## 9. Fair compute accounting and inference

Equal input tokens/steps are the primary exposure control, **not an equal-compute assertion**. R24 updates three times the rank of one active rank-8 slot; modular systems retain multiple slots and need routing passes. Explicitly publish both differences.

Per seed/arm measure separately: download/preparation/tokenization CPU wall time; shared old warm-up; model loading; prefix-feature extraction; detector scoring; GMM fitting/updates; adapter allocation/copy; online optimizer work; replay selection/reads; inference/routing; checkpoint serialization; held-out evaluator passes. Native method total must include its own required computations even when physical cross-arm caching amortizes them. Save both physical experiment totals and per-method attribution; never multiply or divide shared setup silently.

Use `perf_counter` with CUDA synchronization at boundaries for wall time, CUDA events around actual device phases for **device elapsed seconds**, and optional NVML utilization/power samples when already available. CUDA-event elapsed time is not exact busy-SM time; NVML utilization integral is an estimate. Report end-to-end wall, summed event intervals and GPU occupancy reservation time with these labels; do not pretend one is measured FLOPs. Profile representative development-only training/inference batches for operation/FLOP accounting where supported, mark unsupported operations and estimates, and freeze profiler conventions. Count backward, detector, router, eigen/GMM work and repeated candidate generation. No cost-per-capability ratio when improvement <=0.

Inference benchmark: same **64 development QA prompts** initially and final sealed QA prompts after unsealing; batch 1, three training-only warm-up prompts not included, identical context and max32 answer tokens. Profile the permitted 1,024-token prompt maximum as well as the 512-token training window before the memory lock. Report first-token latency, decode tokens/second, end-to-end p50/p95, router/scorer overhead, generated-token count, peak allocated/reserved memory, and model-load cold cost separately. Stop at EOS; do not length-pad useful throughput comparisons or hide shorter answers. Repeat timed inference three times with fixed outputs/seeds; randomize arm order via committed per-seed permutations. No parallel GPU models or competing agents' jobs; lack of exclusive access is a recorded blocker, not permission to change global GPU state.

A useful additional result is the capability/retention versus **measured cumulative online cost** curve using fixed saved checkpoints. Do not choose the most favorable checkpoint after final inspection. A future exact wall/FLOP-matched protocol may truncate or add updates using development throughput, but must be locked separately; this design does not claim that an end-of-run token match supplies that result.

## 10. Failure modes to publish, not patch away

- Known task/source/category ID reaches training, routing or decoding → invalid leakage; quarantine the record, preserve it and use a new untouched final split for a corrected experiment.
- Drift/onset externally supplied to B3 → task-aware method; not the nominated task-free test.
- Feedback NLL calculated after an update or with future suffixes → noncausal detector.
- Better old retention only because B3 never learned new domains → A fails; zero growth is not success.
- Good trained slots but poor automatic routing → system failure, with oracle gap diagnostic.
- Input-density or confidence/energy changes without acquired capability → detector/scoring observation, not growth evidence.
- Larger effective weights or extra generated candidates explain a gain → name that budget tradeoff; do not credit timing or inference energy.
- Missing late triggers or OOM on difficult seeds → include the seeds/failures; no replacement seed selection.
- Retry after an infrastructure-only failure is allowed with exactly the same locked configuration and seed, preserving both attempt logs; numerical failure is a result, not infrastructure.
- Factual QA improves because answers/aliases, final contexts or revisions leaked into scorer training → invalid; neither post-hoc dedup nor changing the acceptance gate restores confirmation.
- Old/core tensors unchanged → a useful engineering invariant, not a guarantee of unchanged system outputs/competence.

## 11. Seal and run authorization checklist

Before any confirmatory model outcome:

1. Owner approves §12 and final thresholds/arms; archive this design plus any explicit amendments. No outcome-driven edits to E15–E19 or this locked revision.
2. Custodian (a separate evaluator/human process, not the training agent) freezes original retrieval, rights records, group partition, final QA aliases and exact code/tokenizer versions. Publish hashes/counts only. Encrypt/ACL-isolate final text, metadata and salt so the training account cannot open them. A folder called `sealed` that the same training account can read is **not** a seal.
3. Publish public commitments for protocol, corpus manifest, runner/tests/config, analysis script, source/model/tokenizer files, training-pool IDs, deterministic random lists and checkpoint hashes. Model weight download and hash verification have **not** occurred in this design task; do not use the Hub repository SHA as a substitute for safetensors-byte verification.
4. Run development-only learnability, memory and runtime profiles, with capped budget, before freezing the implementation; no final score or final-generated example may be inspected. V failure stops the final run. Any substantive method change requires an amended design, a new lock and fresh final data if the old final was exposed.
5. Implementation acceptance tests: denylist test path/metadata reads; group/near-duplicate collisions zero; causality trace has decision_time < next-block update; all arms start function-identical; declared counts/masks match real tensors; cloning doesn't alter parent/core; F produces identical outputs at each checkpoint; never-trigger branch remains a scored non-growing system; scorer pools identical; randomized/permuted labels fail to magically preserve correct QA; parser rejects NaN/missing/duplicate seeds and zero test count. Test the failure paths, not only positive examples.
6. Train only on allowed stream/replay data. Custodian receives immutable all-arm checkpoints, allocation logs and hashes. Trainer cannot modify evaluator/gates or select a checkpoint by final results.
7. Custodian unseals **once**, executes fixed scoring/analysis across all arms/seeds/checkpoints including null/missing outcomes, and publishes results simultaneously. Final evaluator is read-only: no online updates, threshold recalibration, examples returned to trainer, or adaptive query loop. Record access logs. Integrity corrections after exposure require a new experiment and held-out test; retain the negative/invalid record.
8. Independent scientist reruns aggregation from token sums/counts, raw generations and timings without loading a trainable model. Publish raw per-seed results, protocol, source/config hashes and costs. Website publication uses the project's per-EXX checklist; this task did not edit the publication gate or site.

Suggested *future* immutable outputs: `results/E20/lock.json`, `attempts.jsonl`, per-seed/arm `stream.jsonl`, `token_sums.jsonl`, `generations.jsonl`, `timing.jsonl`, `weights.json`, `summary.json`, and an analysis report. These names are an artifact contract, **not existing runners, generated measurements or claims of completed execution**.

## 12. Owner decisions and measured/unmeasured costs

**Decision 1 — scope:** approve the affordable SmolLM2 prose/grounded-QA proxy as the next E20. This moves to genuine generation/perplexity but does not reproduce FiUni/HESTIA or establish a new paradigm. Alternatively fund a separate full-method FiUni/TRACE replication (permission/data-rights resolution needed; changed backbone is still a changed-condition replication). Do not quietly label the cheaper design a full reproduction.

**Decision 2 — resource cap:** proposed **24 exclusive GPU-hours = 86,400 reserved GPU-seconds**, including development profiles, calibration, all eight arms × ten seeds, energy scorer work and evaluation. This is a requested ceiling, **not a measured duration, throughput estimate, cash price or authorization to launch**. Dev-only model work is capped at one GPU-hour within that ceiling. Profile on development to decide whether the full battery fits; if not, ask the owner before dropping controls/seeds or beginning confirmation. Shared warm-up plus seven adapting arms represent **19,660,800 training input tokens**, excluding detector/calibration/held-out/candidate work; actual time depends on measured throughput. Frozen F adds evaluation, not training. No billed compute cost is known here.

**Decision 3 — annotation/rights:** approve preparation of 192 training, 64 development and 512 final human-verified grounded QA items plus corpus/license curation. Annotation hours are unmeasured. If this is declined, run only a explicitly named language-prediction pilot with no full E20-generation PASS and no energy/answer-quality verdict; do not fabricate QA or substitute LLM judging without approval.

**This task's costs:** 0 E20 training runs; 0 model weight downloads; 0 GPU outcome execution. CPU raw-record audit measured 0.2335849000 seconds. Source retrieval and design total time were not comprehensively instrumented, so no aggregate research-cost claim is made. Paper PDFs and metadata were retrieved; method code was not executed. No model-fit claim has been verified on the GPU.

**Review provenance:** a separate reviewer dispatch failed before reading the protocol with provider HTTP 429/quota exhaustion (completed transcript `deleg_c8184dc4/task-0.log`, 3.16 seconds). The parent performed the consistency/citation/arithmetic checks; do not label this document peer-reviewed. No provider configuration was changed. This design remains proposed pending owner approval and the implementation/custodian lock. The lead has separately assigned genuine latent-energy-versus-direct refinement to an **unrun E21** track (`NEW_AI/master-plan.md:161`); the small conditional-energy reranking annex here must not replace or be conflated with that mechanism test.

**Bottom line:** preserve E19's negative verdict, fix the benchmark class before chasing another headline, and demand timing gains over replay/capacity/random/scheduled controls with actual costs. Even a fully passing E20 would be a bounded continual-language result; energy descent, ternary efficiency and autonomous self-evolution remain separate unproven mechanisms.

## Sources

[11] https://openaccess.thecvf.com/content_CVPR_2019/papers/Aljundi_Task-Free_Continual_Learning_CVPR_2019_paper.pdf
[20] https://arxiv.org/html/2608.27070v1
[21] https://raw.githubusercontent.com/mlresearch/v337/main/assets/le26a/le26a.pdf
[24] https://arxiv.org/html/2502.02737v1
[26] https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
[27] https://www.mediawiki.org/wiki/API:Revisions
[29] https://huggingface.co/api/models/HuggingFaceTB/SmolLM2-1.7B
[30] https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B/raw/effd688a12921b4cc83e3312b6feb579f70f9c71/README.md
[31] https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B/raw/effd688a12921b4cc83e3312b6feb579f70f9c71/config.json
[32] https://arxiv.org/abs/2106.09685
[33] https://arxiv.org/pdf/2011.12216
[34] https://arxiv.org/pdf/2310.06762
[35] https://arxiv.org/abs/1810.09136
[37] https://huggingface.co/docs/transformers/perplexity
[38] https://raw.githubusercontent.com/Alisia0303/HESTIA/2d755f7a06c1da99231fc7f627a4d6457ed57e6d/LICENSE
[39] https://raw.githubusercontent.com/BeyonderXX/TRACE/462e39f616134f4f819efeb3baea8638c03c7db4/LICENSE
[40] https://api.github.com/repos/SSG2019/FiUni/git/trees/2fcc502c8af2fd3c14d92c023bc509b37f6ed503?recursive=1
