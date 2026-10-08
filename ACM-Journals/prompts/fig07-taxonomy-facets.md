# Figure 7: The four primary facets of the taxonomy

- **Figure ID:** fig07-taxonomy-facets (matches the filename stem)
- **Status:** ready
- **Purpose:** The reader should see the four primary facets of the SLM taxonomy, the three categories within each, and representative models, and that the facets are separately observable but not orthogonal and assignment is multi-label.
- **Placement:** Main text §3.1 "The Scheme"; replaces the TikZ figure with `\label{fig:taxonomy}` (keep the label).
- **Size:** full width, 139 mm, about 60 mm high.
- **Language:** English
- **Outputs:** SVG, vector PDF, 600 dpi PNG

## Sources

- `ACM-Journals/sections/taxonomy.tex` §3.1 (TikZ code and caption of `fig:taxonomy`, which this brief replaces, and the text on non-orthogonality and multi-label assignment), §3.2, §3.3.
- `ACM-Journals/sections/supp_tables.tex` `tab:taxonomy_summary` (tabular form of the same content).
- Style reference (inspiration only, do not copy): none.

## Layout

A two-by-two grid of panels: Architecture (top left), Training strategy (top right), Modality (bottom left), Application domain (bottom right). Each panel lists three categories, each with a short defining phrase and a line of representative models in a lighter style. Between panels, thin dotted links mark two documented entanglements: Training strategy to Architecture ("pruning plus distillation needs a dense teacher") and Modality to Architecture ("vision encoder"). A footer strip reads "Separately observable, not orthogonal; a model may carry several categories per facet".

## Components

| ID | Label (exact text) | Role | Shown as | Details | Source |
|---|---|---|---|---|---|
| C1 | Architecture | model | full | categories: Dense transformer (GQA, RoPE, gated FFN; Phi-4-mini, Qwen3, SmolLM3, Gemma 3); Mixture-of-experts (sparse activation; Granite 4.0 Tiny; small-active MoE: Mixtral, Qwen3-30B-A3B); Hybrid SSM/attention (linear-time; Falcon-H1, Granite 4.0, Nemotron Nano 2) | taxonomy.tex fig:taxonomy |
| C2 | Training strategy | training-eval | full | categories: From scratch (curated or synthetic data; Phi, Qwen3, SmolLM3); Distillation (from a larger teacher; Gemma 3/4, DeepSeek-R1-Distill, Phi-4-mini-reasoning); Pruning + distillation (shrink a larger model; Minitron, Sheared-LLaMA, Llama 3.2 1B/3B) | taxonomy.tex fig:taxonomy; §3.3 |
| C3 | Modality | tokens | full | categories: Text-only (majority of SLMs; Mistral 7B, SmolLM3, Qwen3); Vision-language (image encoder added; Phi-3-vision, Gemma 3 4B and above, PaliGemma); Text + vision + audio (one sub-10B model; Gemma 3n, Gemma 4, Voxtral Mini for audio) | taxonomy.tex fig:taxonomy |
| C4 | Application domain | clean-data | full | categories: General-purpose (Phi, Gemma, Llama, Qwen, Mistral); Healthcare (Meerkat, OptimCLM encoders); Code / multilingual (StarCoder2, DeepSeek-Coder, Aya 23) | taxonomy.tex fig:taxonomy |
| C5 | Not orthogonal, multi-label | caveat | full | footer strip | taxonomy.tex §3.1 |

## Connections

| From | To | Meaning | Style |
|---|---|---|---|
| C2 | C1 | pruning plus distillation needs a dense teacher | dotted |
| C3 | C1 | vision encoder ties modality to architecture | dotted |

## Annotations and equations

- Use the category and model names exactly as listed; italicise the representative models.
- Role mapping: these facets are not ML pipeline stages; the roles only give each panel a distinct, consistent hue.

## Must not imply

- Not a partition: categories are not mutually exclusive and the panels are not exhaustive lists.
- No counts per category: the inventory does not assign every facet to every variant.
- Healthcare examples are not deployment evidence.

## Open questions

- none
