# Pre-delivery checklist

Work through this before delivering. The script catches structural problems and the
compiler catches syntax; this catches the ones that require reading.

## 1. Citation integrity (highest priority)

- [ ] `check_citations.py` runs clean: no orphan `\cite` keys, no uncited `.bib`
      entries, no entry missing from `sources.md`.
- [ ] Every `.bib` entry has a URL or DOI you personally retrieved this session.
- [ ] No DOI, volume, issue, or page range was inferred, pattern-matched, or recalled.
- [ ] Author names, spellings, and initials match the retrieved record — including
      diacritics and hyphenated surnames.
- [ ] Years match the version cited (published year, not the preprint year, unless you
      are citing the preprint).
- [ ] Preprints, working papers, and non-peer-reviewed reports are identified as such
      in the reference entry.
- [ ] Sources marked `abstract only` in the ledger are cited only for claims an
      abstract can support — no page-specific quotes or table values from them.
- [ ] Nothing cited from a Tier 4 source (Wikipedia, content farms, undated pages).
- [ ] No unfamiliar journal in the list without a predatory-flag check.

## 2. Claim–source alignment

Redrafting silently detaches citations from the sentences they were gathered for. For
each citation, confirm the source actually says what the sentence attributes to it.

- [ ] Every number in the text (rate, percentage, effect size, sample size, cost) is
      traceable to a ledger entry with the same value and the same units.
- [ ] Nothing has been strengthened in translation: a source that "suggests" is not
      cited as having "shown."
- [ ] No source is cited for a claim that appears only in *its* literature review
      rather than its own findings.
- [ ] Interpretive and argumentative sentences that are yours are *not* citation-dressed
      to look like someone else's.
- [ ] Contested claims present both sides with citations, rather than a one-sided
      literature.

## 3. Copyright and originality

- [ ] Every direct quotation is under ~15 words, in quotation marks, with a locator.
- [ ] At most one direct quotation per source, and few overall.
- [ ] No paragraph mirrors a source's sentence structure or ordering — paraphrase means
      rewritten, not word-substituted.
- [ ] No figure, table, or dataset reproduced from a copyrighted source; recreate from
      underlying data with a source note, or describe it instead.
- [ ] Abstracts of cited works are not reproduced.

## 4. Structure and completeness

- [ ] Every element the paper type requires is present (see `paper-architectures.md`).
- [ ] Section nesting is correct and no `\subsection` stands alone in its section;
      numbering itself is LaTeX's job — never hand-typed.
- [ ] Every `\label` has a `\ref` and vice versa; no `??` anywhere in the PDF.
- [ ] No heading stacked directly on another with no text between.
- [ ] Abstract describes the paper that exists, including its actual findings.
- [ ] Keywords (4–6) are terms someone would search, and are not all in the title.
- [ ] Tables and figures are numbered sequentially, referenced in the text before they
      appear, and captioned with source notes where applicable.
- [ ] The gap named in the Introduction is the gap the Discussion claims to address.
- [ ] Limitations are specific and Conclusion introduces nothing new.

## 5. Prose quality

- [ ] Read the first sentence of every body paragraph in sequence — they should form a
      coherent argument outline. If they read as "Several studies have examined…"
      repeatedly, the paragraphs lack claims.
- [ ] No section is a source-by-source walkthrough.
- [ ] Verb strength matches evidence strength; no "proves," no causal language from
      correlational data.
- [ ] Terminology is consistent; abbreviations defined at first use and then used.
- [ ] The machine-tell list in `academic-writing.md` has been swept for.
- [ ] Paragraph lengths vary; sections are within ~20% of their word budgets.
- [ ] Tense is consistent (past for what was done, present for established knowledge).

## 6. Build and formatting

- [ ] `latexmk -pdf` completes and the log is free of `Citation ... undefined`,
      `Reference ... undefined`, and `Empty thebibliography`.
- [ ] The rendered reference list matches the target style in
      `citation-styles.md` — ordering, punctuation, capitalisation, en-dashed ranges.
- [ ] No corporate author split into initials; no acronym lowercased (brace protection).
- [ ] Tables use `booktabs` rules, are referenced in the text before they appear, and
      have their notes below the rule.
- [ ] Rasterised pages checked by eye: title block, one table, the reference list.
- [ ] Word count taken from `detex paper.tex | wc -w`, not from the source file length.
- [ ] Build artefacts removed (`latexmk -c`) so the delivered directory is just
      `paper.tex`, `refs.bib`, `sources.md`.

## 7. Honesty pass

- [ ] No fabricated data, participants, results, or statistics anywhere.
- [ ] Any synthetic or illustrative content is labelled as such in the Methods, in the
      Limitations, and in a note under each affected table or figure.
- [ ] Any claim you could not source has been cut rather than left uncited.
- [ ] The delivery message tells the user: reference count, anything cited from abstract
      only, anything you had to hedge, anything you could not find support for, and any
      LaTeX package or class they need installed that a stock TeX Live lacks.

If a check fails and the fix would require a source you do not have, cut the claim. A
shorter honest paper beats a longer one with a soft spot in it.
