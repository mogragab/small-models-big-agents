#!/usr/bin/env python3
"""Validate a LaTeX manuscript, BibTeX database, and retrieval ledger.

Run with uv:
    uv run --no-project check_citations.py paper.tex references.bib [sources.md]

The checker reports unresolved citation keys, uncited or duplicate BibTeX entries,
missing bibliography-resource commands, missing DOI/URL locators, and references whose
locators do not appear in the source ledger. It exits 1 when an error is found.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
DIM = "\033[2m"

TIER4_DOMAINS = (
    "wikipedia.org",
    "investopedia.com",
    "studocu.com",
    "coursehero.com",
    "chegg.com",
    "scribd.com",
    "quora.com",
    "medium.com",
    "blogspot.",
    "wordpress.com",
    "geeksforgeeks.org",
    "ukessays.com",
    "bartleby.com",
    "answers.com",
    "slideshare.net",
)

CITE_COMMAND = re.compile(
    r"\\(?:cite|citep|citet|citealp|citealt|citeauthor|citeyear|"
    r"parencite|textcite|autocite|footcite|smartcite|supercite|nocite)"
    r"\*?(?:\s*\[[^\]]*\]){0,2}\s*\{([^}]*)\}",
    re.IGNORECASE | re.DOTALL,
)


def strip_tex_comments(text: str) -> str:
    """Remove unescaped TeX comments while preserving line structure."""
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def citation_keys(tex: str) -> list[str]:
    keys: list[str] = []
    for group in CITE_COMMAND.findall(strip_tex_comments(tex)):
        for key in group.split(","):
            key = key.strip()
            if key and key != "*":
                keys.append(key)
    return keys


def parse_bib_entries(text: str) -> list[tuple[str, str, str]]:
    """Return (entry_type, key, raw_entry) tuples using balanced delimiters."""
    entries: list[tuple[str, str, str]] = []
    start_re = re.compile(r"@([A-Za-z]+)\s*([({])")
    pos = 0
    while match := start_re.search(text, pos):
        entry_type = match.group(1).lower()
        opener = match.group(2)
        closer = "}" if opener == "{" else ")"
        depth = 1
        i = match.end()
        in_quote = False
        escaped = False
        while i < len(text) and depth:
            char = text[i]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = not in_quote
            elif not in_quote and char == opener:
                depth += 1
            elif not in_quote and char == closer:
                depth -= 1
            i += 1
        if depth:
            raise ValueError(f"Unclosed @{entry_type} entry beginning near character {match.start()}.")
        raw = text[match.start():i]
        content = text[match.end(): i - 1]
        pos = i
        if entry_type in {"comment", "preamble", "string"}:
            continue
        key_match = re.match(r"\s*([^,\s]+)\s*,", content)
        if not key_match:
            raise ValueError(f"Could not parse the key for an @{entry_type} entry.")
        entries.append((entry_type, key_match.group(1), raw))
    return entries


def locators(text: str) -> tuple[set[str], set[str]]:
    dois = {
        value.rstrip(".,);]}\"").lower()
        for value in re.findall(r"10\.\d{4,9}/[^\s\"'<>]+", text, re.IGNORECASE)
    }
    urls = {
        value.rstrip(".,);]}\"")
        for value in re.findall(r"https?://[^\s\"'<>)\]]+", text, re.IGNORECASE)
    }
    return dois, urls


def resource_mentions_bib(tex: str, bib_path: Path) -> bool:
    clean = strip_tex_comments(tex)
    candidates: list[str] = []
    candidates.extend(re.findall(r"\\addbibresource(?:\[[^\]]*\])?\{([^}]+)\}", clean))
    candidates.extend(re.findall(r"\\bibliography\{([^}]+)\}", clean))
    expected_name = bib_path.name.lower()
    expected_stem = bib_path.stem.lower()
    for group in candidates:
        for item in group.split(","):
            value = Path(item.strip()).name.lower()
            if value == expected_name or Path(value).stem == expected_stem:
                return True
    return False


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2

    tex_path = Path(sys.argv[1])
    bib_path = Path(sys.argv[2])
    ledger_path = Path(sys.argv[3]) if len(sys.argv) > 3 else tex_path.parent / "sources.md"

    missing = [str(path) for path in (tex_path, bib_path, ledger_path) if not path.is_file()]
    if missing:
        for path in missing:
            print(f"{RED}ERROR  {RESET}Required file not found: {path}")
        return 1

    tex = tex_path.read_text(encoding="utf-8")
    bib = bib_path.read_text(encoding="utf-8")
    ledger = ledger_path.read_text(encoding="utf-8")

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    if re.search(r"\\begin\s*\{thebibliography\}", strip_tex_comments(tex)):
        errors.append("The manuscript contains a hand-written thebibliography environment; use references.bib.")

    try:
        entries = parse_bib_entries(bib)
    except ValueError as exc:
        errors.append(str(exc))
        entries = []

    if not entries:
        errors.append("No bibliographic entries found in references.bib.")

    keys = [key for _entry_type, key, _raw in entries]
    counts = Counter(keys)
    for key, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"Duplicate BibTeX key {key!r} appears {count} times.")

    cited = citation_keys(tex)
    cited_set = set(cited)
    bib_set = set(keys)
    for key in sorted(cited_set - bib_set):
        errors.append(f"Unresolved citation key: {key}")
    for key in sorted(bib_set - cited_set):
        errors.append(f"BibTeX entry is never cited: {key}")

    if not cited:
        errors.append("No LaTeX citation commands were found in the manuscript.")

    if not resource_mentions_bib(tex, bib_path):
        errors.append(
            f"paper.tex does not load {bib_path.name}; add \\addbibresource{{{bib_path.name}}} "
            "or the venue's equivalent \\bibliography command."
        )

    ledger_dois, ledger_urls = locators(ledger)
    for _entry_type, key, raw in entries:
        entry_dois, entry_urls = locators(raw)
        if not entry_dois and not entry_urls:
            warnings.append(f"BibTeX entry {key} has no DOI or URL.")
            continue
        in_ledger = bool(entry_dois & ledger_dois) or bool(entry_urls & ledger_urls)
        if not in_ledger:
            normalized_ledger_urls = {url.rstrip("/") for url in ledger_urls}
            in_ledger = any(url.rstrip("/") in normalized_ledger_urls for url in entry_urls)
        if not in_ledger:
            errors.append(f"BibTeX entry {key} has no matching DOI/URL in sources.md.")

        for doi in entry_dois:
            tail = doi.split("/", 1)[1] if "/" in doi else ""
            if len(tail) < 3 or re.fullmatch(r"[a-z]*\.?0*", tail):
                warnings.append(f"Suspicious DOI in {key}: {doi}")
        lower = raw.lower()
        for domain in TIER4_DOMAINS:
            if domain in lower:
                errors.append(f"Tier-4 source in {key} ({domain}); replace it with a scholarly source.")

    years = [int(year) for year in re.findall(r"\b(19\d{2}|20[0-2]\d)\b", bib)]
    if years:
        recent = sum(year >= 2021 for year in years)
        if recent / len(years) < 0.35:
            notes.append(f"Only {recent}/{len(years)} year values are 2021 or later; check literature currency.")

    notes.append(f"Found {len(cited_set)} distinct citation keys and {len(entries)} BibTeX entries.")
    report(errors, warnings, notes)
    return 1 if errors else 0


def report(errors: list[str], warnings: list[str], notes: list[str]) -> None:
    print()
    for note in notes:
        print(f"{DIM}note   {RESET}{note}")
    for warning in warnings:
        print(f"{YELLOW}warn   {RESET}{warning}")
    for error in errors:
        print(f"{RED}ERROR  {RESET}{error}")
    print()
    if errors:
        print(f"{RED}{len(errors)} error(s), {len(warnings)} warning(s). Fix every error before delivery.{RESET}")
    elif warnings:
        print(f"{YELLOW}Citation check passed with {len(warnings)} warning(s) to review.{RESET}")
    else:
        print(f"{GREEN}Citation check passed.{RESET}")


if __name__ == "__main__":
    raise SystemExit(main())
