# Figure 1: The two-bound SLM definition

- **Figure ID:** fig01-slm-definition (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see that a model's active parameters per token (C1, compute) and its total parameters (C2, storage) are separate bounds, and how together they sort models into four classes.
- **Placement:** Main text §1.2.1 "The Operative Definition", after the paragraph on C1 and C2; `\label{fig:slm_definition}`.
- **Size:** full width, 139 mm, about 60 mm high.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/introduction.tex` §1.2.1 (C1, C2, the 119B/6.5B example, the threshold sensitivity sentence) and §1.2.2 (the four distinguished terms).
- `ACM-Journals/sections/taxonomy.tex` §3.2 (Qwen3-30B-A3B, Granite 4.0 Tiny as examples).
- `ACM-Journals/sections/supp_method.tex` "Count History" and `appendix_ecosystem.tex` "Generated Variant Inventory" (class counts 179, 30, 104, 119).
- `source/scripts/apply_inclusion_rules.py`: `classify()` and `decide()` (class logic).
- Style reference (inspiration only, do not copy): none.

## Layout

Single panel, a two-axis schematic (not a data plot). Horizontal axis: total parameters (C2, "storage envelope"); vertical axis: active parameters per token (C1, "compute envelope"). Both axes logarithmic in appearance but unlabelled with tick values except the single threshold mark "about 20B" on each axis. The threshold lines divide the plane into regions. Because active can never exceed total, the region above the diagonal (active > total) is greyed out and labelled "not possible". The lower-left region (both at or below about 20B) is the SLM region; the lower-right region (active at or below 20B, total above) is the small-active MoE region; the region with active above 20B is the LLM region. Dense models lie on the diagonal (active = total). A separate box beside the plot holds "Undisclosed size", which cannot be placed on the plane. Each region carries its class name and its count from the inventory.

A small legend strip under the plot states what each bound governs: C1 bounds per-token compute, latency, and energy; C2 bounds storage and download size (and resident memory only when every weight is kept in memory).

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | Total parameters (C2) | training-eval | full | horizontal axis; threshold mark "about 20B" | introduction.tex §1.2.1 |
| C2 | Active per token (C1) | training-eval | full | vertical axis; threshold mark "about 20B" | introduction.tex §1.2.1 |
| C3 | Dense models: active = total | caveat | full | the diagonal line | introduction.tex §1.2.1 ("coincide for dense models") |
| C4 | Not possible | raw-external | full | greyed region above the diagonal | apply_inclusion_rules.py `classify()` (active cannot exceed total) |
| C5 | SLM (179) | model | full | region: active and total both at or below about 20B | introduction.tex §1.2.2; appendix_ecosystem.tex |
| C6 | Small-active MoE (30) | model | full | region: active at or below about 20B, total above; secondary text "17 of 30 exceed 100B total" | introduction.tex §1.2.2 |
| C7 | LLM (104) | model | full | region: active above about 20B; secondary text "disclosed size" | supp_method.tex "Count History" |
| C8 | Undisclosed size (119) | raw-external | full | box outside the plane; secondary text "cannot be classified" | supp_method.tex "Inclusion Criteria" |
| C9 | Granite 4.0 Tiny | clean-data | full | example point in the SLM region (about 7B total, 1B active), below the diagonal | taxonomy.tex §3.2 |
| C10 | Qwen3-30B-A3B | clean-data | full | example point in the small-active MoE region (30B total, 3B active) | taxonomy.tex §3.2 |
| C11 | 119B total, 6.5B active | clean-data | full | example point far right in the small-active MoE region | introduction.tex §1.2.1 (Mistral Small 4 example) |
| C12 | C1: compute, latency, energy | caveat | full | legend strip item | introduction.tex §1.2.1 |
| C13 | C2: storage, download size | caveat | full | legend strip item; secondary text "resident memory only if all weights stay in memory" | introduction.tex §1.2.1 |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C12 | C2 | the vertical axis is the compute bound | dotted, thin |
| C13 | C1 | the horizontal axis is the storage bound | dotted, thin |

## Annotations and equations

- Threshold marks read "about 20B" on both axes; no other tick values.
- Small note beside the SLM region: "Compact model: SLM at or below about 3B total" as a sub-region in the lower-left corner (source: introduction.tex §1.2.2).

## Must not imply

- The diagonal "active = total" is one straight line of constant slope; on logarithmic axes it need not pass through the axis corner, so do not bend it to reach the corner.
- Do not write figure numbers ("Fig. N") in any label; the paper's numbering differs from the brief IDs.

- The example points are illustrative placements, not a scatter of the inventory; do not plot the 209 records.
- The 20B threshold is a convention, not a natural boundary; do not shade the boundary as if it were sharp in capability.
- Do not imply that small-active MoEs are SLMs or are deployable on phones.
- Do not imply that flash-offloaded models (stored in flash, experts swapped into memory) have resident memory equal to their total; C13's secondary text carries this.

## Open questions

- none
