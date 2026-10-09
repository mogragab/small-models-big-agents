# AI-generated scientific figures

Generated with the built-in AI image-generation tool from the seven original briefs in `../prompts/`, with AI edits to correct scientific connections, variable definitions, and labels. The code-generated figures and their Python generator were removed.

| Prompt | AI-generated PNG | Native dimensions |
|---|---|---|
| [fig01-slm-definition](../prompts/fig01-slm-definition.md) | [PNG](fig01-slm-definition.png) | 1905 × 825 px |
| [fig02-inventory-pipeline](../prompts/fig02-inventory-pipeline.md) | [PNG](fig02-inventory-pipeline.png) | 1791 × 878 px |
| [fig03-hypothesis-conditions](../prompts/fig03-hypothesis-conditions.md) | [PNG](fig03-hypothesis-conditions.png) | 1991 × 790 px |
| [fig04-breakeven-economics](../prompts/fig04-breakeven-economics.md) | [PNG](fig04-breakeven-economics.png) | 1933 × 813 px |
| [fig05-agent-architecture](../prompts/fig05-agent-architecture.md) | [PNG](fig05-agent-architecture.png) | 1905 × 825 px |
| [fig06-falsification-design](../prompts/fig06-falsification-design.md) | [PNG](fig06-falsification-design.png) | 1707 × 921 px |
| [fig07-taxonomy-facets](../prompts/fig07-taxonomy-facets.md) | [PNG](fig07-taxonomy-facets.png) | 1910 × 823 px |

Each final image was visually inspected. The copies in this directory match the AI tool's original files byte for byte. The original prompt files and pre-existing paper figures were retained.

These are raster PNGs at the image tool's native resolution, approximately 312–364 dpi when printed 139 mm wide. They do not reach the briefs' 600 dpi target at that width. They are not editable vector SVGs or vector PDFs.


## Edits after generation and placement in the paper (9 October 2026)

- `fig06-falsification-design.png`: typo "ower" corrected to "over" (pilot-estimates box); "Fig. 5" corrected to "Fig. 6".
- `fig03-hypothesis-conditions.png`: "Fig. 4" corrected to "Fig. 5" (break-even) and "Fig. 5" to "Fig. 6" (agent architecture), matching the paper's numbering.
- `fig02-inventory-pipeline.png`: "fig01" and the two "Fig. 1" stubs corrected to "Fig. 2" (the definition figure in the main text).
- Edits were made by redrawing only the affected glyphs in Libertinus Serif at the measured size, colour, and background; the git history holds the unedited originals.

Placed in the paper: fig02 (Supplement S2), fig03 (Section 1.3), fig04 (Section 7.2.2), fig05 (Section 7.5), fig06 (Section 9.3), fig07 (Section 3.1).
Not placed: `fig01-slm-definition.png` draws the active = total diagonal as a curve near the axis corner, which misstates the dense-model line; the paper keeps its TikZ version of that figure.
