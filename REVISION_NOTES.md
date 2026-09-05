# Response to the peer review of 5 September 2026

Maps each review point to the change made. Section numbers refer to the revised
manuscript (`ACM-Journals/less-is-more.pdf`, 69 pp; the same section files build
`paper_consolidated/paper.pdf`, 62 pp).

Items marked **TO SUPPLY** are values only the authors can provide. They render
in the PDF as conspicuous `[TO SUPPLY: ...]` markers so none can be missed;
setting `\needsdatafinaltrue` in the preamble turns each into a hard build error
for the camera-ready.

---

## Major comments

### 1. Article type and central contribution

The substrate claim is now an explicit, falsifiable conditional, stated as
hypothesis H in a new S1.4, with four named antecedent conditions: the call must
be **bounded**, **recurrent**, **short-context**, and **verifiable**. A new S8.4,
"Where the Hypothesis Does Not Hold," names six workload classes for which a
frontier model remains correct (open-ended planning, long-context synthesis,
uncheckable generation, low-resource-language and safety-sensitive calls, sparse
or unstable call distributions, cold-start deployments) and states that two of
them are categorical rather than transitional. The abstract, S8, S10, S11, and
S12 are aligned to the conditional form.

### 2. Consistent definition of SLM

New S1.2 fixes a two-condition definition:

- **C1 (compute envelope)** bounds *active* parameters per token at ~20B, which
  governs latency, FLOPs, and energy.
- **C2 (residency envelope)** bounds *total* parameters at ~20B, which governs
  storage, download size, and resident memory.

Four terms are distinguished: **SLM** (both conditions), **compact model**
(<=3B), **edge model** (a claim about documented deployment target, not size),
and **small-active-parameter MoE** (C1 but not C2). The last class covers 6 of
the 126 inventory entries and is excluded from every on-device, storage, and
resident-memory claim in the paper. S3.2.2 applies the distinction directly to
Mixtral 8x7B, Qwen3-30B-A3B, and Llama 4 Scout, and notes that Granite 4.0 Tiny
satisfies both. Table 1 lists the eight reporting dimensions the review asked for,
each with its inventory coverage rate.

### 3. Survey methodology and reproducibility

S1.6 now provides: five research questions (RQ1-RQ5); per-stream search protocols
naming the sources searched and giving the full Boolean query verbatim;
inclusion criteria T1-T3 for literature and M1-M4 for model variants, with
per-record exclusion reasons; a two-stage deduplication rule (normalized
title+author, then arXiv ID and DOI); and a four-criterion quality appraisal
whose criteria are deliberately the same ones S7 audits the vendor record
against. Table 3 is the record-flow table. S1.6.5 specifies four deposited
artifacts: the machine-readable inventory, the screening ledger, the source
ledger, and a changelog.

**TO SUPPLY:** retrieval and screening counts (Table 3), the number of
independent screeners, the agreement statistic, the search window dates, and the
archival DOI. I did not invent these; they must come from your actual screening
records.

### 4. Conclusions aligned with the evaluation evidence

S7.1.6 introduces a four-level grading scheme: **A** controlled (one harness,
matched baselines), **B** independent, **C** reported by the interested party,
**D** author interpretation. Table 9 grades the paper's eleven principal claims.
No claim carries grade A, and the paper states this as a finding about the
field's evidence base rather than a defect of the survey. Grades also appear per
row in the compression quality table and the agent-evidence table.

### 5. Table 3 rebuilt

The single compression-ratio / accuracy-retention table is **withdrawn**. S4.1
gives the reasons: the compression ratio conflates reductions in parameters,
memory, and training compute, which trade against different budgets, and it is
undefined for distillation, where student size is a design choice rather than a
property of the method; and an accuracy-retention percentage is uninterpretable
without a baseline precision, model, size, task, metric, and aggregation rule.

Replaced by two tables. Table 4 separates what each technique reduces along five
axes (parameters, weight memory, training compute, decode latency, retraining
requirement). Table 5 states the quality cost as a sourced, scoped, graded claim
rather than a number. The withdrawal and the prohibition on reinstating the old
table without a per-cell ledger are recorded in the provenance appendix.

### 6. Agent-specific evidence

New S8.3 assembles the evidence the general benchmarks cannot supply, organized
by the capability an agent exercises:

- function calling and tool selection (BFCL, Gorilla, ToolBench, API-Bank, xLAM);
- structured-output validity (constrained decoding as a model-size-independent
  guarantee);
- end-to-end agent success (WebArena, GAIA, SWE-bench, AgentBench);
- multi-step reliability (tau-bench pass^k, with the explicit p^n compounding
  argument that motivates hypothesis H's verifiability condition);
- routing, escalation, and cost.

Table 10 grades all ten lines. The honest finding is reported rather than
smoothed: the evidence is strong and independent at the level of the individual
call, and **absent** for router calibration, escalation rate, and cost per
completed task. S7.4 separately explains why MMLU, GSM8K, and HumanEval are the
wrong instrument for the agentic question.

### 7. Deployment and economic claims moderated

New S6.4.1 separates calculated quantities (weight memory, KV-cache size) from
measured ones (throughput, TTFT, sustained rates, energy, TCO) and enumerates the
conditions the latter depend on. Specific fixes:

- The near-linear INT4 speedup is scoped to single-stream, batch-1,
  bandwidth-bound decode, with the regimes where it fails (batching, prefill,
  hardware without native low-precision kernels) stated. The same correction is
  applied in S2.5.
- "Zero marginal cost" is scoped to the operator's per-query cash cost, with
  battery, thermal budget, and device amortization named as real costs.
- The 10-30x serving-cost figure is marked grade C, with the reason for its width
  given and the ordinal claim identified as the part the argument uses.
- New S6.1.1 replaces "no data leaves the device" with the four conditions that
  actually determine egress (telemetry, logging, cloud escalation, other pipeline
  stages). Every privacy claim in the paper is now scoped to it.
- The 10,000-instances energy claim is **withdrawn** as unsourceable. S10.6.1
  sets out the accounting boundary a real environmental comparison would need.

### 8. Taxonomy revised

S3.1 states that the facets are separately observable but **not orthogonal**,
gives the specific entanglements, and makes assignment **multi-label** rather
than a partition, with worked examples. The application-domain facet is
explicitly downgraded, with the reason (it is usually a use-case label, not an
intrinsic property) and an assignment rule. Table 2 adds the five secondary
facets the review asked for: licensing, data transparency, safety alignment,
reasoning mode, and deployment target, each with its values and why it gates
adoption. Context length and active-parameter count are handled as quantities in
Table 1 rather than as categories.

### 9. Factual and bibliographic audit

- **Gemma 3** corrected: the 1B is text-only with a 32K window; vision begins at
  4B via a SigLIP encoder. Verified against Google's model documentation.
- **SmolLM2** references reconciled: the two entries sharing arXiv:2502.02737
  are merged into one matching the arXiv record exactly, with the collision
  documented in the `.bib`.
- **Aya** corrected: Aya-101 is a 13B mT5 model covering 101 languages, above the
  compact band; Aya 23 is the 8B/23-language decoder-only model. Both are now
  cited correctly, and the breadth-versus-depth trade-off is explained.
- **Gemma 3 token budget** is now per-size (2T for 1B up to 14T for 27B) instead
  of the 27B figure applied to the family.
- **Llama** capitalization normalized (LLaMA retained only for the original 2023
  release and for published names such as Sheared-LLaMA).
- **Training tokens** in Table 6 are now split into per-variant and series-level
  rows, with both lists given, and the note states that no claim compares across
  the two. Context lengths reached by interpolation are flagged.

Spot checks against the machine-readable inventory found it correct in every case
checked, including Gemma 3 1B's modality and Aya 23's language count. The errors
were in prose that contradicted the paper's own data.

**NOT DONE:** a complete primary-source re-verification of all 126 variants. The
flagged errors are fixed and the inventory now carries a per-record source URL
and retrieval date, but a full re-audit is a separate pass.

### 10. Related work and temporal-snapshot policy

S2.7 adds and, more importantly, *distinguishes* three recent lines rather than
merely listing them: small-reasoning-model benchmarking (Srivastava et al., 72
models across 14 benchmarks under a common protocol, noted as the closest thing
in the literature to the controlled evaluation this paper says is missing),
efficient-reasoning surveys (Feng et al.), and LLM multi-agent surveys (Chen et
al.). Table 8 extends to seven prior works. S1.6.6 gives the snapshot and
versioned-update policy: how in-review releases are handled, when tables are
regenerated, and the statement that the deposited artifact, not the paper, is the
authority on inventory contents at any date.

---

## Minor comments

| Point | Where addressed |
|---|---|
| Define variant, family, checkpoint, release, pretrained, instruction-tuned, reasoning-tuned | S1.2.4, plus a naming convention for family names versus checkpoint identifiers |
| Series-level training tokens copied into every size row | Table 6 note: per-variant and series-level rows listed separately |
| Benchmark versions, prompt templates, extraction rules, decoding, harness | S7.1.2, as five named conditions, with the point that a source omitting any has not reported a comparable result |
| Confidence or evidence grades | S7.1.6, Table 9, and per-row in Tables 5 and 10 |
| How missing values were treated | S7.1.7: never imputed, interpolated, or carried across sibling sizes or base/instruct pairs; absence is itself reported; no statistic silently drops absent tuples |
| "de facto standard", "state-of-the-art" | Replaced with specific, sourced descriptions throughout |
| Consistent model-name capitalization | Normalized; convention stated in S1.2.4 |
| Scope of environmental claims | S10.6.1: teacher training, compression pipeline, device embodied carbon, grid intensity, update distribution, rebound effect |
| Healthcare and legal more descriptive than evidential | New S9.1.1 (exam benchmarks are not deployment evidence; no prospective evaluation found; OptimCLM is single-study). S9.2 now states plainly that no evidence of the required grade exists for legal, and why the domain also fails hypothesis H's verifiability and short-context conditions |
| On-device privacy claims conditional | S6.1.1, applied to every privacy claim in the paper |
| HIPAA/GDPR not automatic | S9.1: what each actually requires, and that on-premises hosting removes one transfer difficulty rather than conferring compliance |
| Placeholder DOI, unfinished revision and acceptance dates | Removed rather than left as `XXXXXXX`; `\setcopyright{none}` until the rights form is completed |
| ACM footers for a non-ACM journal | Retained, since CSUR is the stated target; the consolidated build in `paper_consolidated/` is the non-ACM variant and shares the same section files |
| PDF accessibility, embedded Unicode, figure readability, wide tables | Every figure carries a `\Description`; all fonts embedded with Unicode maps; the generated inventory tables were re-columned (in `source/scripts/generate_model_tables.py` as well as the emitted partials) and now fit the landscape page. One 1pt overfull box remains in the whole document |

---

## Build status

| | Pages | Undefined refs | Overfull boxes | References |
|---|---|---|---|---|
| `ACM-Journals/less-is-more.pdf` | 69 | 0 | 1 (1.0pt) | 149, all cited |
| `paper_consolidated/paper.pdf` | 62 | 0 | 1 | 149, all cited |

Fourteen references added (BFCL, Gorilla, ToolLLM, API-Bank, tau-bench,
AgentBench, WebArena, GAIA, SWE-bench, guided generation, ThinkSLM, efficient
reasoning survey, multi-agent survey, Aya 23); one duplicate removed. Every
added entry was verified against arXiv or the publisher record before being
cited.

## Journal target

The review's alternative-venue table is not acted on here. The manuscript remains
formatted for ACM Computing Surveys, which is what the current build targets. If
you decide to redirect to Artificial Intelligence Review or IEEE Access, the
section files are template-independent and the `paper_consolidated` build already
demonstrates that; the ACM-specific parts are confined to
`ACM-Journals/less-is-more.tex`.
