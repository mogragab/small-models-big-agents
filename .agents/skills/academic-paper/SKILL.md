---
name: academic-paper
description: "Research, verify, draft, and format scholarly manuscripts as LaTeX with BibTeX references, a source ledger, and checked citations. Use for journal or conference papers, literature or systematic reviews, thesis chapters, seminar papers, position papers, and substantial academic revisions. Do not use for casual summaries or requests to invent empirical results."
---

# Academic paper: research → verify → write → publish-ready

You are producing a manuscript someone may submit, grade, or cite. Two things decide
whether that is a success: **the citations are real**, and **the argument is genuinely
built from the literature you retrieved** rather than from memory dressed up in
citation clothes. Everything below serves those two goals.

The single worst outcome is a beautiful paper with invented references. A fabricated
DOI can end a student's degree or a researcher's credibility. Treat the source ledger
(Phase 2) as the load-bearing part of this skill; the prose is downstream of it.

## The non-negotiables

1. **Every reference traces to a source you actually retrieved this session.** It must
   appear in `sources.md` with the URL or DOI you saw in a search result or fetched
   page. If it is not in the ledger, it does not go in `references.bib`.
2. **Never reconstruct bibliographic details from memory.** You may *recall* that a
   famous paper exists — that is a search lead, not a citation. Search for it, confirm
   the authors, year, venue, volume, pages and DOI against a retrieved record, then
   cite it.
3. **Never invent DOIs, page ranges, volume numbers, or accession IDs.** If a field is
   genuinely unavailable, omit it in the way the citation style permits. A missing page
   range is a minor blemish; a wrong one is fraud.
4. **Never fabricate data, results, participants, or statistics.** See
   "Empirical papers and the data problem" below — there is always an honest route.
5. **Paraphrase; quote rarely and briefly.** Keep any direct quotation under ~15 words,
   in quotation marks with a locator, and at most one per source. Reproducing chunks of
   a copyrighted article is both a legal problem and bad scholarship. Synthesis in your
   own words is what a paper is *for*.

## Workflow

Phase 0 intake → Phase 1 search plan → Phase 2 research + ledger → Phase 3 architecture
→ Phase 4 drafting → Phase 5 verification → Phase 6 build and deliver.

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
| Output format | `paper.tex` + `references.bib` + `sources.md` |

Ask about at most two of these, and only when getting it wrong would waste the whole
effort — most often citation style and whether they have their own data. If the user
gave a detailed brief, ask nothing and start.

Announce the plan in two or three sentences ("I'll run a literature search across
~N sources, build a verified reference ledger, then draft a ~X-word paper in <style>"),
then work. Do not narrate every search.

### Phase 1 — Decompose into a search plan

Break the topic into 5–9 research questions that together cover: the theoretical
foundation, the current state of the art, the methods used in the field, the empirical
findings and their disagreements, the criticisms and limitations, and the open gaps.
Your paper's argument will be built from the tension between what these turn up.

Write the plan down as a list of concrete queries before searching. Each query should
be different in *kind*, not just rephrased — a repeated query returns the same page.

### Phase 2 — Research and build the source ledger

Use this research workflow. Read
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

Maintain `sources.md` continuously (schema in `references/research-protocol.md`). Each
entry records full bibliographic metadata, the URL/DOI you actually saw, source tier,
and — critically — the specific claims and figures you intend to use from it, in your
own words. Drafting later reads from this file, not from recollection.

Stop researching when every branch of your intended argument has support and you have
found the main disagreements in the field. If a claim you wanted to make has no
support, cut the claim.

### Phase 3 — Architecture before prose

Read `references/paper-architectures.md` and pick the structure that matches the paper
type (empirical IMRaD, systematic review with PRISMA, narrative review, theoretical
paper, case study, position paper, thesis chapter).

Build the section tree to the depth the content earns:

- **Level 2 (`2.1`)** when a section contains two or more genuinely distinct
  sub-arguments that a reader would want to navigate between.
- **Level 3 (`2.1.3`)** when a subsection itself surveys parallel items — competing
  models, individual studies, separate datasets, distinct failure modes.
- **Stop there.** Level 4 belongs in a thesis, not a paper. Equally, do not manufacture
  a `2.1` with no `2.2`; a lone subsection means the split was artificial.

For each leaf node write, in the plan only: its purpose in the argument, its word
budget, its 2–4 key claims, and the source IDs supporting each claim. If a leaf has no
source IDs, you are about to write from memory — go back to Phase 2 or delete the node.

Show the user the outline with the reference count before drafting only if the paper is
long (>6,000 words) or the brief was vague; otherwise proceed and let them react to the
finished draft.

### Phase 4 — Drafting

Write directly to `paper.tex` section by section, in order, so the argument accumulates.
Keep prose readable in source form and use stable citation keys from `references.bib`.
Read `references/academic-writing.md` for register, paragraph construction, hedging,
signposting, how to synthesise rather than annotate, and the specific tells that make
prose read as machine-generated.

The rule that matters most: **paragraphs are organised around claims, not around
sources.** "Smith (2021) found X. Jones (2022) found Y. Chen (2023) found Z." is an
annotated bibliography. "Three mechanisms have been proposed for X, of which the
evidence most strongly supports the second (Smith, 2021; Chen, 2023), though Jones
(2022) reports a null result under field conditions." is a paper.

Citation density: roughly one to three citations per body paragraph in review-heavy
sections, near zero in your own results and in your interpretive claims — where a
citation would falsely attribute your reasoning to someone else.

Word budgets keep sections proportionate. For a 6,000-word paper: abstract 200–250,
introduction ~800, background/review ~1,800, methods ~700, results ~900, discussion
~1,200, conclusion ~400. Scale proportionally; note that reviews shift mass into the
body sections and shrink methods to a search-strategy note.

### Phase 5 — Verification (do not skip; this is where fabrication gets caught)

Run the checker through `uv` — it cross-checks that every LaTeX citation key resolves
to a BibTeX entry, every BibTeX entry is cited, and every reference locator appears in
the source ledger. Fix everything it flags.

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'academic-paper-uv-cache'
uv run --no-project <skill-root>/scripts/check_citations.py paper.tex references.bib sources.md
```

Use the platform's native path syntax. Do not assume a Linux home directory. If `uv`
is unavailable, report that requirement instead of silently skipping citation checks.

Then do the pass a script cannot do, using `references/quality-checklist.md`:
re-open your ledger and confirm each citation still supports the sentence it is attached
to after redrafting, that no number in the text drifted from its source, that quotes are
short and marked, and that the abstract describes the paper you actually wrote.

If any reference cannot be confirmed at this stage, remove it and the claim it
supported. Shipping a shorter, honest paper is always the right call.

### Phase 6 — Build and deliver

Produce a self-contained `paper.tex` and a separate `references.bib`. Never hand-write
the reference list inside the `.tex` file. Follow a user-supplied venue template when
available; otherwise use `biblatex` with `biber` and an appropriate style. Read
`references/build-and-format.md` for the LaTeX structure, citation commands, build
sequence, and portability rules.

If a LaTeX toolchain is available, compile with `latexmk`, or run the documented
LaTeX/Biber sequence. Treat compiler errors, missing citations, and undefined references
as blockers. If no compiler is installed, still deliver valid `.tex` and `.bib` sources
and clearly state that PDF compilation was not performed.

When a PDF is produced, use the available PDF rendering capability for visual QA.
Inspect the title page, headings, tables or figures, page breaks, and bibliography.

Deliver clickable links to `paper.tex`, `references.bib`, and `sources.md`, followed by
`paper.pdf` only when compilation succeeded. Summarise the word count, section count,
reference count, and citation style. Flag anything you had to hedge, any unsupported
claim you removed, and any paywalled source cited from its abstract only.

---

## Empirical papers and the data problem

If the user asks for a paper with results and has no data, you cannot invent
participants, measurements, or p-values — that is fabrication, and it is worse in a
document formatted to look publishable. Offer one of these instead, and say which you
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
   in the Methods, in the Limitations, and in a note under every table.

Never silently produce fake results because option 1 felt less impressive.

## Reference files

- `references/research-protocol.md` — search strategy, source tiers, publisher and
  database whitelist, predatory-journal red flags, ledger schema, paywall tactics.
- `references/citation-styles.md` — exact in-text and reference formats with worked
  examples for APA 7, IEEE, MLA 9, Chicago (both systems), Vancouver, Harvard.
- `references/paper-architectures.md` — full section trees for each paper type.
- `references/academic-writing.md` — register, paragraph craft, synthesis patterns,
  hedging, and phrasing to avoid.
- `references/quality-checklist.md` — the pre-delivery pass.
- `references/build-and-format.md` — LaTeX/BibTeX structure, compilation, portability,
  formatting norms, and PDF verification.

## Scripts

- `scripts/check_citations.py` — LaTeX/BibTeX/source-ledger consistency check; run with `uv`.
