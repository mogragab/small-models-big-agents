# End-to-end manuscript review

Date: 8 October 2026. Advisory assessment: **major revision before submission**.

## Scope and overall judgment

Reviewed the current ACM main manuscript, all 17 supplement sections and their tables/captions, the shared consolidated section sources, bibliography structure, inventory v3.5, inclusion script and relevant figure-generation logic. The existing ACM PDFs contain 44 main pages and 47 supplement pages. The section copies and bibliography copies agree byte for byte. Existing edits were preserved; no manuscript, bibliography, database, or figure was changed.

This is a useful structured narrative survey with a defensible architectural distinction and a potentially useful practitioner hypothesis. It is substantially stronger than the earlier design described in the October 3 revision notes. It appropriately separates vendor reports from measurements, acknowledges the agentic success gap, and explicitly labels H as a hypothesis. Its main weakness is that its strongest contributions—the rule-derived inventory, benchmark-record audit, and evidence-graded decision rule—are still less reproducible or less tightly supported than their presentation suggests.

The revision should strengthen these contributions, rather than merely add more model names. An original benchmark campaign is **not required** for a publishable survey. A source-backed inventory, observable audit results, and an internally coherent synthesis are required for the contributions this paper chooses to claim.

The strongest alternative explanation is that existing hosted generalist small models, constrained decoding, and better agent scaffolds deliver most of the proposed benefit without a fleet of specialized models. The paper recognizes this comparator but does not yet provide evidence that specialization's incremental benefit exceeds its full cost. That uncertainty should remain central to H.

## Supported strengths

- Separating total and active parameters prevents sparse models from being mistaken for phone-resident models.
- Separating parameter, weight-memory, training-compute, and latency effects improves the compression review substantially.
- The main text now attributes the conversion argument to Belcak and engages the closest agentic survey, Sharma and Mehta.
- The distinction between syntactic validity, content quality, per-call success, and complete trajectories is scientifically important.
- Privacy and clinical deployment discussions now include useful boundaries; on-device execution is correctly distinguished from complete application privacy.
- The database counts reproduce: 209 included entries, 178 strict SLMs, 31 small-active MoEs; 219 comparison entries and 11 exclusions. Annual included counts are 37, 74, 56, and 42 for 2023–2026.
- Static citation checks find 174 bibliography keys and 174 cited keys across the scanned sources, with no missing keys or duplicate bibliography keys. This establishes structural consistency, not source accuracy.

## Prioritized major findings

### M1. The inventory does not yet establish the claimed primary-source verification and mechanical inclusion

**Location:** Introduction, “Survey Method and Sources”; supplement S2 and S17; `source/scripts/apply_inclusion_rules.py`; inventory records.

**Observed:** The Introduction says every one of 209 entries links a vendor primary source. Eleven `reference_url` values instead point to OpenRouter and two to VentureBeat. Some also carry vendor Hub links, but Ling 3.0 Flash Sante, Ling 3.0 Flash Fin, and Dots3-Note Preview have neither a paper URL nor a Hugging Face URL in the inspected records. Thus the universal primary-source assertion is not established by the released fields. OpenRouter is an aggregator, not the developer's primary source.

The inclusion script checks sizes, selected name-based exceptions, and prior placement. It does not check source identity/content, a dated release, checkpoint identity, or architecture for every record. `ENCODER_DECODER` contains only Flan-T5; derivative exclusions are manually named. For undisclosed sizes, `was_slm` influences whether a record is an exclusion or a comparison entry. This is reproducible bookkeeping, but it is not a full mechanical implementation of M1–M4.

**Confirmed factual error:** Voxtral Mini is excluded as having an undisclosed parameter count. Mistral's July 15, 2025 announcement and official model card explicitly document the 3B open-weight model. If the database means the distinct transcription API product, its identity must be clarified; the current unqualified exclusion is wrong. [Mistral release](https://mistral.ai/fr/news/voxtral/), [official model card](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507).

**Why it matters:** The inventory is a headline original contribution. A source link cannot substitute for a verified field, and a reproducible classifier cannot validate erroneous input metadata. Changing even one exclusion affects the count, generated tables, and figures; do not simply change 209 to 210 without the full reconciliation.

**Remedy:** Record a developer source, source passage/location, retrieval date, architecture class, release event, canonical variant ID, and field-level verification status. Split source verification from size classification. Validate M1–M4 against explicit fields, retain an “unverified” state, correct Voxtral's identity, and regenerate all derivatives only after reconciliation. Describe manually adjudicated exclusions as such. Audit the new 2026 entries and legacy architectural metadata first.

### M2. The inventory and figure pipeline disagree about architecture and parameter semantics

**Location:** Supplement S5 Figures S1–S5; taxonomy section; `generate_figures_v2.py` functions `is_moe`, `effective_params_billions`, and `fig_family_size_range`.

**Observed:** Classification derives sparse status from active/total counts, whereas figures trust `parameters.is_moe`. The stored flag identifies 30 MoEs and 179 dense entries; 37 records have active parameters below total. Five entries classified as small-active MoEs lack the flag: Mixtral-8x7B, Phi-3.5-MoE, Qwen2-57B-A14B, Snowflake Arctic, and Nemotron 3 Nano-30B. The inspected MoE/dense plot therefore places known MoEs in its dense group. Its dense memory median and the assumption “active equals total” are consequently contaminated.

The figure parser also unwraps nested dictionaries by trying `total_params` before `active_params`, reintroducing the semantic risk the inclusion script was designed to fix. The family-range plot uses active counts for flagged MoEs and total counts for other models, under the ambiguous axis “Effective parameters.” This is neither a total-parameter nor a consistently active-parameter figure.

**Remedy:** Use the canonical parsed fields and one architecture classification across inclusion, tables, and figures. Make total and active panels explicit; keep PLE-effective memory descriptors distinct. Add focused data-integrity checks for the five named MoEs and nested parameter records. Relabel the population “SLMs and small-active MoEs,” or plot the 178 strict SLMs separately. The database's `type: SLM` field for 124B-total sparse records should also agree with `slm_class`.

### M3. The negative benchmark-audit result is asserted without the audit output needed to evaluate it

**Location:** Main §5, especially source reconciliation and “Why a Common Benchmark Table Cannot Be Built”; supplement S8 and S16.

**Observed:** The paper says its reconciliation rules exclude nearly every cell, but presents neither a candidate-cell denominator nor an 18-model coverage/protocol matrix. S16 supplies model-level sources and broad source classes, not the checkpoint–benchmark–condition extraction ledger. Three family examples illustrate heterogeneity but do not establish a cohort-wide impossibility.

The conclusion also depends on demanding independent cross-checks for vendor values. Rejection under that rule can reflect the chosen inclusion standard, not an inherent impossibility of presenting qualified source-reported values. A descriptive table with explicit incompatible settings is different from a table purporting to rank models under one protocol.

**Remedy:** Publish the extracted matrix with checkpoint, score, benchmark/version, shots, prompt, extraction, decoding, harness/version, source location, and eligibility reason. Report the number of candidate, eligible, incompatible, and insufficiently documented tuples. State: “Our specified criteria did not yield a fully comparable 18-model matrix,” if that is what the ledger demonstrates. Preserve compatible partial comparisons. The audit can be an original descriptive result without running any models.

### M4. The recurring SLMQuant claim is not supported by the inspected source

**Location:** Compression quality table; main §5 quantization summary and claim grades; Discussion; supplement S8.

**Observed:** The survey attributes greater INT4 loss in smaller models and especially mathematical/multi-step reasoning to SLMQuant. Its accessible v1 full text evaluates SmolLM-135M and Qwen2.5-0.5B, with MMLU, ARC, PIQA, HellaSwag, and WikiText2; it does not evaluate GSM8K or MATH. It uses W4A8, not a blanket weight-only INT4 deployment recipe. It even describes larger Qwen as more affected than smaller SmolLM, qualifying any monotonic size claim. Tables show substantial degradation under some methods, rather than uniformly small losses. [SLMQuant, §4.1–§5.1 and Tables 1–2](https://arxiv.org/html/2511.13023v1).

**Why it matters:** This claim is repeatedly graded B and used to guide deployment and agent reliability. Independence does not supply evidence for unmeasured tasks.

**Remedy:** Limit the source-backed conclusion to model- and method-dependent low-bit sensitivity in the tested architectures/settings. Obtain actual mathematics evaluations for the reasoning-specific statement or remove it. Record the exact source version and distinguish W4A8, W4A16, and mixed GGUF schemes. Consider the source's own reporting limitations when appraising it; do not upgrade it based on the title alone.

### M5. H4 needs semantic error detection, and H2 needs cascade economics

**Location:** Introduction H1–H4; §7 economics, structured-output evidence, and trajectory reliability; verification experiment.

**Observed:** H4 treats a schema validator, executor, unit test, or constraint as a cheap checker, then uses checker rejection to escalate. Valid syntax and successful execution can accept the wrong tool, wrong recipient, wrong amount, or wrong edit. H4's stated existence/cost condition does not bound these undetected errors. The paper acknowledges syntax/content differences later but does not incorporate that distinction into H.

H2 uses `N > F/(c_L-c_S)` before measuring the candidate's costs, escalation, retries, or checker accuracy, although it claims the conditions are checkable before model choice. With escalation probability e and verification/routing cost v, even a simplified one-attempt cascade costs `c_S + v + e*c_L`; savings are `c_L - c_S - v - e*c_L`. The denominator must be positive. It also depends on a selected candidate and operating point. Complete-task cost requires success rates and trajectory overhead as well.

**Remedy:** Specify a semantic checker and calibrated false-acceptance/false-rejection bounds, including consequences of an irreversible tool action before verification. State H2 as a feasibility estimate with ranges and then a measured deployment gate. Include retries, idle provisioning, routing, maintenance, and escalation. Define cost per success as total cost of **all attempted tasks** divided by successful tasks, with fixed costs amortized over a declared horizon. Costing successful runs alone hides the expense of failures.

The `p^n` example is valid under independent equal-reliability steps with no recovery; state that assumption. A checker alone does not eliminate compounding without sufficient coverage and effective recovery. Define model-selection budgets and statistical noninferiority confidence intervals for the proposed δ=2 percentage-point test. A nonsignificant difference is not evidence of equivalence.

### M6. Absolute evidence-gap statements need an updated, bounded literature synthesis

**Location:** §7 routing and agent success; Challenges; Conclusion; “None” rows.

**Observed:** The paper repeatedly states that agent routing calibration and cost measurements are absent. A targeted search located *Scaling Small Agents Through Strategy Auctions* (SALE), covering Qwen3 4B–32B agents on search/coding workloads, with cost-quality comparisons and routing diagnostics. Its cost model uses estimated provider pricing, and its comparator is 32B rather than a current frontier model; it therefore does not settle H. It does, however, make a broad claim that agent routing has no cost or diagnostic evidence untenable. [SALE, experimental setup, results, Appendix B and H](https://arxiv.org/html/2602.02751v1).

Aragog also studies multi-stage model assignment, runtime scheduling, throughput, and latency, although its accessible abstract is not enough to establish its applicability to sub-10B success-normalized economics. [Aragog abstract](https://arxiv.org/abs/2511.20975). AgentRouter is a post-cutoff September 2026 lead on step routing and end-to-end completion; full-text HTML access failed, so its empirical claims remain unchecked. [AgentRouter abstract](https://arxiv.org/abs/2609.22951).

**Remedy:** Separate (i) measured or estimated agent cost-quality tradeoffs, (ii) success-normalized cost, (iii) frontier-versus-small baselines, and (iv) specialized verifier cascades meeting H. For each absence claim provide searched sources, queries, cutoff, and eligibility boundaries. “No exact test of H was identified within [scope]” is much more defensible than “no measurement” throughout the field. Treat post-cutoff work separately and follow the paper's update policy.

### M7. The legal section mistakes a coverage gap for absence of public benchmarks

**Location:** Main Applications and Limitations; supplement S12 “Legal NLP”.

**Observed:** The text says legal NLP lacks public standardized benchmarks and a legal equivalent of MedQA/HumanEval, and concludes capability evidence is absent. LexGLUE provides standardized legal NLU datasets and model comparisons; LegalBench provides legal reasoning tasks and comparisons of open/commercial models. These do not prove agentic deployment adequacy, but they directly undermine the domain-wide absence claim. [LexGLUE, ACL 2022](https://aclanthology.org/2022.acl-long.297/), [LegalBench](https://arxiv.org/abs/2308.11462).

**Remedy:** Include these benchmarks and distinguish their architectures, sizes, tasks, and evaluation conditions from a deployment-ready small-agent comparison. Review decoder-only sub-10B evidence before making a bounded insufficiency claim. Do not call every repeated legal/clinical/code operation an agentic system; relate it to an actual control loop or label it an adjacent application. The claim that local hosting satisfies privilege constraints also needs the same application-level qualification used in healthcare.

### M8. Active parameters bound approximate compute, not realized latency, energy, or price

**Location:** Definitions, taxonomy MoE discussion, deployment conclusion, sustainability discussion, supplement S15.

**Observed:** A 30B-total/3B-active model is repeatedly described as costing roughly the same as a 3B dense model per token. Active count is informative about approximate weight-related FLOPs, but realized latency/energy depend on routing, expert dispatch, memory locality, bandwidth, batch size, communication, KV traffic, kernels, and utilization. A larger resident expert pool is not free merely because it is not all active for one token.

The deployment discussion still says right-sizing is preferable on cost, latency, energy, and privacy once accuracy clears a threshold, and S15 infers one-to-two-order energy savings from compute arithmetic. Yet the paper correctly states elsewhere that these quantities require measurement. Comparing INT4 small weights to FP16 large weights also combines precision and size effects.

**Remedy:** Keep C1 as an approximate compute proxy and C2 as a weight-residency proxy; do not define them as quantitative latency/energy bounds. Present the favorable deployment outcomes as conditional, with matched success, hardware, precision, utilization, prompt/output lengths, and accounting boundaries. Separate measured joules from FLOPs and provider price. Energy proportionality does not follow from FLOPs alone. C2 permits weight residency under an assumed format, not guaranteed runtime fit.

### M9. Evidence grading conflates design, independence, and support

**Location:** §5 grading; compression and agent-evidence tables; broad claims of only one controlled result.

**Observed:** Grade A describes controlled design while B/C describe source independence. A method author's carefully matched experiment can satisfy A and C simultaneously; a community leaderboard can be independent without isolating one variable. The rule that A conditions differ only in the variable of interest does not naturally describe a comparison across model families with differing data, architecture, and post-training. “Every substantive quantitative claim is graded” is also untrue of several supplementary scores, throughput estimates, and introductory energy figures.

The paper acknowledges existing shared-harness studies while claiming that proposed work would provide the first controlled cross-model evidence in an area currently having none. This is a coverage/scoping inconsistency, not a demonstrated absence in the field. Mixed-evidence rows such as pruning should carry claim-specific rather than strongest-source grades.

**Remedy:** Use separate columns for evaluation design, source independence, directness/applicability, and verification/support status. Describe “no original controlled measurement in this survey” precisely. Reserve a grade for a defined claim, source version, and operating condition. Either grade quantitative statements consistently or narrow the grading promise to selected principal claims. Do not equate lower multilingual perplexity with demonstrated relative demographic harm.

### M10. Corrections did not propagate into the supplement, and several broad claims remain unsupported

**Location:** Supplement S6 taxonomy, S4 technical background, S13 ethics, S16 provenance, and main background.

**Observed:** S6 still attributes Minitron to Llama 3.1 and calls the result 40× less training compute. The cited original report describes Nemotron-4 15B-derived 8B/4B models, up to 40× fewer training tokens per derived model, and 1.8× compute saving for the family. The main compression section has the corrected distinction. [Original Minitron report](https://arxiv.org/abs/2407.14679).

Blodgett et al. is a critical survey of bias conceptualization and evaluation; it does not directly demonstrate that quantization/pruning disproportionately degrades dialect or demographic performance. The manuscript repeatedly uses it for that empirical claim. Multilingual compression evidence does not on its own establish demographic fairness effects. [Blodgett et al.](https://arxiv.org/abs/2005.14050). An empirical quantization-bias paper located in this review reports nuanced outcomes, making a universal amplification claim inappropriate without task/group qualifications. [How Quantization Shapes Bias, abstract](https://arxiv.org/abs/2508.18088).

Other statements needing targeted source support include GPT-4/Gemini Ultra parameter counts in the hundreds of billions; uniformly worse hallucination at smaller size; corpus composition having a larger effect than architecture; and prompt/prefix adaptation routinely underperforming LoRA for complex reasoning. These are currently broad assertions, not established comparisons in the presented ledger.

**Remedy:** Perform a claim-by-claim supplement synchronization pass. Preserve the corrected Minitron quantities; use actual compression fairness studies or label risks as hypotheses. Cite model cards for Llama 3.2 specifications rather than assuming the Llama 3 report supports every later release. Keep evidence of a deficit distinct from a universal size law. The AI declaration's assurance that every factual claim and reference was verified needs author confirmation and a support ledger; metadata repair alone cannot establish it.

## Section-by-section revision map

| Component | Assessment and required action |
|---|---|
| Title/front matter | Survey framing is appropriate. Shorten the dense abstract; state achievable contributions without universal evidence claims. The rendered first page still contains a dummy DOI and default journal reference metadata. |
| Introduction | Strong RQs and candid narrative-survey description. Fix source coverage, H2/H4, energy generalization, and claims of pre-choice checkability. Keep release cutoff distinct from collection/version dates. |
| Related work | Engage closest prior work with verified passages, rather than relying only on “stated scope” for Y/P/absent ratings. Incorporate relevant 2025–2026 routing/agent evidence. |
| Taxonomy | Useful multi-label design. Call the released inventory a partial implementation of the taxonomy. Repair architecture flags and parameter meanings; separate structural modality from code specialization. |
| Compression | Four-axis synthesis is a strength. Remove deterministic proportional latency/products from “by construction” entries; distillation does not universally reduce training compute. Correct SLMQuant scope and all Minitron occurrences. |
| Evaluation record | Convert the three illustrative examples into an auditable 18-model extraction/coverage result. Scope the negative conclusion to an explicit comparability criterion. |
| Deployment | Keep arithmetic and measurements separate throughout, including the concluding ordinal assertions. Add per-artifact sources/settings for the throughput notes or remove the numbers. |
| Agentic argument | Retain the conditional hypothesis and contrary evidence. Add semantic-checker operating characteristics, realistic cascade economics, and current bounded evidence synthesis. |
| Applications | Distinguish exam/classification evidence from actual agents; repair legal benchmark coverage. Encoder examples should remain explicitly outside the operative SLM population. |
| Discussion | Remove categorical dominance statements unsupported by matched cost/energy/latency evidence. Reflect the exact strengths and limitations of the repaired audit. |
| Challenges/experiments | Prioritize the benchmark coverage matrix and exact H test. Define held-out model selection, noninferiority inference, repeated trials, pricing/energy boundaries, and feasible hardware admission. The seven-model edge proposal includes 14B Phi-4, which may exceed phone/8GB budgets once runtime memory is included. Avoid promising weeks/single-GPU feasibility without a budget. |
| Conclusion | Replace field-wide “no published study” and “first controlled evidence” assertions with a documented search-bounded gap. State that H remains untested under the specified conditions. |
| Declarations | Confirm funding, conflicts, CRediT roles, all-author approval, submission date, and exact AI-use scope with authors. Do not change these facts based on a review. Give review-time access to artifacts even if the archival DOI is reserved for acceptance. |
| Supplement | Reconcile S1 field coverage, S2 source rules, S3 family numbers/checkpoints, S4 technique overstatements, S5 figures, S6 stale Minitron claim, S7 KD classifications, S8 source scope, S9 tables, S10 device assumptions, S11 self-verification limits, S12 legal coverage, S13 fairness/energy, S14 future-work novelty, S15 energy inference, S16 claim-level provenance, and S17 variant identity/cutoff. |

## Localized numerical and presentation findings

1. **Context missingness:** 136/209 context values are known. Year-specific coverage is 6/37 (2023), 38/74 (2024), 52/56 (2025), 40/42 (2026). Medians of reported values are 2,048; 12,288; 131,072; and 262,144 tokens. The trend is descriptive of known entries, with strongly changing coverage; it does not establish that long context became standard in the full population or sub-10B subset. Show denominators and the plotted size/class subset.
2. **Release-band caption:** Figure S1 says the 3–7B band is largest by 2025; its image and main taxonomy text show the 7–10B band is larger. Correct the caption.
3. **Population labels:** SLM plot titles include the 31 models that the operative definition excludes from SLMs. Rename or separate these populations. The cumulative figure's caption already explains the combined population; apply that clarity everywhere.
4. **Modality:** The modality plot includes “Code” alongside text, audio, video, and vision. Code is a text domain/task representation here; document a coherent ontology. Mixed input/output modalities also need explicit direction.
5. **Licenses:** “See source” is missing extraction, not evidence of absence of a license file. Do not interpret the “unspecified” bar as research checkpoints without attached licenses without checking source artifacts.
6. **Memory:** Under 4.4–5.8 effective bits per weight, 20B weights occupy 11–14.5 decimal GB, not the 10–11GB stated for C2. Ten GB is ideal packed 4-bit storage. Make ideal weight arithmetic, estimated artifact sizes, and peak runtime memory distinct. Main deployment gives 3.2–3.4× while the tables give 2.8–3.6×; align the assumptions.
7. **Counting:** Decide whether dated checkpoint revisions and domain-specific editions are new variants or updates. S17's 0731/version/domain records require a documented rule consistent with “one released parameter size within a family,” not just deduplication by name.
8. **Cohort dates:** Six months of public history alone does not explain a cohort ending in early 2025 under a September 2026 inventory cutoff. State the actual evaluation collection date and the purposive family choice; avoid presenting age as a sufficient explanation.
9. **Internal prose counts:** S16 says “one of three categories” and then supplies more categories. S17 announces three ecosystem trends and lists four. These are minor editorial inconsistencies.
10. **Cross-document build:** Existing main and supplement logs contain multiply-defined natbib citations and generated labels (`tocindent*`, `TotPages`), despite no duplicate bibliography keys. The reciprocal unprefixed `xr` auxiliary imports are a likely cause. Prefix/filter imported labels and references, rebuild in dependency order, and inspect warnings. Do not repair the bibliography for an auxiliary-import problem.
11. **Layout coverage:** The three rendered pages inspected are readable without material overlap. Main p1 still prints `10.1145/nnnnnnn.nnnnnnn`; the family-range axis says “Effective parameters” although the caption does not define that quantity. This was a targeted visual review, not every-page layout certification. The 44-page main and 47-page supplement counts are verified from existing PDFs, not a fresh build.
12. **Venue requirements:** The official CSUR author-guidelines page could not be fetched. This report does not certify the current abstract or page limit; verify against the official journal instructions before applying a numerical limit. Do not infer compliance from a different layout or secondary template website.

## Revision order and completion criteria

1. **Repair source and data validity:** verify exclusions, primary-source coverage, architecture flags, and variant identity. Success: every retained record has a supported inclusion decision or an explicit unverified status; counts reconcile; plots use canonical parsed fields.
2. **Make the audit a result:** release the coverage/protocol matrix and eligibility counts. Success: a reader can reproduce the negative or partial-comparability finding from the ledger without trusting narrative examples.
3. **Repair consequential source support:** SLMQuant, Minitron, legal benchmarks, compression fairness, and broad absence claims. Success: every principal claim has a versioned source location and explicit support/scope assessment.
4. **Operationalize H:** separate syntax from semantic verification; use cascade economics and a declared cost-per-success denominator. Success: candidate selection, calibration, break-even, and falsification can be implemented from the stated protocol.
5. **Unify final language and artifacts:** main/supplement, grades, captions, disclosure, and cross-document references. Success: no contradictory parameter/compute units, dummy publication metadata, or material auxiliary warnings; author-only statements confirmed.

## Coverage limits

External verification was targeted at consequential claims and closest/missing literature, not an exhaustive review of all 174 references or all 439 database records. The static audit scans all ACM section/partial sources; it is not a full TeX expansion or BibTeX parser. Bibliography existence, claim support, and correction/retraction status are separate checks; no complete correction-status audit was performed. No model experiments, full LaTeX rebuild, fresh cost measurements, or publication submissions were performed. Existing source comments/revision notes informed the audit but were not treated as proof that corrections were completed.

The associated `evidence_2026-10-08.md` records checked sources and access boundaries; `search_log_2026-10-08.md` records actual web queries. `audit_2026-10-08.json` and `audit_2026_10_08.py` retain reproducible local checks.
