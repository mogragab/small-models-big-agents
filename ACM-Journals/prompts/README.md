# Figure prompts: A Survey of Small Language Models for Agentic AI

Index and shared requirements for this paper's figure briefs. This file is not
a figure. Generate with the Codex scientific-figures skill:
`Use $scientific-figures to generate all figures described in prompts/ and save them in figures/.`

## Shared requirements

- **Venue / sizes:** ACM Computing Surveys, `acmsmall` format. Text width is about
  139 mm; use full width (139 mm) for every figure here. Heights are given per
  brief and are tight: the main text must stay within 35 pages including
  references (it is 34 pages with the TikZ versions of these figures in place).
- **Language:** English labels.
- **Terminology:** use the manuscript's terms exactly: "SLM", "small-active-parameter
  MoE" (short form "small-active MoE"), "C1 (compute envelope)", "C2 (storage
  envelope)", "H1 bounded", "H2 recurrent", "H3 short-context", "H4 checkable",
  "validity check (H4a)", "correctness check (H4b)", "escalation", "frontier LLM",
  "cost per completed task". Never write "substrate".
- **Consistency:** the same component keeps the same label and role in every
  figure. Specialized SLMs are `model`; the frontier or generalist LLM is `model`
  with a distinct shade from the SLM; checks, metrics, costs, and decision rules
  are `training-eval`; external listings, providers, and traces are
  `raw-external`; curated records and the released inventory are `clean-data`;
  scope limits and failure conditions are `caveat`.
- **Palette:** match the paper's existing figures: muted categorical hues
  (blue #7397B8, sage #79A88E, apricot #D8A879, lavender #9B8FB5, rose #C9858C,
  slate #A2AAB1, ink #34404A). Text in Libertinus Serif to match the body.
- **No numbers that are not in the brief.** These are schematics; none of them
  plots data, and none may show performance results.
- **No em dashes** in any label.
- **Output folder:** `figures/` (inside `ACM-Journals/`). Outputs: SVG, vector PDF,
  600 dpi PNG.

## Figure plan

Planned on 9 October 2026 at the author's request to cover every diagram the
revised paper needs. One row per figure; each figure has one job.

| ID | File | Purpose (one sentence) | Placement | Replaces or adds | Status |
|---|---|---|---|---|---|
| fig01-slm-definition | [fig01-slm-definition.md](fig01-slm-definition.md) | Show how the two bounds C1 and C2 sort models into SLMs, small-active MoEs, LLMs, and undisclosed records. | Main §1.2.1, `fig:slm_definition` | adds | ready |
| fig02-inventory-pipeline | [fig02-inventory-pipeline.md](fig02-inventory-pipeline.md) | Show how the released inventory was built, verified, and filtered, and which decisions are computed versus editorial. | Supplement S2, `fig:inventory_pipeline` | adds | ready |
| fig03-hypothesis-conditions | [fig03-hypothesis-conditions.md](fig03-hypothesis-conditions.md) | Show how one agent call type is assessed against H1 to H4 at design time and assigned a default model. | Main §1.3, `fig:hypothesis_conditions` | adds | ready |
| fig04-breakeven-economics | [fig04-breakeven-economics.md](fig04-breakeven-economics.md) | Show why specialization pays only above the break-even volume N* once retries, checks, and escalations are counted. | Main §7.2.2, `fig:breakeven` | adds | ready |
| fig05-agent-architecture | [fig05-agent-architecture.md](fig05-agent-architecture.md) | Show the runtime path of a call through router, specialized SLM, validity and correctness checks, and escalation. | Main §7.5, `fig:hetero_agent` | replaces the TikZ figure | ready |
| fig06-falsification-design | [fig06-falsification-design.md](fig06-falsification-design.md) | Show the pre-registered comparison that would refute H for a workload: six configurations, shared checks, metrics, and decision rule. | Main §9.3, `fig:falsification` | adds | ready |
| fig07-taxonomy-facets | [fig07-taxonomy-facets.md](fig07-taxonomy-facets.md) | Show the four primary facets of the taxonomy with their categories and representative models. | Main §3.1, `fig:taxonomy` | replaces the TikZ figure | ready |

Considered and not drawn:

- Evidence-grading scheme (design by independence to grades A to D): the four-item list in §5.1.2 is as clear as a diagram.
- Audit coverage ledger: already a table in the supplement (`tab:audit_ledger`); a heatmap would be a data plot, which belongs to the generated-figure pipeline, not a brief.
- Compression axes: Table 2 (`tab:compression_axes`) does this job.
- Release-trend and inventory plots (Fig. 1 and the supplement inventory figures): generated from the inventory by `source/scripts/generate_figures_v2.py`, not drawn from briefs.

## Concept coverage

Each concept is drawn in full in exactly one figure; other figures show it as a
reference stub (`ref <owner>` in their Components table).

| Concept | Drawn in full in | Referenced in |
|---|---|---|
| C1 / C2 bounds and the four classes (SLM, small-active MoE, LLM, undisclosed) | fig01-slm-definition | fig02-inventory-pipeline (SLM, small-active MoE stubs) |
| Conditions H1 to H4 | fig03-hypothesis-conditions | fig05-agent-architecture (branch label only), fig06-falsification-design (qualifying call types only) |
| Break-even volume N* | fig04-breakeven-economics | fig03-hypothesis-conditions |
| Router, specialized SLM, frontier LLM, validity and correctness checks, escalation | fig05-agent-architecture | fig03-hypothesis-conditions (specialized SLM stub) |
| Comparator configurations and decision rule | fig06-falsification-design | none |
| Taxonomy facets | fig07-taxonomy-facets | none |

## Placement status (9 October 2026)

All seven briefs were rendered (see `figures/AI-FIGURES.md`). Six are placed in
the paper: fig02 (Supplement S2, `fig:inventory_pipeline`), fig03 (§1.3,
`fig:hypothesis_conditions`), fig04 (§7.2.2, `fig:breakeven`), fig05 (§7.5,
`fig:hetero_agent`), fig06 (§9.3, `fig:falsification`), fig07 (§3.1,
`fig:taxonomy`). Hard-coded figure numbers in fig02, fig03, and fig06 and a typo
in fig06 were corrected after rendering. fig01 is not placed: its active = total
diagonal is drawn as a curve near the axis corner; the paper keeps the TikZ
version of `fig:slm_definition`. To replace it, regenerate fig01 with the
diagonal as one straight line (it need not pass through the axis corner on
logarithmic axes) and without figure numbers in any label.

## Open questions across figures

- none
