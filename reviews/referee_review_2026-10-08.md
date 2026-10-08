# Review: A Survey of Small Language Models for Agentic AI: Architectures, Compression, Deployment, and Evaluation

*Reviewed 8 October 2026 · Mode: full review plus re-review against `less-is-more_peer_review.md` (5 Sept 2026) · Coverage: `ACM-Journals/less-is-more.tex` and all included sections and partials, `supplement.tex` and all 17 supplement sections, `bibliography.bib`, the Oct 3 PDFs (44 + 47 pp), `source/merged_llm_database.json` v3.5, and `source/scripts/apply_inclusion_rules.py`. Sources are unchanged since the Oct 3 build. Venue: ACM Computing Surveys.*

Method: five separate passes (contribution and fit, methods and evidence, domain and literature, devil's advocate, and comment-by-comment re-review). Their findings were merged here and the load-bearing ones were re-checked against the files and the cited external sources. All passes run on one underlying model, so where several raise the same point that is repetition, not independent confirmation. No manuscript file was edited.

## Summary of the submission

The paper surveys small language models (SLMs) with an agentic focus. It does six things:

1. Defines an SLM by two bounds of about 20B parameters: active parameters per token (C1) and total parameters (C2).
2. Releases an inventory of 209 variants from 2023 to 2026, made up of 178 SLMs and 31 small-active MoEs, selected by a stated rule.
3. Reviews compression along separate axes.
4. Audits the vendor evaluation record for an 18-model cohort, with a negative result: no defensible cross-model table can be built from it.
5. States a conditional hypothesis H. A specialized SLM should be the default for agent calls that meet four conditions: bounded (H1), recurrent enough to repay specialization (H2), short-context (H3) and cheaply checkable (H4). The paper gives a falsifier for H.
6. Grades the evidence and proposes six experiments.

## Overall assessment

**Not ready to submit. Advisory recommendation: major revision before submission.**

The revision after the 5 Sept review addressed most of the conceptual problems:

- The thesis is now conditional and falsifiable.
- The definition is frozen.
- The retention-percentage table is gone.
- An agent-specific evidence section exists.
- Privacy, compliance and energy claims are scoped.

Nothing found here invalidates the main claim, because H is honestly graded D and its gaps are stated.

What stops submission falls into four groups:

1. **Venue length.** The paper is over CSUR's normal length, and the main text depends on a 47-page supplement.
2. **The three empirical contributions are less solid than presented.**
   - The inventory's "mechanical" rule and "209 of 209 vendor sources" are contradicted by the released file.
   - The audit's negative result is partly a consequence of its own exclusion rule, with factual errors in its illustrations.
   - The evidence grades are applied unevenly.
3. **H2 and the falsifier.** H2's economics leave out escalation and checking cost. The falsifier has no statistical decision rule and does not treat the comparators equally.
4. **Missed literature.** Several "None" and "not located" verdicts at the centre of the evidence gap are contradicted by 2025 work the paper does not cite.

All of these are fixable without new experiments. The paper's own `REVISION_NOTES.md` lists the full primary-source audit as not done, and this review found further errors of exactly that kind.

## Strengths

- **C1/C2 definition.** The split separates per-token compute from storage and residency. It handles MoE models consistently and is written into every record (`meets_c1_active_le_20b`, `meets_c2_total_le_20b`, `slm_class`) (§1.2.1).
- **Reproducible counts.** Rerunning the inclusion script on a scratch copy reproduces 178/31/219/11 exactly. The count history reconciles: 126 + 27 = 153; 153 + 64 − 2 = 215; 215 + 5 − 11 = 209. Per-year counts are 37/74/56/42.
- **Operational, honest H.** H has a tolerance δ, a refutation condition and four comparator configurations, including a hosted unspecialized small model and a no-escalation arm (§1.4, §10.3). It is graded D, and cost per completed task is marked as unmeasured.
- **Counterexamples.** §7.4 names six workload classes where H fails and says two of them are not transitional.
- **Compression review.** The single compression ratio was withdrawn in favour of axis-separated tables (Tables 2 and 3). The 4-bit speedup claim is limited to batch-1, bandwidth-bound decoding (§6.3.1).
- **Privacy scoping.** The paper states what on-device does and does not guarantee (§6.1.1), and that on-premises deployment is not compliance (supplement, healthcare section).
- **Accurate figures where checked.** Agent-benchmark numbers (WebArena, GAIA, SWE-bench, τ-bench, p^n) and the APIGen/xLAM leaderboard claims are reported accurately and with hedges.
- **Honest attribution.** The paper credits Belcak et al. explicitly for the structure of §7.
- **Clean build.** Neither PDF has undefined references or citations, `??` or `TO SUPPLY` markers. Every figure has a `\Description`, and all fonts are embedded.

## Critical and major issues

No issue is critical: none on its own invalidates the main claim as written. The first item, however, can cause desk rejection.

### 1. Length exceeds CSUR's norm, and the main text is not self-contained (major, submission blocker)

- **Location:** whole manuscript; `\documentclass[manuscript,screen,review]`.
- **Issue:**
  - The main PDF is 44 pp: body to p.36, Declarations, then References to p.44.
  - A scratch rebuild in `acmsmall` gave 45 pp, with about 37 pp of body.
  - CSUR's guidance, as published in mirrors of its author guide, says surveys "should not normally exceed 35 pages when formatted using the Surveys style". It allows an electronic supplement "when justified" and warns that excessive length may be rejected without review.
- **Material the main text depends on but that sits only in the supplement:**
  - the taxonomy figure (`fig:taxonomy`);
  - the cohort table (`tab:model_specs`);
  - the reporting-dimensions table;
  - every inventory figure.
  The main text has 51 `\suppsec` references. §3.3–3.5, §2.3 and §8 are stubs that point to the supplement.
- **Why it matters:** this risks desk rejection, and a headline contribution (the taxonomy) cannot be seen in the article.
- **Remedy:** cut to 35 pp in `acmsmall`. Bring the taxonomy figure and a compact cohort table into the main text. Fold §8 into §9. Move the count history and build narrative in §1 to the supplement. State in the cover letter which pages form the article. The official page (dl.acm.org/journal/csur/author-guidelines) returned 403, so confirm whether references count, either on that page or with the editorial office.
- *Raised by:* contribution, re-review.

### 2. The inventory's "mechanically applied" rule and "209 of 209 vendor primary sources" are not supported by the released file (major)

- **Location:** abstract ("selected by a mechanically applied inclusion rule"); `introduction.tex:210-212` ("209 of 209 records link one"); Declarations ("each retained record was checked against the vendor source it links"); `apply_inclusion_rules.py`.
- **Issue: sourcing.**
  - 11 SLM records have `reference_url` on openrouter.ai and 2 on venturebeat.com.
  - Ling 3.0 Flash Fin, Ling 3.0 Flash Sante and Dots3-Note Preview have no other source.
- **Issue: what the script actually checks.**
  - It computes C1/C2 mechanically.
  - Encoder-decoder, derivative and duplicate exclusions are hard-coded name lists.
  - M2 (public artifact) and M4 (dated release) are never checked, and M1 is checked only as "a parameter count parses".
  - Records of undisclosed size are routed by their prior placement (`was_slm`). As a result, GPT-4o mini and Nova Micro/Lite are excluded, while GPT-4.1 mini, o4-mini, Claude Haiku and Gemini Flash-Lite remain in the LLM comparison set.
  - 115 of the 219 LLM records have undisclosed size but are plotted as "large" in Fig. 1.
- **Issue: record errors confirmed in the file.**
  - All three SmolLM2 records link the SmolLM3-3B page.
  - "Mistral 7B v0.3" is dated 2023-09-27; v0.3 is a 2024 checkpoint.
  - Voxtral Mini is excluded as "undisclosed" and tagged API, while its Hugging Face link points to Mistral-Small-3.1-24B. The official card (huggingface.co/mistralai/Voxtral-Mini-3B-2507) shows an open-weight Apache-2.0 model.
  - The Command R7B family link points to an Embed v3 post, and the DeepSeek V4 Flash family link points to the DeepSeek-Coder repository.
- **Why it matters:** the inventory is a headline contribution, and the value of a rule-derived inventory is that each decision can be audited. This is also the peer review's priority action 11, which the authors' own notes mark NOT DONE.
- **Remedy:**
  - Describe the rule as "C1/C2 computed mechanically; exclusions by named editorial decision".
  - Replace `was_slm` with an explicit field.
  - Re-source the 13 aggregator records, or report "N of 209 link a vendor source".
  - Fix the listed records, correct Voxtral's identity and re-run the pipeline. Do not hand-edit 209 to 210.
  - Label the comparison curve "exceeds C1 or undisclosed".
  - Add per-record retrieval dates: only 27 of the 209 SLM records have them.
- *Raised by:* methods, re-review, contribution.

### 3. The headline count and Fig. 1 present frontier MoEs as SLMs, and the "acceleration" claim is false for SLMs proper (major)

- **Location:** abstract; Fig. 1 caption ("SLM releases accelerate sharply from mid-2024"); `introduction.tex:9` ("shows the resulting acceleration … 42 released in 2026 alone").
- **Issue: frontier models in the headline count.** The 31 "small-active MoEs" in the headline 209 include Llama 4 Maverick (400B), Qwen3.5-397B-A17B, Nex-N2-Pro (397B), MiMo-V2-Flash (309B), DeepSeek V4 Flash (284B), Dots3 (280B) and gpt-oss-120b.
- **Issue: release trend.** Counted from the released file, strict SLMs (C1 and C2) per year are 36 / 71 / 49 / 22, with 2026 counted through 4 Sept. Twenty of the 42 releases in 2026 exceed 20B total. Only the combined curve rises. The source used to seed the inventory also changed to the OpenRouter catalogue in 2026, which can create apparent trends.
- **Why it matters:** the opening narrative is carried by models the paper's own definition says are not SLMs, and the field would not call 400B flagships small.
- **Remedy:**
  - Make 178 the headline count.
  - Plot the two classes separately, and add releases per period, not only the cumulative curve.
  - Correct the caption and text, and note the change in seed source.
  - Consider a total-parameter cap on the companion class.
- *Raised by:* devil's advocate, methods, literature.

### 4. The audit's negative result is partly produced by its own rule, has no denominator, and its illustrations contain factual errors (major)

- **Location:** §5.1.3 (rule (a); "exclude nearly every cell"); §5.2, `reported_performance.tex:168-190`.
- **Issue: rule (a).** It excludes any cell with "only a single self-reported value [that] could not be cross-checked". Applied to a vendor-only record, it removes nearly everything by construction.
- **Issue: no denominator.**
  - The paper gives no model × benchmark × condition matrix and no count of cells removed by each rule.
  - The collection date is never stated, so criterion (4) cannot be checked.
  - 14 of the 18 models come from four vendors.
- **Issue: factual errors in the illustrations** (checked against huggingface.co/microsoft/Phi-4-mini-instruct and arXiv:2503.19786).
  - "GSM8K and MATH alone" are common to the three families. MMLU-Pro is also common: Phi-4-mini reports 52.8, 0-shot CoT.
  - The Gemma 3 "only for the former / only for the latter" statement is wrong.
  - The Phi-4-mini card contains a single-harness matched table covering six cohort models (Phi-3.5-mini, Llama-3.2-3B, Qwen2.5-3B/7B, Gemma2-9B and itself). The audit never mentions this class of vendor-run matched evidence.
- **Issue: prior work.** The general point is the premise of HELM, the Open LLM Leaderboard and Biderman et al. 2024 (arXiv:2405.14782), none of which is positioned against. Biderman et al. is not cited at all.
- **Why it matters:** the audit is one of four headline contributions, and as written it is an informed observation, not a documented audit.
- **Remedy:**
  - Release an 18 × benchmark coverage ledger with counts excluded under rules (a), (b) and (c), and show the result under (b) and (c) alone.
  - Give collection dates.
  - Correct the three sentences.
  - Add a paragraph on vendor-run matched tables (they satisfy the harness condition but carry selection bias).
  - Cite Biderman et al. and HELM.
- *Raised by:* all four lenses.

### 5. H2's break-even omits escalation and checking cost, so H2 is neither correct nor checkable in advance (major)

- **Location:** §1.4 H2 (N > F/(c_L − c_S)); §7.2.2; abstract ("conditions that can be checked in advance").
- **Issue:** under the system H prescribes, the saving per call is about (1 − e)·c_L − c_S − c_v, where e is the escalation rate and c_v the checking cost. If e ≥ 1 − (c_S + c_v)/c_L there is no saving at all. The paper's own §7.3.4 says a cheaper model that needs retries "is not cheaper", but the formal condition ignores it. e, F and c_S are known only after a model has been specialized. FrugalGPT and AutoMix, both cited, model exactly this.
- **Why it matters:** a call type can satisfy H2 as written while the SLM-first system costs more, which is the falsifier itself. This also undermines the claim, made against Sharma & Mehta, that H's conditions can be checked in advance.
- **Remedy:** restate N* with e, c_v and expected attempts. Mark H2 as estimated from a pilot, with values recorded before the run and held fixed. Limit "checkable in advance" to H1, H3 and H4.
- *Raised by:* devil's advocate, methods, literature, contribution.

### 6. H4's checker detects invalid output, not wrong output (major)

- **Location:** §1.4 H4 ("a schema validator, an executor, a unit test, or a constraint"); §7.3.2 ("the gap between well-formed and correct output is where small models still lose ground").
- **Issue:** a wrong tool called with valid arguments passes any schema validator, and with a schema validator as the checker, H4 is trivially met by every H1 call. Yet "H4 … is what breaks this compounding" holds only if the checker catches semantic errors.
- **Why it matters:** it is the small model's typical failure (valid but wrong output) that escapes escalation and compounds as p^n, so this undercuts the mechanism H relies on.
- **Remedy:** split H4 into a validity check and a correctness check, and require the second at a cost well below c_L. State that schema validation alone does not satisfy H4. In Experiment 5, report the rate of silent errors that pass the checker.
- *Raised by:* devil's advocate. This review accepts it on the paper's own text.

### 7. The falsification design cannot decide δ = 2 pp and does not treat the comparators equally (major)

- **Location:** §1.4 (δ); §10.3, Experiment 5.
- **Issue: no statistical rule.** The design gives no number of tasks, repeats, test or interval. At n ≈ 50–115 tasks per τ-bench domain and p ≈ 0.5, the standard error is 4.7–7 pp, more than twice δ.
- **Issue: unequal comparators.** Configuration 1 ("a frontier model throughout") gets no checker or retry loop, so "small and specialized" is confounded with "verified and retried".
- **Issue: missing alternatives.** Prompt caching, batch pricing and hosted fine-tuned mini models are absent from the comparators; prompt caching is not mentioned anywhere in the manuscript. These are the cheapest real alternatives for the repetitive calls H targets, and they raise N*.
- **Remedy:**
  - Pre-register a non-inferiority test with task-clustered variance and a power-based task count.
  - Give every configuration the same checker and retry budget.
  - Add a cached or batched frontier configuration and a fine-tuned hosted-mini configuration.
  - State how many workload-level failures reject H for a class.
- *Raised by:* devil's advocate, methods.

### 8. Missing 2024–2025 literature contradicts the central "None / not located" verdicts (major)

- **Location:** Table `tab:agentic_evidence` ("Cost per completed task: None"); §7.3.1 ("we did not locate published sub-10B standings on the later multi-turn and agentic splits"); §7.3.4; abstract ("no measurement of cost per completed task"; "a size gap").
- **Uncited work, existence checked:**
  - APIGen-MT / xLAM-2 (arXiv:2504.03601): 1–70B models on τ-bench and BFCL multi-turn, with smaller models reported to surpass larger ones in multi-turn settings. Developer-reported, so grade C, but exactly the evidence said not to exist.
  - Cost-of-Pass (arXiv:2504.13359): measures the expected cost of a correct answer across model classes.
  - "AI Agents That Matter" (arXiv:2407.01502): joint cost–accuracy evaluation of agents.
  - HAL (arXiv:2510.11977): 21,730 agent rollouts across 9 models and 9 benchmarks, with cost tracked.
  - Also missing: MobileLLM (arXiv:2402.14905), RouterBench (arXiv:2403.12031), XGrammar (arXiv:2411.15100), grammar-aligned decoding (arXiv:2405.21047), and Gupta et al.'s SLM survey (arXiv:2501.05465, updated 2026).
- **ThinkSLM (arXiv:2502.11569) is misdescribed** (§2.5). The paper says it uses 14 benchmarks and "does not treat compression". It uses 17 and studies quantization, pruning and distillation, finding that quantization preserves reasoning while pruning disrupts it. That corroborates the paper's one grade-A claim but conflicts with the grade-B "INT4 hurts multi-step reasoning more" claim.
- **Why it matters:** the "None" cells carry the evidence gap in the abstract and conclusion, and the paper's search for this literature is not recorded (§1.6).
- **Remedy:**
  - Add these works and grade them.
  - Narrow the gap to "no SLM-first vs all-LLM agent comparison on one workload".
  - Adopt cost-of-pass terminology.
  - Bound every "we found no" statement by search date and sources.
  - Correct the ThinkSLM description and reconcile it with the SLMQuant-based claim. Cite the specific SLMQuant table, since its abstract does not state that trend.
- *Raised by:* all four lenses.

### 9. Novelty against the closest work is overstated, and the agentic increment is diluted (major)

- **Location:** `background.tex:27` ("Judging from its stated scope, it does not … state when the SLM-default design fails"); Table `tab:survey_compare`; title; §3, §4, §6 and §8; abstract ("organize them under a multi-label faceted taxonomy").
- **Issue: Sharma & Mehta.** Their abstract (arXiv:2510.03847, checked) "delineate[s] limits where fallback remains valuable (open-domain reasoning and some long-horizon planning)". It also proposes SLM-default with LLM fallback, verifier cascades and cost per successful task, and scopes models at 1–12B and sometimes up to 20B. The genuine increment is narrower:
  - the C1/C2 split;
  - the evidence grading;
  - explicit conditions and a δ-based falsifier;
  - a fuller list of counterexamples.
- **Issue: agentic material is a minority of the paper.** It is about 25–30% of the main text. Taxonomy, compression and deployment are general SLM coverage that overlaps Wang et al. (TIST) and Van Nguyen et al.
- **Issue: the inventory carries no agent-relevant fields.** It has no function-calling support and no agent-benchmark coverage, so no agentic claim is computed from it.
- **Issue: the taxonomy is not applied.** "Assigning every facet to all 209 variants is left to a future version" (§3.1).
- **Remedy:**
  - Correct the Sharma & Mehta description from the full text, citing sections, and narrow the novelty claim to the four items above.
  - Either reorient the general sections around H1–H4 (for example, add agent-relevant facets and benchmark coverage to the inventory) or state the increment over prior surveys section by section.
  - Either assign facets per variant or describe the taxonomy as an exemplar-based indexing scheme and drop it from the abstract's claims.
- *Raised by:* contribution, devil's advocate, literature.

### 10. Evidence grading is applied inconsistently, and headline sentences outrun the grades (major)

- **Location:** §5.1.4; Tables `tab:claim_grades`, `tab:compression_quality` and `tab:agentic_evidence`; §9.1; §6.3.1; §9.2; §7 title.
- **Issue: inconsistent grades.**
  - The scheme mixes control (A) with independence (B).
  - Single-harness cross-model studies the paper itself accepts (Lu et al., Srivastava et al., Open LLM Leaderboard v2) yield no graded claims. That makes "only one grade-A claim is a property of the field" partly a product of the authors' choices.
  - "End-to-end sub-10B success is low" is graded B. Yet WebArena, GAIA and SWE-bench report no sub-10B models, and the "size gap" rests on AgentBench's 2023 comparison of open models up to 70B against commercial APIs, which confounds size with open versus closed status. That is grade D.
  - The 10–30× and 40–70% figures from Belcak et al. are a position paper's estimates (D, not C).
- **Issue: ungraded headline claims that drop H2 and H3** and contradict "cost per completed task: None":
  - §9.1, bold: "Right-sizing beats scaling … inverted for any task whose requirements can be stated in advance and checked";
  - §6.3.1: "ordinal and robust … the small model is cheaper by a wide margin";
  - §6.3: "the large model buys nothing that the task can use";
  - "a grade on every substantive claim" (§1.5) is not borne out.
- **Remedy:**
  - Give a two-axis grading rule and regrade under it.
  - Downgrade the size-gap claim and re-word the abstract ("a gap between open ≤70B and commercial models on 2023 benchmarks").
  - Restate the headline sentences conditional on H1–H4 and grade them D.
  - Retitle §7 to match H, for example "When SLMs Should Be the Default in Agents".
  - Change the abstract to "the experiment that would refute it for a given workload".
- *Raised by:* methods, devil's advocate, contribution.

### 11. The C2 "residency" rationale is contradicted by a model in the paper's own inventory (major)

- **Location:** §1.2.1 C2 ("about 10–11 GB at 4-bit … can be resident"); §3.2.2 ("resident memory track[s] total parameters").
- **Issue:** Apple's AFM 3 Core Advanced (20B total, 1–4B active), listed as on-device, keeps "the full model … in flash memory" and swaps experts into DRAM on demand (machinelearning.apple.com, AFM third-generation page). Weight streaming from flash is established prior work: "LLM in a flash", arXiv:2312.11514, uncited. Total parameters bound storage and download size, not resident memory.
- **Issue: the bound itself.** The paper's own rationale does not single out 20B. A 30–35B model at 4-bit also fits a 24 GB consumer GPU, as Qwen3-30B-A3B (about 17 GB) does. The figure "10–11 GB at the bound" also conflicts with the paper's own 4.4–5.8 effective bits, which give 11–14.5 GB for 20B parameters.
- **Remedy:**
  - Restate C2 as a storage and residency bound, and treat resident DRAM as architecture-dependent.
  - Discuss flash offloading.
  - Either justify 20B with an explicit hardware target or present it as a convention, with a count sensitivity analysis at 13B, 20B and 32B (the released fields allow this).
- *Raised by:* literature, devil's advocate.

## Minor issues

**Factual and internal consistency**

1. §3.2.3: "Jamba … 2.6× lower KV-cache memory" → Jamba reports 8× (arXiv:2403.19887).
2. `taxonomy.tex:69`: Phi-3, Phi-4, Gemma 3 and Llama 3.2 all use θ = 500,000–1,000,000 → wrong. Phi-4 uses θ = 250,000 with 16K context; Phi-3-mini-128k reaches 128K via LongRoPE with θ = 10,000.
3. §3.2.1: SwiGLU is said to be the "default in every major family" → Gemma uses GeGLU.
4. `supp_taxonomy.tex:23`: Minitron is said to prune "Llama 3.1 8B … 40× reduction in training compute". This contradicts the main text, which correctly says Nemotron-4 15B, 40× fewer tokens and 1.8× compute. The error is carried over from the reviewed version.
5. DeepSeek-R1 distills: "Qwen-2.5 1.5B–14B" in the supplement's taxonomy section vs "1.5B–70B Qwen and Llama" in its distillation section → reconcile.
6. 4-bit memory reduction: 3.2–3.4× (§6.3.1) vs 2.8–3.6× (Table 2, §5.4, table S8) vs "14 GB→4 GB" (§4.3.1) vs "15 GB→4.5 GB" (§5.4) → use the S8 range everywhere.
7. `supp_figures.tex:11`: the caption says 3–7B is "the largest single band by 2025". It isn't: in 2025, 7–10B has 15 records and 3–7B has 13. The caption also contradicts its own `\Description`.
8. `supp_tables.tex:155`: MLC-LLM is listed with an "MCU" target, which contradicts the paper's conclusion that no inventory model fits a microcontroller.
9. §3.2.1: the context-length trend rests on 6 of 37 records in 2023 → report n per year and separate the classes.
10. The counting unit is not applied as stated. Checkpoint and domain variants have separate records (Qwen3-4B-Instruct vs -2507; Ling Flash, Fin and Sante; the Phi-4 reasoning variants).
11. "Compact ≤3B … every documented phone deployment" conflicts with Gemma 3n/4 E-series and AFM 3, which the paper presents as on-device.
12. `supp_applications.tex:88`: "no legal equivalent of MedQA or HumanEval in general use" ignores LegalBench, LexGLUE and CUAD.
13. Supplement residues that contradict the main text or are unsourced:
    - AWQ described as "near-lossless INT4";
    - "synthetic-data-first … more effective";
    - LiteRT "100× CPU speedup";
    - ExecuTorch "serving billions";
    - "strong safety tuning";
    - the unconditional statement on legal data residency in `supp_taxonomy.tex`.
14. Vendor scores in `supp_families.tex` are still ungraded and lack shot settings ("68.8% on MMLU", "remarkable results"). "De facto standard", "state of the art" and "LLaMA" still appear in a few places, against the paper's own convention.
15. The energy argument keeps "one to two orders of magnitude" less energy per query while withdrawing the 10,000-instances claim on the utilization grounds that also undercut the per-query figure. The 2023 web-search comparison (de Vries) should be dated against Google's 2025 measurement of 0.24 Wh for a median prompt (arXiv:2508.15734).
16. Constrained decoding is model-independent, so it neutralises an objection to SLMs rather than supporting P3. Tam et al.'s result has a public rebuttal by the Outlines authors; note that it is contested.
17. §7.6: Apple is used as the production instance. Note the 12 Jan 2026 Apple–Google joint statement that "the next generation of Apple Foundation Models will be based on Google's Gemini models and cloud technology", and say what the Apple case does and does not show.
18. Table `tab:agentic_evidence`, row "Share of calls meeting H1–H4": it reports Belcak et al.'s criterion, which differs from H1–H4 → rename the row. Pin Belcak to its version: v3 is dated 22 Sept 2026, so check the 40–70% and 10–30× figures.

**Bibliography**

19. `smollm3` authors (the blog gives "Bakouch, Elie …") → fix.
20. `abdin2024phi35`: no such technical report was found; Phi-3.5 is in arXiv:2404.14219 → verify.
21. `grattafiori2024llama3` is cited for the Llama 3.2 1B/3B edge models, which that paper does not cover.
22. `qwen2024qwen25` is cited for Qwen2.5-VL → use arXiv:2502.13923.
23. `apple2026afm3` is cited for "third-party cloud models behind the same API surface"; the statement was not found on the cited page.
24. Aya-101 (13B mT5 encoder-decoder) is used as SLM multilingual evidence, although C1 excludes encoder-decoders → use Aya-23 8B.

**Presentation and submission mechanics**

25. The PDF prints `https://doi.org/10.1145/nnnnnnn.nnnnnnn`, "ACM Comput. Surv. 1, 1" and "Received 5 September 2026". The text also describes an October 2026 classification stage. → add `\settopmatter{printacmref=false}` and drop `\received` for submission.
26. Only the first author has an `\orcid` → add ORCID iDs for all authors.
27. CCS: the source comment still says "Verify/refine". Check that `10010520.10010553.10010554` really is "Embedded systems"; one pass recalled it as Robotics, unverified.
28. The inventory and scripts are "deposited on acceptance", and "provided with the manuscript source files" is something reviewers do not receive. → deposit now with a DOI (anonymised if required) and cite it.
29. The text narrates its own revision history (126→215→209; "including our own"; "earlier drafts"). §9.1 says a benchmark campaign "would be a more valuable contribution … than another survey". The conclusion's "less is more" thesis is never introduced. → move the history to the changelog and cut the clause.
30. Snapshot dates disagree: "through 4 September" (Fig. 1); "snapshot 5 September" (treemap); "v3.5 (3 October 2026)" (supplement) → use one.
31. References span two documents: "Sections 7.5–S11.2"; "Section 6, Table S5", where S5 is in S9; `discussion.tex` cites `subsec:applications_legal` without `\suppsec`.
32. The Declarations' "retrieval dates recorded for 27 records" is the SLM-array count; the file has 76 → clarify.
33. The verification agenda (§10.3) targets 2024 models (Mistral-7B, Phi-4 at 14B), has no stated selection rule, seeds or repeats, and its QLoRA experiment maps to no research question.
34. The PDF has 20 dangling `glo:*` link targets and is untagged; the build has 74 "multiply defined" warnings from xr (harmless) → print the glossary or turn off acronym links.
35. `REVISION_NOTES.md` describes an intermediate version: 74 pp, 126→215, "no grade-A claim", Boolean queries, a record-flow table and TO SUPPLY counts, none of which exist now. → rewrite before it is used as a response letter.

## Re-review against the 5 Sept 2026 peer review

There were 31 concerns: 10 major comments, 13 minor comments, 7 priority actions and the CSUR-fit item. Of these, **15 are resolved, 15 partly resolved and 1 not resolved.** The main claim is now adequately bounded. The remaining gaps are reproducibility (nothing deposited), the source audit, and venue fit.

| ID | Original concern | Verdict | Remaining action |
|---|---|---|---|
| M1 | Article type; conditional thesis; counterexamples | Resolved | None (§1.4, §7.4) |
| M2 | Consistent SLM definition; per-model dimensions | Partly | The inventory lacks weight memory and KV cache per variant (derivable) → add them, or say plainly they are absent |
| M3 | Search protocol, counts, deposit with DOI | Partly | Recast as a narrative survey (acceptable), but nothing is deposited, and only 27 of 209 records have retrieval dates |
| M4 | Evidence classes; grading; provenance table | Partly | Provenance is model-level only (no shots, harness or date); ungraded vendor scores remain in S3; grading inconsistent (Major 10) |
| M5 | Rebuild or remove Table 3 | Resolved | None |
| M6 | Agent-specific evidence | Resolved | But see Major 8 on missed literature |
| M7 | Moderate deployment and economic claims | Resolved | Residues: minor 6 and 15 |
| M8 | Taxonomy orthogonality and multi-label facets | Partly | Facets not assigned per variant; licence is "See source" for 100 of 209 records |
| M9 | Full factual and bibliographic audit | Partly | Gemma 3 and SmolLM2 fixed; new errors in Major 2 and minors 1–8 and 19–24 |
| M10 | 2026 related work; update policy | Partly | Policy present; no 2026 survey and no multilingual survey cited |
| m1, m2, m4, m7, m9, m10, m12 | Definitions; token counts; missing values; energy scope; privacy; HIPAA/GDPR; ACM footers | Resolved | One legal-residency residue (minor 13) |
| m3 | Benchmark conditions | Partly | Quoted scores lack shots and harness |
| m5, m6 | "De facto" and "state of the art"; capitalization | Partly | A few residues (minor 14) |
| m8 | Healthcare and legal evidence | Partly | Legal benchmarks ignored (minor 12) |
| m11 | Placeholder DOI and dates | Partly | Still rendered (minor 25) |
| m13 | Accessibility; figures; wide tables | Partly | Untagged PDF; dangling glossary links |
| P6, P7, P9, P10 | Identity; frozen rule; retention values; agent framework | Resolved | — |
| P8 | Release inventory, provenance, scripts | Partly | Deposit now |
| **P11** | **Primary-source audit of every specification** | **Not resolved** | Marked NOT DONE by the authors; errors confirmed (Major 2) |
| P12 | Reformat; remove unfinished metadata | Partly | Minor 25 |
| CSUR fit | Questions, inventory, synthesis, claims, length | Partly | Length (Major 1); deposit |

New issues introduced by the revision: minor 7, 25, 30, 31 and 35, plus the "209 of 209" and "mechanically applied" wording in Major 2.

## Questions for the authors

1. Which 35 pages are the article, and which supplement sections must a reader see to follow the argument?
2. How many model × benchmark × condition cells were examined, how many did each of rules (a), (b) and (c) remove, and does the negative result survive without rule (a)?
3. How will H2 be assessed before an escalation rate exists? What prevents a failed test from being reclassified afterwards as "H2 not met"?
4. What concrete checker satisfies H4 for tool selection, as opposed to argument format?
5. In Experiment 5, does the frontier arm get the same checker and retry budget? Are cached, batched and fine-tuned hosted-mini configurations included? What test and what task count decide "within δ"?
6. How do APIGen-MT, Cost-of-Pass and HAL change the "None" cells and the "size gap" sentence?
7. Should 300–400B flagships be in the 209 headline count, and what is the count with a total-parameter cap?
8. Have you read Sharma & Mehta in full? Where, by section, does it lack failure conditions or an active/total distinction?

## Devil's-advocate points not accepted

- **"The Apple–Gemini announcement undercuts the flagship production instance."** Accepted only as a disclosure point (minor 17). Rejected as evidence against H: the statement concerns what the next foundation models are built on, not whether Apple routes calls between on-device and server models. The paper uses Apple to illustrate routing, not to measure cost.
- **"H is a niche design rule, not a substrate, so the title overstates."** Rejected for the article title: it no longer says "substrate", and H is explicitly conditional with counterexamples. Accepted for the §7 heading, which still reads "Small Language Models as the Substrate of Agentic AI" (Major 10).
- **The shift toward small-active MoE as evidence against H.** Rejected as a finding. The shift may reflect the change in seed source, and the inventory cannot say which. It belongs as an open question in the discussion of Major 3.

All other devil's-advocate points were accepted and merged into Majors 3–10 and minors 16–18.

## Checks performed

- **`check_latex.py`:** run on both documents. It reported undefined labels, but every one is a cross-document `xr` reference; the real build logs have **0 undefined references or citations**. It also flagged 4 supplement figures never referenced in the text (`fig:releases_by_size`, `fig:family_size_range`, `fig:context_by_year`, `fig:moe_vs_dense`) and 49/60 bibliography entries uncited per document. Those two lists are mostly an artefact of the shared bibliography; worth one look.
- **PDF scans:** no `??` and no `TO SUPPLY` markers. The rendered DOI and Received placeholders were confirmed.
- **Inventory, recomputed read-only from v3.5:**
  - class counts 178/31/219/11;
  - per-year strict-SLM counts 36/71/49/22;
  - band counts by year;
  - `reference_url` domains (openrouter.ai 11, venturebeat.com 2);
  - the SmolLM2 links, the Mistral v0.3 date and the Voxtral record.
- **External facts checked:**
  - Sharma & Mehta abstract (arXiv:2510.03847);
  - the Phi-4-mini card's MMLU-Pro value and comparator table;
  - HAL (arXiv:2510.11977);
  - the Apple–Google joint statement (12 Jan 2026).
  Other arXiv IDs and model facts were checked by the individual passes, with the URLs given above.
- **Not checked:**
  - the current official CSUR guideline page (403);
  - the CCS concept ID;
  - SLMQuant's full text;
  - a full reconciliation of every citation against its source, of which about 30 were spot-checked.
