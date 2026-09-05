#!/usr/bin/env python3
"""Generate paper-oriented figures from merged_llm_database.json (v2).

Improvements over v1:
- Generates separate SLM and LLM figure sets
- MoE vs Dense split into proper subplots with independent y-axes
- Context evolution uses max-per-date-per-family for cleaner trends
- Bar charts have y-axis padding to prevent clipped text labels
- Cumulative releases overlays both SLM and LLM lines
- Heatmap suppresses "0" text for cleaner visuals
- Box plots fall back to strip plots when n < 5
- Legends positioned to avoid data overlap
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Palette & colour constants
# ---------------------------------------------------------------------------

# Palette rebuilt September 2026. The previous set was chosen by eye and was not
# colour-vision-deficiency safe; several pairs that carried meaning (teal/mint,
# coral/peach, amber/sand) collapsed under deuteranopia and again in greyscale
# print. This one is validated: every categorical set below clears the adjacent-
# pair CVD floor (OKLab dE >= 8) and the normal-vision floor (dE >= 15) against a
# white surface, and every ordered set is a single hue, monotone in lightness,
# with adjacent dL >= 0.06 and the light end clearing 2:1 against white.
#
# Two rules drive the assignments further down, and they are the substantive
# change rather than the hexes:
#   * Ordered quantities (release year, parameter band, context bucket) get a
#     single-hue ramp, light to dark. They were previously categorical, which
#     asked the reader to learn an arbitrary colour order for data that has a
#     natural one.
#   * Only genuinely nominal quantities (access mode, licence posture, base vs
#     instruct, MoE vs dense) get distinct hues, and never more than three plus
#     a neutral.

PALETTE = {
    # Categorical hues, in fixed assignment order. Never cycled; a fourth
    # nominal category folds into "other" rather than taking a generated hue.
    "blue":      "#2A78D6",
    "orange":    "#EB6834",
    "aqua":      "#1BAF7A",
    "violet":    "#4A3AA7",
    "red":       "#E34948",

    # Single-hue ordinal ramp, light to dark. Five usable steps on white: six
    # cannot hold both the lightness-gap floor and the light-end contrast floor.
    "seq1":      "#86B6EF",
    "seq2":      "#5598E7",
    "seq3":      "#2A78D6",
    "seq4":      "#1C5CAB",
    "seq5":      "#104281",

    # Neutral, for "unknown" and "not reported". Deliberately low chroma so it
    # never reads as one of the meaningful categories.
    "slate":     "#7E8C9A",

    # Utility
    "ink":       "#1F2933",
    "fog":       "#E4EAEE",
    "cloud":     "#FBFCFD",
    "mist":      "#D6DFE5",
}

# Fallback sequence for charts whose category set is data-driven (families,
# developers) and therefore not known in advance. Fixed order, never cycled:
# past the fifth entry the chart is expected to fold the tail into "Other"
# rather than invent a hue, which is what the top-N cutoffs below do.
SOFT_SEQUENCE = [
    PALETTE["blue"], PALETTE["orange"], PALETTE["aqua"],
    PALETTE["violet"], PALETTE["red"], PALETTE["slate"],
]

# Continuous magnitude: one hue, light to dark, lightest step near the surface.
SOFT_HEATMAP = [
    [0.0, PALETTE["cloud"]],
    [0.2, "#CDE2FB"],
    [0.4, PALETTE["seq1"]],
    [0.6, PALETTE["seq3"]],
    [0.8, PALETTE["seq4"]],
    [1.0, "#0D366B"],
]

# Centralized colour maps ------------------------------------------------
#
# Ordered quantities use the single-hue ramp. Parameter band and context bucket
# each have one out-of-range category (">20B" is above the SLM threshold
# entirely) that takes the orange accent instead of a sixth ramp step: it is a
# different kind of value, not the next step up, and a five-step ramp is the
# most a single hue supports on white while keeping the steps apart.

BUCKET_COLORS = {
    "<1B": PALETTE["seq1"], "1-3B": PALETTE["seq2"], "3-7B": PALETTE["seq3"],
    "7-10B": PALETTE["seq4"], "10-20B": PALETTE["seq5"],
    ">20B": PALETTE["orange"], "Unknown": PALETTE["slate"],
}

YEAR_COLORS = {
    "2022": PALETTE["seq1"], "2023": PALETTE["seq2"], "2024": PALETTE["seq3"],
    "2025": PALETTE["seq4"], "2026": PALETTE["seq5"],
}

CONTEXT_BUCKET_COLORS = {
    "<=4K": PALETTE["seq1"], "8K": PALETTE["seq2"], "16K-32K": PALETTE["seq3"],
    "64K-128K": PALETTE["seq4"], ">128K": PALETTE["seq5"],
    "Unknown": PALETTE["slate"],
}

# Nominal quantities: distinct hues, at most three plus a neutral.

STATUS_COLORS = {
    "Active": PALETTE["blue"], "Legacy": PALETTE["orange"],
    "Deprecated": PALETTE["red"], "Unknown": PALETTE["slate"],
}

ACCESS_COLORS = {
    "OW": PALETTE["blue"], "Both": PALETTE["orange"], "API": PALETTE["aqua"],
}

LICENSE_COLORS = {
    "Permissive open": PALETTE["blue"], "Custom/source-available": PALETTE["orange"],
    "Proprietary": PALETTE["aqua"], "Other open": PALETTE["violet"],
    "Unspecified": PALETTE["slate"], "Unknown": PALETTE["slate"],
}


def color_with_alpha(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ---------------------------------------------------------------------------
# Layout & theme constants
# ---------------------------------------------------------------------------

DEFAULT_TEMPLATE = "plotly_white"

# Figure text is set in Libertinus Serif so that it matches the manuscript body
# font exactly rather than approximating it: both builds now load Libertinus,
# and a figure in a different serif is visible on the page. The renderer is
# headless Chrome via kaleido, which resolves fonts by family name from the
# system, so Libertinus must be installed as a system font and not only as a
# LaTeX package. The fallbacks cover a machine where it is not: Linux Libertine
# is the metric-compatible predecessor, then generic serif.
FIGURE_FONT = "Libertinus Serif, Linux Libertine O, Linux Libertine, Libertinus Serif Display, serif"

# On-page figure-text size is governed by (plotly font size) x 644 / (width in px);
# a narrower native canvas is scaled down less at \linewidth, so text lands
# a little larger than the 10 pt body.
#
# scale=4 against the ~780px canvases below puts the raster figures at roughly
# 3100px on the long edge, which is about 400 dpi at the 7.5 in printed width
# ACM single-column uses. That clears the 300 dpi floor most publishers set for
# raster artwork with margin to spare, and keeps text edges clean when a
# reviewer zooms the PDF.
EXPORT_SCALE = 4

FIGURE_SIZES = {
    "default": {"width": 780, "height": 480},
    "wide": {"width": 900, "height": 480},
    "tall": {"width": 780, "height": 620},
}

# Extra top room so the top-centre horizontal legend never overlaps the plot.
BASE_MARGIN = dict(l=74, r=34, t=96, b=70)
TITLELESS_MARGIN = dict(l=74, r=34, t=64, b=70)

MARKER_DEFAULTS = dict(size=11, line=dict(color="white", width=0.8), opacity=0.86)
ANNOTATION_FONT = dict(size=15.5, color=PALETTE["ink"], family=FIGURE_FONT)

SYMBOL_MAP = {"Text-centric": "circle", "Multimodal": "diamond", "Unknown": "x"}

# ---------------------------------------------------------------------------
# Bucket definitions
# ---------------------------------------------------------------------------

SIZE_BUCKETS = ["<1B", "1-3B", "3-7B", "7-10B", "10-20B", ">20B", "Unknown"]
SCALE_BUCKETS = [
    "<1B", "1-3B", "3-7B", "7-10B", "10-20B",
    "20-50B", "50-100B", ">100B", "Unknown",
]
MODALITY_ORDER = ["text", "vision", "audio", "video", "code", "embedding"]
CONTEXT_BUCKETS = ["<=4K", "8K", "16K-32K", "64K-128K", ">128K", "Unknown"]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate publication figures from merged_llm_database.json (v2)."
    )
    parser.add_argument("--input", default="merged_llm_database.json")
    parser.add_argument("--output-dir", default="figures")
    parser.add_argument("--title", default="true", type=parse_bool_arg)
    parser.add_argument("--format", choices=("pdf", "png"), default="pdf")
    return parser.parse_args()


def load_database(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_bool_arg(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected 'true' or 'false'")


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def unwrap_param_value(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, dict):
        raw = (
            value.get("total_params") or value.get("active_params")
            or value.get("total") or value.get("active_per_token")
        )
        return str(raw).strip() if raw else None
    text = str(value).strip()
    return text or None


def parse_param_billions(value: object) -> float | None:
    text = unwrap_param_value(value)
    if not text:
        return None
    lowered = text.lower().replace(",", "").replace("~", "").strip()
    if "undisclosed" in lowered or lowered == "n/a":
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*([mbt])\b", lowered)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        if unit == "m":
            return number / 1000.0
        if unit == "t":
            return number * 1000.0
        return number
    try:
        return float(lowered)
    except ValueError:
        return None


def effective_params_billions(model: dict) -> float | None:
    params = model.get("parameters")
    if isinstance(params, dict):
        if params.get("is_moe"):
            active = parse_param_billions(params.get("active_per_token"))
            if active is not None:
                return active
        total = parse_param_billions(params.get("total"))
        if total is not None:
            return total
        return parse_param_billions(params.get("total_params"))
    return parse_param_billions(params)


def total_params_billions(model: dict) -> float | None:
    params = model.get("parameters")
    if isinstance(params, dict):
        total = parse_param_billions(params.get("total"))
        if total is not None:
            return total
        return parse_param_billions(params.get("total_params"))
    return parse_param_billions(params)


def is_moe(model: dict) -> bool:
    params = model.get("parameters")
    return isinstance(params, dict) and bool(params.get("is_moe"))


def release_year(model: dict) -> int | None:
    value = model.get("release_date")
    if not value:
        return None
    match = re.match(r"^(\d{4})", str(value).strip())
    return int(match.group(1)) if match else None


def release_quarter(model: dict) -> str | None:
    value = model.get("release_date")
    if not value:
        return None
    match = re.match(r"^(\d{4})-(\d{2})", str(value).strip())
    if not match:
        year = release_year(model)
        return str(year) if year is not None else None
    year = int(match.group(1))
    month = int(match.group(2))
    return f"{year}-Q{(month - 1) // 3 + 1}"


def quarter_sort_key(value: str) -> tuple[int, int]:
    match = re.match(r"^(\d{4})(?:-Q(\d))?$", value)
    if not match:
        return (0, 0)
    return (int(match.group(1)), int(match.group(2) or 0))


def normalize_modalities(model: dict) -> set[str]:
    raw = model.get("modalities") or []
    alias = {"image": "vision", "vision": "vision", "text": "text",
             "audio": "audio", "video": "video", "code": "code", "embedding": "embedding"}
    return {alias.get(str(i).strip().lower(), str(i).strip().lower()) for i in raw}


def modality_group(model: dict) -> str:
    m = normalize_modalities(model)
    if not m:
        return "Unknown"
    return "Text-centric" if m.issubset({"text", "code", "embedding"}) else "Multimodal"


def license_group(model: dict) -> str:
    raw = str(model.get("license") or "").strip().lower()
    if not raw or raw == "unknown":
        return "Unknown"
    if raw in {"see source", "see model card"}:
        return "Unspecified"
    if "proprietary" in raw:
        return "Proprietary"
    if any(t in raw for t in ("apache", "mit", "bsd")):
        return "Permissive open"
    if any(t in raw for t in ("community", "custom", "gemma", "stability", "nvidia", "aws")):
        return "Custom/source-available"
    return "Other open"


def size_bucket(value: float | None) -> str:
    if value is None: return "Unknown"
    if value < 1: return "<1B"
    if value < 3: return "1-3B"
    if value < 7: return "3-7B"
    if value < 10: return "7-10B"
    if value <= 20: return "10-20B"
    return ">20B"


def scale_bucket(value: float | None) -> str:
    if value is None: return "Unknown"
    if value < 1: return "<1B"
    if value < 3: return "1-3B"
    if value < 7: return "3-7B"
    if value < 10: return "7-10B"
    if value <= 20: return "10-20B"
    if value <= 50: return "20-50B"
    if value <= 100: return "50-100B"
    return ">100B"


def context_bucket(value: object) -> str:
    if value in (None, "", 0): return "Unknown"
    try:
        tokens = int(value)
    except (TypeError, ValueError):
        return "Unknown"
    if tokens <= 4096: return "<=4K"
    if tokens <= 8192: return "8K"
    if tokens <= 32768: return "16K-32K"
    if tokens <= 131072: return "64K-128K"
    return ">128K"


def normalized_status(model: dict) -> str:
    raw = str(model.get("status") or "unknown").strip().lower()
    if raw == "active": return "Active"
    if raw == "legacy": return "Legacy"
    if "deprecated" in raw: return "Deprecated"
    return raw.capitalize() if raw else "Unknown"


def normalized_base_instruct(model: dict) -> str:
    raw = str(model.get("base_or_instruct") or "").strip().lower()
    return raw.capitalize() if raw in ("base", "instruct", "both") else "Unknown"


def top_developers(models: list[dict], limit: int) -> list[str]:
    counts = Counter(m.get("developer", "Unknown") for m in models)
    return [n for n, _ in counts.most_common(limit)]


def parse_benchmark_value(model: dict, key: str) -> float | None:
    benchmarks = model.get("benchmarks")
    if not isinstance(benchmarks, dict):
        return None
    raw = benchmarks.get(key)
    if raw is None:
        return None
    text = str(raw).strip().lower().replace("%", "")
    if not text or "n/a" in text or "not" in text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

def apply_figure_theme(
    fig: go.Figure, title: str, *, size: str = "default", show_title: bool = True
) -> go.Figure:
    dims = FIGURE_SIZES[size]
    fig.update_layout(
        template=DEFAULT_TEMPLATE,
        title=(
            dict(text=f"<b>{title}</b>", x=0.5,
                 font=dict(size=22, color=PALETTE["ink"], family=FIGURE_FONT))
            if show_title else None
        ),
        font=dict(family=FIGURE_FONT, size=18, color=PALETTE["ink"]),
        width=dims["width"], height=dims["height"],
        margin=BASE_MARGIN if show_title else TITLELESS_MARGIN,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
            bgcolor="rgba(255,255,255,0)",
            bordercolor="rgba(255,255,255,0)", borderwidth=0,
            font=dict(size=16.5, family=FIGURE_FONT),
            title=dict(text=""),
        ),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    fig.update_xaxes(
        showgrid=True, gridcolor=PALETTE["fog"],
        showline=True, linecolor=PALETTE["fog"], linewidth=1, mirror=False,
        title_font=dict(size=18.5, color=PALETTE["ink"], family=FIGURE_FONT),
        tickfont=dict(size=16, color=PALETTE["ink"], family=FIGURE_FONT),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=PALETTE["fog"],
        showline=True, linecolor=PALETTE["fog"], linewidth=1, mirror=False,
        title_font=dict(size=18.5, color=PALETTE["ink"], family=FIGURE_FONT),
        tickfont=dict(size=16, color=PALETTE["ink"], family=FIGURE_FONT),
    )
    fig.update_annotations(font=ANNOTATION_FONT)
    return fig


def pad_yaxis(fig: go.Figure, models_or_values: list, factor: float = 1.15) -> None:
    """Add top padding to y-axis so text labels above bars aren't clipped."""
    fig.update_yaxes(rangemode="tozero")


def save_figure(fig: go.Figure, output_dir: Path, filename: str, fmt: str) -> None:
    path = output_dir / f"{filename}.{fmt}"
    fig.write_image(str(path), format=fmt, scale=EXPORT_SCALE)
    print(f"  saved {path.name}")


# ===========================================================================
# Generic figure functions (work for any model set via `tag` prefix)
# ===========================================================================

def fig_releases_by_size(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    years = sorted({y for y in (release_year(m) for m in models) if y is not None})
    by_year: dict[int, Counter] = defaultdict(Counter)
    for m in models:
        y = release_year(m)
        if y is not None:
            by_year[y][size_bucket(effective_params_billions(m))] += 1

    fig = go.Figure()
    for bucket in SIZE_BUCKETS:
        fig.add_trace(go.Bar(
            x=[str(y) for y in years],
            y=[by_year[y].get(bucket, 0) for y in years],
            name=bucket, marker_color=BUCKET_COLORS[bucket],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, f"{label} Releases by Year and Parameter Bucket", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    save_figure(fig, output_dir, f"paper_{tag}_releases_by_size", fmt)


def fig_context_by_year(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    """Violin (density) of context window per release year.

    Values are plotted in log10 space with a linear axis so the kernel-density
    shape is meaningful; the axis is then relabelled with 1K..10M ticks.
    """
    import math
    years = sorted({y for y in (release_year(m) for m in models) if y is not None})
    fig = go.Figure()
    all_log = []
    for year in years:
        values = [
            m["context_window_tokens"]
            for m in models if release_year(m) == year and m.get("context_window_tokens")
        ]
        if not values:
            continue
        logv = [math.log10(v) for v in values]
        all_log += logv
        color = YEAR_COLORS.get(str(year), PALETTE["slate"])
        fig.add_trace(go.Violin(
            x=[str(year)] * len(logv), y=logv, name=str(year),
            line_color=color, fillcolor=color_with_alpha(color, 0.40),
            box_visible=True, meanline_visible=True,
            box_line_color=color, box_fillcolor=color_with_alpha(color, 0.25),
            meanline_color=PALETTE["ink"],
            points="all", pointpos=0, jitter=0.25,
            marker=dict(size=5, color=color, opacity=0.5, line=dict(width=0)),
            width=0.8, spanmode="hard", scalemode="width",
            showlegend=False,
        ))
    apply_figure_theme(fig, f"{label} Context Windows by Release Year", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    lo = math.floor(min(all_log)) if all_log else 3
    hi = math.ceil(max(all_log)) if all_log else 7
    fig.update_yaxes(
        title_text="Context window (tokens)",
        tickvals=[3, 4, 5, 6, 7],
        ticktext=["1K", "10K", "100K", "1M", "10M"],
        range=[lo - 0.25, hi + 0.25],
    )
    save_figure(fig, output_dir, f"paper_{tag}_context_by_year", fmt)


def fig_context_vs_size(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    points = []
    for m in models:
        p = effective_params_billions(m)
        ctx = m.get("context_window_tokens")
        yr = release_year(m)
        if p is None or not ctx or yr is None:
            continue
        points.append({
            "name": m.get("name", "Unknown"), "year": str(yr),
            "params": p, "context": ctx, "group": modality_group(m),
        })
    if not points:
        return

    labels = set()
    for r in sorted(points, key=lambda r: r["context"], reverse=True)[:4]:
        labels.add(r["name"])
    for r in sorted(points, key=lambda r: r["params"], reverse=True)[:3]:
        labels.add(r["name"])

    fig = go.Figure()
    for year in sorted({r["year"] for r in points}):
        for group in ("Text-centric", "Multimodal", "Unknown"):
            subset = [r for r in points if r["year"] == year and r["group"] == group]
            if not subset:
                continue
            fig.add_trace(go.Scatter(
                x=[r["params"] for r in subset], y=[r["context"] for r in subset],
                mode="markers+text",
                text=[r["name"] if r["name"] in labels else "" for r in subset],
                textposition="top center", textfont=ANNOTATION_FONT,
                marker=dict(**MARKER_DEFAULTS, color=YEAR_COLORS.get(year, PALETTE["slate"]),
                            symbol=SYMBOL_MAP[group]),
                name=f"{year} / {group}",
                hovertemplate=(f"<b>%{{text}}</b><br>Year: {year}<br>"
                               "Params: %{x:.2f}B<br>Context: %{y:,} tokens<extra></extra>"),
            ))
    apply_figure_theme(fig, f"{label} Context-Window Scaling vs Model Size", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameters (billions)", type="log")
    fig.update_yaxes(title_text="Context window (tokens)", type="log")
    save_figure(fig, output_dir, f"paper_{tag}_context_vs_size", fmt)


def fig_developer_portfolio(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    variants = Counter()
    families: dict[str, set] = defaultdict(set)
    mm_counts = Counter()
    for m in models:
        dev = m.get("developer", "Unknown")
        variants[dev] += 1
        families[dev].add(m.get("family", "Unknown"))
        if modality_group(m) == "Multimodal":
            mm_counts[dev] += 1

    top = [n for n, _ in variants.most_common(10)]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=top, y=[variants[n] for n in top], name="Variants",
        marker_color=PALETTE["blue"],
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=top, y=[len(families[n]) for n in top], name="Families",
        mode="lines+markers", line=dict(color=PALETTE["orange"], width=3), marker=dict(size=9),
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=top, y=[round(100 * mm_counts[n] / variants[n], 1) for n in top],
        name="Multimodal %", mode="lines+markers",
        line=dict(color=PALETTE["aqua"], width=2, dash="dot"), marker=dict(size=8),
    ), secondary_y=True)

    apply_figure_theme(fig, f"Developer Concentration in {label} Inventory", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Developer", tickangle=-30)
    fig.update_yaxes(title_text="Variant count", secondary_y=False)
    fig.update_yaxes(title_text="Family count / multimodal %", secondary_y=True)
    save_figure(fig, output_dir, f"paper_{tag}_developer_portfolio", fmt)


def fig_access_mode(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    access_order = ["OW", "Both", "API"]
    access_labels = {"OW": "Open weights", "Both": "Open weights + API", "API": "API only"}
    counts = Counter(m.get("access", "Unknown") for m in models)
    present = [k for k in access_order if k in counts]

    fig = go.Figure(go.Bar(
        x=[access_labels.get(k, k) for k in present],
        y=[counts[k] for k in present],
        marker_color=[ACCESS_COLORS.get(k, PALETTE["slate"]) for k in present],
        text=[counts[k] for k in present], textposition="outside",
    ))
    apply_figure_theme(fig, f"{label} Access Mode Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Access mode")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    # Pad y for text labels
    max_val = max(counts[k] for k in present) if present else 1
    fig.update_yaxes(range=[0, max_val * 1.15])
    save_figure(fig, output_dir, f"paper_{tag}_access_mode", fmt)


def fig_license_posture(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    order = ["Permissive open", "Custom/source-available", "Proprietary",
             "Unspecified", "Other open", "Unknown"]
    counts = Counter(license_group(m) for m in models)
    present = [k for k in order if k in counts]

    fig = go.Figure(go.Bar(
        x=present, y=[counts[k] for k in present],
        marker_color=[LICENSE_COLORS.get(k, PALETTE["slate"]) for k in present],
        text=[counts[k] for k in present], textposition="outside",
    ))
    apply_figure_theme(fig, f"{label} License Posture", show_title=show_title)
    fig.update_xaxes(title_text="License category", tickangle=-25)
    fig.update_yaxes(title_text=f"Number of {label} variants")
    max_val = max(counts[k] for k in present) if present else 1
    fig.update_yaxes(range=[0, max_val * 1.15])
    save_figure(fig, output_dir, f"paper_{tag}_license_posture", fmt)


def fig_modality_distribution(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    counts = Counter()
    for m in models:
        for mod in normalize_modalities(m):
            counts[mod] += 1
    labels = [l.capitalize() for l in MODALITY_ORDER if l in counts]
    values = [counts[l.lower()] for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=SOFT_SEQUENCE[:len(labels)],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, f"{label} Modality Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Modality")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    if values:
        fig.update_yaxes(range=[0, max(values) * 1.15])
    save_figure(fig, output_dir, f"paper_{tag}_modality_distribution", fmt)


def fig_status_distribution(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    statuses = Counter(normalized_status(m) for m in models)
    order = ["Active", "Legacy", "Deprecated", "Unknown"]
    labels = [l for l in order if l in statuses] + [l for l in sorted(statuses) if l not in order]
    values = [statuses[l] for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=[STATUS_COLORS.get(l, PALETTE["slate"]) for l in labels],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, f"{label} Status Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Status")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    if values:
        fig.update_yaxes(range=[0, max(values) * 1.15])
    save_figure(fig, output_dir, f"paper_{tag}_status_distribution", fmt)


def fig_developer_param_heatmap(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    devs = top_developers(models, limit=10)
    buckets = [b for b in SIZE_BUCKETS if b != "Unknown"] + ["Unknown"]
    matrix = []
    for dev in devs:
        params = [size_bucket(effective_params_billions(m)) for m in models if m.get("developer", "Unknown") == dev]
        c = Counter(params)
        matrix.append([c.get(b, 0) for b in buckets])

    # Suppress "0" text — show only non-zero counts
    text_matrix = [[str(v) if v > 0 else "" for v in row] for row in matrix]

    fig = go.Figure(go.Heatmap(
        z=matrix, x=buckets, y=devs,
        colorscale=SOFT_HEATMAP,
        text=text_matrix, texttemplate="%{text}",
        hovertemplate="Developer: %{y}<br>Bucket: %{x}<br>Count: %{z}<extra></extra>",
        colorbar=dict(title="Count"),
    ))
    apply_figure_theme(fig, f"{label} Developer by Parameter Bucket", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameter bucket")
    fig.update_yaxes(title_text="Developer")
    save_figure(fig, output_dir, f"paper_{tag}_developer_param_heatmap", fmt)


def fig_cumulative_releases(
    slms: list[dict], llms: list[dict], tag: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    """Overlay SLM and LLM cumulative release curves."""
    slm_dates = sorted(str(m.get("release_date")) for m in slms if m.get("release_date"))
    llm_dates = sorted(str(m.get("release_date")) for m in llms if m.get("release_date"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=slm_dates, y=list(range(1, len(slm_dates) + 1)),
        mode="lines", name="SLMs",
        line=dict(color=PALETTE["blue"], width=3),
        fill="tozeroy", fillcolor=color_with_alpha(PALETTE["blue"], 0.18),
    ))
    fig.add_trace(go.Scatter(
        x=llm_dates, y=list(range(1, len(llm_dates) + 1)),
        mode="lines", name="LLMs",
        line=dict(color=PALETTE["orange"], width=3),
        fill="tozeroy", fillcolor=color_with_alpha(PALETTE["orange"], 0.12),
    ))
    apply_figure_theme(fig, "Cumulative Model Releases: SLM vs LLM", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release date")
    fig.update_yaxes(title_text="Cumulative number of variants")
    # legend inherits the top-centre horizontal placement from apply_figure_theme
    save_figure(fig, output_dir, f"paper_{tag}_cumulative_releases", fmt)


def fig_release_timeline_by_developer(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    devs = top_developers(models, limit=6)
    quarters = sorted(
        {q for q in (release_quarter(m) for m in models) if q is not None},
        key=quarter_sort_key,
    )
    grouped: dict[str, Counter] = defaultdict(Counter)
    for m in models:
        q = release_quarter(m)
        if q is None:
            continue
        dev = m.get("developer", "Unknown")
        grouped[dev if dev in devs else "Other"][q] += 1

    fig = go.Figure()
    for idx, dev in enumerate(devs + ["Other"]):
        fig.add_trace(go.Bar(
            x=quarters, y=[grouped[dev].get(q, 0) for q in quarters],
            name=dev, marker_color=SOFT_SEQUENCE[idx % len(SOFT_SEQUENCE)],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, f"{label} Release Timeline by Developer", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text=f"Number of {label} variants")
    save_figure(fig, output_dir, f"paper_{tag}_release_timeline_by_developer", fmt)


def fig_context_bucket_distribution(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    counts = Counter(context_bucket(m.get("context_window_tokens")) for m in models)
    values = [counts.get(b, 0) for b in CONTEXT_BUCKETS]

    fig = go.Figure(go.Bar(
        x=CONTEXT_BUCKETS, y=values,
        marker_color=[CONTEXT_BUCKET_COLORS[b] for b in CONTEXT_BUCKETS],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, f"{label} Context-Window Buckets", show_title=show_title)
    fig.update_xaxes(title_text="Context bucket")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    if values:
        fig.update_yaxes(range=[0, max(values) * 1.15])
    save_figure(fig, output_dir, f"paper_{tag}_context_bucket_distribution", fmt)


def fig_family_treemap(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    dev_counts = Counter(m.get("developer", "Unknown") for m in models)
    top_devs = {n for n, _ in dev_counts.most_common(10)}
    grouped: dict[str, Counter] = defaultdict(Counter)
    for m in models:
        dev = m.get("developer", "Unknown")
        grouped[dev if dev in top_devs else "Other developers"][m.get("family", "Unknown")] += 1

    ids, labels_list, parents, values, colors = [], [], [], [], []
    dev_pal = SOFT_SEQUENCE[:11]

    for idx, dev in enumerate(sorted(grouped, key=lambda n: sum(grouped[n].values()), reverse=True)):
        dev_id = f"dev::{dev}"
        color = dev_pal[idx % len(dev_pal)]
        ids.append(dev_id)
        labels_list.append(dev)
        parents.append("")
        values.append(sum(grouped[dev].values()))
        colors.append(color)
        for fam, cnt in grouped[dev].most_common():
            ids.append(f"{dev_id}::fam::{fam}")
            labels_list.append(fam)
            parents.append(dev_id)
            values.append(cnt)
            colors.append(color)

    fig = go.Figure(go.Treemap(
        ids=ids, labels=labels_list, parents=parents, values=values,
        branchvalues="total",
        marker=dict(colors=colors, line=dict(color="white", width=1.4),
                    cornerradius=3),
        textinfo="label+value",
        textfont=dict(family=FIGURE_FONT, size=15),
        tiling=dict(pad=3), maxdepth=2, sort=True,
        hovertemplate="<b>%{label}</b><br>Variants: %{value}<extra></extra>",
    ))
    apply_figure_theme(fig, f"{label} Ecosystem by Developer and Family", size="tall", show_title=show_title)
    # treemaps should fill the frame: strip the plot-style margins/legend room
    fig.update_layout(margin=dict(l=6, r=6, t=6, b=6),
                      uniformtext=dict(minsize=10, mode="hide"))
    save_figure(fig, output_dir, f"paper_{tag}_family_treemap", fmt)


def fig_scale_buckets_comparison(
    slms: list[dict], llms: list[dict],
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    slm_c = Counter(scale_bucket(effective_params_billions(m)) for m in slms)
    llm_c = Counter(scale_bucket(effective_params_billions(m)) for m in llms)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=SCALE_BUCKETS, y=[slm_c.get(b, 0) for b in SCALE_BUCKETS],
        name="SLMs", marker_color=PALETTE["blue"],
    ))
    fig.add_trace(go.Bar(
        x=SCALE_BUCKETS, y=[llm_c.get(b, 0) for b in SCALE_BUCKETS],
        name="LLMs", marker_color=PALETTE["orange"],
    ))
    fig.update_layout(barmode="group")
    apply_figure_theme(fig, "Scale Separation Between SLM and LLM Inventories", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameter bucket")
    fig.update_yaxes(title_text="Model variants")
    save_figure(fig, output_dir, "paper_scale_buckets_slm_vs_llm", fmt)


# ---------------------------------------------------------------------------
# MoE vs Dense — improved with subplots
# ---------------------------------------------------------------------------

def fig_moe_vs_dense(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    moe = [m for m in models if is_moe(m)]
    dense = [m for m in models if not is_moe(m)]

    moe_total = [total_params_billions(m) for m in moe if total_params_billions(m) is not None]
    dense_total = [total_params_billions(m) for m in dense if total_params_billions(m) is not None]
    moe_active = [effective_params_billions(m) for m in moe if effective_params_billions(m) is not None]

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=(
            "Variant count",
            "Median total params (B)",
            "Median active params / token (B)",
        ),
        horizontal_spacing=0.14,
    )
    bar_kw = dict(width=0.55)
    cats = ["MoE", "Dense"]
    col_moe, col_dense = PALETTE["orange"], PALETTE["blue"]

    fig.add_trace(go.Bar(
        x=cats, y=[len(moe), len(dense)],
        marker_color=[col_moe, col_dense],
        text=[str(len(moe)), str(len(dense))], textposition="outside",
        showlegend=False, **bar_kw,
    ), row=1, col=1)

    mp = round(median(moe_total), 1) if moe_total else 0
    dp = round(median(dense_total), 1) if dense_total else 0
    fig.add_trace(go.Bar(
        x=cats, y=[mp, dp],
        marker_color=[col_moe, col_dense],
        text=[f"{mp:g}", f"{dp:g}"], textposition="outside",
        showlegend=False, **bar_kw,
    ), row=1, col=2)

    # active params: for dense this equals total; shows the "same per-token cost" point
    ma = round(median(moe_active), 1) if moe_active else 0
    da = round(median(dense_total), 1) if dense_total else 0
    fig.add_trace(go.Bar(
        x=cats, y=[ma, da],
        marker_color=[col_moe, col_dense],
        text=[f"{ma:g}", f"{da:g}"], textposition="outside",
        showlegend=False, **bar_kw,
    ), row=1, col=3)

    apply_figure_theme(fig, f"{label} MoE vs Dense Comparison", size="wide", show_title=show_title)
    fig.update_annotations(font=dict(size=17, family=FIGURE_FONT, color=PALETTE["ink"]))
    for col in (1, 2, 3):
        fig.update_yaxes(rangemode="tozero", row=1, col=col)
    save_figure(fig, output_dir, f"paper_{tag}_moe_vs_dense", fmt)


def fig_base_vs_instruct(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    years = sorted({y for y in (release_year(m) for m in models) if y is not None})
    by_year: dict[int, Counter] = defaultdict(Counter)
    for m in models:
        y = release_year(m)
        if y is not None:
            by_year[y][normalized_base_instruct(m)] += 1

    bi_colors = {"Base": PALETTE["blue"], "Instruct": PALETTE["orange"],
                 "Both": PALETTE["aqua"], "Unknown": PALETTE["slate"]}

    fig = go.Figure()
    for lbl in ["Base", "Instruct", "Both", "Unknown"]:
        fig.add_trace(go.Bar(
            x=[str(y) for y in years],
            y=[by_year[y].get(lbl, 0) for y in years],
            name=lbl, marker_color=bi_colors[lbl],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, f"{label} Base vs Instruct Releases by Year", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    fig.update_yaxes(title_text=f"Number of {label} variants")
    save_figure(fig, output_dir, f"paper_{tag}_base_vs_instruct", fmt)


def fig_benchmark_vs_params(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    points = []
    for m in models:
        p = effective_params_billions(m)
        mmlu = parse_benchmark_value(m, "MMLU")
        if p is None or mmlu is None:
            continue
        points.append({
            "name": m.get("name", "Unknown"), "params": p, "mmlu": mmlu,
            "year": str(release_year(m) or "Unknown"), "group": modality_group(m),
        })
    if not points:
        print(f"  skipped paper_{tag}_benchmark_vs_params (no MMLU data)")
        return

    labels = set()
    for r in sorted(points, key=lambda r: r["mmlu"], reverse=True)[:5]:
        labels.add(r["name"])
    for r in sorted(points, key=lambda r: r["params"])[:3]:
        labels.add(r["name"])

    fig = go.Figure()
    for year in sorted({r["year"] for r in points}):
        for group in ("Text-centric", "Multimodal", "Unknown"):
            subset = [r for r in points if r["year"] == year and r["group"] == group]
            if not subset:
                continue
            fig.add_trace(go.Scatter(
                x=[r["params"] for r in subset], y=[r["mmlu"] for r in subset],
                mode="markers+text",
                text=[r["name"] if r["name"] in labels else "" for r in subset],
                textposition="top center", textfont=ANNOTATION_FONT,
                marker=dict(**MARKER_DEFAULTS, color=YEAR_COLORS.get(year, PALETTE["slate"]),
                            symbol=SYMBOL_MAP.get(group, "circle")),
                name=f"{year} / {group}",
            ))
    apply_figure_theme(fig, f"{label} MMLU Score vs Parameters (n={len(points)})", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameters (billions)", type="log")
    fig.update_yaxes(title_text="MMLU score (%)")
    save_figure(fig, output_dir, f"paper_{tag}_benchmark_vs_params", fmt)


def fig_developer_diversity_timeline(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    # keep only well-formed YYYY-QN quarters so the axis is consistent
    entries = [(release_quarter(m), m.get("developer", "Unknown"))
               for m in models if release_quarter(m) is not None]
    entries = [(q, d) for q, d in entries if re.fullmatch(r"\d{4}-Q[1-4]", str(q))]
    quarters = sorted({q for q, _ in entries}, key=quarter_sort_key)
    seen: set[str] = set()
    cumul, new_q = [], []
    for q in quarters:
        devs = {d for qq, d in entries if qq == q}
        new = devs - seen
        seen |= devs
        cumul.append(len(seen))
        new_q.append(len(new))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quarters, y=new_q, name="New developers this quarter",
        marker_color=color_with_alpha(PALETTE["seq2"], 0.75),
        marker_line=dict(width=0),
    ))
    fig.add_trace(go.Scatter(
        x=quarters, y=cumul, mode="lines+markers", name="Cumulative distinct developers",
        line=dict(color=PALETTE["orange"], width=3), marker=dict(size=7),
    ))
    apply_figure_theme(fig, f"Developer Diversity in {label} Ecosystem", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text="Distinct developers", rangemode="tozero")
    fig.update_layout(bargap=0.35)
    save_figure(fig, output_dir, f"paper_{tag}_developer_diversity_timeline", fmt)


def fig_family_size_range(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    fam_params: dict[str, list[float]] = defaultdict(list)
    for m in models:
        p = effective_params_billions(m)
        if p is not None:
            fam_params[m.get("family", "Unknown")].append(p)

    # top 15 by span, then order the axis by median so it reads as a progression
    families = sorted(
        [(f, v) for f, v in fam_params.items() if len(v) >= 2],
        key=lambda x: max(x[1]) - min(x[1]), reverse=True,
    )[:15]
    families = sorted(families, key=lambda x: median(x[1]))

    names = [f for f, _ in families]
    mins = [min(v) for _, v in families]
    maxs = [max(v) for _, v in families]
    meds = [round(median(v), 2) for _, v in families]

    line_col = "#C4CFD6"          # soft neutral grey: colour carries no meaning here
    fig = go.Figure()
    # connector lines (min -> max) as one batched trace with gaps
    lx, ly = [], []
    for name, vals in families:
        lx += [min(vals), max(vals), None]
        ly += [name, name, None]
    fig.add_trace(go.Scatter(
        x=lx, y=ly, mode="lines",
        line=dict(color=line_col, width=5),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=mins, y=names, mode="markers", name="Smallest",
        marker=dict(size=10, color=PALETTE["seq1"],
                    line=dict(color="white", width=1.4)),
    ))
    fig.add_trace(go.Scatter(
        x=maxs, y=names, mode="markers", name="Largest",
        marker=dict(size=12, color=PALETTE["seq3"],
                    line=dict(color="white", width=1.4)),
    ))
    fig.add_trace(go.Scatter(
        x=meds, y=names, mode="markers", name="Median",
        marker=dict(size=11, color=PALETTE["orange"],
                    line=dict(color="white", width=1.6)),
    ))
    apply_figure_theme(fig, f"{label} Family Parameter Range (Top 15)", size="tall", show_title=show_title)
    fig.update_xaxes(
        title_text="Effective parameters (billions, log scale)", type="log",
        tickvals=[0.3, 0.5, 1, 2, 3, 5, 10, 20, 30],
        ticktext=["0.3", "0.5", "1", "2", "3", "5", "10", "20", "30"],
        ticks="outside",
    )
    fig.update_yaxes(title_text="", ticks="", automargin=True)
    save_figure(fig, output_dir, f"paper_{tag}_family_size_range", fmt)


def fig_multimodal_timeline(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    quarters = sorted(
        {q for q in (release_quarter(m) for m in models) if q is not None},
        key=quarter_sort_key,
    )
    by_q: dict[str, Counter] = defaultdict(Counter)
    for m in models:
        q = release_quarter(m)
        if q:
            by_q[q][modality_group(m)] += 1

    fig = go.Figure()
    for group, color in [("Text-centric", PALETTE["blue"]), ("Multimodal", PALETTE["orange"])]:
        fig.add_trace(go.Bar(
            x=quarters, y=[by_q[q].get(group, 0) for q in quarters],
            name=group, marker_color=color,
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, f"Rise of Multimodal {label}s", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text=f"Number of {label} variants")
    save_figure(fig, output_dir, f"paper_{tag}_multimodal_timeline", fmt)


def fig_context_evolution_by_family(
    models: list[dict], tag: str, label: str,
    output_dir: Path, show_title: bool, fmt: str,
) -> None:
    """Use max context per date per family for cleaner trend lines."""
    raw_data: dict[str, dict[str, int]] = defaultdict(dict)
    for m in models:
        date = m.get("release_date")
        ctx = m.get("context_window_tokens")
        if not date or not ctx:
            continue
        fam = m.get("family", "Unknown")
        d = str(date)
        raw_data[fam][d] = max(raw_data[fam].get(d, 0), int(ctx))

    eligible = []
    for fam, date_ctx in raw_data.items():
        if len(date_ctx) >= 2 and len(set(date_ctx.values())) >= 2:
            eligible.append((fam, sorted(date_ctx.items())))

    eligible.sort(key=lambda x: max(c for _, c in x[1]), reverse=True)
    eligible = eligible[:8]

    fig = go.Figure()
    for idx, (fam, data) in enumerate(eligible):
        fig.add_trace(go.Scatter(
            x=[d for d, _ in data], y=[c for _, c in data],
            mode="lines+markers", name=fam,
            line=dict(color=SOFT_SEQUENCE[idx % len(SOFT_SEQUENCE)], width=2.5),
            marker=dict(size=8),
        ))
    apply_figure_theme(fig, f"Context Window Evolution by {label} Family", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release date")
    fig.update_yaxes(title_text="Context window (tokens)", type="log")
    # legend inherits the top-centre horizontal placement from apply_figure_theme
    save_figure(fig, output_dir, f"paper_{tag}_context_evolution_by_family", fmt)


# ===========================================================================
# Runner for one model category
# ===========================================================================

def generate_category(
    models: list[dict], tag: str, label: str,
    all_slms: list[dict], all_llms: list[dict],
    output_dir: Path, show_title: bool, fmt: str,
) -> int:
    """Generate all figures for a category (SLM or LLM). Returns count."""
    count_before = len(list(output_dir.glob(f"paper_{tag}_*.{fmt}")))

    fig_releases_by_size(models, tag, label, output_dir, show_title, fmt)
    fig_context_by_year(models, tag, label, output_dir, show_title, fmt)
    fig_context_vs_size(models, tag, label, output_dir, show_title, fmt)
    fig_developer_portfolio(models, tag, label, output_dir, show_title, fmt)
    fig_access_mode(models, tag, label, output_dir, show_title, fmt)
    fig_license_posture(models, tag, label, output_dir, show_title, fmt)
    fig_modality_distribution(models, tag, label, output_dir, show_title, fmt)
    fig_status_distribution(models, tag, label, output_dir, show_title, fmt)
    fig_developer_param_heatmap(models, tag, label, output_dir, show_title, fmt)
    fig_release_timeline_by_developer(models, tag, label, output_dir, show_title, fmt)
    fig_context_bucket_distribution(models, tag, label, output_dir, show_title, fmt)
    fig_family_treemap(models, tag, label, output_dir, show_title, fmt)
    fig_moe_vs_dense(models, tag, label, output_dir, show_title, fmt)
    fig_base_vs_instruct(models, tag, label, output_dir, show_title, fmt)
    fig_benchmark_vs_params(models, tag, label, output_dir, show_title, fmt)
    fig_developer_diversity_timeline(models, tag, label, output_dir, show_title, fmt)
    fig_family_size_range(models, tag, label, output_dir, show_title, fmt)
    fig_multimodal_timeline(models, tag, label, output_dir, show_title, fmt)
    fig_context_evolution_by_family(models, tag, label, output_dir, show_title, fmt)

    count_after = len(list(output_dir.glob(f"paper_{tag}_*.{fmt}")))
    return count_after - count_before


# ===========================================================================
# Audit & main
# ===========================================================================

def print_dataset_audit(slms: list[dict], llms: list[dict]) -> None:
    for tag, models in [("SLM", slms), ("LLM", llms)]:
        ctx_known = sum(1 for m in models if m.get("context_window_tokens"))
        moe_n = sum(1 for m in models if is_moe(m))
        mmlu_n = sum(1 for m in models if parse_benchmark_value(m, "MMLU") is not None)
        bi = dict(Counter(normalized_base_instruct(m) for m in models))
        print(f"  {tag}: {len(models)} variants | context: {ctx_known} | MoE: {moe_n} | MMLU: {mmlu_n} | {bi}")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pio.templates.default = DEFAULT_TEMPLATE

    db = load_database(input_path)
    slms = list(db.get("models", {}).get("slm", []))
    llms = list(db.get("models", {}).get("llm", []))

    print("Dataset audit:")
    print_dataset_audit(slms, llms)

    # --- SLM figures ---
    print("\nGenerating SLM figures...")
    generate_category(slms, "slm", "SLM", slms, llms, output_dir, args.title, args.format)

    # --- LLM figures ---
    print("\nGenerating LLM figures...")
    generate_category(llms, "llm", "LLM", slms, llms, output_dir, args.title, args.format)

    # --- Comparative figures ---
    print("\nGenerating comparative figures...")
    fig_scale_buckets_comparison(slms, llms, output_dir, args.title, args.format)
    fig_cumulative_releases(slms, llms, "combined", output_dir, args.title, args.format)

    generated = sorted(p.name for p in output_dir.glob(f"*.{args.format}") if p.name.startswith("paper_"))
    slm_figs = [n for n in generated if "_slm_" in n]
    llm_figs = [n for n in generated if "_llm_" in n]
    comp_figs = [n for n in generated if n not in slm_figs and n not in llm_figs]

    print(f"\nGenerated {len(generated)} figures in {output_dir.resolve()}:")
    print(f"  SLM: {len(slm_figs)} | LLM: {len(llm_figs)} | Comparative: {len(comp_figs)}")
    for name in generated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
