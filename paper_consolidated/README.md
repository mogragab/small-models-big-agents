# Consolidated paper: SLMs as the Substrate of Agentic AI

This folder is the single consolidated paper built from the three predecessor
manuscripts (`../manuscript`, `../paper1_survey`, `../paper2_meta_analysis`). It
supersedes all three. The predecessors are left in place untouched.

- **`paper.tex`** — root file (LuaLaTeX + Biber).
- **`bibliography.bib`** — merged bibliography (189 entries; ~150 cited).
- **`figures/`** — 40 PDF plots from `../source/scripts/generate_figures_v2.py`
  (serif font to match the Springer body text, top-centre horizontal legends,
  `scale=3` export); 9 are embedded (6 in the body, 3 in Appendix B). Regenerate:
  `uv run python scripts/generate_figures_v2.py --output-dir ../paper_consolidated/figures --format pdf --title false` from `../source/`.
- **Two TikZ diagrams** are inline in the `.tex`: Fig. 2 (four-dimensional
  taxonomy, `taxonomy.tex`) and Fig. 8 (heterogeneous SLM--LLM agent,
  `agentic.tex`). They inherit the document font automatically.
- **`sources.md`** — citation ledger: newly verified entries, repaired inherited
  entries, and a list of inherited entries that still need verification before
  submission.
- **`sections/`** — modular body. New/rewritten: `introduction`, `background`
  (added LLM--SLM collaboration), `reported_performance` (replaces the old
  `methods`+`results`, reframed as reported values with provenance), `agentic`
  (new core section), `discussion`, `conclusion`, `challenges` (merged),
  `appendix_supplementary` (provenance framing).
- **`sections/appendix_ecosystem.tex`** + `partials/model_inventory_slm_by_year.tex`
  — the 125-model SLM inventory generated from `../source/merged_llm_database.json`
  (snapshot 2026-09-03; +18 entries added this session: Gemma 4, Granite 4.0,
  Falcon-H1, LFM2). The 238-model LLM inventory is generated but no longer
  included (out of scope for an SLM paper). Regenerate with
  `uv run python scripts/generate_model_tables.py --output-dir ../paper_consolidated/partials`
  from `../source/`.
  NOTE: `generate_model_tables.py` was edited to give the chronological inventory
  a booktabs style (no vertical rules); the other two table builders in that
  script still use the old `\hline` grid style if you re-enable them.

## Build

**Windows: double-click `build.bat`** (runs lualatex -> biber -> lualatex x2 and
opens the PDF; shows the log tail on error). `clean.bat` removes the aux files.

Or from a terminal:
```
latexmk -lualatex paper.tex
```
`latexmkrc` sets `$pdf_mode = 4` (LuaLaTeX) and `$bibtex = 'biber %O %B'`.

**In TeXStudio** the bibliography only resolves if the build actually runs Biber:
Options -> Configuration -> Build -> Default Compiler = *LuaLaTeX*, Default
Bibliography Tool = *Biber*, then press **F5** (Build & View), not F6. Simplest is
to just run `build.bat`.

## Status / open items before submission

1. **Bib** — cleaned 2026-09-03: 141 entries, all cited, no duplicates, no
   fabricated stubs (see `sources.md`). Remaining: confirm the ~50 bulk-added
   arXiv IDs and expand "and others" author lists with a reference manager.
2. Populate the per-figure provenance table in Appendix B
   (`app:provenance`) — currently a stub inherited from `paper2_meta_analysis`.
3. Regenerate the ecosystem inventory + figures once the model database is updated
   past March 2026 (Gemma 4, Qwen3.5, Granite 4.x are discussed in the prose but
   not yet in the generated tables/figures).
4. `sections/declarations.tex` — drafted, incl. the required generative-AI
   disclosure; fill the bracketed placeholders (funding, acknowledgements) and
   adjust CRediT roles.
5. Convert to the Springer `sn-jnl` class (BibTeX + `sn-basic.bst`; delete the
   `highlights` block; flatten `\input`s for final upload).

## Layout notes

- Tables use a uniform `\footnotesize` + `\adjustbox{max width=\linewidth}`
  (shrink-only, never magnify). Dropping the old `\resizebox{\textwidth}{!}`
  fixed the inconsistent font sizes.
- The former landscape zero-shot table was trimmed to portrait (7 columns);
  MATH/MT-Bench and the extended task set moved to Appendix B, Table~15.
- 47 pages (was 74): the intro's generated landscape overview tables and the
  238-row LLM inventory were removed.
