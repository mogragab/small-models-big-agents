"""Apply the paper's inclusion rule to every record in the inventory.

Version 3.6 of merged_llm_database.json. Run from source/, after
scripts/fix_records_v3_6.py and scripts/verify_sources.py:

    uv run python scripts/apply_inclusion_rules.py

What is computed from fields and what is an editorial decision:

- Computed from fields: C1 and C2 (from the parsed parameter counts), M1 (from
  `developer_source_found`, written by verify_sources.py, and from whether a
  size is stated), and M4 (from `release_date_precision`).
- Named editorial decisions, listed below so each can be reviewed: the
  encoder-decoder exclusion, the derivative-artifact exclusions, and the
  duplicate (API alias) exclusion. They are applied by name, not detected.

What it does, in order:

1. Re-parses every record's parameter counts. Legacy records nest
   {total_params, active_params} under both `parameters.total` and
   `parameters.active_per_token`; the 3.3/3.4 scripts read `total_params` for
   both, so a nested MoE's active count silently became its total and five
   small-active MoEs (Mixtral-8x7B, Phi-3.5-MoE, Qwen2-57B-A14B, Snowflake
   Arctic, Nemotron 3 Nano-30B) were classed as LLMs. This parser reads
   `active_params` for the active count.
2. Treats per-layer-embedding "effective" sizes (Gemma 3n, Gemma 4 E2B/E4B) as
   what they are: not sparse activation. C1 is evaluated on the total count and
   the effective count is kept in `parameters.effective_note`.
3. Recomputes C1 / C2 / slm_class for every record.
4. Applies the model-variant inclusion criteria of Section 1.6.3 and records
   the outcome per record in `inclusion_decision`:
     - architecture: C1 admits autoregressive decoder-only models (attention,
       state-space, or hybrid). Encoder-decoder models are excluded.
     - M1: a primary source must describe the architecture. Records whose
       parameter counts are undisclosed fail it.
     - derivative artifacts: fine-tunes of another party's checkpoint released
       without a technical report describing their own training recipe.
     - duplicates: API aliases of a checkpoint already listed.
5. Rebuilds the arrays: models.slm holds included records of class "slm" or
   "small-active-moe"; models.llm holds records failing C1; models.excluded
   holds records removed by an inclusion criterion, with the reason.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "merged_llm_database.json"
THRESHOLD_B = 20.0
VERSION = "3.6"
DATE = "2026-10-08"

# Inclusion decisions that cannot be computed from fields, named explicitly so
# each is reviewable.
ENCODER_DECODER = {"Flan-T5"}
DERIVATIVE = {
    "Nous Hermes 2 Mixtral": "community fine-tune of Mixtral-8x7B; no technical report",
    "Vicuna-7B v1.5": "LMSYS fine-tune of Llama 2 on shared conversations; no technical report for the model",
    "Vicuna-13B": "LMSYS fine-tune of LLaMA on shared conversations; no technical report for the model",
    "Jan-v1-4B": "fine-tune of Qwen3-4B; no technical report",
}
DUPLICATE = {
    "Mistral Tiny (Mistral-7B-Instruct)": "API alias of the Mistral 7B instruct checkpoint already listed",
}
EFFECTIVE_PARAM_MODELS = {"Gemma 4 E2B", "Gemma 4 E4B", "Gemma-3n-E2B-IT", "Gemma-3n-E4B-IT"}


def parse_b(v, prefer: str = "total_params") -> float | None:
    """Parse '7B', '~5B', '350M', '2.4T', or a nested legacy dict, to billions."""
    if v is None:
        return None
    if isinstance(v, dict):
        return parse_b(v.get(prefer) if v.get(prefer) is not None else v.get("total_params"))
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v)
    if re.search(r"undisclosed|unknown|n/a|proprietary", s, re.I):
        return None
    nums = re.findall(r"([\d.]+)\s*([BTM])", s, re.I)
    if not nums:
        return None
    # For a range such as "1-4B" take the upper bound.
    m = re.search(r"([\d.]+)\s*-\s*([\d.]+)\s*([BTM])", s, re.I)
    n, unit = (float(m.group(2)), m.group(3)) if m else (float(nums[0][0]), nums[0][1])
    unit = unit.upper()
    return n * 1000 if unit == "T" else n / 1000 if unit == "M" else n


def classify(rec: dict) -> None:
    p = rec.setdefault("parameters", {})
    total = parse_b(p.get("total"), "total_params")
    active = parse_b(p.get("active_per_token"), "active_params")
    if rec["name"] in EFFECTIVE_PARAM_MODELS:
        if "effective" in str(p.get("active_per_token", "")):
            p["effective_note"] = (
                f"Vendor-stated effective size {p['active_per_token']} reflects per-layer "
                "embeddings held off-accelerator, not sparse activation; C1 uses the total."
            )
            p["active_per_token"] = p.get("total")
        p["is_moe"] = False
        active = total
    is_moe = bool(p.get("is_moe")) or (
        total is not None and active is not None and active < total * 0.9
    )
    if active is None and not is_moe:
        active = total
    c1 = None if active is None else active <= THRESHOLD_B
    c2 = None if total is None else total <= THRESHOLD_B
    if c1 is None and c2 is None:
        cls = "undisclosed"
    elif c1 is False:
        cls = "llm"
    elif c1 and c2:
        cls = "slm"
    elif c1 and c2 is False:
        cls = "small-active-moe"
    else:
        cls = "undisclosed"
    rec["meets_c1_active_le_20b"] = c1
    rec["meets_c2_total_le_20b"] = c2
    rec["slm_class"] = cls
    rec["parsed_total_params_b"] = total
    rec["parsed_active_params_b"] = active


def decide(rec: dict) -> tuple[str, str]:
    """Return (array, inclusion_decision).

    Every record of undisclosed size is treated alike, whatever its marketing:
    it cannot be classified against C1 or C2, so it is kept in models.llm with
    slm_class "undisclosed" as part of the comparison set and is never plotted
    or counted as a large model.
    """
    name = rec["name"]
    if name in ENCODER_DECODER:
        return "excluded", "excluded: encoder-decoder architecture (outside C1)"
    if name in DUPLICATE:
        return "excluded", f"excluded: duplicate ({DUPLICATE[name]})"
    if name in DERIVATIVE:
        return "excluded", f"excluded: derivative artifact ({DERIVATIVE[name]})"
    cls = rec["slm_class"]
    if cls == "undisclosed":
        return "llm", "comparison set: parameter count undisclosed (cannot be classified against C1 or C2)"
    if cls in ("slm", "small-active-moe") and rec.get("developer_source_found") is False:
        return "excluded", ("excluded: M1 (no developer source located; the only reference is "
                            "a model aggregator or press article)")
    if cls in ("slm", "small-active-moe") and rec.get("release_date_precision") == "none":
        return "excluded", "excluded: M4 (no dated release)"
    if cls == "llm":
        return "llm", "out of scope: fails C1 (active parameters above 20B)"
    if cls == "small-active-moe":
        return "slm", "included: small-active-parameter MoE (meets C1, not C2)"
    return "slm", "included: SLM (meets C1 and C2)"


def main() -> None:
    db = json.loads(DB.read_text(encoding="utf-8"))
    models = db["models"]
    before = {k: [m["name"] for m in v] for k, v in models.items()}
    every = models.get("slm", []) + models.get("llm", []) + models.get("excluded", [])
    out = {"slm": [], "llm": [], "excluded": []}
    for rec in every:
        classify(rec)
        arr, why = decide(rec)
        rec["inclusion_decision"] = why
        out[arr].append(rec)

    key = lambda m: (str(m.get("release_date") or ""), m["name"])
    for arr in out.values():
        arr.sort(key=key, reverse=True)

    moved = {
        "into_slm": sorted(set(m["name"] for m in out["slm"]) - set(before.get("slm", []))),
        "out_of_slm": sorted(set(before.get("slm", [])) - set(m["name"] for m in out["slm"])),
    }
    db["models"] = out

    counts = {}
    for m in out["slm"]:
        counts[m["slm_class"]] = counts.get(m["slm_class"], 0) + 1
    meta = db["metadata"]
    meta["version"] = VERSION
    meta["total_slm_variants"] = len(out["slm"])
    meta["total_slm_strict"] = counts.get("slm", 0)
    meta["total_small_active_moe"] = counts.get("small-active-moe", 0)
    meta["total_llm_variants"] = len(out["llm"])
    meta["total_excluded"] = len(out["excluded"])
    meta["total_models"] = sum(len(v) for v in out.values())
    meta["classification_rules"]["array_placement"] = (
        "models.slm holds every included record meeting C1 (class 'slm' when C2 also holds, "
        "'small-active-moe' when it does not). models.llm holds records failing C1. "
        "models.excluded holds records removed by an inclusion criterion (architecture, M1, "
        "derivative artifact, duplicate); each record's inclusion_decision states why. "
        "C1, C2, M1 (developer_source_found, stated size) and M4 (release_date_precision) are "
        "computed from fields by scripts/apply_inclusion_rules.py; the encoder-decoder, "
        "derivative and duplicate exclusions are named editorial decisions listed in that script. "
        "Records of undisclosed size are kept in models.llm with slm_class 'undisclosed'."
    )
    meta["classification_rules"]["C1"] = (
        "meets_c1_active_le_20b: autoregressive decoder-only model (attention, state-space, "
        "or hybrid) with active parameters per token <= 20B."
    )
    meta["changelog"].append(
        {
            "date": DATE,
            "version": VERSION,
            "summary": (
                "Source verification and record corrections. Every inventory record's developer "
                "source checked against the Hugging Face Hub API (source_check, "
                "developer_source_found); 12 aggregator- or press-only references replaced by the "
                "developer's Hub repository; Ling 3.0 Flash Sante excluded under M1 (no developer "
                "source); Voxtral Mini corrected to the open-weight Voxtral Mini 3B and included; "
                "BitNet b1.58 corrected to the released 2B4T checkpoint; SmolLM2, Mistral 7B v0.3 "
                "and Granite 4.1 sources and dates fixed; undisclosed-size records all kept in the "
                "comparison set with slm_class 'undisclosed' instead of by prior placement."
            ),
            "moved_into_slm_names": moved["into_slm"],
            "moved_out_of_slm_names": moved["out_of_slm"],
            "counts": {
                "slm": counts.get("slm", 0),
                "small_active_moe": counts.get("small-active-moe", 0),
                "llm": len(out["llm"]),
                "excluded": len(out["excluded"]),
            },
        }
    )
    DB.write_text(json.dumps(db, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"slm array: {len(before.get('slm', []))} -> {len(out['slm'])}  {counts}")
    print(f"llm array: {len(before.get('llm', []))} -> {len(out['llm'])}")
    print(f"excluded: {len(out['excluded'])}")
    print("moved into slm:", moved["into_slm"])
    print("moved out of slm:", moved["out_of_slm"])
    for m in out["excluded"]:
        print(f"  {m['name']}: {m['inclusion_decision']}")


if __name__ == "__main__":
    main()
