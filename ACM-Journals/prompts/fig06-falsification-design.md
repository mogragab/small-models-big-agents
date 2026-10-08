# Figure 6: The pre-registered test of hypothesis H

- **Figure ID:** fig06-falsification-design (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see the design of verification study 5: one workload, call types fixed in advance, six configurations run end to end under the same checks and retry budget, the metrics reported for each, and the two-part decision rule that refutes H for the workload.
- **Placement:** Main text §9.3 "Empirical-Verification Agenda", next to item 5; `\label{fig:falsification}`.
- **Size:** full width, 139 mm, about 75 mm high.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/challenges.tex` §9.3, item 5 "Cost per completed task (RQ5, the test of H)": configurations (i) to (vi), metrics, decision rule, sample-size formula and its three worked values, workload-class and general refutation rules.
- `ACM-Journals/sections/introduction.tex` §1.3 (refutation rule; pilot estimates recorded before the comparison).
- Style reference (inspiration only, do not copy): none.

## Layout

Three columns. Left column, "Fixed in advance": the workload with a checkable success criterion, the call types meeting H1, H3, and H4 (stub), the pilot estimates for H2, the margin delta and the sample size. Middle column, "Six configurations, same checks and retry budget": six stacked rows (i) to (vi), each a short label; row (v) is highlighted as the configuration H prescribes; a bracket across all six reads "same checks, same retry budget". Right column, "Reported per configuration": the metric list, then the decision rule box with two tests, (1) non-inferiority of (v) against (i) on task success at margin delta, (2) cost per completed task of (v) lower than every other configuration, and the outcome "H refuted for this workload if either test fails". Under the decision box, one line: "H rejected as a general rule if it fails on most of at least 3 pre-registered workloads".

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | Workload with success criterion | raw-external | full | e.g. a $\tau$-bench domain or a production workload | challenges.tex §9.3 item 5 |
| C2 | Qualifying call types | caveat | full | call types meeting H1, H3, and H4 by inspection (conditions as in fig03) | challenges.tex §9.3 item 5 |
| C3 | Pilot estimates for H2 | caveat | full | N, F, a, e recorded before the comparison | challenges.tex §9.3 item 5 |
| C4 | Margin and sample size | training-eval | full | $n \approx 3.09/\delta^2$ per arm (independent arms, success near 0.5, one-sided alpha 0.05, power 0.8) | challenges.tex §9.3 item 5 |
| C5 | (i) Frontier LLM throughout | model | full | | challenges.tex §9.3 item 5 |
| C6 | (ii) Frontier, cached and batched | model | full | prompt caching and batch pricing where offered | challenges.tex §9.3 item 5 |
| C7 | (iii) Hosted small model | model | full | general-purpose small model or small-active MoE, unspecialized | challenges.tex §9.3 item 5 |
| C8 | (iv) Hosted fine-tuned small model | model | full | through the provider's service | challenges.tex §9.3 item 5 |
| C9 | (v) Specialized SLM with escalation | model | full | the configuration H prescribes (runtime path as in fig05); highlighted | challenges.tex §9.3 item 5 |
| C10 | (vi) Specialized SLM, no escalation | model | full | measures what escalation buys | challenges.tex §9.3 item 5 |
| C11 | Same checks and retry budget | caveat | full | bracket across C5 to C10 | challenges.tex §9.3 item 5 |
| C12 | Reported metrics | training-eval | full | task success; calls and retries per completed task; escalation rate; valid but wrong outputs passing the checks; latency; monetary and energy cost per completed task; F separately | challenges.tex §9.3 item 5 |
| C13 | Test 1: non-inferiority | training-eval | full | (v) vs (i) on task success at margin delta; one-sided, task-clustered bootstrap | challenges.tex §9.3 item 5 |
| C14 | Test 2: cost per task | training-eval | full | (v) lower than every other configuration | challenges.tex §9.3 item 5 |
| C15 | H refuted for this workload | caveat | full | if either test fails | introduction.tex §1.3 |
| C16 | General rule rejected | caveat | full | fails on most of at least 3 pre-registered workloads with distinct call types | introduction.tex §1.3 |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C1 | C2 | call types selected | solid |
| C2 | C3 | estimates made before running | solid |
| C3 | C4 | fixed before running | solid |
| C4 | C11 | design applied to every configuration | solid |
| C11 | C12 | run end to end | solid |
| C12 | C13 | success data | solid |
| C12 | C14 | cost data | solid |
| C13 | C15 | fails | solid, red-tinted |
| C14 | C15 | fails | solid, red-tinted |
| C15 | C16 | across workloads | dashed |

## Annotations and equations

- Inside C4, three worked values as a mini-table: delta 2 points: about 7,700 tasks per arm; 5 points: 1,240; 10 points: 310. Note: "paired designs need fewer".
- Small note under C1: "a few hundred tasks can decide only a margin of about 10 points".

## Must not imply

- No results: this study has not been run.
- Configurations are not ranked; only (v) is highlighted because it is the one H prescribes.
- The checks are identical across configurations; do not draw checks only on the SLM rows.

## Open questions

- none
