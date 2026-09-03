# Writing `refs.bib`

The `.bib` is the paper's factual backbone. Every entry is a claim that a document
exists with exactly these attributes — so each field is copied from a record you
retrieved, never reconstructed. This file covers how to write entries that are both
true and typeset correctly.

## Contents
1. Citekeys
2. Entry types and required fields
3. Worked entries
4. Brace protection: the two failure modes
5. Names, accents, and non-Latin scripts
6. DOIs, URLs, and access dates
7. Preprints, datasets, standards, and grey literature
8. Common breakages

---

## 1. Citekeys

`firstauthorsurname` + `year` + `first distinctive title word`, all lowercase ASCII:

```
okonkwo2023attention        nakamura2024storage        who2024airquality
```

Stable, readable in the middle of a sentence you are drafting, and collision-resistant.
Two entries that still collide get `a`/`b` suffixes (`smith2021bias`, `smith2021biasb`)
— and if they are the same author and year, the author–date styles need `year = {2021a}`
too so the in-text citation disambiguates.

Write the entry into `refs.bib` at the moment you retrieve the source, together with
its `sources.md` record. Batch-writing the bibliography at the end is how invented
volume numbers get in: by then you are working from memory of a page you saw an hour ago.

## 2. Entry types and required fields

`check_citations.py` enforces this table.

| Type | Required | Also include when the record has it |
|---|---|---|
| `@article` | author, title, journal, year | volume, number, pages, doi |
| `@inproceedings` | author, title, booktitle, year | pages, publisher, address, doi |
| `@book` | author *or* editor, title, publisher, year | address, edition, isbn |
| `@incollection` | author, title, booktitle, publisher, year | editor, pages, address |
| `@techreport` | author, title, institution, year | number, address, url |
| `@phdthesis` / `@mastersthesis` | author, title, school, year | address, url |
| `@misc` | title, year | author, howpublished, url, note, eprint |
| `@unpublished` | author, title, note | year, url |

Use `@misc` for datasets, web resources, software, and preprints; `@techreport` for
institutional reports (WHO, OECD, IEA, national statistics offices); `@manual` for
standards and documentation. If a field is genuinely absent from the record, omit it —
BibTeX handles absence gracefully and invents nothing. That is the whole point.

## 3. Worked entries

```bibtex
@article{okonkwo2023attention,
  author  = {Okonkwo, Ada N. and Silva, Rui and Marek, Jan},
  title   = {Attention allocation under algorithmic curation: A field experiment},
  journal = {Journal of Communication},
  year    = {2023},
  volume  = {73},
  number  = {4},
  pages   = {412--431},
  doi     = {10.1093/joc/jqad021}
}

@inproceedings{zhang2026sparse,
  author    = {Zhang, Wei and Ferreira, Tomás},
  title     = {Sparse retrieval for long-context reasoning},
  booktitle = {Proceedings of the 64th Annual Meeting of the Association for
               Computational Linguistics},
  year      = {2026},
  pages     = {1142--1157},
  doi       = {10.18653/v1/2026.acl-long.92}
}

@book{bourdieu1990logic,
  author    = {Bourdieu, Pierre},
  title     = {The Logic of Practice},
  publisher = {Stanford University Press},
  address   = {Stanford, CA},
  year      = {1990},
  note      = {Translated by Richard Nice}
}

@incollection{hale2022network,
  author    = {Hale, Sofia},
  title     = {Network effects in civic platforms},
  booktitle = {Digital Publics},
  editor    = {Fournier, Léa and Adeyemi, Kunle},
  publisher = {Oxford University Press},
  address   = {Oxford},
  year      = {2022},
  pages     = {88--114}
}

@techreport{iea2025weo,
  author      = {{International Energy Agency}},
  title       = {World Energy Outlook 2025},
  institution = {International Energy Agency},
  address     = {Paris},
  year        = {2025},
  url         = {https://www.iea.org/reports/world-energy-outlook-2025}
}

@misc{eurostat2025renewables,
  author       = {{Eurostat}},
  title        = {Renewable energy share by country},
  year         = {2025},
  howpublished = {Dataset},
  url          = {https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren},
  note         = {Accessed 21 August 2026}
}
```

Note `--` for page ranges (it renders as an en dash), `and` as the author separator —
never a comma between authors — and `{{International Energy Agency}}` for a corporate
author.

## 4. Brace protection: the two failure modes

Most `.bst` files rewrite what you give them. Two habits prevent the damage:

**Acronyms and proper nouns in titles get lowercased** by styles that use sentence case
(APA, `apalike`, `unsrtnat`). Brace anything whose capitalisation is not optional:

```bibtex
title = {{DNA} methylation and {COVID}-19 severity in {Malaysia}}
```

Without braces this becomes "Dna methylation and covid-19 severity in malaysia".

**Corporate authors get split into first and last names.** `author = {World Health
Organization}` renders as "Organization, W. H." Double-brace it:

```bibtex
author = {{World Health Organization}}
```

The rule generalises: outer braces delimit the field, inner braces mean "treat this as
one unbreakable unit". `check_citations.py` warns on unbraced all-caps in titles.

## 5. Names, accents, and non-Latin scripts

- Write names as `Surname, Given` — unambiguous for compound surnames.
  `{van der Berg}, Anneke` keeps the particle attached; `Okonkwo, Ada N.` is fine.
- With `pdflatex` + `inputenc`, UTF-8 accents (`Tomás`, `Müller`, `Łukasz`) work
  directly on modern TeX Live. If a build breaks on one, the ASCII escapes are
  `{\'a}`, `{\"u}`, `{\l}` — but preserve the character, never silently drop the accent.
- Non-Latin scripts (Chinese, Arabic, Cyrillic author names) need `xelatex` or
  `lualatex` with `fontspec`. If the paper is otherwise plain `pdflatex`, transliterate
  in the author field and record the original in `note`, rather than switching engines
  for one entry.
- Suffixes: `Okonkwo, Jr., Ada N.` — the comma-separated middle slot is where BibTeX
  expects "Jr.", "III", and similar.

## 6. DOIs, URLs, and access dates

- **DOI over URL** whenever the record has one. Store the bare DOI
  (`10.1093/joc/jqad021`), not the resolver prefix — most `.bst` files add
  `https://doi.org/` themselves.
- **Never construct a DOI.** A DOI you did not see on the record is a fabrication even
  if the paper is real. The checker flags patterned-looking ones, but it cannot catch a
  plausible invention — that is on you.
- **URL for anything without a DOI**: reports, datasets, standards, web pages. Add
  `note = {Accessed <date>}` for pages that can change.
- A URL with `%` or `#` in it needs escaping (`\%`, `\#`) or the `url` package's
  verbatim handling; `hyperref` usually copes, but a URL that breaks the build is
  always the first place to look.

## 7. Preprints, datasets, standards, and grey literature

**Preprints** must be identifiable as such. If a published version exists, cite that
instead. If not:

```bibtex
@misc{zhang2026sparse,
  author       = {Zhang, Wei and Ferreira, Tomás},
  title        = {Sparse retrieval for long-context reasoning},
  year         = {2026},
  eprint       = {2601.04412},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  note         = {Preprint},
  url          = {https://arxiv.org/abs/2601.04412}
}
```

`check_citations.py` warns when an arXiv/bioRxiv/SSRN item is filed as `@article` with
no journal — that combination presents a preprint as peer-reviewed, which is the single
most common accidental misrepresentation in a reference list.

**Datasets**: `@misc` with `howpublished = {Dataset}`, the version or access date, and
the landing page URL. **Standards**: `@manual` with `organization = {{ISO}}` and the
designation in the title. **Legislation and case law** rarely fit BibTeX cleanly; use
`@misc` and check the discipline's convention — law papers usually want footnotes rather
than a bibliography, in which case say so instead of forcing it.

## 8. Common breakages

| Symptom in the PDF | Cause |
|---|---|
| Author printed as "Organization, W. H." | Corporate name not double-braced |
| Title lowercased | Acronym or proper noun unbraced (sentence-case `.bst`) |
| Entry missing from the list entirely | Never cited, or a typo'd key — the checker catches both |
| "?" or `[?]` where a citation should be | Key not in the `.bib`, or BibTeX did not run |
| Page range with a hyphen instead of an en dash | Single `-` instead of `--` |
| Authors run together | Comma used as separator instead of `and` |
| Extra unwanted entries in the list | A stray `\nocite{*}` |
| BibTeX error `I was expecting a ","` | Missing comma between fields, or an unbalanced brace — the line number in `.blg` is reliable |

Run `uv run scripts/check_citations.py paper.tex refs.bib sources.md` after every batch
of entries rather than once at the end. The failures are cheap to fix while you still
remember the source and expensive to fix later.
