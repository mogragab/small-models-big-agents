# Figure 4: Break-even volume for specialization

- **Figure ID:** fig04-breakeven-economics (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see that an SLM-first system pays a fixed specialization cost F and then saves less per call than the gap between large- and small-model prices, because retries, checks, and escalations are paid too, so specialization pays only above a break-even volume N*.
- **Placement:** Main text §7.2.2 "P2: Economics", after the paragraph that derives the per-call saving; `\label{fig:breakeven}`.
- **Size:** full width, 139 mm, about 55 mm high; two panels side by side.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/introduction.tex` §1.3, condition H2 and Eq. (1).
- `ACM-Journals/sections/agentic.tex` §7.2.2 "P2: Economics": per-call saving $c_L - (a\,c_S + c_V + e\,c_L)$, no saving once $e \ge 1 - (a\,c_S + c_V)/c_L$, and the factors that lower $c_L$ or $F$ (prompt caching, batch pricing, hosted fine-tuning, price declines).
- Style reference (inspiration only, do not copy): none.

## Layout

Two panels, both schematic with unlabelled axes except for symbols.

(a) "Cost over the planning horizon": horizontal axis N (number of calls of this type), vertical axis cumulative cost. Line 1, "All-LLM", starts at the origin with slope $c_L$. Line 2, "SLM-first", starts at height F on the vertical axis with slope $a\,c_S + c_V + e\,c_L$. The two lines cross at N*, marked with a vertical dashed line labelled $N^{*}$. To the left of N* a shaded band reads "specialization does not pay"; to the right "specialization pays".

(b) "What moves N*": a compact list of arrows next to a small copy of the N* mark: "higher escalation rate e", "more attempts a", "costlier check c_V", "prompt caching or batch pricing lowers c_L", "hosted fine-tuning lowers the comparator's F", each with an arrow showing that N* moves right (rises). One item, "larger gap c_L - c_S", shows N* moving left.

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | Calls of this type, N | training-eval | full | horizontal axis of panel (a) | introduction.tex Eq. (1) |
| C2 | Cumulative cost | training-eval | full | vertical axis of panel (a) | agentic.tex §7.2.2 |
| C3 | All-LLM: slope $c_L$ | model | full | line from the origin | agentic.tex §7.2.2 |
| C4 | SLM-first: slope $a c_S + c_V + e c_L$ | model | full | line starting at F | agentic.tex §7.2.2 |
| C5 | Fixed cost F | caveat | full | intercept of C4: specialization and maintenance | introduction.tex §1.3 (H2) |
| C6 | $N^{*}$ | training-eval | full | crossing point; vertical dashed line | introduction.tex Eq. (1) |
| C7 | Specialization pays | clean-data | full | region right of N* | agentic.tex §7.2.2 |
| C8 | Does not pay | caveat | full | region left of N* | agentic.tex §7.2.2 |
| C9 | Raises N* | caveat | full | panel (b) group: higher e, more attempts a, costlier check c_V, caching or batch pricing, hosted fine-tuning | agentic.tex §7.2.2 |
| C10 | Lowers N* | clean-data | full | panel (b) item: larger gap $c_L - c_S$ | introduction.tex Eq. (1) |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C5 | C4 | intercept | dotted |
| C3 | C6 | lines cross | none (geometry) |
| C4 | C6 | lines cross | none (geometry) |
| C9 | C6 | moves N* right | solid arrow |
| C10 | C6 | moves N* left | solid arrow |

## Annotations and equations

- Below panel (a): $N^{*} = F / \left(c_L - (a\,c_S + c_V + e\,c_L)\right)$ (Eq. 1).
- Small note in panel (a): "If $e \ge 1 - (a\,c_S + c_V)/c_L$, the lines never cross".

## Must not imply

- No numbers on either axis and no real prices: the slopes and intercept are illustrative.
- Not a measurement: the paper reports no measured N* for any workload.
- The SLM-first slope must stay below the all-LLM slope in the drawing, but the gap should look modest, not dramatic.

## Open questions

- none
