---
title: "New AI — original-source EBM code review and a bounded small-LM ablation"
tags: [new-ai, energy-based-models, source-review, language-models, experimental-design]
status: draft
created: 2026-10-05
---

# Original-source EBM reconnaissance

**Requested by:** Cloud AI Generalist, New AI thread `47ff4515b673e26334f26fba90af389fb3ff266d96e38ff961414709af5953f0`.
**Author:** Energy Model Engineer.
**Scope:** Static inspection of original papers and pinned upstream code. No upstream program was imported or executed, no model weights or datasets downloaded, no GPU experiment conducted, and no shared research code, evaluator, sealed test, master-plan gate or production website edited. This is a design handoff, not a new EXX outcome or evidence of a model win.

## 1. Conclusion and project constraints

**Best next mechanism to isolate:** train a small conditional scalar energy over a continuous prediction latent on top of a frozen pretrained causal LM, and compare its actual gradient-based update against an exactly parameter-matched direct recurrent update. EBT supplies the clearest language-specific recipe, but adapting its principle to pretrained hidden states is a **new approximation**, not a reproduction of its architecture or scaling claims.[8][21]

**mini-AGI is relevant continual-learning engineering, not an explicit energy-descent LM.** Its inspected prediction path uses recurrent transformer updates, token cross-entropy and a learned halting distribution. Its expert routing is linear scoring/softmax/top-k; growth is resource/use/survival-gated. None of those operations is an inference update of the form `z <- z - alpha * grad_z E` in the traced prediction path.[16][17][18]

**Three license-confirmed original EBM implementations were inspected:** EBT, IBC and JEM, all Apache-2.0 at the pinned revisions. A fourth, the original Du–Mordatch image EBM release, has visible source but **no license file in the complete pinned tracked tree**; it is informative to read but is not counted as a license-cleared reuse candidate.[20][27][34] The missing-license conclusion is backed by the saved `git ls-tree` audit, not by a GitHub label.

### Local scientific context read first

- `NEW_AI/master-plan.md:29–48,115–141`: M1 iterative reasoning and M2 growth/timing are different claims; lower energy can be gamed; toy success does not establish an LLM advantage. Existing acceptance gates remain unchanged.
- `REPOS/new-ai-e19/PROTOCOL_E19.md:3–21`: hashing-feature linear news classifier; five seeds; strict causal-timing advantage and retention gates.
- `REPOS/new-ai-e19/E19_REPORT.md:5–19`: feedback tied scheduled at 74.66% balanced accuracy, new accuracy 59.15%, and routing sent only 19–28% of new articles to the adapter. These are existing E19 measurements, not measurements from this review. E19 remains failed.
- `REPOS/new-ai-e18/PRIOR_ART_E18.md:9–15`: close task-free adaptation/routing literature must shape the independent E20 benchmark; this review does not implement FiUni or density-guided routing.

E19 checkout during this review: `0cdc379b2cd43d24780318becf9cae55af26c814`, branch `research/e19-text-gate`. Its pre-existing untracked `research-site/` was left untouched. A better energy refiner cannot retroactively repair E19's route or timing verdict.

## 2. Pinned source inventory

All repositories were fetched with shallow `git clone`, pinned with `git rev-parse HEAD`, and read locally. File ranges below refer to these commits, not moving `main`/`master` URLs. Source-object hashes and line counts are recorded in `RESEARCH/NEW_AI_EBM_SOURCE_MANIFEST_2026_10_05.json`.

| Project | Exact inspected commit | Rights observed | Prediction/training substrate |
|---|---|---|---|
| `volotat/mini-AGI` | `8fa5c23107645729fad3beac5f295eefa0fb0fff` | MIT, `LICENSE:1–21`.[15] | Byte-level recurrent transformer, paged experts, ordinary optimizer updates.[16][17][18] |
| `alexiglad/ebt` | `19420cbeae655bbf11930219a675ade6897019e8` | Apache-2.0, `LICENSE:1–5`.[20] | PyTorch/Lightning; conditional energy and continuous vocabulary-logit optimization.[21] |
| `google-research/ibc` | `db89ddbb852603fe9b64cf0f502b1fd3d6037d33` | Apache-2.0, `LICENSE:2–6` and source headers.[27] | TensorFlow/TF-Agents; conditional action energy; Langevin or derivative-free optimization.[30][32][33] |
| `wgrathwohl/JEM` | `3d01161547109b464eee87304f07b2dac8519d03` | Apache-2.0, `LICENSE:1–5` and training source header.[34][35] | PyTorch; classifier logits reused as an unnormalized joint/marginal density.[35] |
| `openai/ebm_code_release` | `051850ee63cb4a9804bc89303f9110b119c0f6c1` | No license/copying path in pinned tracked tree; reuse permission unresolved | TensorFlow 1.12-era image/trajectory EBM; short-run Langevin negatives.[37][38] |

These licenses describe source code. They do **not** automatically clear training datasets, externally hosted checkpoints, dependent libraries, or commercial use of third-party data. No checkpoint redistribution permission was assessed here.

## 3. What qualifies as energy descent in this handoff

Keep three distinct concepts:

1. **Similarity/density/confidence statistic:** cosine distance, negative classifier log-sum-exp, entropy, or a learned confidence output. It can rank, route or alarm, but that alone does not show energy-based inference or energy-specific training.
2. **Explicit energy model with implicit prediction:** a learned scalar `E_theta(context, z)` and an implemented optimizer/sampler over `z` using that scalar. In the gradient variant, the actual inference path must differentiate the energy with respect to the candidate, not merely update model parameters.[8][6]
3. **Training the landscape:** either contrastive/density training with real versus model/counter-example samples, or an optimization-based loss backpropagated through the energy-derived prediction updates. EBT is an example of the latter; IBC and JEM expose the former.[21][31][35]

Gradient descent is not required for every EBM: IBC's derivative-free sampler is a genuine energy-based implicit model. However, it is **not** the explicit latent-gradient mechanism M1 asks us to test. Conversely, recurrence, adaptive halting or sparse expert selection does not by itself imply a learned scalar potential.[6][32][16]

**Critical calibration limitation:** if inference uses only `grad_z E(context,z)`, adding an arbitrary context-only offset `c(context)` does not change its prediction update. A token-CE loss through that update does not uniquely calibrate absolute energy. Therefore, an optimization-trained energy cannot automatically be used as a universal novelty/growth threshold. JEM similarly explains the scalar-logit-shift freedom of a classification-only model; its additional density objective uses that degree of freedom rather than leaving it unidentified.[11][21] Any future trigger needs separate validation and label-only/covariate-shift controls; no universal detector claim follows from the mechanisms reviewed.

## 4. mini-AGI: what the inspected code actually does

### Objective and inference

- [`minagi/recur.py:248–304`](https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/minagi/recur.py#L248-L304) initializes a recurrent state, combines it with input embeddings through an adapter, applies recurrent blocks, and produces logits through a readout. This is `h_next = recurrent(adapter(h, x))`, not differentiation of a scalar energy.[16]
- `minagi/recur.py:305–370` computes sigmoid halting probabilities, token CE at each depth, expected CE weighted by stopping mass, and a KL term toward a geometric halting prior. The code calls this PonderNet. The halting output is a stopping policy, not an energy gradient.[16]
- `minagi/recur.py:372–404` generates characters by repeated model calls and `pick_next`, with cache/context handling and optional repetition controls. It does not optimize a candidate character by `autograd.grad(E, candidate)`.[16]
- [`minagi/pool.py:362–442`](https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/minagi/pool.py#L362-L442) computes learned linear router scores, admissions and softmax/top-k expert weights. A load-balancing auxiliary term acts on router probabilities.[17]

### Learning, growth, preservation

- [`train.py:1095–1126`](https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/train.py#L1095-L1126) adjusts optimizer rates via a plasticity controller, calls the reading loss, then `loss.backward()`, gradient clipping and `opt.step()`. `config.yaml:123–130` sets trunk LR to 0.1 times the experts' rate: **slow learning is not a frozen trunk**.[18][19]
- `minagi/pool.py:620–668,730–774` schedules speculative expansion and checks room, staleness/use, survival and in-flight cohorts. `val_loss` is logged in `AutoGrow.step`; the actual expansion condition is `room and used and kept`, not persistent high learned energy. `train.py:1252–1303` supplies the train/held-out gap brake and resynchronizes optimizers/checkpoints after growth/pruning.[17][18]
- The author explicitly describes the model as toy-level (`README.md:3–8`), says final weights are not yet published (`:15`), and reports remaining forgetting in the massed new-domain arm (`:258–312`). The same README says the reported continual-learning arms predate a routing-rule change (`:269`). These are **author-reported results**, not our replicated measurements.[14]

### Transfer recommendation

Borrow engineering questions, not capability claims: expert-state ownership across paging; preserving optimizer moments when experts move; separate reporting of trunk and expert updates; LR-ratio versus replay/interleaving controls; explicit checkpointing after topology change. A future adaptation of these components must be a separate experiment because it changes capacity, routing and I/O costs at once. Do not use its live-learning loop to modify an evaluator or final test. MIT permits code reuse with the notice retained, but corpus/checkpoint rights need their own review.[15]

## 5. EBT: closest original language-specific explicit-descent recipe

**Original paper:** Gladstone et al., *Energy-Based Transformers are Scalable Learners and Thinkers*, arXiv:2507.02092v1 (2025); inspected §§3.2–3.4, 4.1 and Appendix D.5.[8]

### Objective, signal and update

Let `u` be a continuous candidate next-token logit vector and `x` the observed prefix. The code learns scalar energies conditioned on context and candidate embeddings, then updates the candidate:

`u_(k+1) = u_k - alpha * grad_u E_theta(x, u_k)`

Token CE/NLL after these updates provides the training signal. With `create_graph=True`, the CE gradient trains the energy parameters through the derivative used in the inner update. This is a real trained energy mechanism; it is **not** just a scalar head fit to label an existing prediction as confident.[21]

### Exact call path

- [`model/nlp/ebt.py:25–51`](https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/model/nlp/ebt.py#L25-L51): tokenizer, embeddings, candidate vocabulary-to-embedding projection and `setup_ebt`.[21]
- `model/model_utils.py:423–441` selects default, time-embedding or AdaLN EBT. The inspected example uses `time_embed`; `model/ar_ebt_time_embed.py:701–757` adds optimization-step conditioning and returns a scalar per candidate position through `Linear(dim, 1)`.[22][23]
- `model/nlp/ebt.py:88–153`: candidate corruption/replay, gradient enabling, optional inter-step detach, embedding concatenation, energy evaluation and `torch.autograd.grad`. `:164–186` applies the energy-derived update and returns distributions.[21]
- `:190–246`: next-token target shift, NLL/CE, per-step versus final-step loss, optional contrastive branch. The minimal example sets `contrastive_loss=False`, `no_mcmc_detach=False`, `truncate_mcmc=False` and two inner steps (`example_code/minimal_nlp_training_loop.py:83–118`). **Do not describe all EBT training as contrastive divergence or as full unrolling:** these switches materially change gradient flow.[21][24]
- `inference/nlp/generate_text.py:37–50,108–124`: generation calls the EBT forward with `learning=False`, takes final candidate logits and samples/argmaxes a token. Despite the outer `no_grad`, EBT forward re-enables gradients for the candidate; inference still needs first-order input derivatives. This is different from training-time higher-order derivatives.[26][21]

### Practical limitations and 24 GB transfer

The paper explicitly says its architectures were pretrained **from scratch** and are incompatible with simply fine-tuning existing foundation models (§4). It evaluates small language models primarily with perplexity because many task accuracies are low. A frozen-pretrained-backbone energy head therefore tests a derivative mechanism, not the published EBT scaling result.[8]

Appendix D.5 estimates greater per-token training cost from input gradients and Hessian-vector products; its 6.66x two-step S1 cost is an **author approximation**, not measured cost on this laptop. `CODE_INFO.md:33–34` warns about averaging batch perplexities and says inference lacks a working KV cache; the actual generator reprocesses `tokens[:, :cur_pos]` and forces `start_pos=0`. Do not copy that path and claim equal forward counts mean equal compute.[8][25][26]

Useful pieces: a scalar potential, differentiable continuous predictions, CE through the update, bounded steps, gradient checks, and independent task evaluation. Defer full-model second-order pretraining, randomized landscapes, replay and best-of-N until the plain bounded mechanism has a validated instrument. The minimal example itself warns it is not an exact reproduction (`:19`). Apache-2.0 reuse must retain notices and identify modified files.[24][20]

## 6. IBC: conditional contrastive energy, with an important sign convention

**Original paper:** Florence et al., *Implicit Behavioral Cloning*, CoRL 2021 / PMLR 164 (2022), §2: conditional action prediction by minimizing energy, InfoNCE counter-examples, derivative-free and Langevin variants.[6]

### Objective and code trace

Paper convention: `p(a|o) proportional to exp(-E(o,a))`. The inspected implementation outputs a **high-is-good score** `S=-E`: its InfoNCE uses `softmax(predictions / temperature)` and its action-gradient helper explicitly flips the sign. Copying the paper's minus sign and the code's minus sign without reconciling them would invert the update.[31][32]

- `ibc/train/get_cloning_network.py:75–78` passes a scalar output spec `TensorSpec([1])` to MLPEBM. This matters: the `action_spec` argument inside that network describes its **output**, not the original action vector dimension.[28]
- [`networks/mlp_ebm.py:72–96`](https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/networks/mlp_ebm.py#L72-L96) concatenates observation and candidate action, applies the MLP, projects to a scalar and squeezes the scalar axis.[29]
- `ibc/agents/ibc_agent.py:163–225,302–338`: generates negative actions, stop-gradients candidate actions for the normal scoring loss, and selects InfoNCE/CD variants. `ibc/losses/ebm_loss.py:21–48` assigns the true example to the last candidate column and trains its softmax score against counter-examples. `ibc_agent.py:227–237` optionally adds an action-gradient penalty.[30][31]
- [`ibc/agents/mcmc.py:164–191,227–262`](https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/agents/mcmc.py#L164-L262): differentiates score with respect to actions, flips to the energy convention, clips gradient/update, adds noise, subtracts the update and bounds actions. `:332–408` performs the chain with configurable step schedule and optional `stop_gradient` between steps.[32]
- `ibc/agents/ibc_policy.py:240–328`: samples candidate actions, optionally runs derivative-free or Langevin refinement, evaluates candidate probabilities and returns a distribution over the optimized candidates. `mcmc.py:59–150` is a separate derivative-free resample/perturb path, not gradient descent.[33][32]

### Transfer and limits

Adapt the conditional counter-example objective, sign tests, bounded candidate domain, and late fusion: encode the context once and score many candidates cheaply. IBC's late-fusion loss/sampler paths explicitly support cached observation encodings.[30][32]

It is a continuous robotic-action method, **not** a language model. Tokens require a continuous relaxation, a latent decoder or discrete search; uniform action negatives cannot be assumed appropriate for text. A finite-negative InfoNCE loss is not an exact text partition-function estimator. A port to PyTorch/pretrained embeddings would be a method-inspired adaptation; no robot or LM results were reproduced. The README pins TensorFlow 2.6/TF-Agents-era dependencies; do not install those into the shared current training environment just to borrow the objective.[6][5]

## 7. JEM: why an energy-looking classifier score is insufficient

**Original paper:** Grathwohl et al., *Your Classifier Is Secretly an Energy Based Model and You Should Treat It Like One*, ICLR 2020, §§3–4.[11][12]

For class logits `f_y(x)`, JEM defines joint energy `E(x,y)=-f_y(x)` and marginal energy `E(x)=-logsumexp_y f_y(x)`. Crucially, the original method also trains a density objective with model-generated samples; it is not merely relabeling a supervised confidence score.[11][35]

### Exact implementation

- [`train_wrn_ebm.py:52–77`](https://github.com/wgrathwohl/JEM/blob/3d01161547109b464eee87304f07b2dac8519d03/train_wrn_ebm.py#L52-L77): `CCF.forward` returns `logsumexp(logits)` or the selected class logit. Thus code returns score `S=-E`, not low-is-good energy.[35]
- `:202–237`: replay/random initialization and the actual sampling update `x_k += sgld_lr * grad_x S(x_k) + noise`. Gradient **ascent** on that score is descent on `E`. The final sample is detached and put back in the replay buffer.[35]
- `:313–341`: density loss `-(mean S(real)-mean S(sampled))` plus ordinary class CE. The class-only case does not establish a trained input-density landscape. `:343–352` contains a separate conditional joint-density objective.[35]
- `:381–393` evaluates the original test set each epoch. This is an upstream practice to **not** copy into our sealed-final-test workflow; checkpoint/tuning must use development only.[35]

### Transfer and limits

JEM is a strong conceptual baseline for testing whether a trained density statistic adds anything beyond CE/entropy/logit magnitude. Its classic sampler optimizes **images**, while class prediction is still a feed-forward classifier; therefore it does not show iterative token reasoning or growth. On a frozen LM, sampling hidden features instead of text would learn a density in that representation, not automatically a normalized text model or a correct trigger for semantic shifts.[11][35]

Reuse its score-sign discipline and CE-only versus CE+density ablation. Do not map an existing classifier's log-sum-exp to E19-style growth and call it JEM without the density training and generated-negative path. Source reuse is Apache-2.0; original image results remain author-reported.[34]

## 8. Du–Mordatch original release: useful negative-phase example, license unresolved

**Original paper:** Du and Mordatch, *Implicit Generation and Modeling with Energy-Based Models*, arXiv:1903.08689v3 (2019), §§3.1–3.3 / Algorithm 1.[9]

The paper defines `p_theta(x) proportional to exp(-E_theta(x))`, uses Langevin-generated negatives, and approximates the likelihood gradient with data-energy minus model-sample-energy gradients. It describes a sample replay buffer, spectral normalization and squared-energy regularization.[9]

The original release exposes the actual low-is-good scalar via `models.py` (e.g. scalar energy/readout at `:180–185`). `train.py:734–796` adds noise, differentiates energy with respect to candidate input, subtracts the step, clips the input and stop-gradients the final negative for its scoring path. `:837–855` builds CD `mean(E_real)-mean(E_negative)`, adds squared-energy regularization and differentiates the parameter loss.[41][37]

`README.md:54–73` uses `--zero_kl` in its training commands; omitting that flag activates the additional `loss_energy` branch at `train.py:847–848`. Thus the shipped code has branches beyond the paper's simplest detached-negative CD recipe. Explicit configuration is necessary before claiming a reproduction.[36][37]

**Reuse blocker:** the full tracked tree contains no LICENSE/COPYING file. Its old dependencies include TensorFlow 1.12, torch 0.3.1 and Horovod 0.16 (`requirements.txt:1–6`). Read the algorithm/paper, but do not vendor its source until permission is clarified. A from-scratch mathematical implementation is still a new adaptation, not a reproduced image experiment. No old dataset URL or pretrained-checkpoint link was exercised here.[38]

## 9. Comparison for a pretrained small-LM experiment

| Method | Energy-specific training | Actual optimized variable | What can be adapted | What must not be claimed |
|---|---|---|---|---|
| mini-AGI | No explicit energy-training/descent path in the inspected LM loop | Recurrent hidden state via direct transformer mapping; weights via CE optimizer | Paging state discipline; slow-trunk/replay controls; recurrent non-energy comparator | EBM, frozen-core continual learning, or our replication of its reported retention.[16][18] |
| EBT | CE through derivative-based candidate updates; optional contrastive branch | Continuous vocabulary logits | Scalar potential plus higher-order training confined to a small head | Pretrained conversion reproduces EBT; fewer NFEs implies fewer GPU-seconds.[21][8] |
| IBC | Conditional InfoNCE/CD against negative actions; optional gradient penalty | Continuous action candidates; Langevin or DFO | Conditional negative sampling, bounds, sign checks, late fusion | Robot success predicts language performance; DFO is explicit gradient descent.[30][32] |
| JEM | CE plus marginal/joint density objective and sampled negatives | Image input during SGLD; class logits for normal prediction | Density-vs-confidence baseline and gauge/sign checks | Classifier free energy alone is trained generative reasoning or an all-shift detector.[35][11] |
| Du–Mordatch release | Data versus model-negative energy with regularization | Image/trajectory candidate | Algorithmic negative-phase/replay comparison after a rights-safe implementation | Code is license-cleared or short chains are exact equilibrium samples.[9][37] |

## 10. One testable ablation proposal: energy-derived versus direct latent refinement

**Proposal only — not an E20 protocol, approval, run, outcome or amendment of existing gates.** Integrate it with Evaluation Scientist's independently specified language stream, then have the lead commit the agreed protocol before any outcomes. This isolates **M1-like latent inference**, not growth-trigger timing, paging, ternary precision, self-play or self-evolution.

### 10.1 Backbone and tractable parameter space

Candidate: `HuggingFaceTB/SmolLM2-360M`, revision `f8027fd0eaeea54caa13c31d31b9fdc459c38b49`; model card declares Apache-2.0. Pin tokenizer artifacts separately to this revision and hash all downloaded files before a later run. The retrieved config specifies hidden width 960, vocabulary 49,152 and tied embeddings.[39][40]

Hub metadata reports 361,821,120 BF16 parameters. The arithmetic-only BF16 weight payload is **723,642,240 bytes (~690.12 MiB)**, computed from that count, **not measured VRAM**. No weights were loaded. This makes a frozen-base/small-head prototype plausible within the stated 24 GB constraint, but activations, optimizer state, output logits and nested autograd peak memory require a bounded future smoke test before feasibility can be asserted.

Use frozen prefix hidden state `h` and a 64-dimensional candidate residual `z`, initialized to zero. Decode full-vocabulary logits with the frozen LM readout from `h + P z`, where `P` is a fixed seeded orthonormal lift shared by every arm. Keep all pretrained weights, normalization and tokenizer unchanged. Only generated tokens enter subsequent LM contexts; refined residuals do not overwrite the base KV cache. This is a **readout-latent adaptation**, not converting the entire LM into an EBT.

### 10.2 Exact trainable-capacity matching

Give both mechanisms the same smooth head architecture:

`g_theta([h,z]) = (s_theta(h,z), v_theta(h,z))`

with input 1,024, hidden 256 (SiLU), output 65, and biases on both linear layers. Both outputs participate in each mechanism, not dummy padding weights. Analytically this head has **279,105 trainable parameters** in each arm; the fixed lift and frozen backbone are identical. A future runner must independently count functional/trainable/total parameters and assert equality.

**Energy arm:** define an explicit scalar

`E_theta(h,z) = s_theta(h,z) * (1 + dot(q,z) + 0.5 * ||z||^2) + dot(z, v_theta(h,z)) + (lambda/2) * ||z||^2`.

Here `q` is a fixed seeded unit vector shared by the arms. Its linear coupling makes the scalar-output bias affect the candidate update; without that coupling an additive energy-head bias would be functionally unused. It also keeps the direct arm's scalar gate active at `z=0`, including the one-step comparator.

Perform bounded updates `z_next = project(z - alpha * grad_z E_theta(h,z))`. Train the head with full-vocabulary next-token CE **through the updates**, requiring `create_graph=True` during training; retain only first-order candidate derivatives during evaluation. The fixed quadratic term and projection bound are regularizers, not substitutes for learning the potential.

**Direct-update non-energy arm:** use the same-sized separately trained head to produce

`U_phi(h,z) = v_phi(h,z) + s_phi(h,z) * (z + q) + lambda * z`,

then `z_next = project(z - alpha * U_phi(h,z))`, trained with the identical final next-token CE. There is no explicit scalar being optimized or candidate-energy differentiation in this arm; the general learned vector field need not be conservative. Its scalar output is an update gate, not an energy. This is a recurrent residual comparator with the same functional weight count, rather than giving the energy arm extra trainable capacity.

The scalar parameterization and direct vector rule are **our proposed constructions**, not code copied from EBT/IBC/JEM. State that explicitly in the protocol. Both use the same fixed `lambda * z` restoring drift, projection and decoder; capacity is tightly controlled, but differing inductive biases remain part of what is being tested.

### 10.3 Required comparisons

- Frozen LM / `K=0`, also the exact bypass evaluation of each trained head: must reproduce base logits. This does **not** promise an untrained head preserves the function when `K>0`.
- Energy head trained at a development-locked inner depth, proposed `K_train=4`, evaluated at `K=1,4,8`; all settings reported, no test-selected winner.
- Direct-update head with the same training depth and `K=1,4,8` evaluations. Add a separately trained one-step head of identical capacity as the feed-forward adaptation baseline.
- Zero-gradient/bypass and frozen-random-energy diagnostic: lower energy or more capacity without a learned useful update must not count as a win. Random-energy results are diagnostics, not the equal-training comparator.
- The lead's fixed LoRA/replay and no-adaptation arms remain stronger practical references. This energy sub-ablation must not displace the independent E20 routing, feedback/random/scheduled or replay comparisons.

Use five **fresh paired** seed IDs selected and committed by the evaluator, identical data/split/order and initial fixed projection per pair. Test logits/target isolation, finite-difference energy-gradient sign, nonzero energy-head training gradients, finite updates, baseline bypass identity, full parameter counts and no final-test access. Deterministic updates can fail to decrease energy at an oversized step; record that failure rather than silently adding test-tuned line search.

### 10.4 Task, compute and falsification

**Execution prerequisites:** the independent evaluator must first freeze the actual licensed natural-language stream, document-disjoint train/development/final manifests and a prompt-to-answer generation task with a fixed answer parser. Do not reuse already inspected E19 tests. Prefer newly authored or temporal-held-out language material; investigate near duplicates, source licenses and possible pretrained contamination. These data choices are unresolved in this reconnaissance, so this is not a run-ready preregistration.

Primary independent measures: corpus-token-weighted next-token NLL (perplexity computed once from aggregate NLL), free-running answer exact match or the evaluator's locked task-quality metric, old-domain retention, and generation failure/repetition rates. Energy, gradient norms and `E(z0)-E(zK)` are mechanism diagnostics only. Include per-seed paired deltas and all raw per-example outputs; do not reward the model for merely agreeing with its own energy.[25]

For the causal mechanism comparison, preregister an **equal-token/data exposure diagnostic** and an **equal measured-compute primary comparison** rather than pretending both are guaranteed by equal optimizer steps. Measure base encoding, head training, validation/tuning, detector/routing if present, candidate input-gradients and full autoregressive generation. Give the direct arm the same total training GPU-time allowance and permit more repeated training passes over the same allowed pool; disclose resulting exposure differences. Select inference depths/budget points on development only, then freeze them. Equal K is a diagnostic, not compute matching.

Record synchronized wall time, CUDA-event elapsed time with the event interval declared, GPU occupancy/utilization if available, peak allocated/reserved memory, token counts, head/total weights, throughput and p50/p95 generation latency. CUDA-event elapsed time is not automatically GPU busy-time or FLOPs. Any incomplete matching is a limitation that prevents a compute-advantage claim, not permission to substitute analytical estimates.

**Suggested decision rule for evaluator/owner approval, not an adopted gate:** the energy arm should improve held-out NLL by at least 0.02 nats/token over both the matched recurrent and one-step controls, with positive paired advantage in at least 4/5 seeds; improve the independent generation metric by at least 2 percentage points; and remain within a 2-point old-task retention loss at the agreed measured compute budget. The evaluator must assess baseline feasibility, sample size and uncertainty before adopting any numeric rule. Existing project gates remain sealed.

**Falsifiers:** energy falls but task quality does not; energy only beats frozen, not the matched direct update; the direct update catches up when granted equal measured compute; longer refinement damages generation or retention; or gains require additional weights/task-oracle routing. Each is a publishable narrow negative, not a reason to rewrite the gate. If NLL alone improves, report a readout language-loss result, not improved reasoning. Even a positive result would establish only this small-LM latent mechanism on this task—not EBT replication, autonomous growth, a competitive LLM, or the full self-evolving thesis.

## 11. Handoff and unresolved items

1. **Lead decision:** choose this energy-vs-direct update sub-ablation or defer it. Evaluation Scientist owns independent data, sealed tests, task metric and acceptance design. Majied must approve any compute-budget enlargement or project-gate change; this review authorizes neither.
2. **Rights:** three original codebases have inspected Apache-2.0 source licenses; mini-AGI is MIT. The Du–Mordatch release needs reuse permission. Model-card licensing does not settle all pretraining-data rights.
3. **Replication status:** no paper's measured result was replicated; no installed dependency compatibility, model-load peak memory, throughput or training stability was tested. No inaccessible code/paper blocked the three licensed reviews. Linked weights and datasets were intentionally not fetched.
4. **Reproducibility record:** full commits, canonical Git-blob SHA-256, file line counts and license-tree discovery in `RESEARCH/NEW_AI_EBM_SOURCE_MANIFEST_2026_10_05.json`. Inspection checkouts remain in `.scratch/ebm-review-2026-10-05/`; these are disposable convenience copies, not a durable experiment worktree.
5. **Next executable work requires a new bounded assignment:** its own research worktree; protocol commit before outcomes; tests and multiple paired seeds; immutable prior negatives; raw measurements and source handoff; website publication only by the authorized lead workflow.

## Sources

[1] https://github.com/alexiglad/ebt
[5] https://github.com/google-research/ibc
[6] https://proceedings.mlr.press/v164/florence22a/florence22a.pdf
[8] https://arxiv.org/html/2507.02092v1
[9] https://arxiv.org/html/1903.08689v3
[11] https://arxiv.org/html/1912.03263v2
[12] https://arxiv.org/pdf/1912.03263
[14] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/README.md — volotat/mini-AGI README.md @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[15] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/LICENSE — volotat/mini-AGI LICENSE @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[16] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/minagi/recur.py — volotat/mini-AGI minagi/recur.py @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[17] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/minagi/pool.py — volotat/mini-AGI minagi/pool.py @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[18] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/train.py — volotat/mini-AGI train.py @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[19] https://github.com/volotat/mini-AGI/blob/8fa5c23107645729fad3beac5f295eefa0fb0fff/config.yaml — volotat/mini-AGI config.yaml @ 8fa5c23107645729fad3beac5f295eefa0fb0fff
[20] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/LICENSE — alexiglad/ebt LICENSE @ 19420cbeae655bbf11930219a675ade6897019e8
[21] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/model/nlp/ebt.py — alexiglad/ebt model/nlp/ebt.py @ 19420cbeae655bbf11930219a675ade6897019e8
[22] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/model/model_utils.py — alexiglad/ebt model/model_utils.py @ 19420cbeae655bbf11930219a675ade6897019e8
[23] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/model/ar_ebt_time_embed.py — alexiglad/ebt model/ar_ebt_time_embed.py @ 19420cbeae655bbf11930219a675ade6897019e8
[24] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/example_code/minimal_nlp_training_loop.py — alexiglad/ebt example_code/minimal_nlp_training_loop.py @ 19420cbeae655bbf11930219a675ade6897019e8
[25] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/CODE_INFO.md — alexiglad/ebt CODE_INFO.md @ 19420cbeae655bbf11930219a675ade6897019e8
[26] https://github.com/alexiglad/ebt/blob/19420cbeae655bbf11930219a675ade6897019e8/inference/nlp/generate_text.py — alexiglad/ebt inference/nlp/generate_text.py @ 19420cbeae655bbf11930219a675ade6897019e8
[27] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/LICENSE — google-research/ibc LICENSE @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[28] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/train/get_cloning_network.py — google-research/ibc ibc/train/get_cloning_network.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[29] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/networks/mlp_ebm.py — google-research/ibc networks/mlp_ebm.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[30] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/agents/ibc_agent.py — google-research/ibc ibc/agents/ibc_agent.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[31] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/losses/ebm_loss.py — google-research/ibc ibc/losses/ebm_loss.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[32] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/agents/mcmc.py — google-research/ibc ibc/agents/mcmc.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[33] https://github.com/google-research/ibc/blob/db89ddbb852603fe9b64cf0f502b1fd3d6037d33/ibc/agents/ibc_policy.py — google-research/ibc ibc/agents/ibc_policy.py @ db89ddbb852603fe9b64cf0f502b1fd3d6037d33
[34] https://github.com/wgrathwohl/JEM/blob/3d01161547109b464eee87304f07b2dac8519d03/LICENSE — wgrathwohl/JEM LICENSE @ 3d01161547109b464eee87304f07b2dac8519d03
[35] https://github.com/wgrathwohl/JEM/blob/3d01161547109b464eee87304f07b2dac8519d03/train_wrn_ebm.py — wgrathwohl/JEM train_wrn_ebm.py @ 3d01161547109b464eee87304f07b2dac8519d03
[36] https://github.com/openai/ebm_code_release/blob/051850ee63cb4a9804bc89303f9110b119c0f6c1/README.md — openai/ebm_code_release README.md @ 051850ee63cb4a9804bc89303f9110b119c0f6c1
[37] https://github.com/openai/ebm_code_release/blob/051850ee63cb4a9804bc89303f9110b119c0f6c1/train.py — openai/ebm_code_release train.py @ 051850ee63cb4a9804bc89303f9110b119c0f6c1
[38] https://github.com/openai/ebm_code_release/blob/051850ee63cb4a9804bc89303f9110b119c0f6c1/requirements.txt — openai/ebm_code_release requirements.txt @ 051850ee63cb4a9804bc89303f9110b119c0f6c1
[39] https://huggingface.co/HuggingFaceTB/SmolLM2-360M/blob/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/README.md — HuggingFaceTB/SmolLM2-360M pinned model card
[40] https://huggingface.co/HuggingFaceTB/SmolLM2-360M/blob/f8027fd0eaeea54caa13c31d31b9fdc459c38b49/config.json
[41] https://github.com/openai/ebm_code_release/blob/051850ee63cb4a9804bc89303f9110b119c0f6c1/models.py
