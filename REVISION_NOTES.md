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

## Snapshot refresh, 5 September 2026

After the revision above, the inventory was brought forward from its 2026-09-04
state to 2026-09-05 and the paper regenerated from it. Two things changed the
headline numbers.

**The May-September 2026 release wave was added: 75 records.** Sources are
OpenRouter's public model catalogue (retrieved 2026-09-05) for ids, dates,
context lengths and Hugging Face ids, plus vendor announcements and model cards
for parameter counts and licences. Fields no source states are null, not
estimated. New entries include, at the small end, Granite 4.1 and 4.2 (3B/8B),
LFM2.5 (230M through 8.3B-A1B), Hy-MT2 (1.8B, 7B) and Nemotron 3.5 Content
Safety (4B); in the small-active-MoE band, Nemotron 3.5 Lightning (30B/3B),
North Mini Code (30B/3B), Laguna XS 2.1 (33B/3B), Ling 3.0 Flash (124B/5.1B) and
DeepSeek V4 Flash (284B/13B); and at the frontier, GPT-5.6 Sol/Terra/Luna and
GPT-6 Astra, Claude Opus 4.8 / Fable 5 / Sonnet 5 / Opus 5 / Fable 5.1, the
Gemini Flash line from 3.1 to 3.8, Grok 4.5/4.6, the Qwen3.7 and Qwen3.8 lines,
GLM 5.2/5.3, Kimi K3, Meta's Muse Spark and Muse Glimmer 30B, and MAI-Thinking-1.

**The inclusion rule was applied mechanically, which moved 64 records.** An audit
against C1 and C2 found that the March 2026 merge had filed a large block of
qualifying models outside the SLM inventory: Llama-2-7B, Llama-3-8B, Qwen2.5-14B,
OLMo 2-7B, Pixtral-12B, Falcon 3, StarCoder and 57 others, none of them
duplicates. Two 24B dense models (Mistral Small 3.1 and 3.2) had been filed
inside it. Placement now derives from the rule rather than from the merge.

The consequence is that the headline count moves from **126 to 215 SLM
variants**: 183 satisfying both C1 and C2, 27 small-active-parameter MoE, and 5
vendor-positioned small models with undisclosed parameters. Section 1.2 states
the reconciliation in the paper itself rather than silently restating the
number, and the released changelog lists the move per record. All 40 generated
figures and both inventory tables were regenerated; the count was updated in the
abstract, Section 1.1, Section 1.2, Section 1.5, the screening table, the
conclusion and the appendix.

Database version 3.4. Every record now carries `meets_c1_active_le_20b`,
`meets_c2_total_le_20b` and `slm_class`, so a reader can recompute the inventory
under a different threshold.

## Presentation pass, 6 September 2026

**Typography.** Both builds are now set entirely in Libertinus, replacing the
Linux Libertine + newtxmath stack acmart loads by default and the Source Sans +
Fira Math stack the consolidated template used. `pdffonts` on the ACM build
reports only `LibertinusSerif-{Regular,Bold,Italic}`, `LibertinusSans-*`,
`LibertinusMono-Regular` and `LibertinusT1Math`; no other face appears. Getting
math onto Libertinus under pdfLaTeX required marking `newtxmath` as
pre-loaded before `\documentclass` so acmart's own `\RequirePackage` becomes a
no-op; the two lines that do this are commented in `less-is-more.tex` with the
fallback to use if a future acmart release needs newtxmath's macros. The figures
set their text in Libertinus Serif too, so the page has one typeface throughout.

**Figures: PNG at 400-480 dpi.** All 40 figures are now exported as PNG at
`EXPORT_SCALE = 4`, roughly 3100-3600 px on the long edge, which is about
400-480 dpi at the printed column width and clears the usual 300 dpi floor for
raster artwork. The PDF versions are removed and all `\includegraphics` calls
updated. `ACM-Journals/figures/README.md` documents the regeneration command and
the font dependency.

**Palette rebuilt and validated.** The previous palette was chosen by eye and was
not colour-vision-deficiency safe: teal/mint, coral/peach and amber/sand
collapsed under deuteranopia and again in greyscale. The replacement was
validated rather than eyeballed, and clears the adjacent-pair CVD floor
(OKLab ΔE ≥ 8), the normal-vision floor (ΔE ≥ 15) and the chroma floor against a
white surface.

The substantive change is not the hexes but the encoding. Ordered quantities
(release year, parameter band, context bucket) now use a single-hue ramp, light
to dark, instead of arbitrary categorical hues: those data have a natural order
and the old colours asked the reader to memorise one. Only genuinely nominal
quantities (access mode, licence posture, base vs instruct, MoE vs dense) get
distinct hues, never more than three plus a neutral. Two details worth recording:
a single hue supports only five ordered steps on white before either the
lightness gaps or the light-end contrast fails, so the `>20B` band takes the
orange accent instead of a sixth step, which is also semantically right since it
is the out-of-scope band rather than the next size up; and the low-contrast hues
are only used on charts that carry direct value labels, which is the relief the
contrast warning requires.

The TikZ taxonomy figure in `sections/taxonomy.tex` was updated to the same four
categorical hues, since it claims to share the generated palette.

**Authorship.** The fourth author is now W. Eltayeb Ahmed (Department of
Mathematics and Statistics, College of Science, Imam Mohammad Ibn Saud Islamic
University, Riyadh; waahmed@imamu.edu.sa), replacing the previous fourth author
in both builds and in the consolidated `metadata.tex`. The Funding statement now
records IMSIU grant IMSIU-DDRSP2602 in place of "no funding was received", an
Acknowledgements subsection carries the same statement, and "Funding
acquisition" is restored to the fourth author's CRediT line, which resolves the
inconsistency flagged in the declarations file.

## Build status

| | Pages | Undefined refs | Overfull boxes | References |
|---|---|---|---|---|
| `ACM-Journals/less-is-more.pdf` | 74 | 0 | 1 (1.0pt) | 149, all cited |
| `paper_consolidated/paper.pdf` | 67 | 0 | 1 | 149, all cited |

Inventory: 215 SLM + 224 LLM variants across 113 families, 439 records total.

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
