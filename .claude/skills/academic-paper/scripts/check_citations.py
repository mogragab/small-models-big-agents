#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
check_citations.py - verify citation integrity before delivering a LaTeX paper.

    uv run check_citations.py paper.tex [refs.bib] [sources.md]
    python3 check_citations.py paper.tex

The .bib is read from the \\bibliography{...} command if not given; the ledger
defaults to sources.md beside the paper.

Checks, in order of how badly they matter:

  1. LEDGER    every .bib entry's DOI/URL appears in sources.md - i.e. the source
               was actually retrieved this session, not remembered
  2. ORPHAN    every \\cite key resolves to an entry in the .bib
  3. UNCITED   every .bib entry is cited at least once in the .tex
  4. FIELDS    entries have the fields their type requires, and a DOI or URL
  5. HYGIENE   duplicate keys, constructed-looking DOIs, Tier-4 domains, long
               quotations, unlabelled preprints, unbraced acronyms, TODOs

Exit code is 1 if any error-level problem is found.
"""

import re
import sys
from pathlib import Path
from collections import Counter, OrderedDict

RESET, RED, YEL, GRN, DIM = "\033[0m", "\033[31m", "\033[33m", "\033[32m", "\033[2m"

TIER4 = (
    "wikipedia.org", "investopedia.com", "studocu.com", "coursehero.com",
    "chegg.com", "scribd.com", "quora.com", "medium.com", "blogspot.",
    "wordpress.com", "geeksforgeeks.org", "ukessays.com", "bartleby.com",
    "answers.com", "slideshare.net", "researchgate.net",
)

# type -> (required fields, recommended fields). "a|b" means at least one of them.
REQUIRED = {
    "article": (["author", "title", "journal", "year"], ["volume", "pages", "doi"]),
    "inproceedings": (["author", "title", "booktitle", "year"], ["pages", "doi"]),
    "conference": (["author", "title", "booktitle", "year"], ["pages", "doi"]),
    "book": (["author|editor", "title", "publisher", "year"], ["address"]),
    "inbook": (["author|editor", "title", "publisher", "year"], ["pages"]),
    "incollection": (["author", "title", "booktitle", "publisher", "year"], ["pages", "editor"]),
    "techreport": (["author", "title", "institution", "year"], ["url"]),
    "phdthesis": (["author", "title", "school", "year"], ["url"]),
    "mastersthesis": (["author", "title", "school", "year"], ["url"]),
    "manual": (["title", "year"], ["organization", "url"]),
    "unpublished": (["author", "title", "note"], ["year", "url"]),
    "misc": (["title", "year"], ["author", "url"]),
    "online": (["title", "year"], ["author", "url"]),
    "electronic": (["title", "year"], ["author", "url"]),
}

CITE_CMDS = (
    r"cite|citep|citet|citeal[pt]|citeauthor|citeyear|citeyearpar|citenum|"
    r"parencite|textcite|autocite|footcite|fullcite|nocite|citeA|shortcite"
)
CITE_RE = re.compile(
    r"\\(?:" + CITE_CMDS + r")\*?"       # command, optional star
    r"(?:\s*\[[^\]]*\]){0,2}"             # up to two optional arguments
    r"\s*\{([^{}]*)\}"
)


# ------------------------------------------------------------------ tex side

def strip_tex_comments(text):
    """Drop % comments, keeping \\% escapes."""
    out = []
    for line in text.splitlines():
        buf, i = [], 0
        while i < len(line):
            c = line[i]
            if c == "\\" and i + 1 < len(line):
                buf.append(line[i:i + 2])
                i += 2
                continue
            if c == "%":
                break
            buf.append(c)
            i += 1
        out.append("".join(buf))
    return "\n".join(out)


def parse_tex(path):
    raw = path.read_text(encoding="utf-8")
    text = strip_tex_comments(raw)
    cites = OrderedDict()
    nocite_star = False
    for m in CITE_RE.finditer(text):
        for key in m.group(1).split(","):
            key = key.strip()
            if not key:
                continue
            if key == "*":
                nocite_star = True
                continue
            cites.setdefault(key, m.start())
    bibfiles = []
    for m in re.finditer(r"\\(?:bibliography|addbibresource)\{([^{}]*)\}", text):
        for f in m.group(1).split(","):
            f = f.strip()
            if f:
                bibfiles.append(f if f.endswith(".bib") else f + ".bib")
    ms = re.search(r"\\bibliographystyle\{([^{}]*)\}", text)
    style = ms.group(1).strip() if ms else None
    return raw, text, cites, nocite_star, bibfiles, style


# ------------------------------------------------------------------ bib side

def parse_bib(text):
    """Minimal BibTeX parser: returns list of (type, key, {field: value}, raw)."""
    entries = []
    i, n = 0, len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        m = re.match(r"@(\w+)\s*[{(]", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        start = at + m.end()
        depth, j = 1, start
        while j < n and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        blob = text[start:j - 1]
        raw = text[at:j]
        i = j
        if etype in ("comment", "preamble", "string"):
            continue
        key, _, rest = blob.partition(",")
        key = key.strip()
        fields = {}
        for fm in re.finditer(
            r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\s}]+)", rest
        ):
            val = fm.group(2).strip()
            if val and val[0] in "{\"":
                val = val[1:-1]
            fields[fm.group(1).lower()] = " ".join(val.split())
        entries.append((etype, key, fields, raw))
    return entries


def locators(text):
    dois = {d.rstrip(".,);]").lower() for d in re.findall(r"10\.\d{4,9}/[^\s\"'<>{},]+", text)}
    urls = {u.rstrip(".,);]") for u in re.findall(r"https?://[^\s\"'<>)\]},]+", text)}
    return dois, urls


def entry_locators(fields, raw):
    dois, urls = locators(raw)
    if fields.get("doi"):
        dois.add(fields["doi"].replace("https://doi.org/", "").strip().lower())
    return dois, urls


# ------------------------------------------------------------------ main

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    tex_path = Path(sys.argv[1])
    if not tex_path.exists():
        print(f"{RED}No such file: {tex_path}{RESET}")
        return 2

    raw_tex, tex, cites, nocite_star, declared_bibs, bibstyle = parse_tex(tex_path)

    if len(sys.argv) > 2:
        bib_paths = [Path(sys.argv[2])]
    else:
        bib_paths = [tex_path.parent / b for b in declared_bibs] or [tex_path.parent / "refs.bib"]
    ledger_path = Path(sys.argv[3]) if len(sys.argv) > 3 else tex_path.parent / "sources.md"

    errors, warnings, notes = [], [], []

    if not declared_bibs:
        errors.append("No \\bibliography{...} in the .tex - the reference list will be empty.")
    if not bibstyle:
        warnings.append("No \\bibliographystyle{...} found; BibTeX will not produce a list.")

    entries = []
    for bp in bib_paths:
        if not bp.exists():
            errors.append(f"Bibliography file not found: {bp}")
            continue
        entries.extend(parse_bib(bp.read_text(encoding="utf-8")))

    if not entries:
        report(errors + ["No entries parsed from the .bib file."], warnings, notes)
        return 1

    by_key = {}
    for etype, key, fields, raw in entries:
        by_key.setdefault(key, (etype, fields, raw))

    for key, count in Counter(k for _, k, _, _ in entries).items():
        if count > 1:
            errors.append(f"Duplicate citekey in .bib: {key} appears {count} times.")

    # ---- 1. ledger
    ledger_text = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    if not ledger_text:
        warnings.append(
            f"No source ledger at {ledger_path} - cannot verify that references were "
            "actually retrieved. Every entry should trace to a ledger record."
        )
    l_dois, l_urls = locators(ledger_text)
    l_lower = ledger_text.lower()

    for etype, key, fields, raw in entries:
        dois, urls = entry_locators(fields, raw)
        if not dois and not urls:
            warnings.append(f"{key}: no DOI or URL - how would a reader find this?")
            continue
        if not ledger_text:
            continue
        ok = any(d in l_dois for d in dois) or any(
            u in l_urls or any(u.rstrip("/") == lu.rstrip("/") for lu in l_urls) for u in urls
        )
        if not ok:
            ok = any(d in l_lower for d in dois) or any(u in ledger_text for u in urls)
        if not ok:
            errors.append(f"NOT IN LEDGER - was {key} actually retrieved this session?")

    # ---- 2. orphans
    for key in cites:
        if key not in by_key:
            errors.append(f"Orphan citation \\cite{{{key}}} - no such entry in the .bib.")

    # ---- 3. uncited
    if nocite_star:
        notes.append("\\nocite{*} present: every .bib entry prints whether cited or not.")
    else:
        for key in by_key:
            if key not in cites:
                errors.append(f"Entry {key} is in the .bib but never cited in the text.")

    # ---- 4. fields
    for etype, key, fields, raw in entries:
        if etype not in REQUIRED:
            notes.append(f"{key}: unusual entry type @{etype} - check your .bst supports it.")
        req, rec = REQUIRED.get(etype, ([], []))
        for spec in req:
            if not any(fields.get(alt) for alt in spec.split("|")):
                errors.append(f"{key} (@{etype}): missing required field '{spec}'.")
        missing_rec = [f for f in rec if not fields.get(f)]
        if missing_rec:
            warnings.append(f"{key}: no {', '.join(missing_rec)} - add if the record has them.")
        year = fields.get("year", "")
        if year and not re.fullmatch(r"\d{4}[a-z]?|in press|n\.d\.", year.strip(), re.I):
            warnings.append(f"{key}: year looks wrong ('{year}').")

    # ---- 5. hygiene
    for etype, key, fields, raw in entries:
        for d in re.findall(r"10\.\d{4,9}/[^\s\"'<>{},]+", raw):
            tail = d.split("/", 1)[1]
            if re.fullmatch(r"[a-z]*\.?0*", tail) or len(tail) < 3:
                warnings.append(f"{key}: suspicious DOI, looks constructed ({d}).")
        low = raw.lower()
        for dom in TIER4:
            if dom in low:
                errors.append(f"{key}: Tier-4 source ({dom}) - replace with a scholarly record.")
        if any(p in low for p in ("arxiv", "biorxiv", "medrxiv", "ssrn")):
            if etype == "article" and not fields.get("journal"):
                warnings.append(f"{key}: preprint filed as @article with no journal - use "
                                "@misc or @unpublished and label it as a preprint.")

        tm = re.search(r"title\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", raw, re.S)
        if tm:
            for acro in re.findall(r"(?<![{\w])([A-Z]{2,})(?![\w}])", tm.group(1)):
                warnings.append(f"{key}: '{acro}' in the title is unbraced - most styles will "
                                f"lowercase it. Write {{{acro}}}.")
                break

    for m in re.finditer(r"``(.{5,400}?)''|\\enquote\{([^{}]{5,400}?)\}", tex, re.S):
        qt = m.group(1) or m.group(2)
        wc = len(qt.split())
        if wc >= 15:
            warnings.append(f"Direct quotation of ~{wc} words - paraphrase or trim: \"{qt[:60]}...\"")

    if re.search(r"%\s*TODO|\\todo\{|TODO:", raw_tex):
        warnings.append("TODO markers still in the .tex - remove before delivering.")
    if "\\begin{abstract}" not in tex:
        warnings.append("No \\begin{abstract} in the manuscript.")

    years = [int(y) for y in re.findall(
        r"year\s*=\s*[{\"]?((?:19|20)\d{2})", " ".join(e[3] for e in entries))]
    if years:
        recent = sum(1 for y in years if y >= 2021)
        if recent / len(years) < 0.35:
            notes.append(f"Only {recent}/{len(years)} references are 2021 or later - "
                         "consider searching for more recent literature.")

    numeric = (bibstyle or "").lower() in {
        "ieeetr", "ieeetran", "unsrt", "unsrtnat", "vancouver", "plain", "abbrv"
    }
    notes.append(f"{len(by_key)} entries in the .bib; {len(cites)} distinct keys cited; "
                 f"bibliographystyle={bibstyle or 'none'} "
                 f"({'numeric' if numeric else 'author-date'}).")

    report(errors, warnings, notes)
    return 1 if errors else 0


def report(errors, warnings, notes):
    print()
    for n in notes:
        print(f"{DIM}note   {RESET}{n}")
    for w in warnings:
        print(f"{YEL}warn   {RESET}{w}")
    for e in errors:
        print(f"{RED}ERROR  {RESET}{e}")
    print()
    if errors:
        print(f"{RED}{len(errors)} error(s), {len(warnings)} warning(s). Fix every error "
              f"before delivering - an unverifiable citation is worse than a missing one.{RESET}")
    elif warnings:
        print(f"{GRN}Clean on errors{RESET}, {YEL}{len(warnings)} warning(s) worth a look.{RESET}")
    else:
        print(f"{GRN}Citation check passed.{RESET}")


if __name__ == "__main__":
    sys.exit(main())
