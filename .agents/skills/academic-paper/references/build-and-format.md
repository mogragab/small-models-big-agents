# Building and formatting the LaTeX manuscript

## Required deliverables

Create three auditable source files:

- `paper.tex` — the complete manuscript.
- `references.bib` — every cited bibliographic record, with stable citation keys.
- `sources.md` — the retrieval ledger, including the URL or DOI actually checked and
  the claims supported by each source.

Create `paper.pdf` only after the LaTeX sources pass citation checks and compile cleanly.
Do not create a DOCX unless the user separately requests one.

## Default LaTeX structure

Follow an official journal or conference template when the user supplies or names one.
Otherwise use a portable article layout and BibLaTeX/Biber:

```latex
\documentclass[11pt]{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{csquotes}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}
\usepackage[backend=biber,style=authoryear,sorting=nyt]{biblatex}
\addbibresource{references.bib}

\title{Manuscript title}
\author{Author name}
\date{}

\begin{document}
\maketitle

\begin{abstract}
Abstract text.
\end{abstract}

\noindent\textbf{Keywords:} keyword one; keyword two; keyword three

\section{Introduction}
Narrative citation: \textcite{smith2024reliable}. Parenthetical citation:
\parencite{smith2024reliable}.

\printbibliography
\end{document}
```

Use `style=apa` for APA, `style=ieee` for IEEE, `style=numeric-comp` for Vancouver,
or an appropriate `authoryear` style for general/Harvard work. A venue template may
instead require classic BibTeX commands such as `\bibliographystyle{IEEEtran}` and
`\bibliography{references}`; follow the venue rather than forcing BibLaTeX.

## BibTeX records

Use readable, stable keys such as `surname2024keyword`. Every entry must contain only
metadata verified from a retrieved source. Include a DOI when one exists, otherwise a
URL. Do not reconstruct page ranges, issue numbers, or DOIs from memory.

```bibtex
@article{smith2024reliable,
  author       = {Smith, Jane},
  title        = {Reliable Automation in Scholarly Workflows},
  journaltitle = {Journal of Reproducible Research},
  year         = {2024},
  volume       = {12},
  number       = {3},
  pages        = {101--119},
  doi          = {10.1234/example.2024.001}
}
```

Escape LaTeX special characters in field values. Preserve meaningful capitalization
with braces sparingly, for example `{GPU}` or `{COVID-19}`. Do not wrap entire titles
in extra braces merely to force capitalization.

## Citation verification

Run all Python through `uv`:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'academic-paper-uv-cache'
uv run --no-project <skill-root>/scripts/check_citations.py paper.tex references.bib sources.md
```

Fix every error before delivery. The checker validates citation-key resolution,
uncited and duplicate BibTeX entries, source-ledger coverage, locator hygiene, and the
presence of a bibliography resource command.

## Compilation

Prefer `latexmk` when available:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```

For BibLaTeX/Biber without `latexmk`:

```powershell
lualatex -interaction=nonstopmode -halt-on-error paper.tex
biber paper
lualatex -interaction=nonstopmode -halt-on-error paper.tex
lualatex -interaction=nonstopmode -halt-on-error paper.tex
```

For a classic BibTeX venue template, replace `biber paper` with `bibtex paper`. Run the
final LaTeX pass until cross-references stabilize. Search the log for `undefined`,
`citation`, `reference`, `error`, and overfull boxes; fix material problems.

If no compatible LaTeX toolchain is installed, do not download one unless the user
authorizes it. Deliver the checked `.tex` and `.bib` sources and disclose that PDF
compilation was not performed.

## Visual verification

When compilation succeeds, render the PDF and inspect representative pages. Check:

1. Title, author block, abstract, and keywords.
2. Heading hierarchy and page breaks.
3. Tables and figures for clipping, illegible text, and missing captions.
4. In-text citations and the generated bibliography.
5. Widows, orphans, overfull boxes, and malformed characters.

## Submission-specific formatting

Check the target venue's current author instructions for its class file, anonymity,
word limits, line numbering, bibliography backend/style, figure placement, and
supplementary-material rules. For double-blind review, remove identifying author data
and rewrite self-references neutrally. State which venue conventions were applied.
