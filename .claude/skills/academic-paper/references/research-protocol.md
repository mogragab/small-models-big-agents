# Research protocol

How to run the literature search so that the reference list is real, current, and
actually load-bearing for the argument.

## Contents
1. Search tactics
2. Where to search
3. Source quality tiers
4. Recognised publishers and databases
5. Predatory and unreliable source red flags
6. The source ledger
7. Paywalls, preprints, and what you may cite from an abstract
8. Gap analysis (wave two)

---

## 1. Search tactics

**Vary the *kind* of query, not just the wording.** Re-running a rephrased query returns
the same ten results. Each of these angles surfaces a different literature:

| Angle | Example query shape |
|---|---|
| Canonical/theoretical | `<concept> theoretical framework review` |
| State of the art | `<topic> 2025 systematic review` |
| Methods | `<topic> methodology comparison` |
| Quantitative findings | `<topic> meta-analysis effect size` |
| Counter-evidence | `<claim> criticism limitations null result` |
| Applied/sectoral | `<topic> <industry or country> case study` |
| Venue-targeted | `<topic> site:nature.com` / `<topic> IEEE Transactions` |
| Repository-targeted | `<topic> arXiv 2026`, `<topic> PubMed` |
| Data | `<topic> dataset World Bank OECD statistics` |

Keep queries 3–8 words. Start broad, then narrow using the specific terminology the
first results reveal — fields have their own vocabulary, and picking it up mid-search
is what separates a real literature search from a keyword crawl.

**Fetch, don't just skim snippets.** Search snippets are two sentences of marketing.
Fetch the landing page or abstract page of anything you intend to cite: that is where
the year, volume, issue, page range and DOI actually live. Citing from a snippet is how
volume numbers get invented.

**Prefer the publisher of record.** If a paper appears on ResearchGate, a course page,
and doi.org, cite the DOI version and fetch that one.

**Date discipline.** Today is in 2026. "Recent literature" means roughly 2023–2026.
Search explicitly for recent work (`2025`, `2026`) — the default ranking favours older,
more-linked pages, and a paper whose newest citation is from 2021 reads as stale.
Foundational work of any age is fine and expected; the balance is what matters, roughly
60–75% from the last five years for an active field.

## 2. Where to search

Open-access and metadata sources that respond well to search and fetch:

- **Semantic Scholar** (`semanticscholar.org`) — good metadata, abstracts, citation counts
- **PubMed / PubMed Central** — biomedical, free abstracts, full text on PMC
- **arXiv / bioRxiv / medRxiv / SSRN** — preprints (label them as such)
- **DOAJ**, **CORE**, **OpenAlex**, **Crossref** — open-access indexes and DOI metadata
- **PLOS ONE**, **Scientific Reports**, **Frontiers**, **MDPI** — open access, mixed
  quality; check the individual journal, not just the publisher
- **Publisher sites** — sciencedirect.com, link.springer.com, onlinelibrary.wiley.com,
  tandfonline.com, journals.sagepub.com, ieeexplore.ieee.org, dl.acm.org,
  academic.oup.com, cambridge.org, nature.com, science.org
- **Institutional and governmental** — WHO, OECD, World Bank, IMF, Eurostat, national
  statistics offices, NIST, EPA, IPCC, IEA, national academies
- **Standards and legal** — ISO, IEEE Standards, EUR-Lex, national legislation portals

Google Scholar itself often blocks automated fetching; search the web generally and land
on the publisher instead.

## 3. Source quality tiers

Aim for the bulk of the reference list in Tier 1–2.

**Tier 1 — cite freely.** Peer-reviewed journal articles from established journals;
peer-reviewed conference proceedings in fields where that is the venue of record (CS,
engineering); scholarly monographs from academic presses; systematic reviews and
meta-analyses; standards documents.

**Tier 2 — cite with attribution to the body.** Reports from international bodies and
national statistical agencies; national academy and government research reports;
well-documented public datasets; theses from recognised universities.

**Tier 3 — cite sparingly and label.** Preprints (always identify as preprint); working
paper series (NBER, IZA); industry research with disclosed method; reputable technical
blogs from the research groups that built the thing (label as such).

**Tier 4 — do not cite; use only for orientation.** Wikipedia, encyclopaedias, news
aggregators, content farms, SEO listicles, undated web pages, LLM-generated summaries,
essay mills. Wikipedia is a fine way to find the *real* sources in its reference list —
follow them and cite those.

News outlets are a special case: cite them for events, policy announcements, and
contemporary discourse, not for scientific claims. A Reuters piece is evidence that
something was reported, not evidence that it is true.

## 4. Recognised publishers and databases

Safe to describe as reputable: Elsevier, Springer Nature, Wiley, Taylor & Francis, SAGE,
IEEE, ACM, Oxford University Press, Cambridge University Press, MIT Press, University of
Chicago Press, Routledge, Palgrave Macmillan, De Gruyter, Emerald, AAAS (*Science*),
Nature Portfolio, Cell Press, PNAS, The Lancet, BMJ, JAMA network, NEJM, APA journals,
AIP, ACS, RSC, IOP, INFORMS, AEA journals, Annual Reviews, PLOS.

## 5. Predatory and unreliable source red flags

Check before citing an unfamiliar journal. Any two of these together mean skip it:

- Journal title mimics a famous one ("International Journal of Advanced Research in…")
- Scope so broad it spans medicine, engineering and education in one journal
- Promises of publication in days or weeks; visible APC-first framing
- No named editorial board, or board members listed without affiliation
- Article PDFs with typographic errors in the header, misaligned DOIs, or no DOI
- Impact factor claimed from a body you cannot identify ("Global Impact Factor")
- Not indexed in Scopus, Web of Science, DOAJ, PubMed, or Ei Compendex
- Site hosted on a free platform; contact address is a webmail account

Also treat as unreliable: retracted papers (check Retraction Watch or the publisher's
notice if a claim seems extraordinary), papers whose only presence is a PDF on an
aggregator site, and "papers" that turn out to be conference abstracts or slide decks.

## 6. The source ledger

Keep `sources.md` in the working directory from the first search. Append as you go —
reconstructing it at the end defeats the purpose.

```markdown
## S07 — `nakamura2024storage`
- **Authors:** Nakamura, H., & Oyelaran-Oyeyinka, B.
- **Year:** 2024
- **Title:** Grid-scale storage economics under variable renewable penetration
- **Venue:** Energy Policy, 189, 114102
- **DOI/URL:** https://doi.org/10.1016/j.enpol.2024.114102
- **Tier:** 1 (Elsevier, peer-reviewed)
- **Accessed:** 2026-08-21 — full text / abstract only
- **Claims to use:**
  - Storage LCOE fell 38% between 2018 and 2023 across the 14 markets sampled (Table 3)
  - Argues curtailment costs are systematically underestimated in national plans (p. 6)
  - Limitation: OECD markets only; authors flag limited generalisability
- **Position in argument:** §3.2 cost trajectory; counterweight to S03's pessimism
```

Rules that make the ledger worth keeping:
- One ID per source, used everywhere in your outline and drafting notes, and one
  citekey — the same string you use in `refs.bib` and in every `\citep{...}`. The chain
  ledger → `.bib` → `.tex` is what `check_citations.py` walks; a break anywhere in it
  means a citation nobody can trace.
- Write the `.bib` entry in the same edit as the ledger entry, while the retrieved
  record is still in front of you. See `bibtex-guide.md` for entry types and fields.
- Claims recorded **in your own words** with a locator. If you copy the abstract in
  verbatim you will paraphrase it badly later; digest it now.
- Record what the source does *not* support, and its limitations — that is where the
  Discussion's critical edge comes from.
- Mark `abstract only` when you never saw full text, so Phase 5 can check what you
  claimed from it.
- Never add an entry you did not retrieve. The ledger is the boundary between research
  and invention.

## 7. Paywalls, preprints, and abstract-only citing

Paywalls are normal and not a blocker. When full text is unavailable:

- Look for the preprint (arXiv, bioRxiv, SSRN, institutional repository, PMC) — often
  the same content, and citable; cite the published version if it exists and note the
  preprint only if that is the only version.
- Abstracts legitimately support: the research question, the method in outline, the
  headline finding, and the reported effect direction and often its magnitude.
- Abstracts do **not** support: page-specific quotations, table values you did not see,
  subgroup results, or characterisations of the authors' argument beyond their summary.
- If a claim needs the full text and you cannot get it, find another source for it.

Citing a review or meta-analysis for a claim it aggregates is legitimate and often
better than citing a primary study you have not read. What is illegitimate is citing the
primary study you found *inside* that review as though you read it.

## 8. Gap analysis (wave two)

Before drafting, put the outline and the ledger side by side and ask:

1. Which claims have exactly one source? Single-sourced claims are fragile — find a
   second, or hedge the claim explicitly.
2. Where is the counter-evidence? A section with no disagreement in it is either a
   settled question or an incomplete search; usually the latter.
3. What is the newest source? If nothing is from the last 18 months in an active field,
   search again with the current year.
4. Are there numbers? A paper with no figures, rates, effect sizes or sample sizes reads
   as vague. Go find two or three concrete quantities you can put in a table.
5. Is any geography, population, or sector over-represented? Note it in Limitations if
   you cannot fix it — that is honest scholarship, not a weakness.
6. Does any part of the outline still have no source IDs? That part gets cut or
   researched. It does not get written from memory.
