"""Build the benchmark-coverage ledger for the vendor-record audit (Section 5).

Run from source/:

    uv run python scripts/build_audit_ledger.py

Scope. The 14 cohort models from the four vendors that account for most of the
cohort (Microsoft Phi, Alibaba Qwen2.5, Meta Llama 3.2, Google Gemma 2 and 3), at
the instruction-tuned (IT) checkpoint, against the eight benchmarks that recur in
their headline reporting. Each cell records whether the model's primary release
document reports an IT value and, if so, under which stated protocol. Cells were
transcribed by the authors from the documents and locations listed in SOURCES,
retrieved on 2026-10-08; scores are not transcribed, only coverage and protocol.

Protocol codes: "5" = 5-shot, "8+CoT" = 8-shot chain-of-thought, "0+CoT" =
zero-shot chain-of-thought, "SE" = OpenAI simple-evals defaults, "unstated" = an
IT value is reported but the document gives no shot count for it, "" = not
reported.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "audit_coverage_ledger.csv"
BENCH = ["MMLU", "MMLU-Pro", "ARC-C", "HellaSwag", "GSM8K", "MATH", "HumanEval", "MBPP"]

SOURCES = {
    "Phi-3-mini": "Phi-3-mini-4k-instruct model card, benchmark table (huggingface.co/microsoft/Phi-3-mini-4k-instruct)",
    "Phi-3.5-mini": "Phi-3.5-mini-instruct model card, benchmark table (huggingface.co/microsoft/Phi-3.5-mini-instruct)",
    "Phi-4-mini": "Phi-4-mini-instruct model card, benchmark table (huggingface.co/microsoft/Phi-4-mini-instruct)",
    "Phi-4": "phi-4 model card, simple-evals table (huggingface.co/microsoft/phi-4)",
    "Qwen2.5": "Qwen2.5 Technical Report (arXiv:2412.15115), instruction-tuned tables for 0.5B-7B",
    "Llama 3.2": "Llama 3.2 model card, instruction-tuned table (github.com/meta-llama/llama-models, models/llama3_2/MODEL_CARD.md)",
    "Gemma 2": "Gemma 2 report (arXiv:2408.00118), PT/IT comparison table",
    "Gemma 3": "Gemma 3 Technical Report (arXiv:2503.19786), Tables 6 and 18 (IT) with protocol Table 21",
}

ROWS = {
    # model: (source key, separate PT table in the same document?, {benchmark: protocol})
    "Phi-3-mini": ("Phi-3-mini", False, {"MMLU": "5", "ARC-C": "10", "HellaSwag": "5",
                                          "GSM8K": "8+CoT", "HumanEval": "0", "MBPP": "3"}),
    "Phi-3.5-mini": ("Phi-3.5-mini", False, {"MMLU": "5", "MMLU-Pro": "0+CoT", "ARC-C": "10",
                                              "HellaSwag": "5", "GSM8K": "8+CoT", "MATH": "0+CoT",
                                              "HumanEval": "0", "MBPP": "3"}),
    "Phi-4-mini": ("Phi-4-mini", False, {"MMLU": "5", "MMLU-Pro": "0+CoT", "ARC-C": "10",
                                          "HellaSwag": "5", "GSM8K": "8+CoT", "MATH": "0+CoT"}),
    "Phi-4": ("Phi-4", False, {"MMLU": "SE", "MATH": "SE", "HumanEval": "SE"}),
    **{f"Qwen2.5-{s}": ("Qwen2.5", True, {"MMLU-Pro": "unstated", "GSM8K": "unstated",
                                          "MATH": "unstated", "HumanEval": "unstated",
                                          "MBPP": "unstated"})
       for s in ("0.5B", "1.5B", "3B", "7B")},
    **{f"Llama 3.2-{s}": ("Llama 3.2", True, {"MMLU": "5", "ARC-C": "0", "HellaSwag": "0",
                                              "GSM8K": "8+CoT", "MATH": "0+CoT"})
       for s in ("1B", "3B")},
    **{f"Gemma 2-{s}": ("Gemma 2", True, {"MMLU": "unstated", "MBPP": "unstated"})
       for s in ("2B", "9B")},
    **{f"Gemma 3-{s}": ("Gemma 3", True, {"MMLU": "0", "MMLU-Pro": "0", "GSM8K": "0+CoT",
                                          "MATH": "0", "HumanEval": "0", "MBPP": "3"})
       for s in ("1B", "4B")},
}


def main() -> None:
    rows = []
    for model, (src, pt_sep, cells) in ROWS.items():
        for b in BENCH:
            rows.append({"model": model, "checkpoint": "instruction-tuned", "benchmark": b,
                         "reported": "yes" if b in cells else "no", "protocol": cells.get(b, ""),
                         "pt_reported_separately": "yes" if pt_sep else "no",
                         "source": SOURCES[src], "retrieved": "2026-10-08"})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n_models = len(ROWS)
    reported = [r for r in rows if r["reported"] == "yes"]
    stated = [r for r in reported if r["protocol"] != "unstated"]
    print(f"models {n_models}, benchmarks {len(BENCH)}, cells {len(rows)}")
    print(f"cells with an IT value: {len(reported)}; with a stated protocol: {len(stated)}")
    print(f"models whose vendor tabulates PT separately: "
          f"{sum(1 for v in ROWS.values() if v[1])}")
    best = 0
    for b in BENCH:
        rb = [r for r in reported if r["benchmark"] == b]
        protos = Counter(r["protocol"] for r in rb if r["protocol"] != "unstated")
        top = protos.most_common(1)[0] if protos else ("-", 0)
        best = max(best, top[1])
        print(f"  {b:10s} reported {len(rb):2d}/{n_models}; stated {sum(protos.values()):2d}; "
              f"largest single-protocol group {top[1]} ({top[0]}); protocols {dict(protos)}")
    every = [b for b in BENCH if all(any(r['model'] == m and r['benchmark'] == b and r['reported'] == 'yes'
                                         for r in rows) for m in ROWS)]
    print(f"benchmarks reported for all {n_models} models: {every or 'none'}")
    print(f"largest group of models sharing one stated protocol on any benchmark: {best}")
    write_latex(rows)


CODE = {"": "--", "unstated": "u", "SE": "SE", "0+CoT": "0c", "8+CoT": "8c"}


def write_latex(rows: list[dict]) -> None:
    """Emit the ledger as a LaTeX table for the supplement (partials/)."""
    out = Path(__file__).resolve().parent.parent.parent / "journal" / "partials" / "audit_coverage_ledger.tex"
    cell = {(r["model"], r["benchmark"]): CODE.get(r["protocol"], r["protocol"]) for r in rows}
    bs = "\\"
    lines = [
        "% Generated by source/scripts/build_audit_ledger.py; do not edit by hand.",
        bs + "begin{table}[t]",
        bs + "centering",
        bs + "caption{Coverage ledger for the instruction-tuned checkpoints of the 14 cohort models from the four largest vendors: "
        "the protocol under which each model's primary release document reports each benchmark. Numbers are shot counts; "
        "``c'' marks chain-of-thought; ``SE'' OpenAI simple-evals defaults; ``u'' a value reported without a stated protocol; "
        "``--'' not reported. Sources and locations are listed in " + bs + "file{audit" + bs + "_coverage" + bs + "_ledger.csv}; "
        "transcribed on 8~October 2026.}",
        bs + "label{tab:audit_ledger}",
        bs + "footnotesize",
        bs + "begin{tabular}{l" + "c" * len(BENCH) + "}",
        bs + "toprule",
        bs + "textbf{Model} & " + " & ".join(bs + "textbf{" + b + "}" for b in BENCH) + " " + bs + bs,
        bs + "midrule",
    ]
    for m in ROWS:
        lines.append(m + " & " + " & ".join(cell[(m, b)] for b in BENCH) + " " + bs + bs)
    rep = [r for r in rows if r["reported"] == "yes"]
    lines.append(bs + "midrule")
    lines.append("Reported (of 14) & " + " & ".join(
        str(sum(1 for r in rep if r["benchmark"] == b)) for b in BENCH) + " " + bs + bs)
    lines += [bs + "bottomrule", bs + "end{tabular}", bs + "end{table}", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"LaTeX table written to {out}")


if __name__ == "__main__":
    main()
