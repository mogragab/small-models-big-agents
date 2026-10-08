"""Record-level corrections for inventory version 3.6 (2026-10-08).

Run once from source/, before verify_sources.py and apply_inclusion_rules.py:

    uv run python scripts/fix_records_v3_6.py

Each correction is listed explicitly with the source it was checked against, so
that it can be reviewed. The script is idempotent: re-running it leaves an
already-corrected record unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "merged_llm_database.json"
CHECK_DATE = "2026-10-08"

# Records whose only reference was a model aggregator or a press article. Each
# links a developer-owned repository on the Hugging Face Hub (existence checked
# through the Hub API on CHECK_DATE), which becomes the reference; the
# aggregator URL is kept in `discovered_via`.
RESOURCE_TO_HUB = {
    "DeepSeek V4 Flash Vision Exp": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp",
    "DeepSeek V4 Flash 0731": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731",
    "Inkling Small": "https://huggingface.co/thinkingmachines/Inkling-Small",
    "Ling 3.0 Flash": "https://huggingface.co/inclusionAI/Ling-3.0-flash",
    "Laguna S 2.1": "https://huggingface.co/poolside/Laguna-S-2.1",
    "Laguna XS 2.1": "https://huggingface.co/poolside/Laguna-XS-2.1",
    "North Mini Code 1.0": "https://huggingface.co/CohereLabs/North-Mini-Code-1.0",
    "Nex-N2-Pro": "https://huggingface.co/nex-agi/Nex-N2-Pro",
    "Granite 4.0 Nano 350M": "https://huggingface.co/ibm-granite/granite-4.0-nano-350m",
    "Granite 4.0 Nano 1B": "https://huggingface.co/ibm-granite/granite-4.0-nano-1b",
    # Previously aggregator-only; developer repositories located on the Hub.
    "Ling 3.0 Flash Fin": "https://huggingface.co/inclusionAI/Ling-3.0-flash-Fin",
    "Dots3-Note Preview": "https://huggingface.co/dots-studio/dots3-note-prev",
}

FIELD_FIXES = {
    # Open weights under MIT on the Hub, not API-only as recorded.
    "Ling 3.0 Flash Fin": {"access": "OW", "license": "MIT",
                           "huggingface_url": "https://huggingface.co/inclusionAI/Ling-3.0-flash-Fin"},
    "Dots3-Note Preview": {"license": "Apache 2.0",
                           "huggingface_url": "https://huggingface.co/dots-studio/dots3-note-prev"},
    # The three SmolLM2 records linked the SmolLM3-3B page.
    "SmolLM2-360M-Instruct": {"reference_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct",
                              "release_date": "2024-10-31"},
    "SmolLM2-135M": {"reference_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-135M",
                     "release_date": "2024-10-31"},
    "SmolLM2-1.7B-Instruct": {"reference_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct",
                              "release_date": "2024-10-31"},
    # v0.3 is the May 2024 checkpoint (Hub repository created 2024-05-22).
    "Mistral 7B v0.3": {"release_date": "2024-05-22",
                        "huggingface_url": "https://huggingface.co/mistralai/Mistral-7B-v0.3"},
    # Granite 4.1 linked the Granite 4.2 blog post.
    "Granite 4.1 8B": {"reference_url": "https://huggingface.co/ibm-granite/granite-4.1-8b",
                       "huggingface_url": "https://huggingface.co/ibm-granite/granite-4.1-8b"},
    "Granite 4.1 3B": {"reference_url": "https://huggingface.co/ibm-granite/granite-4.1-3b",
                       "huggingface_url": "https://huggingface.co/ibm-granite/granite-4.1-3b"},
}

# The 2024 BitNet b1.58 paper released no weights; the record linked the 2025
# 2B4T checkpoint. The record now describes the released artifact
# (arXiv:2504.12285, "BitNet b1.58 2B4T Technical Report", 16 April 2025).
BITNET = {
    "name": "BitNet b1.58 2B4T",
    "release_date": "2025-04-16",
    "parameters": {"total": "2B", "active_per_token": "2B", "is_moe": False},
    "reference_url": "https://huggingface.co/microsoft/bitnet-b1.58-2B-4T",
    "huggingface_url": "https://huggingface.co/microsoft/bitnet-b1.58-2B-4T",
    "paper_url": "https://arxiv.org/abs/2504.12285",
    "license": "MIT",
    "source_note": "Corrected in v3.6: the 2024 paper (arXiv:2402.17764) released no weights; "
                   "this record is the 2025 2B4T release that the record's Hub link pointed to.",
}

# Voxtral Mini was excluded as undisclosed and tagged API, with a Hub link to
# Mistral Small 3.1. The open-weight Voxtral Mini 3B (Apache 2.0) is documented
# by Mistral's announcement, its model card and arXiv:2507.13264; the Hub
# safetensors count is 4.68B (3B language decoder plus audio encoder).
VOXTRAL = {
    "name": "Voxtral Mini 3B",
    "developer": "Mistral AI",
    "release_date": "2025-07-15",
    "access": "OW",
    "parameters": {"total": "4.7B", "active_per_token": "4.7B", "is_moe": False},
    "modalities": ["text", "audio"],
    "license": "Apache 2.0",
    "reference_url": "https://mistral.ai/news/voxtral",
    "huggingface_url": "https://huggingface.co/mistralai/Voxtral-Mini-3B-2507",
    "paper_url": "https://arxiv.org/abs/2507.13264",
    "source_note": "Corrected in v3.6: previously excluded as undisclosed with a wrong Hub link. "
                   "Total is the Hub safetensors count (3B language decoder plus audio encoder).",
}

FAMILY_LINK_FIXES = {
    "Command": "https://cohere.com/blog/command-r7b",
    "DeepSeek": "https://huggingface.co/deepseek-ai",
    "Granite": "https://huggingface.co/ibm-granite",
}


def main() -> None:
    db = json.loads(DB.read_text(encoding="utf-8"))
    every = [r for arr in db["models"].values() for r in arr]
    by_name = {r["name"]: r for r in every}
    log = []

    for name, hub in RESOURCE_TO_HUB.items():
        r = by_name.get(name)
        if r is None:
            continue
        old = r.get("reference_url")
        if old != hub:
            r.setdefault("discovered_via", old)
            r["reference_url"] = hub
            r["huggingface_url"] = r.get("huggingface_url") or hub
            r["source_retrieved"] = CHECK_DATE
            log.append(f"{name}: reference {old} -> {hub}")

    for name, fix in FIELD_FIXES.items():
        r = by_name.get(name)
        if r is None:
            continue
        for k, v in fix.items():
            if r.get(k) != v:
                log.append(f"{name}: {k} {r.get(k)!r} -> {v!r}")
                r[k] = v
        r["source_retrieved"] = CHECK_DATE

    for old_name, new in (("BitNet b1.58", BITNET), ("Voxtral Mini", VOXTRAL)):
        r = by_name.get(old_name) or by_name.get(new["name"])
        if r is None:
            continue
        for k, v in new.items():
            if r.get(k) != v:
                log.append(f"{old_name}: {k} -> {v!r}")
                r[k] = v
        r["source_retrieved"] = CHECK_DATE

    for fam in db["families"]:
        if fam["name"] in FAMILY_LINK_FIXES and fam["url"] != FAMILY_LINK_FIXES[fam["name"]]:
            log.append(f"family {fam['name']}: {fam['url']} -> {FAMILY_LINK_FIXES[fam['name']]}")
            fam["url"] = FAMILY_LINK_FIXES[fam["name"]]

    # Date precision is recorded rather than guessed.
    import re
    for r in every:
        d = str(r.get("release_date") or "")
        r["release_date_precision"] = ("day" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) else
                                       "month" if re.fullmatch(r"\d{4}-\d{2}", d) else
                                       "year" if re.fullmatch(r"\d{4}", d) else "none")

    db["metadata"].setdefault("record_corrections_v3_6", log)
    DB.write_text(json.dumps(db, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n".join(log) or "no changes")


if __name__ == "__main__":
    main()
