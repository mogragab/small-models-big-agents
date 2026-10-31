"""Repair arXiv-linked BibTeX entries against the arXiv API.

For every entry whose url/eprint names an arXiv identifier:
  - author: replaced with the arXiv author list whenever the .bib list is not a
    faithful prefix of it (wrong co-authors) or is truncated with "and others".
    Lists longer than MAX_AUTHORS keep the first MAX_AUTHORS and end in "and
    others". Corporate authors written in braces ({Qwen Team}) are left alone.
  - title: replaced only when it differs materially from the arXiv title
    (word-set Jaccard < 0.8), so existing brace-protection is kept otherwise.
  - eprint / archivePrefix fields are added.
Prints a log of every change. Run from source/:

    uv run python scripts/repair_bib_from_arxiv.py ../journal/bibliography.bib
"""

from __future__ import annotations

import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET

MAX_AUTHORS = 30
NS = {"a": "http://www.w3.org/2005/Atom"}
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})|eprint\s*=\s*\{(\d{4}\.\d{4,5})", re.I)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"[{}\\]", "", s))


def surname(name: str) -> str:
    name = name.strip()
    s = name.split(",")[0] if "," in name else (name.split()[-1] if name.split() else "")
    return norm(s).replace(" ", "")


def fetch(ids: list[str]) -> dict[str, tuple[str, list[str]]]:
    meta = {}
    for i in range(0, len(ids), 40):
        url = "https://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids[i : i + 40])
        root = ET.fromstring(urllib.request.urlopen(url, timeout=60).read())
        for en in root.findall("a:entry", NS):
            eid = re.search(r"abs/(\d{4}\.\d{4,5})", en.find("a:id", NS).text).group(1)
            meta[eid] = (
                " ".join(en.find("a:title", NS).text.split()),
                [n.find("a:name", NS).text.strip() for n in en.findall("a:author", NS)],
            )
        time.sleep(3)
    return meta


def tex_escape(name: str) -> str:
    repl = {"&": r"\&", "%": r"\%", "_": r"\_"}
    return "".join(repl.get(c, c) for c in name)


def field_span(entry: str, field: str):
    """Return (start, end, value) of a brace-delimited field, handling nesting."""
    m = re.search(rf"\n(\s*){field}\s*=\s*\{{", entry, re.I)
    if not m:
        return None
    i = m.end()
    depth = 1
    while depth and i < len(entry):
        depth += {"{": 1, "}": -1}.get(entry[i], 0)
        i += 1
    return m.start(), i, entry[m.end() : i - 1]


def main(path: str) -> None:
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"(?=\n@)", text)
    targets = []
    for idx, p in enumerate(parts):
        m = ARXIV_RE.search(p)
        if m and re.match(r"\s*@\w+\{", p):
            targets.append((idx, m.group(1) or m.group(2)))
    meta = fetch(sorted({a for _, a in targets}))

    for idx, aid in targets:
        entry = parts[idx]
        key = re.match(r"\s*@\w+\{([^,]+),", entry).group(1)
        if aid not in meta:
            print(f"NOT FOUND {key} {aid}")
            continue
        rtitle, rauth = meta[aid]
        indent = re.search(r"\n(\s*)\w+\s*=", entry).group(1)

        a = field_span(entry, "author")
        if a and not a[2].strip().startswith("{"):
            bib_names = [n for n in re.split(r"\s+and\s+", a[2]) if n.strip()]
            truncated = any(n.strip().lower() == "others" for n in bib_names)
            bib_s = [surname(n) for n in bib_names if n.strip().lower() != "others"]
            real_s = [surname(n) for n in rauth]
            faithful = bib_s == real_s[: len(bib_s)]
            if truncated or not faithful:
                names = [tex_escape(n) for n in rauth[:MAX_AUTHORS]]
                if len(rauth) > MAX_AUTHORS:
                    names.append("others")
                new = " and ".join(names)
                line = entry[a[0] : a[1]]
                newline = re.sub(r"=\s*\{.*\}\s*$", "= {" + new + "}", line, flags=re.S)
                entry = entry[: a[0]] + newline + entry[a[1] :]
                why = "wrong co-authors" if not faithful else "expanded 'and others'"
                print(f"AUTHOR {key}: {why} -> {len(rauth)} authors")

        t = field_span(entry, "title")
        if t:
            tw, rw = set(norm(t[2]).split()), set(norm(rtitle).split())
            if len(tw & rw) / max(1, len(tw | rw)) < 0.8:
                line = entry[t[0] : t[1]]
                newline = re.sub(r"=\s*\{.*\}\s*$", "= {" + tex_escape(rtitle) + "}", line, flags=re.S)
                entry = entry[: t[0]] + newline + entry[t[1] :]
                print(f"TITLE  {key}: '{t[2]}' -> '{rtitle}'")

        if not re.search(r"\beprint\s*=", entry, re.I):
            entry = re.sub(
                r"\n\}\s*$",
                f",\n{indent}eprint = {{{aid}}},\n{indent}archivePrefix = {{arXiv}}\n}}",
                entry.rstrip(),
            ) + "\n"
            entry = re.sub(r",\s*,", ",", entry)
        parts[idx] = entry

    open(path, "w", encoding="utf-8").write("".join(parts))


if __name__ == "__main__":
    main(sys.argv[1])
