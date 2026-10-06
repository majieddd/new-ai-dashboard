---
title: "Harness Engineering (arXiv 2609.00006): application review for kr8 and its agent stack"
tags: [new-ai, kr8, harness-engineering, research-only, agent-stack]
status: draft
created: 2026-10-06
assignment_date: 2026-10-05
revision: "R1 — research handoff, pending Orchestrator QA"
author: "Researcher"
---

# Decision in brief

**Use this paper to improve the system around kr8’s agents, not as evidence that our proposed model can grow its own intelligence.** My recommendation is to retain the existing runtime and collaboration surfaces, make their boundaries observable, and test a read-only evidence/context handoff before considering autonomous modification. The applications below are engineering hypotheses, not measured kr8 improvements. No pilot, app change, agent change, installation, model execution, GPU run, wiki admission, or shared-memory change was performed.

The useful distinction is between a model, its execution runtime, the collaboration host, and the evaluator. The paper explicitly separates agent harnesses from evaluation harnesses and orchestrators (§2.2, pp.3–4); Figure 1 places the interface beside the runtime’s subsystems (§2.3, p.4).[1] For kr8, I propose assigning collaboration, identity, review, and durable evidence to the host while leaving model interaction, tool execution, and context processing with the selected runtime. This is a responsibility split to evaluate, not an established product blueprint.

## 1. Exact source and reading coverage

**Title:** *Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents — A Source-Code Study of Eleven Systems*. **Authors:** Paul Barbaste, Tristan Darrigol, Germain Vu, Tom Wiltberger. The retained arXiv record lists **v1, July 15, 2026, 10:33:30 UTC**; the PDF also prints July 2026.[1][2] This is anomalous relative to the identifier’s `2609` prefix. I report the record literally rather than silently assigning September 1 or claiming independent resolution of that metadata discrepancy.

The exact PDF was retrieved October 5, 2026, at 21:27:03 UTC: `PAPER_V1.pdf`, 963,456 bytes, SHA-256 **`e81b5a4855adda8cc5e46db0a05cd69e0d0d542bd49cec6b157c17e6001395d7`**. Metadata and retrieval timestamps are retained in `RETRIEVAL.json`. All **83 PDF pages** were read: main text through p.74; **Appendix A, Detailed Comparison Tables**, Tables 16–18 on pp.75–77; references pp.78–83. Appendix A contains prompt rhetoric, advanced API features, and the Claude Code/Codex pipeline comparison—not a hidden performance experiment.[1] Figures 1 and 6 were also inspected as rendered pages. Page numbers below refer to this exact copy, not a future revision.

Sources are in `RESEARCH/NEW_AI_ARXIV_2609_00006_SOURCES_2026_10_05/`: PDF, page-indexed text, owner discussion, CLI receipts, official runtime documentation, source inventory, and citation ledger. The report’s full-file hash is supplied in the handoff receipt; embedding its own hash would change it.

## 2. What the paper actually establishes

### Mechanism and architecture

This is a **comparative source-code study**, not a new neural architecture or a benchmark-winning agent. Its analysis dimensions are agent loop; model integration; tools/actions; memory/context; safety/permissions; orchestration; extensibility (§2.3, Table 1; §4.2).[1] It examines eleven runtime systems plus Omnigent as an orchestration contrast, pins July-era snapshots in Table 3, and compares retained April snapshots for longitudinal observations (§§4.1–4.2, pp.9–11; §14.5, p.62).[1]

Its actionable mechanism is ordinary runtime engineering: scoped tool exposure, explicit execution policies, bounded resource use, incremental context management, isolated task contexts, and inspectable extension packages. Sections 8–12 explain implementations; §16 turns those observations into eighteen recommendations. Listing 3 is an approximately ninety-line illustration, explicitly **not production code**, omitting sandboxing, orchestration, and extensions (§16.10, pp.71–72).[1] It is not a safe drop-in replacement for kr8’s runtime.

### Experiments, comparisons, and counter-evidence

The paper did **not** execute all eleven systems on matched tasks, establish a fastest runtime, measure kr8, or validate a general self-improvement loop. Section 15.6 admits source reading rather than runtime measurement, qualitative judgment, incomplete dependency-path coverage, and an unofficial March Claude Code snapshot as its weakest reproducibility point (pp.66–67).[1] Table 4’s footnote withdraws cross-system benchmark rankings because underlying models/configurations differ (p.11).[1] Therefore neither large codebases nor minimal loops can be ranked causally from this study.

A material citation error matters for our project: §15.5 (p.66) attributes **71.9% on SWE-bench Verified to AHE**.[1]
The directly referenced AHE **original v1** instead places **71.9% in the Codex Terminal-Bench 2 baseline**; AHE is **77.0% versus its 69.7% seed** there. Its SWE-bench table reports **75.6% versus 75.2%**, not 71.9% (AHE v1 pp.6–7, Tables 1–2).[13]
The retained v4 agrees on these central figures.[4]
The supplied survey’s reference number 85 also lists authors inconsistent with the linked AHE paper’s first page.[1][13] Use the primary paper for these claims.

AHE’s actual experiment holds the base model fixed and edits harness components. It uses an observable component workspace, layered trajectory reports with raw-trace drill-down, and a manifest predicting next-round fixes/regressions (AHE §§3.1–3.3, pp.4–5).[13] Its single ten-iteration campaign used 89 Terminal-Bench tasks, two rollouts per task per iteration, extended timeouts, and shared GPT-5.4-high role agents; ACE and TF-GRPO were comparison loops from the same seed (§4.1–4.2, p.6).[13] These are external reported experiments, **not runs reproduced here**.

The caution is substantial: AHE’s components interact non-additively; some repositories regress; regression predictions miss most regressions; budgets are coupled to the evolution model; human-in-the-loop production remains untested (AHE pp.7–10, Table 3/Figure 4, Limitations).[13][4] Selection on the evolution benchmark is not an untouched generalization test. The small aggregate SWE-bench difference should not be inflated into universal improvement. Nor does an external skill/tool update demonstrate parameter learning, energy-based reasoning, dynamic layer growth, or recursive intelligence gains.

### Which prescriptions should not become dogma

The survey’s absence of general-purpose agent frameworks and embedding-based **code retrieval** is a corpus finding, with acknowledged inspection limits (§13.2, pp.53–56; §15.6).[1] It does not prove that no framework is useful, or that semantic retrieval over kr8’s conversations/documents is inappropriate. The paper itself distinguishes conversation embeddings from code retrieval and describes framework/harness convergence (§14.2, p.60).[1] Likewise its approximate tool-count and compaction thresholds are observed design choices, not kr8 performance gates. Prefer a small existing surface and measured additions—not mandatory rewrites.

## 3. kr8 today versus the owner’s intended stack

### Verified capability boundaries

The following separates supported interfaces from locally exercised reads. It is not a full kr8 source/security audit.

| Surface | Evidence and present status | What is not established |
|---|---|---|
| Spaces, messages, threads, project/repository/task routing | Bundled CLI help exposes messages, channels, projects, repositories, issues, and patches. Owner-authored searches and thread reads were actually exercised.[5][6][7] | A shared scheduler, exactly-once task execution, or a complete durable tool trace. |
| Owner-reviewed agent drafts | `agents draft-create` / `draft-update` help and bundled docs explicitly open forms. Creation happens after owner save; a draft is not an active identity.[5][7] | Headless creation/activation, or an accepted automatic build path. |
| Workflow API | Create/update/trigger/approve interfaces exist; this channel’s list returned `[]`.[5] | A workflow was executed. Bundled docs warn `workflows runs` always returns `[]`, so it is not execution evidence.[7] |
| Canvas / saved Toolbox tools | Read-only bridge health returned `ok:true`, version 2. Inventory reported `exists:false`, `initialized:false`, `toolCount:0` for this vault’s Toolbox.[5] | An installed, approved pilot tool or runnable board graph. Zero here does not mean Hermes has no tools. |
| Tool governance | Canvas docs specify typed ports, exact-byte trust, `agentGate.mayRun`, approved-tool-only execution, run/status/resume, and forbidden actor impersonation.[9] | Denied-action enforcement was not adversarially tested here; same-OS-user capability files are not process isolation. |
| Runtime hosting | Official Hermes docs describe ACP sessions, model selection, file/tool notifications, permission requests, cancellation, persistence, and cwd binding.[10][11] This session is routed through ACP. | Conformance across all alternative runtimes; a locally verified permission prompt path. |
| Portable capability packages | Bundled skills and the builder/import documentation exist. Imports and licensing decisions are human-controlled.[8][9] | A tested marketplace, automatic safe skill promotion, or runtime-equivalent capabilities. |

The CLI does not accept `--version`; that failed read is retained rather than inventing an app revision.[5] Original local documents are copied into the evidence bundle so citations remain reviewable if bundled files change. No credentials/configuration secrets were read.

### Recovered product intent—and its limits

The October 5 owner message asks specifically about usefulness for **kr8 itself and its eventual Agents stack**. Other owner-authored relay messages ask for workflow/tool recreation for kr8, full-stack efficiency, and a draft-to-build path that avoids manual clicking; the latter is event `9974bdde836dd65331c8ea4b31565bcdfba414dba5f3e6a5f852ff1495e1dcb1`.[6] These establish direction, not a detailed architecture or blanket execution authority.

The owner-supplied conversation records model-level ideas: alternating frozen/editable components (line 21), inference-time configuration/engram changes (35), modular growth/checkpoints (60), heterogeneous memory (198, 619), a minimal testable core (237), and speed/token efficiency (362).[3] These are **owner prompts within a summarized conversation**, not an independent scientific source. Assistant assertions in that document were not treated as verified mechanisms. Searching it found no `kr8` passage or formal agent-stack specification.

I did not recover a signed product specification fixing runtime roster, hosting mode, permission model, cross-space memory scope, scheduling/ownership, or promotion authority. Consequently the responsibility split here is explicitly proposed. Before implementation, the owner must resolve those choices. That missing detail does not prevent a general read-only application review; it does prevent claiming an approved target stack.

## 4. Ranked applications

The ranking is my proposed order for learning value versus integration risk, not a paper result. Permission containment is a prerequisite to every rank, not a tradeable feature.

### 1 — Evidence-backed handoffs and just-in-time context

**Workflow:** research → engineering → independent review, or a resumed agent deciding which revision/result is current. **Paper grounding:** context lineage and incremental summaries (§§9.5–9.7, pp.32–34), deferred information (§8.3), and explicit evaluation limits (§15.6).[1] **kr8 grounding:** actual thread/search reads and CLI output contracts; current workflow-history limitations.[5][7]

**Boundary:** retain the raw thread/source record; introduce a task-scoped index linking assignment, owner, current producing revision, artifact/hash, observed checks, unresolved decisions, and superseded results. The index is a navigation aid, not a memory rewrite, evaluator, or new authority. Tools fetch the original evidence when needed.

**Required data/tools:** authorized task messages, artifact reads, stable IDs, producing revisions, read-only verification commands, and a retention rule. A receipt should distinguish command completion, test outcome, author interpretation, and independent review. Record infrastructure/provider failure separately from scientific failure.

**Benefit hypothesis:** less repeated reading and fewer stale-result or false-completion handoffs. **Risks:** private transcript disclosure, fabricated provenance, stale pointers, and instructions hidden in retrieved material. Preserve access scope and treat records as data. **Failure condition:** lower information cost accompanied by lost owner constraints, unverified claims, or cross-space leakage. This is the recommended pilot.

### 2 — Reviewed capability bundles, not uncontrolled self-modification

**Workflow:** recurring kr8 procedures become versioned skills or approved Toolbox chains. **Paper grounding:** skills versus MCP and review/provenance (§12.5, pp.48–50); safety and extension recommendations (§16.6/16.8, pp.69–70).[1] **kr8 grounding:** human-controlled imports, exact-byte trust/gates, saved-tool run/status/resume.[8][9]

**Boundary:** an agent proposes a package/diff with its rationale, source/license, declared inputs/outputs, required permissions, expected fixes, regression risks, and rollback version. A human reviews promotion. Execution remains at the approved-tool boundary; drafting never grants identity or execution rights.

**Required data/tools:** repeatable authorized task evidence, package manifests, dependency/license checks, a separate reviewer, and regression cases. Existing Toolbox inventory is empty locally, so this is an integration proposal, not an already running optimization loop.[5]

**Benefit hypothesis:** useful procedures can accumulate without replacing model weights. **Risks:** malicious package content, permission expansion, hidden dependencies, and overfitting to one task. **Failure condition:** the package cannot reproduce its benefit under matched conditions, cannot disclose its reach, or requires bypassing approval. AHE supplies inspiration for a manifest—not proof that autonomous promotion is safe.[13]

### 3 — Bounded orchestration with ownership and aggregate budgets

**Workflow:** a coordinator assigns genuinely independent research/review/build units while retaining one owner per artifact.
**Paper grounding:** Table 9 and Figure 6 (§11.1, pp.39–41) distinguish orchestration shapes; Recommendation 12 says to justify delegation rather than add it universally (§16.7).[1]
**kr8 grounding:** current space/thread/task routing plus runtime-managed delegation, not evidence of a global kr8 scheduler.[5][7][10]

**Boundary:** kr8 records assignments and results; the runtime manages its own child execution. Define parent/task/attempt IDs, exclusive write ownership, cancellation propagation, a bounded fan-out and aggregate resource ceiling. Different channel sessions must not be mistaken for the same worker or for independent security principals.

**Required data/tools:** task dependencies, runtime lifecycle receipts, actual cost/usage where available, isolated workspaces for writers, and explicit retry/deduplication policy. Provider availability and elapsed time must be observed rather than inferred from a fresh assignment.

**Benefit hypothesis:** independent work can finish sooner with clearer review. **Risks:** duplicated work, shared-file races, multiplied spend, provider outages, and coordinator loops. **Failure condition:** coordination consumes the expected benefit, repeated work lacks a producing revision, or one agent’s failure/permission scope contaminates another. Do not adopt a mesh protocol merely because agents exist.

### 4 — A small host/runtime conformance contract

**Workflow:** kr8 hosts interchangeable ACP-compatible runtimes without reimplementing each model loop.
**Paper grounding:** protocol placement (§13.3, pp.56–58), meta-harness boundary (§14.4, pp.61–62), and Recommendation 13.[1]
**kr8 grounding:** documented ACP tool events, session model selection/cancellation/cwd binding, and owner-reviewed runtime changes.[5][10][11]

**Boundary:** host identity/authorization and evidence stay in kr8; runtime-specific editing, compaction, provider quirks, and child execution remain below the adapter. Expose capability differences instead of pretending all agents are equivalent.

**Required data/tools:** approved runtime identities and harmless conformance fixtures for streaming, tool completion, model override, interruption, denial, restart/resume, and failed-call handling. A declared capability is not a passed probe.

**Benefit hypothesis:** fewer duplicated runtime features and lower switching friction. **Risks:** approval translation errors, credential inheritance, lost cancellation, and misleading UI status. **Failure condition:** an adapter cannot deny an operation, correlate a tool’s terminal outcome, preserve task scope, or disclose unsupported behavior. No new runtime or configuration is authorized by this review.

## 5. Security boundary that cannot wait for “evolution”

Current official Hermes ACP documentation warns that Buzz hosts can answer permission requests programmatically with `allow_once`; an approval protocol on the wire is not necessarily a human approval dialog. It also warns about exposing host-shell capabilities to non-owner authors.[10] I **did not test whether this exact behavior applies to the installed kr8 build**, and did not change respond-to settings or toolsets.

The local Canvas contract independently says capability files are accessible to processes under the same OS user; actor/community binding is not per-process isolation.[9] General runtime docs likewise distinguish command policies from OS containment.[12] Therefore neither a new agent identity, worktree, prompt, nor empty “approval required” label establishes least privilege. Any future pilot needs actual approved read-only containment and must fail closed when its intended deny boundary cannot be established. No cross-user containment or prompt-injection immunity is claimed here.

## 6. Recommended reversible pilot — evidence/context handoff

**Status: proposed only; requires separate owner authorization.** It is independent of E20/E21/E22, with no access to their final sets, keys, scientific gates, or model checkpoints.

**Hypothesis:** on bounded status-reconstruction tasks, an indexed evidence handoff preserves verified correctness while reducing context/retrieval effort relative to the current unstructured thread handoff. This tests a host/context design, not intelligence growth or self-modification.

**Data:** prepare synthetic, explicitly labelled kr8-like task archives and harmless public artifacts, not private channel exports by default. Include stale earlier results, a superseding owner instruction, mismatched artifact hashes, cancelled tasks, provider errors, and quoted malicious instructions. Each task asks for the current verified state, producing evidence, uncertainty, and next required decision. Ground truth belongs to a separate evaluator and is not placed in the index. Do not present synthetic fixtures as real project outcomes.

**Matched arms:** control gets the archive/files in current unstructured form; treatment gets a task index over the **same accessible bytes**, with raw drill-down available. The index may organize existing metadata but may not add grading labels or answers. Keep model/provider/reasoning, tool access, limits, prompt objective, and terminal environment identical; randomize paired arm order and start clean sessions. Freeze package bytes before evaluation. Do not simultaneously alter tools, prompts, memory, or model selection.

**Proposed scale:** 12 development cases, then 24 fresh evaluation cases, two repetitions per arm: **96 scored runs**, plus separately accounted development work. These counts are proposals, not adopted gates. No evaluation cases feed edits. The evaluator should be blind to arm labels where feasible. A pilot of this size can justify a larger study or reject an integration; it cannot establish broad superiority.

**Outcomes:** paired verified-state accuracy; false-completion/stale-revision/unsupported-claim counts; preservation of owner constraints; denied-action/attempted-leak counts; actual input/output tokens, elapsed time, retrieval calls, and human correction time. Classify infrastructure failures separately and report both all-attempt and completed-attempt results. Missing usage/pricing is missing—not estimated dollar savings. Report per-case deltas and uncertainty, not just an aggregate score.

**Requirements before starting:** owner approval of dataset rights, evaluator, scoring rubric, fixed configuration, retention/egress, maximum spend and runtime, and enforceable read-only scope. Exact cost is unknown until the model route and budget are chosen; this research used no model/GPU experimental runs. No weights or corpus downloads are required for the proposed design. If existing runtime access costs money, authorization still precedes runs.

**Stop conditions:** any unapproved write/send, privacy leak, exposed grading answers, unenforced deny boundary, exceeded approved resource cap, or persistent provider failure stops the affected pilot immediately. Stop tuning at the frozen development limit; no repair after viewing evaluation outcomes. If correctness regresses or efficiency gains depend on omitting evidence, reject the treatment. A safety violation blocks promotion even if accuracy improves.

**Reversibility:** everything stays in an isolated research directory and temporary task contexts. Disable the index and return to the control handoff; no app deployment, permanent skill installation, agent activation, wiki admission, or shared memory promotion is part of the pilot. Any later UI integration or automatic harness editing is a new decision.

## 7. Limits, decision, and handoff

The complete supplied paper was read; the independently checked numerical claim required AHE v1 and v4. Only directly relevant primary papers, owner records, official runtime docs, and bundled/local CLI contracts were used. Eleven upstream implementations were **not** independently re-audited, external benchmarks were not rerun, installed permission enforcement was not tested, and a formal intended stack remains unrecovered. These limits prevent stronger product or self-improvement claims.

**Owner decision requested after Orchestrator QA:** approve or decline the read-only pilot, and if approved select its budget, evaluator, data/retention boundary, and runtime. Separately clarify the intended agent-stack specification and draft-to-activation authorization. The research handoff is complete; execution stops here. Cloud AI Generalist may queue accepted findings for the website, but this report does not publish there or modify the existing experiments.

## Sources

[1] https://arxiv.org/pdf/2609.00006v1 — Harness Engineering — exact v1 PDF
[2] https://arxiv.org/abs/2609.00006 — arXiv metadata and version history
[3] https://docs.google.com/document/d/1uoH2B7XWXKFBNIBhnte1_l-lf6C-LWaMrqvjAkCDXyk/export?format=txt — Owner-supplied summarized conversation
[4] https://arxiv.org/pdf/2604.25850v4 — Agentic Harness Engineering — v4 primary benchmark paper
[5] file:///C:/Users/Majied/.kr8/RESEARCH/NEW_AI_ARXIV_2609_00006_SOURCES_2026_10_05/KR8_CAPABILITY_RECEIPTS.json — Read-only kr8 CLI and bridge receipts
[6] file:///C:/Users/Majied/.kr8/RESEARCH/NEW_AI_ARXIV_2609_00006_SOURCES_2026_10_05/OWNER_RELAY_SEARCH.json — Owner-authored relay discussion retrieved October 6
[7] file:///C:/Users/Majied/.kr8/.agents/skills/buzz-cli/SKILL.md — Bundled Buzz CLI documentation
[8] file:///C:/Users/Majied/.kr8/.agents/skills/kr8-builder/SKILL.md — Bundled kr8 Toolbox/import boundary
[9] file:///C:/Users/Majied/.kr8/.agents/skills/kr8-canvas/SKILL.md — Bundled kr8 Canvas and tools contract
[10] https://hermes-agent.nousresearch.com/docs/user-guide/features/acp — Hermes ACP user guide
[11] https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals — Hermes ACP internals
[12] https://hermes-agent.nousresearch.com/docs/user-guide/security — Hermes security model
[13] https://arxiv.org/pdf/2604.25850v1 — Agentic Harness Engineering — original v1 cited-study check

### Source ledger: dates, reliability, and limits

| Source | Date / exact record | Reliability for this review |
|---|---|---|
| [1] | Retained v1; PDF/record display July 15, 2026; retrieved October 5. Hash above. | Primary architecture survey, not independently reproduced; benchmark citation error and metadata anomaly disclosed. |
| [2] | Abstract HTML retrieved October 5; captured history lists one version. | Authoritative for what arXiv displayed at capture, not independent resolution of the anomalous identifier/date. |
| [3] | Owner-supplied export, retrieved October 5; SHA-256 `b41399e9927865d7358d47ed6037f023a6060bf3f984694dfdbdaf76144c1e1b`. | Evidence of the recorded owner prompts; summarized, not a verbatim authenticated original chat; assistant research claims not trusted. |
| [4] | v4 PDF prints May 18, 2026; retrieved October 6; SHA-256 `299f2633b4c13db7bed52434b4db7c48ea621993581014d30e7bcd036d3464df`. | Primary reported experiment; no local reproduction or claim of latest version. |
| [5] | Read-only commands captured October 6 with command/timestamp/exit results. | Direct evidence of this CLI/bridge read behavior; no inference of successful writes or permission enforcement. |
| [6] | October 6 searches of owner-authored relay events; original event IDs/timestamps retained. | Direct product-intent discussion in retrieved events, not a complete signed stack specification. |
| [7]–[9] | Bundled local docs, captured October 6; byte copies and hashes in source inventory. | Authoritative supported contracts; behavior not exercised is labelled documentary. No whole-app source audit. |
| [10]–[12] | Official Hermes pages retrieved October 6; HTML/text and hashes retained. | Primary current runtime documentation; installed-build conformance and local safety configuration remain unverified. |
| [13] | Original v1 PDF prints April 28, 2026; retrieved October 6; SHA-256 `c22ba4d4561912ddfbf3d93f5bf77d556390106fbd5046646b1ec2cb2376a8ec`. | Primary version check eliminates a later-revision explanation of the survey’s 71.9% misattribution; experiments not reproduced. |

### Application self-check

| Application | Exact paper locator | Actual supported kr8/runtime evidence | Claim boundary |
|---|---|---|---|
| Indexed evidence/context handoff | [1] §§8.3, 9.5–9.7, pp.27–28, 32–34 | [5] message/thread/search reads; [7] lines 50–73 and 124–128 | Navigation proposal; no measured accuracy/cost gain. |
| Reviewed capability bundles | [1] §12.5, Tables 10, pp.48–50; §16.8, p.70 | [8] lines 50–65; [9] lines 222–226; [5] empty local Toolbox | Review/approval contract exists; no approved package was installed or run. |
| Bounded orchestration | [1] §11.1, Table 9/Figure 6, pp.39–41; §16.7, p.69 | [5] routing interfaces; [10] ACP toolset and session behavior | Runtime delegation is not proof of a global kr8 scheduler or throughput benefit. |
| Host/runtime conformance | [1] §13.3, Table 14, pp.56–58; §14.4, pp.61–62 | [10] host integration; [11] event, permission and session lifecycle | Supported adapter surface; denial/cancellation probes remain proposed. |
