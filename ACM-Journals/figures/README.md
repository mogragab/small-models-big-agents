# Figures

Place paper figures in this directory. The template's `\graphicspath` already
points here, so use filenames directly in `\includegraphics`.

Every `paper_*.png` here is generated, not hand-made. Do not edit them; edit the
generator and re-run it:

```
cd source
uv run python scripts/generate_figures_v2.py \
    --input merged_llm_database.json \
    --output-dir ../ACM-Journals/figures --format png
```

Notes on the output format:

- **PNG, not PDF.** Exported at `EXPORT_SCALE = 4` against ~780 px canvases,
  which gives roughly 3100-3600 px on the long edge, about 400-480 dpi at the
  printed column width. That is comfortably above the 300 dpi floor publishers
  set for raster artwork.
- **Libertinus Serif.** The figures set their text in the same family as the
  manuscript body. kaleido renders through headless Chrome and resolves fonts by
  family name from the system, so Libertinus must be installed as a *system*
  font, not only as a LaTeX package. If it is missing the figures silently fall
  back to another serif and will not match the page.
- **Palette.** Defined once in `PALETTE` in the generator and validated for
  colour-vision deficiency. Ordered quantities (year, parameter band, context
  bucket) use a single-hue light-to-dark ramp; only nominal quantities get
  distinct hues. Keep the TikZ colours at the top of
  `sections/taxonomy.tex` in step with it.
