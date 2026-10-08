# Released artifacts: A Survey of Small Language Models for Agentic AI

Supplementary files for the ACM Computing Surveys submission. Inventory version
3.6, releases through 4 September 2026, source checks dated 8 October 2026.

## Files

| File | Contents |
|---|---|
| `merged_llm_database.json` | The variant inventory. `models.slm` holds the 209 inventory records (179 with `slm_class = "slm"`, 30 with `"small-active-moe"`); `models.llm` holds 223 comparison records (104 `"llm"`, 119 `"undisclosed"`); `models.excluded` holds 7 excluded records. Every record carries `meets_c1_active_le_20b`, `meets_c2_total_le_20b`, `slm_class`, `inclusion_decision`, `developer_source_found`, `source_check`, and `release_date_precision`. `metadata.changelog` names every record added, moved, or removed per version; `metadata.record_corrections_v3_6` lists the version-3.6 corrections. |
| `source_check_log.csv` | One row per checked record: reference class, Hugging Face Hub repository, whether it exists, owner, creation date, licence, Hub parameter count, and its ratio to the recorded total. |
| `audit_coverage_ledger.csv` | The coverage ledger of the evaluation audit: for 14 cohort models x 8 benchmarks, whether the primary release document reports an instruction-tuned value, under which stated protocol, and the source document. Coverage only; no scores. |
| `scripts/fix_records_v3_6.py` | The explicit record corrections of version 3.6, each with the source it was checked against. |
| `scripts/verify_sources.py` | Checks every record's developer source against the Hugging Face Hub API (network required) and writes `source_check` and the log. |
| `scripts/apply_inclusion_rules.py` | Computes C1, C2, M1, M4 from fields, applies the named editorial exclusions, and rebuilds the arrays. |
| `scripts/build_audit_ledger.py` | Writes the coverage ledger CSV and prints its summary counts. |
| `scripts/generate_model_tables.py`, `scripts/generate_figures_v2.py` | Generate the inventory tables and every inventory figure in the paper. |

## Reproducing

With [uv](https://docs.astral.sh/uv/) and Python 3.14, from this folder:

```
uv run python scripts/build_audit_ledger.py           # ledger summary (69 of 112 cells; max 5 sharing a protocol)
uv run python scripts/generate_figures_v2.py --input merged_llm_database.json --output-dir figures --format png
uv run python scripts/generate_model_tables.py --input merged_llm_database.json --output-dir partials
```

The scripts expect to sit in `scripts/` beside `merged_llm_database.json`.
`build_audit_ledger.py` also writes a LaTeX table to the paper's `partials/`
folder when run inside the manuscript repository. Re-running
`verify_sources.py` queries the live Hub and may return different results as
repositories change; the released log records the state on 8 October 2026.
Re-running `fix_records_v3_6.py` and `apply_inclusion_rules.py` on the released
file is idempotent apart from appending a changelog entry.
