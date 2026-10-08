# Figure 3: Assessing a call type against H1 to H4

- **Figure ID:** fig03-hypothesis-conditions (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see how one recurring agent call type is assessed, at design time and before any comparison, against the four conditions of hypothesis H, which conditions are checked by inspection and which by pilot estimate, and what default each outcome assigns.
- **Placement:** Main text §1.3 "The Agentic Turn and the Thesis", directly after the boxed statement of H; `\label{fig:hypothesis_conditions}`.
- **Size:** full width, 139 mm, about 55 mm high.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/introduction.tex` §1.3: statement of H (H1, H2 with Eq. (1), H3, H4a, H4b), the paragraph on which conditions can be checked by inspection and which from pilot estimates, and the refutation rule.
- `ACM-Journals/sections/agentic.tex` §7.4 "Where the Hypothesis Does Not Hold" (failure classes per condition) and §7.6 "Conversion and Adoption" (clustering step).
- `ACM-Journals/sections/supp_agentic.tex` "Converting an LLM Agent to an SLM Agent" (step S3).
- Style reference (inspiration only, do not copy): none.

## Layout

Left to right decision flow for one call type. A start node (the call type, taken from clustered logs) leads to three inspection gates in a row, H1, H3, and H4, grouped under the heading "Checked by inspection". The H4 gate shows its two parts stacked inside it: validity (H4a) and correctness (H4b), with a note that both are required. After the inspection gates, one gate H2, under the heading "Checked from pilot estimates, recorded in advance", compares expected volume N with the break-even volume N* (a stub pointing to fig04). Passing every gate leads to the outcome "Specialized SLM" as the default (stub for the runtime architecture, fig05). Failing any gate leads downwards to the outcome "Frontier or hosted model default". Each failure arrow carries the name of the workload class that typically fails at that gate.

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | Recurring call type | raw-external | full | from logged and clustered agent calls | agentic.tex §7.6; supp_agentic.tex step S3 |
| C2 | H1 bounded | training-eval | full | tool selection, fixed-schema record, fixed label set, or local edit of a few lines | introduction.tex §1.3 |
| C3 | H3 short-context | training-eval | full | input fits in a few thousand tokens without retrieval over a large corpus | introduction.tex §1.3 |
| C4 | H4 checkable | training-eval | full | contains C5 and C6; both required | introduction.tex §1.3 |
| C5 | Validity (H4a) | training-eval | full | schema validation, parsing, type checking | introduction.tex §1.3 |
| C6 | Correctness (H4b) | training-eval | full | executor with observable effects, unit test, constraint solver, or reference lookup | introduction.tex §1.3 |
| C7 | H2 recurrent: N > N* | training-eval | full | N = expected calls over the planning horizon | introduction.tex §1.3, Eq. (1) |
| C8 | $N^{*}$ | training-eval | ref fig04-breakeven-economics | stub only: the break-even volume | introduction.tex Eq. (1) |
| C9 | Pilot estimates | caveat | full | estimates of a, e, c_S, F recorded before the comparison and held fixed | introduction.tex §1.3 |
| C10 | Specialized SLM | model | ref fig05-agent-architecture | outcome: SLM-first default, escalation on a failed check | introduction.tex §1.3 |
| C11 | Frontier or hosted model default | model | full | frontier LLM or hosted general-purpose model | agentic.tex §7.4 |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C1 | C2 | assess | solid |
| C2 | C3 | met | solid |
| C3 | C4 | met | solid |
| C4 | C7 | met | solid |
| C7 | C10 | met | solid |
| C9 | C7 | supplies the estimates | dashed |
| C8 | C7 | threshold | dashed |
| C2 | C11 | fails: open-ended planning | solid, red-tinted |
| C3 | C11 | fails: long or heterogeneous context | solid, red-tinted |
| C4 | C11 | fails: output cannot be checked for correctness | solid, red-tinted |
| C7 | C11 | fails: rare, unstable, or cold-start call types | solid, red-tinted |

## Annotations and equations

- Under C7: $N^{*} = F / \left(c_L - (a\,c_S + c_V + e\,c_L)\right)$ (Eq. 1).
- Heading over C2 to C4: "Checked by inspection". Heading over C7: "Checked from pilot estimates".
- Small note under C5 and C6: "Validity alone does not satisfy H4".

## Must not imply

- Not a runtime flow: no per-request routing is shown here (that is fig05).
- Passing the gates does not prove H; it identifies where H applies. No success rates or costs.
- The gate order H1, H3, H4, H2 reflects checking cost, not importance.

## Open questions

- none
