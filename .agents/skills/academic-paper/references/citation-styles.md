# Citation styles

## LaTeX and BibTeX requirements

Store every bibliographic record in `references.bib` and cite it from `paper.tex` with
stable keys such as `smith2024reliable`. Never type a formatted reference list directly
into the manuscript. Prefer a venue's official class and bibliography instructions. If
none are supplied, use `biblatex` with `biber`: `style=apa` for APA, `style=ieee` for
IEEE, `style=numeric-comp` for Vancouver, and a suitable `authoryear` style for Harvard
or general scholarly work. Use `\textcite{key}` for narrative citations and
`\parencite{key}` for parenthetical citations; numeric styles may use `\cite{key}`.

Each BibTeX entry must include the metadata actually verified from a retrieved source.
Include `doi` when one exists and `url` for sources without a DOI. Escape LaTeX special
characters and protect capitalization in titles with braces only where necessary.

Worked formats for the six styles that cover almost every request. Pick one, apply it
consistently, and match the reference-list heading name and ordering to the style.

## Contents
1. Choosing a style
2. APA 7
3. IEEE
4. Vancouver
5. MLA 9
6. Chicago (author–date and notes–bibliography)
7. Harvard
8. Cross-cutting rules

---

## 1. Choosing a style

| Field | Default |
|---|---|
| Psychology, education, social sciences, business | APA 7 |
| Engineering, computer science, electronics | IEEE |
| Medicine, nursing, public health, biomedical | Vancouver (or AMA) |
| Humanities, literature, languages | MLA 9 |
| History, some social sciences, book-length work | Chicago |
| UK/Commonwealth general academic | Harvard |

If the user names a target journal, follow that journal's style; when unsure which it
uses, say which you applied and note it is adjustable.

---

## 2. APA 7

**In-text.** Author–date. Narrative: `Okonkwo (2023) argued…`. Parenthetical:
`(Okonkwo, 2023)`. With locator: `(Okonkwo, 2023, p. 47)`. Two authors: both names, `&`
inside parentheses, `and` in narrative. Three or more: `(Okonkwo et al., 2023)` from the
first citation. Multiple works in one parenthesis: alphabetical, semicolon-separated —
`(Chen, 2021; Okonkwo et al., 2023; Silva & Marek, 2024)`. Organisation as author:
spell out first, then abbreviate — `(World Health Organization [WHO], 2024)`, then
`(WHO, 2024)`. No date: `(Okonkwo, n.d.)`.

**Reference list.** Heading `References`, alphabetical by first author surname, hanging
indent 0.5″, double-spaced. Sentence case for article and book titles; title case for
journal names. Italicise journal name, volume, and book titles. Include DOI as a full
`https://doi.org/…` link. Up to 20 authors listed; with 21+, list the first 19, an
ellipsis, then the final author.

```
Journal article:
Okonkwo, A. N., Silva, R., & Marek, J. (2023). Attention allocation under algorithmic
    curation: A field experiment. Journal of Communication, 73(4), 412–431.
    https://doi.org/10.1093/joc/jqad021

Book:
Bourdieu, P. (1990). The logic of practice (R. Nice, Trans.). Stanford University Press.

Chapter:
Hale, S. (2022). Network effects in civic platforms. In L. Fournier & K. Adeyemi (Eds.),
    Digital publics (pp. 88–114). Oxford University Press.

Report:
World Health Organization. (2024). Global report on air quality and health.
    https://www.who.int/publications/i/item/9789240012345

Preprint:
Zhang, W., & Ferreira, T. (2026). Sparse retrieval for long-context reasoning
    (arXiv:2601.04412). arXiv. https://arxiv.org/abs/2601.04412

Dataset:
Eurostat. (2025). Renewable energy share by country [Data set].
    https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren
```

---

## 3. IEEE

**In-text.** Bracketed numerals in order of first appearance: `…as shown in [3]`,
`…several studies [4], [7], [11]–[13]`. The number is reused on every later mention.
Cite as a noun sparingly: `Reference [3] shows…` when starting a sentence. Page
locators: `[3, p. 47]`, `[3, Fig. 2]`.

**Reference list.** Heading `References`, numbered in citation order (not alphabetical),
with the number in square brackets. Author initials precede surnames. Article titles in
quotation marks, sentence case; journal names italicised and abbreviated per IEEE
practice (`IEEE Trans. Neural Netw. Learn. Syst.`); include vol., no., pp., and year.

```
[1] A. N. Okonkwo, R. Silva, and J. Marek, "Attention allocation under algorithmic
    curation," IEEE Trans. Comput. Soc. Syst., vol. 10, no. 4, pp. 412–431, Aug. 2023,
    doi: 10.1109/TCSS.2023.3245678.
[2] S. Hale, Network Architectures for Civic Platforms. Cambridge, U.K.: Cambridge
    Univ. Press, 2022.
[3] W. Zhang and T. Ferreira, "Sparse retrieval for long-context reasoning," 2026,
    arXiv:2601.04412.
[4] International Energy Agency, "World energy outlook 2025," IEA, Paris, France, Rep.,
    2025. [Online]. Available: https://www.iea.org/reports/world-energy-outlook-2025
```

For six or more authors, list the first three then `et al.`

---

## 4. Vancouver (biomedical)

**In-text.** Superscript or bracketed numerals in order of appearance: `…risk was
elevated.¹` or `…risk was elevated [1]`. Be consistent; bracketed is safer in Word.

**Reference list.** Heading `References`, numbered in citation order. Authors as
surname + initials without periods, up to six then `et al.` Journal titles abbreviated
per NLM. No italics required.

```
1. Okonkwo AN, Silva R, Marek J. Attention allocation under algorithmic curation: a
   field experiment. J Commun. 2023;73(4):412-31. doi:10.1093/joc/jqad021
2. World Health Organization. Global report on air quality and health. Geneva: WHO;
   2024.
3. Hale S. Network effects in civic platforms. In: Fournier L, Adeyemi K, editors.
   Digital publics. Oxford: Oxford University Press; 2022. p. 88-114.
```

---

## 5. MLA 9

**In-text.** Author–page, no comma: `(Okonkwo 47)`. Narrative: `Okonkwo argues … (47)`.
No page number for unpaginated web sources: `(Okonkwo)`.

**Works cited.** Heading `Works Cited`, alphabetical, hanging indent. MLA 9 uses the
"core elements" template: Author. "Title of Source." *Title of Container*, Other
contributors, Version, Number, Publisher, Publication date, Location.

```
Okonkwo, Adaeze N., et al. "Attention Allocation under Algorithmic Curation: A Field
    Experiment." Journal of Communication, vol. 73, no. 4, 2023, pp. 412–31,
    https://doi.org/10.1093/joc/jqad021.

Bourdieu, Pierre. The Logic of Practice. Translated by Richard Nice, Stanford UP, 1990.

Hale, Sofia. "Network Effects in Civic Platforms." Digital Publics, edited by Léa
    Fournier and Kunle Adeyemi, Oxford UP, 2022, pp. 88–114.
```

---

## 6. Chicago

**Author–date (sciences, social sciences).** In-text `(Okonkwo, Silva, and Marek 2023,
47)`; reference list headed `References`, alphabetical.

```
Okonkwo, Adaeze N., Rui Silva, and Jan Marek. 2023. "Attention Allocation under
    Algorithmic Curation: A Field Experiment." Journal of Communication 73 (4): 412–31.
    https://doi.org/10.1093/joc/jqad021.
```

**Notes–bibliography (humanities).** Superscript note numbers in text; footnotes carry
the citation; a `Bibliography` follows.

```
Note:  1. Adaeze N. Okonkwo, Rui Silva, and Jan Marek, "Attention Allocation under
       Algorithmic Curation: A Field Experiment," Journal of Communication 73, no. 4
       (2023): 419.
Short: 4. Okonkwo, Silva, and Marek, "Attention Allocation," 421.
Bib:   Okonkwo, Adaeze N., Rui Silva, and Jan Marek. "Attention Allocation under
       Algorithmic Curation: A Field Experiment." Journal of Communication 73, no. 4
       (2023): 412–31.
```

---

## 7. Harvard

Close to APA but with variations by institution; state the variant used.

**In-text.** `(Okonkwo, Silva and Marek, 2023, p. 47)` — note `and` rather than `&` in
many Harvard variants, and a comma before the year.

**Reference list.** Alphabetical, headed `Reference List` or `References`.

```
Okonkwo, A.N., Silva, R. and Marek, J. (2023) 'Attention allocation under algorithmic
    curation: a field experiment', Journal of Communication, 73(4), pp. 412–431.
    doi: 10.1093/joc/jqad021.

Hale, S. (2022) 'Network effects in civic platforms', in Fournier, L. and Adeyemi, K.
    (eds.) Digital publics. Oxford: Oxford University Press, pp. 88–114.
```

---

## 8. Cross-cutting rules

- **One style throughout.** Mixed styles are the most visible sign of an assembled
  rather than written paper. If you switch mid-draft, re-render every citation.
- **In-text and list must be bijective.** Every in-text citation has a list entry;
  every list entry is cited at least once. `scripts/check_citations.py` enforces this.
- **Numbered styles renumber when sections move.** Do the renumbering at the end, once
  the section order is final, and re-run the checker afterwards.
- **DOI over URL.** Give a DOI when the record has one; a URL only when it does not.
  Never construct a DOI from a pattern — copy it from the retrieved record.
- **Access dates** are needed for web pages that can change (Harvard, MLA, Chicago) and
  in APA only for unarchived, frequently updated content.
- **Alphabetical styles**: order by first author surname; same author, order by year
  ascending; same author and year, append `a`, `b`, `c` to the year in both the list and
  every in-text citation.
- **Non-Latin and diacritics**: preserve them exactly as printed; do not transliterate
  silently.
- **Translated works**: give the translator and, where relevant, the original year in
  the form the style prescribes.
