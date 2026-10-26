# Response to the peer review of 5 September 2026

This letter maps each comment of the 5 September 2026 review to the current
manuscript: `ACM-Journals/less-is-more.pdf` (ACM Computing Surveys, `acmsmall`,
34 pages including references) and its electronic supplement
`ACM-Journals/supplement.pdf` (Supplementary Sections S1–S18). The same section
files build `paper_consolidated/paper.pdf`. Section numbers refer to the current
main text; "S" numbers to the supplement. A full per-item record of the later
revision of 8–9 October 2026 is in `reviews/revision_2026-10-09.md`.

We thank the reviewer. The main changes are: the thesis is now a conditional,
falsifiable hypothesis with stated failure classes and a pre-registered test; the
SLM definition separates active from total parameters; the inventory is released
with a per-record source check and the scripts that apply the inclusion rule;
the retention-percentage table is withdrawn; every principal claim carries an
evidence grade; and agent-specific evidence replaces general benchmarks as the
basis for the agentic argument.

## Major comments

**1. Article type and central contribution.** Done. The paper is a structured
narrative survey with a position stated as hypothesis H (§1.3): for call types
that are bounded (H1), recurrent enough to clear a break-even volume that counts
retries, checks, and escalations (H2, Eq. 1), short-context (H3), and checkable
for validity and correctness (H4a, H4b), a specialized SLM should be the default
with escalation on a failed check. §1.3 states the refutation rule; §7.4 names the
workload classes where H fails (open-ended planning, long or heterogeneous
context, uncheckable output, low-resource-language and safety-sensitive calls,
sparse or unstable call distributions, cold start); §9.3 specifies the test.

**2. Consistent definition of SLM.** Done, with one limit. §1.2.1 defines C1
(active parameters per token at most about 20B) and C2 (total parameters at most
about 20B), explains why both are needed for MoE models, and gives counts under
other thresholds. §1.2.2 distinguishes SLM, compact model, edge model, and
small-active-parameter MoE; the latter are counted and plotted separately. The
evaluation cohort's sub-10B scope is stated and justified (§5.1.1). The reporting
dimensions requested are listed with their coverage in Table S1: total parameters
(209/209), active parameters, context length (135/209), and target hardware are
recorded; weight memory, FLOPs, and KV cache are derivable; peak runtime memory is
not reported by vendors and is marked as such rather than estimated.

**3. Methodology and reproducibility.** Partly done. §1.5 describes how each body
of evidence was actually assembled and is explicit that the technique literature
was not screened under a recorded protocol, so no retrieval counts or agreement
statistics are reported for it; "no study found" statements are bounded by a dated
search. For the inventory: the inclusion criteria (S2), the excluded records with
reasons, a per-record developer-source check against the Hugging Face Hub API
(`verify_sources.py`, `source_check_log.csv`), the record corrections, the count
history, the changelog, and every script are released (`release/`). The
persistent-identifier deposit is pending (author action).

**4. Conclusions aligned with the evidence.** Done. §5.1.2 defines grades A–D
from the design of the strongest source and its independence; Table 4 grades the
principal claims, Tables 3 and 5 grade the technique and agent evidence. Only one
claim reaches grade A. The cross-model comparison finding is now measured: the
coverage ledger (Table S2, Supplementary Section S9) records for 14 cohort models and 8
benchmarks whether each vendor document reports an instruction-tuned value and
under which protocol (69 of 112 cells reported, 45 with a stated protocol, no
benchmark for all 14, at most 5 sharing one protocol). Model-level provenance is
in Table S10; the ledger CSV gives the document and
table for each cell.

**5. Table 3 rebuilt.** Done. The retention-percentage and single-ratio table is
withdrawn (§4.1 explains why). Table 2 separates reductions in parameters, weight
memory, training compute, and decode latency; Table 3 states what the literature
supports about quality cost, with scope and grade.

**6. Agent-specific evidence.** Done. §7.3 reviews function calling (single- and
multi-turn), format adherence, structured-output validity and its limits,
end-to-end agent success, compounding multi-step error, routing and escalation,
cost per correct outcome, and cost per completed task; Table 5 grades each line,
including contrary results. Router calibration and SLM-first versus all-LLM cost
per completed task are marked as not reported.

**7. Deployment and economic claims.** Done. §6.2 separates calculated from
measured quantities and restricts the 4-bit speedup to single-stream,
bandwidth-bound decoding, citing a vendor measurement of 2.6x (not 4x) on a phone.
"No data leaves the device" is replaced by a scope condition (§6.1). The 10–30x
figure is attributed and graded D, and H2 replaces per-token ratios with a
break-even condition that includes caching, batching, and hosted alternatives
(§7.2.2). The energy claim is conditional on utilization (S16); the
10,000-instance claim is not made.

**8. Taxonomy.** Done. §3.1 states that the facets are separately observable but
not orthogonal and that assignment is multi-label; the scheme is described as an
exemplar-based indexing scheme. Table S9 adds licensing,
data transparency, safety alignment, reasoning mode, and deployment target;
context length is a recorded quantity (Table S1).

**9. Factual and bibliographic audit.** Done for the items found. The Gemma 3
statement is corrected (vision from 4B; S6). SmolLM2 is a single entry. Every
included inventory record's developer source was checked; 12 aggregator- or
press-sourced records were re-sourced, and record errors were corrected (S2,
"Source Verification"). Bibliography entries were checked with `verify_refs.py`
(127 cited entries; no mismatch or retraction notice) and several citations were
corrected (S2; `reviews/revision_2026-10-09.md`, minors 19–24).

**10. Related work and snapshot policy.** Partly done. §2 adds the 2026 update of
the SLM survey of Gupta et al., the 2026 edge-agent position of Tian et al., the
small-reasoning-model benchmark of Srivastava et al., efficient-reasoning and
multi-agent surveys, and the closest agentic survey (Sharma and Mehta), compared
from its full text. A dedicated 2026 multilingual-LM survey is not added. S2
states the snapshot (releases through 4 September 2026, inventory v3.6) and the
update policy, which was applied to one post-snapshot study.

## Minor comments

| Comment | Response | Location |
|---|---|---|
| Define variant, family, checkpoint, release, pretrained, instruction-tuned, reasoning-tuned | Defined | §1.2.2, S1.2 |
| Series-level training tokens | Marked per-variant vs series-level | Table S4 note |
| Benchmark version, template, extraction, decoding, harness | Five conditions defined; ledger records stated protocols | §5.1.1, S9 |
| Evidence grades; missing values | Grades A–D; missing values never imputed | §5.1.2, S9 |
| "De facto", "state-of-the-art" | Replaced or attributed | throughout |
| Capitalization | Convention stated and applied | S1.2 |
| Scope of environmental claims | Accounting boundary stated | S16 |
| Healthcare and legal evidence | Evidence stated separately; legal benchmarks (LegalBench, LexGLUE, CUAD) cited; no independent deployment study found | §8.3, S13 |
| On-device privacy conditional | Scope condition | §6.1 |
| HIPAA/GDPR not automatic | Stated | S13.1 |
| Placeholder DOI and dates | Removed from the rendered PDF | preamble |
| ACM footers for non-ACM venue | Not applicable: target is ACM CSUR | n/a |
| Accessibility, figures, wide tables | Alt text on every figure; fonts embedded; acronym links disabled; inventory table landscape; PDF not tagged | both PDFs |

## Suitability for ACM Computing Surveys

The paper now meets CSUR's 35-page limit including references (34 pages in the
Surveys style), with the supplement holding detail that the main text summarizes.
Remaining author actions: ORCID iDs for three authors, the persistent-identifier
deposit of `release/`, and confirmation of CRediT roles.
