---
name: academic-paper
description: "Research and write complete, publication-ready academic papers as LaTeX: a compiling .tex manuscript plus a .bib bibliography, with abstract, keywords, numbered sections, in-text citations, and references built only from real, verifiable literature from recognised publishers (Elsevier, Springer Nature, Wiley, IEEE, ACM, SAGE, Nature, arXiv). Works like a deep research run: literature search first, verified source ledger second, LaTeX manuscript third. Use whenever the user asks for a research paper, journal or conference article, literature or systematic review, thesis chapter, term or seminar paper, position paper, or white paper with citations, or says things like 'write me a paper on X', 'I need an academic article about Y with references', 'draft a publishable manuscript', 'LaTeX paper with BibTeX', or 'APA/IEEE format paper' - even if they never say 'academic' or 'LaTeX'. Also use to turn an existing draft, abstract, outline, or Word document into a properly cited, journal-formatted LaTeX manuscript."
---

# Academic paper: research → verify → write → LaTeX

You are producing a manuscript someone may submit, grade, or cite. Three things decide
whether that is a success: **the citations are real**, **the argument is genuinely built
from the literature you retrieved** rather than from memory dressed up in citation
clothes, and **the `.tex` actually compiles on the user's machine**. Everything below
serves those goals.

The single worst outcome is a beautiful paper with invented references. A fabricated
DOI can end a student's degree or a researcher's credibility. Treat the source ledger
and `refs.bib` (Phase 2) as the load-bearing part of this skill; the prose is downstream
of it.

The second worst outcome is a `.tex` file that throws errors when the user runs it. You
have LaTeX available — never hand over a manuscript you have not compiled yourself.

## Deliverables

`paper.tex` and `refs.bib`, plus `sources.md` so the user can audit every citation.
Compile locally to prove the build is clean, but **do not ship the PDF unless the user
asks** — they will build it in their own editor or on Overleaf.

## The non-negotiables

1. **Every `@entry` in `refs.bib` traces to a source you actually retrieved this
   session.** It must appear in `sources.md` with the URL or DOI you saw in a search
   result or fetched page. If it is not in the ledger, it does not go in the `.bib`.
2. **Never reconstruct bibliographic details from memory.** You may *recall* that a
   famous paper exists — that is a search lead, not a citation. Search for it, confirm
   the authors, year, venue, volume, pages and DOI against a retrieved record, then
   write the entry.
3. **Never invent DOIs, page ranges, volume numbers, or accession IDs.** If a field is
   genuinely unavailable, omit it — BibTeX degrades gracefully. A missing page range is
   a minor blemish; a wrong one is fraud.
4. **Never fabricate data, results, participants, or statistics.** See
   "Empirical papers and the data problem" below — there is always an honest route.
5. **Paraphrase; quote rarely and briefly.** Keep any direct quotation under ~15 words,
   in quotation marks with a locator, and at most one per source. Reproducing chunks of
   a copyrighted article is both a legal problem and bad scholarship. Synthesis in your
   own words is what a paper is *for*.
6. **The manuscript compiles clean.** No undefined citations, no missing references, no
   unresolved `??` in the output. Phase 5 is not optional.

## Tooling available

Both runtimes are present; use whichever fits the job.

- **LaTeX**: `pdflatex`, `xelatex`, `lualatex`, `latexmk`, `bibtex`, plus base TeX Live.
  Journal classes (`IEEEtran`, `elsarticle`, `acmart`, `apa7`, `llncs`), `apacite` and
  `biber` are one `apt-get` away — see `references/latex-build.md`.
- **Node + npm** for scripts that manipulate text or generate files.
  `scripts/new_paper.js` needs no dependencies; `npm i <pkg>` works if you want one.
- **Python via `uv`**: `uv run scripts/check_citations.py …` runs it directly, and
  `uv run --with <pkg> script.py` pulls dependencies without touching the system
  environment. Plain `python3` works too — the bundled scripts are stdlib-only.

## Workflow

Phase 0 intake → Phase 1 search plan → Phase 2 research + ledger + `.bib` →
Phase 3 architecture → Phase 4 LaTeX drafting → Phase 5 verification and compile →
Phase 6 deliver.

Do not skip Phase 2 to save time. A paper written before the research is a paper whose
citations were chosen to fit sentences that already existed — which is exactly how
fabrication happens.

---

### Phase 0 — Intake (keep it to one round)

You need six things. Infer what you can from the request, ask only for what genuinely
changes the output, and state your assumptions rather than interrogating the user.

| Parameter | Sensible default if unstated |
|---|---|
| Topic and angle | Narrow the user's topic to a defensible thesis yourself; show it to them |
| Paper type | Literature review / critical review (safest without user data) |
| Discipline and venue | Infer from topic; general scholarly register |
| Length | 5,000–7,000 words, ~30–45 references |
| Citation style | APA 7 (or IEEE for engineering/CS, Vancouver for medicine) |
| Document class | `article` + `natbib` with the matching `.bst`; a journal class only when the user names the venue |

Ask about at most two of these, and only when getting it wrong would waste the whole
effort — most often citation style and whether they have their own data. If the user
gave a detailed brief, ask nothing and start.

Announce the plan in two or three sentences ("I'll run a literature search across
~N sources, build a verified `refs.bib`, then draft a ~X-word LaTeX manuscript in
<style>"), then work. Do not narrate every search.

### Phase 1 — Decompose into a search plan

Break the topic into 5–9 research questions that together cover: the theoretical
foundation, the current state of the art, the methods used in the field, the empirical
findings and their disagreements, the criticisms and limitations, and the open gaps.
Your paper's argument will be built from the tension between what these turn up.

Write the plan down as a list of concrete queries before searching. Each query should
be different in *kind*, not just rephrased — a repeated query returns the same page.

### Phase 2 — Research, ledger, and bibliography

This is the Claude Research–style engine of the skill. Read
`references/research-protocol.md` for search tactics, source-quality tiers, publisher
whitelists, predatory-journal red flags, and how to extract usable evidence from an
abstract when the full text is paywalled.

Scale of effort, as a floor rather than a target:

| Paper length | Distinct searches | Sources fetched | References cited |
|---|---|---|---|
| 2,000–3,000 words | 10–15 | 8–12 | 15–20 |
| 5,000–7,000 words | 18–30 | 15–25 | 30–45 |
| 10,000+ words / review | 30–50 | 25–40 | 50–80 |

Work in two waves. **Wave one**: broad queries per research question; skim results;
fetch the ones that look load-bearing. **Wave two**: after you can see the shape of the
argument, hunt specifically for what is missing — the counter-evidence, the recent
2024–2026 work, the methodological critique, the numbers you want in a table. A paper
that only cites what came up first reads like a search results page.

**Write both files as you go, in the same edit.** When a source survives triage, append
its ledger entry to `sources.md` (schema in `references/research-protocol.md`) *and*
its BibTeX entry to `refs.bib`, sharing one citekey — `okonkwo2023attention`. The
ledger records what you will use it for in your own words; the `.bib` records the
metadata exactly as retrieved. Drafting later reads from these files, not from
recollection. Entry types, required fields, and the brace-protection rules that stop
BibTeX mangling names and acronyms are in `references/bibtex-guide.md`.

Stop researching when every branch of your intended argument has support and you have
found the main disagreements in the field. If a claim you wanted to make has no
support, cut the claim.

### Phase 3 — Architecture before prose

Read `references/paper-architectures.md` and pick the structure that matches the paper
type (empirical IMRaD, systematic review with PRISMA, narrative review, theoretical
paper, case study, position paper, thesis chapter).

Build the section tree to the depth the content earns:

- **`\subsection`** when a section contains two or more genuinely distinct
  sub-arguments that a reader would want to navigate between.
- **`\subsubsection`** when a subsection itself surveys parallel items — competing
  models, individual studies, separate datasets, distinct failure modes.
- **Stop there.** `\paragraph` as a fourth level belongs in a thesis, not a paper.
  Equally, do not manufacture a `2.1` with no `2.2`; a lone subsection means the split
  was artificial. LaTeX numbers sections for you, so the tree is the only thing you
  control — get it right here.

For each leaf node write, in the plan only: its purpose in the argument, its word
budget, its 2–4 key claims, and the citekeys supporting each claim. If a leaf has no
citekeys, you are about to write from memory — go back to Phase 2 or delete the node.

Show the user the outline with the reference count before drafting only if the paper is
long (>6,000 words) or the brief was vague; otherwise proceed and let them react to the
finished draft.

### Phase 4 — Drafting in LaTeX

Scaffold first, so you are writing into a preamble that is already known to compile:

```bash
node <skill>/scripts/new_paper.js --style apa --title "…" --author "…" --out paper.tex
```

It writes a `paper.tex` with the right class, packages, `\bibliographystyle`, title
block and section skeleton, an empty `refs.bib` if none exists, and a `.latexmkrc`.
Flags and the style→class→`.bst` mapping are in `references/latex-build.md`; read that
file before hand-rolling a preamble.

Then fill sections in order, in the file, so the argument accumulates. Read
`references/academic-writing.md` for register, paragraph construction, hedging,
signposting, how to synthesise rather than annotate, and the specific tells that make
prose read as machine-generated.

The rule that matters most: **paragraphs are organised around claims, not around
sources.** "\citet{smith2021} found X. \citet{jones2022} found Y." is an annotated
bibliography. "Three mechanisms have been proposed for X, of which the evidence most
strongly supports the second \citep{smith2021,chen2023}, though \citet{jones2022}
reports a null result under field conditions." is a paper.

LaTeX specifics that matter while drafting:

- `\citep{key}` for parenthetical, `\citet{key}` for narrative, `\citep[p.~47]{key}`
  with a locator, `\citep{a,b,c}` for several at once. Never type a citation by hand.
- One sentence per line, or wrap at ~90 characters. Diffs and your own re-reading
  both get easier, and it costs the output nothing.
- Escape `%`, `&`, `_`, `#`, `$` in prose. An unescaped `%` silently eats the rest of
  the line, which is the most common way a paragraph goes missing.
- `~` before citations and cross-references (`Section~\ref{sec:methods}`) to stop line
  breaks in ugly places; `--` for number ranges, `---` for em dashes.
- Tables with `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), never vertical rules.
  Label everything and reference it in the text before it appears.

Citation density: roughly one to three citations per body paragraph in review-heavy
sections, near zero in your own results and in your interpretive claims — where a
citation would falsely attribute your reasoning to someone else.

Word budgets keep sections proportionate. For a 6,000-word paper: abstract 200–250,
introduction ~800, background/review ~1,800, methods ~700, results ~900, discussion
~1,200, conclusion ~400. Scale proportionally; reviews shift mass into the body
sections and shrink methods to a search-strategy note. Count with
`detex paper.tex | wc -w` — it strips markup, so the number reflects prose, not source.

### Phase 5 — Verification and compile (do not skip)

Three passes, in this order. Each catches what the previous one cannot.

**1. Citation integrity.** Run the checker:

```bash
uv run <skill>/scripts/check_citations.py paper.tex refs.bib sources.md
```

It cross-checks that every `\cite*` key resolves to a `.bib` entry, every `.bib` entry
is cited at least once, every entry traces to the ledger by DOI or URL, and flags
duplicate keys, missing required fields, constructed-looking DOIs, Tier-4 domains, and
over-long quotations. Fix everything it flags as an error.

**2. Compile.** Build twice through BibTeX so cross-references resolve:

```bash
latexmk -pdf -interaction=nonstopmode paper.tex
```

Then read the log, not just the exit code: `Citation ... undefined`, `Reference ...
undefined`, `There were undefined references`, and `Empty thebibliography` all mean the
PDF is wrong even though the build "succeeded". `references/latex-build.md` has an error
triage table for the failures you will actually hit.

**3. The pass a script cannot do**, using `references/quality-checklist.md`: re-open
your ledger and confirm each citation still supports the sentence it is attached to
after redrafting, that no number in the text drifted from its source, that quotes are
short and marked, and that the abstract describes the paper you actually wrote. Then
rasterise a couple of pages (`pdftoppm -jpeg -r 100 paper.pdf page`) and *look* at the
title block, a table, and the reference list.

If any reference cannot be confirmed at this stage, remove it and the claim it
supported. Shipping a shorter, honest paper is always the right call.

### Phase 6 — Deliver

Present with `present_files`: `paper.tex` first, then `refs.bib`, then `sources.md`.
Delete the build artefacts (`.aux`, `.bbl`, `.blg`, `.log`, `.fls`, `.fdb_latexmk`,
`.out`, and the `.pdf` unless it was asked for) so the user gets a clean directory.

Summarise in a few lines: word count, section count, reference count, citation style,
document class, and the exact command to rebuild it. Flag anything you had to hedge,
any claim you could not source, and any paywalled source you cited from its abstract
only. If the paper needs a class that is not in a stock TeX Live installation, say so
and name the package the user needs.

---

## Empirical papers and the data problem

If the user asks for a paper with results and has no data, you cannot invent
participants, measurements, or p-values — that is fabrication, and it is worse in a
document typeset to look publishable. Offer one of these instead, and say which you
chose:

1. **Reframe as a review, meta-synthesis, or theoretical paper** — full IMRaD is not
   required for publication-quality scholarship. Usually the best answer.
2. **Secondary analysis of a real public dataset** — World Bank, Eurostat, WHO, NHANES,
   national statistics offices, Kaggle-hosted government data, replication packages.
   Retrieve the actual numbers, analyse them, report honestly.
3. **Use the user's own data** if they have it — then Methods and Results describe what
   they really did.
4. **A protocol or registered-report-style paper** — methods and analysis plan for a
   study not yet run, with Results replaced by expected outcomes. Clearly labelled.
5. **An explicitly labelled illustrative simulation**, with the synthetic origin stated
   in the Methods, in the Limitations, and in a `\floatfoot`-style note under every
   table.

Never silently produce fake results because option 1 felt less impressive.

## Reference files

- `references/research-protocol.md` — search strategy, source tiers, publisher and
  database whitelist, predatory-journal red flags, ledger schema, paywall tactics.
- `references/bibtex-guide.md` — `.bib` entry types and required fields, citekey
  convention, brace protection, accents, DOIs, and how entries break.
- `references/latex-build.md` — style→class→`.bst` mapping, preamble anatomy, journal
  classes, tables/figures/equations, the compile loop, error triage, anonymised
  submission.
- `references/citation-styles.md` — what each style's output should look like, so you
  can check the `.bst` rendered what you expected.
- `references/paper-architectures.md` — full section trees for each paper type.
- `references/academic-writing.md` — register, paragraph craft, synthesis patterns,
  hedging, and phrasing to avoid.
- `references/quality-checklist.md` — the pre-delivery pass.

## Scripts

- `scripts/new_paper.js` — Node, no dependencies. Scaffolds a compiling `paper.tex`
  preamble, `refs.bib`, and `.latexmkrc` for a given style or journal class.
- `scripts/check_citations.py` — stdlib Python (run with `uv run` or `python3`).
  `.tex` ↔ `.bib` ↔ `sources.md` consistency and hygiene check.
