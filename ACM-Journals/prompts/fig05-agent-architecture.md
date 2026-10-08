# Figure 5: Heterogeneous SLM-LLM agent at runtime

- **Figure ID:** fig05-agent-architecture (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see the runtime path of one model call in an agent built to hypothesis H: the router sends call types meeting H1 to H4 to a specialized SLM, every SLM output passes a validity check and a correctness check, and a failed check escalates the call to a frontier LLM, which also takes the call types that fail the conditions.
- **Placement:** Main text §7.5 "Heterogeneous SLM-LLM Systems"; replaces the TikZ figure with `\label{fig:hetero_agent}` (keep the label).
- **Size:** full width, 139 mm, about 60 mm high.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/agentic.tex` §7.5 (figure caption and TikZ code of `fig:hetero_agent`, which this brief replaces), §7.3.2 "Structured Output: Validity Is Not Correctness", §7.3.3 (compounding errors and why H4b breaks it), §7.5.1 "Routing Designs".
- `ACM-Journals/sections/introduction.tex` §1.3 (H4a, H4b; escalation on a failed check).
- After Belcak et al. (cited in the caption); inspiration only.

## Layout

Left to right. User task enters the agent control loop; tools and memory sit below the loop and connect to it. The loop sends each model call to the router. From the router, two branches: an upper branch labelled "H1 to H4 met" to the specialized SLM, and a lower branch labelled "otherwise" to the frontier LLM. The SLM's output passes through two checks in sequence, validity (H4a) then correctness (H4b). Passing both returns the result to the loop. Failing either check sends the call along a dashed "check fails: escalate" arrow to the frontier LLM. The frontier LLM's output returns to the loop. Draw the two checks as small gates on the SLM's return path, not as separate models.

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | User task | raw-external | full | | agentic.tex fig:hetero_agent |
| C2 | Agent control loop | model | full | issues model calls | agentic.tex §7.1 |
| C3 | Tools and memory | raw-external | full | shared by the loop | agentic.tex fig:hetero_agent |
| C4 | Router | training-eval | full | decides per call type; secondary text "call type, cost, privacy, network" | agentic.tex fig:hetero_agent; §7.5.1 |
| C5 | Specialized SLM | model | full | default for H1 to H4 call types; secondary text "tool selection, argument filling, extraction, classification, short patch" | agentic.tex fig:hetero_agent |
| C6 | Validity check (H4a) | training-eval | full | schema validation, parsing | introduction.tex §1.3 |
| C7 | Correctness check (H4b) | training-eval | full | executor, unit test, constraint, or reference lookup | introduction.tex §1.3 |
| C8 | Frontier LLM | model | full | escalation target; secondary text "planning, decomposition, long context, broad knowledge" | agentic.tex fig:hetero_agent |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C1 | C2 | task | solid |
| C3 | C2 | tool results and memory | solid, two-way |
| C2 | C4 | model call | solid |
| C4 | C5 | H1 to H4 met | solid |
| C4 | C8 | otherwise | solid |
| C5 | C6 | output | solid |
| C6 | C7 | valid | solid |
| C7 | C2 | correct: result returned | solid |
| C6 | C8 | invalid: escalate | dashed |
| C7 | C8 | wrong: escalate | dashed |
| C8 | C2 | result returned | solid |

## Annotations and equations

- Small note near C6 and C7: "Valid but wrong outputs pass C6; only C7 stops them compounding".
- Caption draft: "Heterogeneous SLM-LLM agent. A per-call router sends call types meeting H1 to H4 to a specialized SLM; each output passes a validity and a correctness check, and a failed check escalates the call to a frontier LLM, which also handles planning-like and long-context calls. The split between paths varies by agent. After Belcak et al."

## Must not imply

- No share of traffic on either path: the split is not established in general.
- The branch label "H1 to H4 met" names the conditions drawn in full in fig03-hypothesis-conditions; do not redraw them here.
- No costs, latencies, or accuracies.
- Speculative decoding is not part of this figure.
- Do not draw the checks as models; they are programs (validators, executors, tests).

## Open questions

- none
