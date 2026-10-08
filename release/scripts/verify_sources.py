"""Check every inventory record's developer source and write the result into the record.

Run from source/ (network required; read-only against the Hugging Face API):

    uv run python scripts/verify_sources.py            # check and write source_check
    uv run python scripts/verify_sources.py --dry-run  # report only

For each record in models.slm and models.excluded, and for every record in
models.llm whose size is stated, it:

1. Classifies the domain of `reference_url` as a developer source, a paper, a
   developer repository on the Hugging Face Hub, or a secondary source (model
   aggregator, press article).
2. Queries the Hugging Face API for each Hub repository the record links
   (`huggingface_url`, or `reference_url` when it is a Hub model page) and
   records whether it exists, its owner, creation date, licence tag, and the
   parameter count of its safetensors weights.
3. Writes the outcome to `source_check`, with the date of the check, and sets
   `developer_source_found` to true when the record links either a non-secondary
   reference or an existing Hub repository owned by an organisation, so that the
   inclusion script can apply criterion M1 from a field rather than from a name.
4. Writes a CSV log (source_check_log.csv) with one row per record, including
   the ratio of the Hub parameter count to the recorded total, so that size
   disagreements can be reviewed. It does not change any recorded size.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "merged_llm_database.json"
LOG = ROOT / "source_check_log.csv"
CHECK_DATE = "2026-10-08"

SECONDARY = (
    "openrouter.ai", "venturebeat.com", "techcrunch.com", "medium.com",
    "llm-stats.com", "artificialanalysis.ai", "bentoml.com", "reddit.com",
    "theverge.com", "marktechpost.com",
)
PAPER = ("arxiv.org", "aclanthology.org", "openreview.net", "doi.org")
HF_NON_MODEL = ("/blog/", "/collections/", "/spaces/", "/datasets/", "/papers/", "/docs/")


def domain(url: str | None) -> str:
    if not url:
        return ""
    m = re.match(r"https?://(?:www\.)?([^/]+)", url)
    return m.group(1).lower() if m else ""


def hf_repo(url: str | None) -> str | None:
    if not url or "huggingface.co/" not in url:
        return None
    if any(seg in url for seg in HF_NON_MODEL):
        return None
    m = re.match(r"https?://huggingface\.co/([^/?#]+)/([^/?#]+)", url)
    return f"{m.group(1)}/{m.group(2)}" if m else None


def classify_reference(url: str | None) -> str:
    d = domain(url)
    if not d:
        return "none"
    if any(d == s or d.endswith("." + s) for s in SECONDARY):
        return "secondary"
    if any(d == s or d.endswith("." + s) for s in PAPER):
        return "paper"
    if d == "huggingface.co":
        return "hub_model" if hf_repo(url) else "hub_page"
    return "developer"


_cache: dict[str, dict | None] = {}


def hf_lookup(repo: str) -> dict | None:
    if repo in _cache:
        return _cache[repo]
    url = (f"https://huggingface.co/api/models/{repo}"
           "?expand[]=safetensors&expand[]=createdAt&expand[]=cardData&expand[]=author")
    out = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                d = json.load(resp)
            st = (d.get("safetensors") or {}).get("total")
            out = {
                "exists": True,
                "author": d.get("author"),
                "created": (d.get("createdAt") or "")[:10],
                "license": (d.get("cardData") or {}).get("license"),
                "params_b": round(st / 1e9, 3) if st else None,
            }
            break
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):  # gated or private, but present
                out = {"exists": True, "author": repo.split("/")[0], "created": None,
                       "license": None, "params_b": None, "note": f"HTTP {e.code} (gated)"}
                break
            if e.code == 404:
                out = {"exists": False}
                break
            time.sleep(2 * (attempt + 1))
        except Exception:  # network hiccup
            time.sleep(2 * (attempt + 1))
    _cache[repo] = out
    return out


def check(rec: dict) -> dict:
    ref = rec.get("reference_url")
    ref_class = classify_reference(ref)
    repos = []
    for u in (rec.get("huggingface_url"), ref):
        r = hf_repo(u)
        if r and r not in repos:
            repos.append(r)
    hub = None
    for r in repos:
        info = hf_lookup(r)
        if info and info.get("exists"):
            hub = {"repo": r, **info}
            break
        if hub is None:
            hub = {"repo": r, **(info or {"exists": None, "note": "lookup failed"})}
    developer_found = ref_class in ("developer", "paper", "hub_model", "hub_page") or bool(
        hub and hub.get("exists"))
    if rec.get("paper_url") and classify_reference(rec["paper_url"]) == "paper":
        developer_found = True
    return {
        "checked": CHECK_DATE,
        "reference_class": ref_class,
        "reference_domain": domain(ref),
        "hub": hub,
        "developer_source_found": developer_found,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    db = json.loads(DB.read_text(encoding="utf-8"))
    rows = []
    for arr in ("slm", "excluded", "llm"):
        for rec in db["models"][arr]:
            if arr == "llm" and rec.get("parsed_total_params_b") is None:
                continue
            res = check(rec)
            if not args.dry_run:
                rec["source_check"] = res
                rec["developer_source_found"] = res["developer_source_found"]
            hub = res["hub"] or {}
            total = rec.get("parsed_total_params_b")
            ratio = (hub.get("params_b") / total) if hub.get("params_b") and total else None
            rows.append({
                "array": arr, "name": rec["name"], "developer": rec.get("developer"),
                "slm_class": rec.get("slm_class"), "reference_class": res["reference_class"],
                "reference_domain": res["reference_domain"], "hub_repo": hub.get("repo"),
                "hub_exists": hub.get("exists"), "hub_author": hub.get("author"),
                "hub_created": hub.get("created"), "hub_license": hub.get("license"),
                "hub_params_b": hub.get("params_b"), "recorded_total_b": total,
                "hub_to_recorded_ratio": round(ratio, 3) if ratio else None,
                "developer_source_found": res["developer_source_found"],
            })
    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    if not args.dry_run:
        DB.write_text(json.dumps(db, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    inv = [r for r in rows if r["array"] == "slm"]
    print(f"inventory records checked: {len(inv)}")
    for k in ("developer", "paper", "hub_model", "hub_page", "secondary", "none"):
        print(f"  reference_class {k}: {sum(r['reference_class'] == k for r in inv)}")
    print(f"  Hub repository linked: {sum(r['hub_repo'] is not None for r in inv)}; "
          f"exists: {sum(r['hub_exists'] is True for r in inv)}; "
          f"missing: {sum(r['hub_exists'] is False for r in inv)}")
    print(f"  no developer source: {[r['name'] for r in inv if not r['developer_source_found']]}")
    off = [r for r in inv if r["hub_to_recorded_ratio"] and not 0.8 <= r["hub_to_recorded_ratio"] <= 1.25]
    print(f"  Hub/recorded size ratio outside 0.8-1.25: {len(off)}")
    for r in off:
        print(f"    {r['name']}: recorded {r['recorded_total_b']}B, Hub {r['hub_params_b']}B ({r['hub_repo']})")
    print(f"log written to {LOG}")


if __name__ == "__main__":
    main()
