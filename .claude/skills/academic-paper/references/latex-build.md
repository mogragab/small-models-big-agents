# LaTeX: classes, preamble, build, and error triage

## Contents
1. Style → class → `.bst` mapping
2. Scaffolding with `new_paper.js`
3. Preamble anatomy (and what not to add)
4. Journal classes and how to install them
5. Structure, tables, figures, equations
6. The compile loop
7. Error triage
8. Anonymised submission and journal requirements
9. When the user wants something other than `.tex`

---

## 1. Style → class → `.bst` mapping

The citation style dictates three things at once: the `.bst`, whether `natbib` runs in
author–date or numeric mode, and which `\cite` commands are meaningful.

| Style | Class | `\bibliographystyle` | natbib option | In-text |
|---|---|---|---|---|
| APA 7 | `article` (or `apa7`) | `apacite` → `apalike` | `authoryear,round`, or `\usepackage[natbibapa]{apacite}` | `\citep`, `\citet` |
| Harvard | `article` | `agsm` → `apalike` | `authoryear,round` | `\citep`, `\citet` |
| Chicago author–date | `article` | `chicago` → `apalike` | `authoryear` | `\citep`, `\citet` |
| MLA 9 | `article` | `apalike` (approximate) | `authoryear` | `\citep`, `\citet` |
| IEEE | `IEEEtran` → `article` | `IEEEtran` → `ieeetr` | `numbers,sort&compress` | `\cite` |
| Vancouver | `article` | `vancouver` → `unsrtnat` | `numbers,sort&compress` | `\cite` |

`→` means "use the first if installed, else fall back". `new_paper.js` does this probe
for you with `kpsewhich` and tells you what it picked.

Two consequences worth internalising:

- **`apacite` needs its `natbibapa` option**: `\usepackage[natbibapa]{apacite}`. Loaded
  bare, it defines `\cite` and `\citeA` but *not* `\citep`/`\citet`, and the build dies
  with `Undefined control sequence` on your first citation. With `natbibapa` it loads
  `natbib` itself, so `\citep`/`\citet` work and the output is true APA. Do not also load
  `natbib` by hand — that is the `Command \citet already defined` error.
- **In numeric styles, never hand-number anything.** `\cite{a,b,c}` with
  `sort&compress` renders `[1]–[3]` on its own. Typing `[3]` as literal text produces a
  number that stops matching the moment a reference is added.

## 2. Scaffolding with `new_paper.js`

```bash
node <skill>/scripts/new_paper.js \
  --style apa --title "Grid-Scale Storage Economics" \
  --author "A. N. Okonkwo" --affil "University of Example" \
  --keywords "energy storage; levelised cost; curtailment" \
  --sections "Introduction,Literature Review,Methods,Findings,Discussion,Conclusion" \
  --out paper.tex
```

| Flag | Effect |
|---|---|
| `--style apa\|ieee\|vancouver\|mla\|chicago\|harvard\|plain` | class, `.bst`, natbib mode, font size, spacing |
| `--class`, `--bst` | override either independently |
| `--columns 2`, `--spacing`, `--fontsize` | override the preset |
| `--sections "A,B,C"` | section skeleton (default IMRaD) |
| `--toc`, `--lineno`, `--anonymous` | contents page, line numbers, double-blind |
| `--bib refs.bib`, `--out paper.tex`, `--force` | file names; overwrite |

It also writes `refs.bib` (if absent) and `.latexmkrc`. Read the generated header
comments — they record which class and `.bst` were chosen and why.

## 3. Preamble anatomy (and what not to add)

A preamble that compiles everywhere is short. The scaffold produces roughly:

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}                  % Times-alike
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{threeparttable}
\usepackage{caption}
\usepackage{microtype}
\usepackage[authoryear,round]{natbib}
\usepackage[hidelinks]{hyperref}       % load last
\doublespacing
\bibliographystyle{apalike}
```

Rules that save debugging time:

- **`hyperref` loads last** (before `cleveref` only). Loaded early it gets overwritten by
  other packages and cross-references break in ways that look unrelated.
- **Do not add packages speculatively.** Each one is a chance the user's TeX Live lacks
  it. If you do not use `tikz`, do not load it.
- **`inputenc`/`fontenc` are harmless on modern TeX Live and required on older ones**, so
  keep them for `pdflatex`. If you switch to `xelatex`/`lualatex`, drop `inputenc` and
  use `fontspec` instead.
- **Redefining section formatting is almost always a mistake.** The class knows what the
  style wants; `titlesec` tinkering is how a manuscript stops matching its own template.

## 4. Journal classes and how to install them

Base TeX Live carries `article`, `natbib`, and the `apalike`/`plainnat`/`unsrtnat`/
`ieeetr` bundle. Journal classes and `apacite` come from two extra packages:

```bash
apt-get install -y --no-install-recommends texlive-publishers texlive-bibtex-extra
# adds IEEEtran, elsarticle, acmart, apa7, llncs, revtex, apacite, vancouver, agsm, biber
```

Run this when the user names a venue. If it fails (no network, no permissions), fall
back to `article` with the closest `.bst`, and **say so in the delivery message** — the
user needs to know the file will look different once they build it with the real class.

| Venue | Class | Notes |
|---|---|---|
| IEEE journals and conferences | `IEEEtran` | `\documentclass[conference]{IEEEtran}`; ships its own `IEEEtran.bst` |
| Elsevier journals | `elsarticle` | `\begin{frontmatter}` block instead of `\maketitle`; `elsarticle-harv` or `-num` |
| ACM conferences | `acmart` | `\documentclass[sigconf]{acmart}`; ACM's own metadata commands |
| Springer LNCS | `llncs` | `\institute{}`, `splncs04.bst` |
| APA-formatted manuscripts | `apa7` | `\documentclass[man,12pt]{apa7}`; uses `apacite` |
| Physics (APS/AIP) | `revtex4-2` | `\documentclass[aps,prl,twocolumn]{revtex4-2}` |

These classes replace parts of the standard title block. Do not mix a journal class with
the `article` title block the scaffold generates — regenerate with `--class` instead.

## 5. Structure, tables, figures, equations

**Sections.** `\section` / `\subsection` / `\subsubsection`, each with a `\label`
(`sec:methods`). Reference them as `Section~\ref{sec:methods}`. Never write section
numbers by hand — LaTeX renumbers, your text will not.

**Tables.** `booktabs` rules only, caption above, notes below via `threeparttable`:

```latex
\begin{table}[htbp]
\centering
\begin{threeparttable}
\caption{Levelised cost of storage by market, 2018--2025.}
\label{tab:lcos}
\begin{tabular}{lrrr}
\toprule
Market & 2018 (USD/MWh) & 2025 (USD/MWh) & Change \\
\midrule
Germany & 187 & 116 & $-38\%$ \\
Japan   & 204 & 141 & $-31\%$ \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]\small
\item \textit{Note.} Compiled from \citet{okonkwo2023attention} and \citet{iea2025weo}.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

Vertical rules and `\hline` are the visual signature of a table built by someone who has
not read a journal recently. Use `$-38\%$` or `\%` — a bare `%` starts a comment.

**Figures.** `\includegraphics[width=\linewidth]{fig1.pdf}` with caption *below* and a
`\label`. If the figure file does not exist the build fails, so either generate the
asset (matplotlib via `uv run --with matplotlib`, or a `pgfplots` block) or leave the
figure out. Never reproduce a copyrighted figure from a source; recreate it from the
underlying numbers with a source note, or describe it in prose.

**Equations.** `\begin{equation}...\label{eq:x}\end{equation}` for numbered,
`\[ ... \]` for unnumbered display, `$...$` inline. `amsmath` gives you `align` for
multi-line derivations.

**Word count.** `detex paper.tex | wc -w` strips markup and counts prose. `texcount` is
better if installed. The `\wordcount` of the source file is not the word count of the
paper.

## 6. The compile loop

```bash
latexmk -pdf -interaction=nonstopmode paper.tex
```

`latexmk` runs `pdflatex → bibtex → pdflatex → pdflatex` as many times as needed. Doing
it by hand is the same thing spelled longer, and one pass short of correct is the usual
reason a reference list comes out empty.

**Read the log, not the exit code.** These lines mean the PDF is wrong even when the
build "succeeds":

```bash
grep -Ei "undefined|Citation|Empty thebibliography|multiply defined" paper.log
```

| Log line | Meaning |
|---|---|
| `Citation 'x' undefined` | key is cited but not in the `.bib`, or BibTeX has not run yet |
| `There were undefined references` | run again; if it persists, the key is genuinely missing |
| `Empty thebibliography environment` | nothing was cited, or the `.bib` path is wrong |
| `LaTeX Warning: Reference 'tab:x' undefined` | `\ref` without a matching `\label` |
| `Overfull \hbox` | cosmetic; only worth fixing if text runs into the margin |

Clean up afterwards: `latexmk -c` removes `.aux`, `.log`, `.blg`, `.fls`, `.fdb_latexmk`
but keeps the PDF; `latexmk -C` removes the PDF too.

**Look at the output at least once**, especially the title block, one table, and the
reference list:

```bash
pdftoppm -jpeg -r 100 paper.pdf page   # then view page-1.jpg, page-N.jpg
```

## 7. Error triage

Ordered by how often they actually happen.

| Symptom | Cause and fix |
|---|---|
| A paragraph vanished | Unescaped `%` ate the rest of the line. Write `\%`. |
| `Undefined control sequence` | Package not loaded, or a typo'd command. Check the line number in the log — LaTeX reports the line where it noticed, sometimes just after the cause. |
| `Missing $ inserted` | A `_`, `^`, `&` or `#` used in prose. Escape as `\_`, `\^{}`, `\&`, `\#`. |
| Reference list empty | BibTeX did not run (use `latexmk`), `\bibliography{refs}` names the wrong file (no `.bib` extension), or nothing is cited. |
| `I found no \citation commands` | The `.aux` predates your citations; delete `.aux` and rebuild. |
| `File 'X.sty' not found` | Missing package. Install via `apt-get install texlive-…`, or remove the dependency. |
| Author–date citations print as numbers | `natbib` loaded without `authoryear`, or a numeric `.bst`. |
| `Command \citet already defined` | `natbib` loaded alongside `apacite[natbibapa]`. Drop the bare `natbib`. |
| `Undefined control sequence` on `\citep` | `apacite` loaded without `natbibapa`. |
| Names appear as "OKONKWO, A." or acronyms lowercased | Brace protection — see `bibtex-guide.md`. |
| `!pdfTeX error: cannot find image` | Figure file missing; generate it or drop the figure. |
| Build hangs | A `\begin{...}` without its `\end{...}`; `-interaction=nonstopmode` turns the hang into an error you can read. |

If a single stubborn error is blocking delivery, bisect: comment out half the body,
rebuild, and narrow down. Faster than staring at the log.

## 8. Anonymised submission and journal requirements

For double-blind review: `--anonymous` drops the author block; also remove funding and
acknowledgements, rewrite self-citations in the third person ("Okonkwo (2023) showed",
not "our earlier work"), and check that `\thanks`, PDF metadata, and file names carry no
names.

If the user names a target journal, check its author guidelines for line spacing,
line numbering (`--lineno`), figure placement (inline vs. `endfloat` at the end),
word limits, structured-abstract requirements, and whether they supply their own class
file. State in the delivery message which conventions you applied so the user can
adjust.

## 9. When the user wants something other than `.tex`

- **PDF**: only when asked. `latexmk -pdf` produces it; deliver it alongside the source.
- **Word**: `pandoc paper.tex --bibliography=refs.bib --citeproc -o paper.docx`.
  Formatting fidelity is partial — say so rather than implying it is submission-ready.
- **Overleaf**: the `.tex` + `.bib` pair uploads directly; no changes needed. Worth
  mentioning in the delivery message, since it is where most users will build it.
- **arXiv**: wants the `.tex`, the `.bbl` (not the `.bib`), and figure files. Run the
  build first so a `.bbl` exists, and include it.
