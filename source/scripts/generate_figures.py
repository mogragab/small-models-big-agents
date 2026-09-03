#!/usr/bin/env python3
"""Generate paper-oriented figures from merged_llm_database.json."""

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

PALETTE = {
    # Core sequence — saturated enough to distinguish, soft enough for print
    "indigo":    "#6C5B7B",
    "teal":      "#45B7A0",
    "coral":     "#E8836B",
    "amber":     "#F2B05E",
    "sky":       "#5BA4CF",
    "plum":      "#C06C84",
    "mint":      "#88D8B0",
    "peach":     "#F7C59F",
    "slate":     "#7E8C9A",
    "lavender":  "#B8A9C9",
    "ocean":     "#3D7EA6",
    "rose":      "#E8A0BF",
    "olive":     "#9AB87A",
    "sand":      "#D4C5A9",
    # Utility
    "ink":       "#2D3436",
    "fog":       "#E8EEF0",
    "cloud":     "#F8FAFB",
    "mist":      "#DDE6EA",
}

SOFT_SEQUENCE = [
    PALETTE["indigo"],
    PALETTE["teal"],
    PALETTE["coral"],
    PALETTE["amber"],
    PALETTE["sky"],
    PALETTE["plum"],
    PALETTE["mint"],
    PALETTE["peach"],
    PALETTE["ocean"],
    PALETTE["lavender"],
    PALETTE["olive"],
    PALETTE["rose"],
    PALETTE["slate"],
    PALETTE["sand"],
]

SOFT_HEATMAP = [
    [0.0, PALETTE["cloud"]],
    [0.25, "#D6EAF0"],
    [0.5, PALETTE["sky"]],
    [0.75, PALETTE["teal"]],
    [1.0, PALETTE["ocean"]],
]

# Centralized colour maps ------------------------------------------------

BUCKET_COLORS = {
    "<1B": PALETTE["mint"],
    "1-3B": PALETTE["sky"],
    "3-7B": PALETTE["indigo"],
    "7-10B": PALETTE["teal"],
    "10-20B": PALETTE["amber"],
    ">20B": PALETTE["coral"],
    "Unknown": PALETTE["slate"],
}

YEAR_COLORS = {
    "2022": PALETTE["slate"],
    "2023": PALETTE["sky"],
    "2024": PALETTE["teal"],
    "2025": PALETTE["amber"],
    "2026": PALETTE["coral"],
}

STATUS_COLORS = {
    "Active": PALETTE["teal"],
    "Legacy": PALETTE["amber"],
    "Deprecated": PALETTE["coral"],
    "Unknown": PALETTE["slate"],
}

ACCESS_COLORS = {
    "OW": PALETTE["teal"],
    "Both": PALETTE["amber"],
    "API": PALETTE["coral"],
}

LICENSE_COLORS = {
    "Permissive open": PALETTE["teal"],
    "Custom/source-available": PALETTE["amber"],
    "Proprietary": PALETTE["coral"],
    "Unspecified": PALETTE["slate"],
    "Other open": PALETTE["sky"],
    "Unknown": PALETTE["lavender"],
}

CONTEXT_BUCKET_COLORS = {
    "<=4K": PALETTE["mint"],
    "8K": PALETTE["sky"],
    "16K-32K": PALETTE["teal"],
    "64K-128K": PALETTE["amber"],
    ">128K": PALETTE["coral"],
    "Unknown": PALETTE["slate"],
}


def color_with_alpha(hex_color: str, alpha: float) -> str:
    """Convert a hex colour to an rgba() string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ---------------------------------------------------------------------------
# Layout & theme constants
# ---------------------------------------------------------------------------

DEFAULT_TEMPLATE = "plotly_white"

FIGURE_SIZES = {
    "default": {"width": 960, "height": 560},
    "wide": {"width": 1120, "height": 560},
    "tall": {"width": 1080, "height": 720},
}

BASE_MARGIN = dict(l=72, r=32, t=72, b=68)
TITLELESS_MARGIN = dict(l=72, r=32, t=36, b=68)

MARKER_DEFAULTS = dict(size=11, line=dict(color="white", width=0.8), opacity=0.86)
ANNOTATION_FONT = dict(size=11, color=PALETTE["ink"])

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
        description="Generate publication figures from merged_llm_database.json."
    )
    parser.add_argument(
        "--input",
        default="merged_llm_database.json",
        help="Path to the merged model inventory JSON.",
    )
    parser.add_argument(
        "--output-dir",
        default="figures",
        help="Directory for generated figure PDFs.",
    )
    parser.add_argument(
        "--title",
        default="true",
        type=parse_bool_arg,
        help="Whether to show figure titles: true or false (default: true).",
    )
    parser.add_argument(
        "--format",
        choices=("pdf", "png"),
        default="pdf",
        help="Output image format (default: pdf).",
    )
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
            value.get("total_params")
            or value.get("active_params")
            or value.get("total")
            or value.get("active_per_token")
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
    """Return total parameter count (ignoring MoE active distinction)."""
    params = model.get("parameters")
    if isinstance(params, dict):
        total = parse_param_billions(params.get("total"))
        if total is not None:
            return total
        return parse_param_billions(params.get("total_params"))
    return parse_param_billions(params)


def is_moe(model: dict) -> bool:
    params = model.get("parameters")
    if isinstance(params, dict):
        return bool(params.get("is_moe"))
    return False


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
    quarter = (month - 1) // 3 + 1
    return f"{year}-Q{quarter}"


def quarter_sort_key(value: str) -> tuple[int, int]:
    match = re.match(r"^(\d{4})(?:-Q(\d))?$", value)
    if not match:
        return (0, 0)
    return (int(match.group(1)), int(match.group(2) or 0))


def normalize_modalities(model: dict) -> set[str]:
    raw_modalities = model.get("modalities") or []
    alias_map = {
        "image": "vision", "vision": "vision", "text": "text",
        "audio": "audio", "video": "video", "code": "code",
        "embedding": "embedding",
    }
    return {alias_map.get(str(item).strip().lower(), str(item).strip().lower()) for item in raw_modalities}


def modality_group(model: dict) -> str:
    modalities = normalize_modalities(model)
    if not modalities:
        return "Unknown"
    if modalities.issubset({"text", "code", "embedding"}):
        return "Text-centric"
    return "Multimodal"


def license_group(model: dict) -> str:
    raw = str(model.get("license") or "").strip().lower()
    if not raw or raw == "unknown":
        return "Unknown"
    if raw in {"see source", "see model card"}:
        return "Unspecified"
    if "proprietary" in raw:
        return "Proprietary"
    if any(token in raw for token in ("apache", "mit", "bsd")):
        return "Permissive open"
    if any(token in raw for token in ("community", "custom", "gemma", "stability", "nvidia", "aws")):
        return "Custom/source-available"
    return "Other open"


def size_bucket(value: float | None) -> str:
    if value is None:
        return "Unknown"
    if value < 1:
        return "<1B"
    if value < 3:
        return "1-3B"
    if value < 7:
        return "3-7B"
    if value < 10:
        return "7-10B"
    if value <= 20:
        return "10-20B"
    return ">20B"


def scale_bucket(value: float | None) -> str:
    if value is None:
        return "Unknown"
    if value < 1:
        return "<1B"
    if value < 3:
        return "1-3B"
    if value < 7:
        return "3-7B"
    if value < 10:
        return "7-10B"
    if value <= 20:
        return "10-20B"
    if value <= 50:
        return "20-50B"
    if value <= 100:
        return "50-100B"
    return ">100B"


def context_bucket(value: object) -> str:
    if value in (None, "", 0):
        return "Unknown"
    try:
        tokens = int(value)
    except (TypeError, ValueError):
        return "Unknown"
    if tokens <= 4096:
        return "<=4K"
    if tokens <= 8192:
        return "8K"
    if tokens <= 32768:
        return "16K-32K"
    if tokens <= 131072:
        return "64K-128K"
    return ">128K"


def normalized_status(model: dict) -> str:
    raw = str(model.get("status") or "unknown").strip().lower()
    if not raw:
        return "Unknown"
    if raw == "active":
        return "Active"
    if raw == "legacy":
        return "Legacy"
    if "deprecated" in raw:
        return "Deprecated"
    return raw.capitalize()


def normalized_base_instruct(model: dict) -> str:
    raw = str(model.get("base_or_instruct") or "").strip().lower()
    if raw in ("base", "instruct", "both"):
        return raw.capitalize()
    return "Unknown"


def top_developers(models: list[dict], limit: int) -> list[str]:
    counts = Counter(model.get("developer", "Unknown") for model in models)
    return [name for name, _ in counts.most_common(limit)]


def parse_benchmark_value(model: dict, key: str) -> float | None:
    """Extract a numeric benchmark score (e.g. MMLU) from a model."""
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
    if match:
        return float(match.group(1))
    return None


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

def apply_figure_theme(
    fig: go.Figure, title: str, *, size: str = "default", show_title: bool = True
) -> go.Figure:
    dimensions = FIGURE_SIZES[size]
    fig.update_layout(
        template=DEFAULT_TEMPLATE,
        title=(
            dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=18, color=PALETTE["ink"]))
            if show_title
            else None
        ),
        font=dict(family="Helvetica, Arial, sans-serif", size=12, color=PALETTE["ink"]),
        width=dimensions["width"],
        height=dimensions["height"],
        margin=BASE_MARGIN if show_title else TITLELESS_MARGIN,
        legend=dict(
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=PALETTE["fog"],
            borderwidth=1,
            font=dict(size=11),
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=PALETTE["fog"],
        showline=True,
        linecolor=PALETTE["fog"],
        linewidth=1,
        mirror=False,
        title_font=dict(size=13, color=PALETTE["ink"]),
        tickfont=dict(size=11, color=PALETTE["ink"]),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=PALETTE["fog"],
        showline=True,
        linecolor=PALETTE["fog"],
        linewidth=1,
        mirror=False,
        title_font=dict(size=13, color=PALETTE["ink"]),
        tickfont=dict(size=11, color=PALETTE["ink"]),
    )
    fig.update_annotations(font=ANNOTATION_FONT)
    return fig


def save_figure(
    fig: go.Figure, output_dir: Path, filename: str, output_format: str
) -> None:
    path = output_dir / f"{filename}.{output_format}"
    fig.write_image(str(path), format=output_format)
    print(f"  saved {path.name}")


# ===========================================================================
# Figure functions (existing 13, improved for consistency)
# ===========================================================================

def figure_slm_releases_by_size(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    years = sorted({y for y in (release_year(m) for m in slms) if y is not None})
    by_year: dict[int, Counter] = defaultdict(Counter)
    for model in slms:
        y = release_year(model)
        if y is not None:
            by_year[y][size_bucket(effective_params_billions(model))] += 1

    fig = go.Figure()
    for bucket in SIZE_BUCKETS:
        fig.add_trace(go.Bar(
            x=[str(y) for y in years],
            y=[by_year[y].get(bucket, 0) for y in years],
            name=bucket,
            marker_color=BUCKET_COLORS[bucket],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, "SLM Releases by Year and Parameter Bucket", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_releases_by_size", output_format)


def figure_slm_context_by_year(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    years = sorted({y for y in (release_year(m) for m in slms) if y is not None})
    fig = go.Figure()
    for year in years:
        values = [
            m["context_window_tokens"]
            for m in slms
            if release_year(m) == year and m.get("context_window_tokens")
        ]
        if not values:
            continue
        color = YEAR_COLORS.get(str(year), PALETTE["slate"])
        fig.add_trace(go.Box(
            name=str(year), y=values, boxmean=True,
            marker_color=color, line_color=color, boxpoints="outliers",
        ))
    apply_figure_theme(fig, "SLM Context Windows by Release Year", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    fig.update_yaxes(title_text="Context window (tokens)", type="log")
    save_figure(fig, output_dir, "paper_slm_context_by_year", output_format)


def figure_slm_context_vs_size(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    points = []
    for model in slms:
        params = effective_params_billions(model)
        context = model.get("context_window_tokens")
        year = release_year(model)
        if params is None or not context or year is None:
            continue
        points.append({
            "name": model.get("name", "Unknown"),
            "year": str(year),
            "params": params,
            "context": context,
            "modality_group": modality_group(model),
        })

    labels = set()
    for row in sorted(points, key=lambda r: r["context"], reverse=True)[:4]:
        labels.add(row["name"])
    for row in sorted(points, key=lambda r: r["params"], reverse=True)[:3]:
        labels.add(row["name"])

    fig = go.Figure()
    for year in sorted({r["year"] for r in points}):
        for group in ("Text-centric", "Multimodal", "Unknown"):
            subset = [r for r in points if r["year"] == year and r["modality_group"] == group]
            if not subset:
                continue
            fig.add_trace(go.Scatter(
                x=[r["params"] for r in subset],
                y=[r["context"] for r in subset],
                mode="markers+text",
                text=[r["name"] if r["name"] in labels else "" for r in subset],
                textposition="top center",
                textfont=ANNOTATION_FONT,
                marker=dict(
                    **MARKER_DEFAULTS,
                    color=YEAR_COLORS.get(year, PALETTE["slate"]),
                    symbol=SYMBOL_MAP[group],
                ),
                name=f"{year} / {group}",
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    + f"Year: {year}<br>"
                    + "Params: %{x:.2f}B<br>"
                    + "Context: %{y:,} tokens<extra></extra>"
                ),
            ))
    apply_figure_theme(fig, "SLM Context-Window Scaling vs Model Size", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameters (billions)", type="log")
    fig.update_yaxes(title_text="Context window (tokens)", type="log")
    save_figure(fig, output_dir, "paper_slm_context_vs_size", output_format)


def figure_developer_portfolio(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    variants = Counter()
    families: dict[str, set] = defaultdict(set)
    multimodal_counts = Counter()
    for model in slms:
        dev = model.get("developer", "Unknown")
        variants[dev] += 1
        families[dev].add(model.get("family", "Unknown"))
        if modality_group(model) == "Multimodal":
            multimodal_counts[dev] += 1

    top = [name for name, _ in variants.most_common(10)]
    family_counts = [len(families[n]) for n in top]
    variant_counts = [variants[n] for n in top]
    mm_share = [round(100.0 * multimodal_counts[n] / variants[n], 1) for n in top]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=top, y=variant_counts, name="Variants", marker_color=PALETTE["indigo"],
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=top, y=family_counts, name="Families", mode="lines+markers",
        line=dict(color=PALETTE["amber"], width=3), marker=dict(size=9),
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=top, y=mm_share, name="Multimodal share (%)", mode="lines+markers",
        line=dict(color=PALETTE["rose"], width=2, dash="dot"), marker=dict(size=8),
    ), secondary_y=True)

    apply_figure_theme(fig, "Developer Concentration in the SLM Inventory", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Developer", tickangle=-30)
    fig.update_yaxes(title_text="Variant count", secondary_y=False)
    fig.update_yaxes(title_text="Family count / multimodal share", secondary_y=True)
    save_figure(fig, output_dir, "paper_slm_developer_portfolio", output_format)


def figure_slm_access_mode(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    access_order = ["OW", "Both", "API"]
    access_labels = {"OW": "Open weights", "Both": "Open weights + API", "API": "API only"}
    access_counts = Counter(m.get("access", "Unknown") for m in slms)

    present = [k for k in access_order if k in access_counts]
    fig = go.Figure(go.Bar(
        x=[access_labels.get(k, k) for k in present],
        y=[access_counts[k] for k in present],
        marker_color=[ACCESS_COLORS.get(k, PALETTE["slate"]) for k in present],
        text=[access_counts[k] for k in present],
        textposition="outside",
    ))
    apply_figure_theme(fig, "SLM Access Mode Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Access mode")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_access_mode", output_format)


def figure_slm_license_posture(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    license_order = [
        "Permissive open", "Custom/source-available", "Proprietary",
        "Unspecified", "Other open", "Unknown",
    ]
    license_counts = Counter(license_group(m) for m in slms)

    present = [k for k in license_order if k in license_counts]
    fig = go.Figure(go.Bar(
        x=present,
        y=[license_counts[k] for k in present],
        marker_color=[LICENSE_COLORS.get(k, PALETTE["slate"]) for k in present],
        text=[license_counts[k] for k in present],
        textposition="outside",
    ))
    apply_figure_theme(fig, "SLM License Posture", show_title=show_title)
    fig.update_xaxes(title_text="License category", tickangle=-25)
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_license_posture", output_format)


def figure_slm_modality_distribution(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    modality_counts = Counter()
    for model in slms:
        for mod in normalize_modalities(model):
            modality_counts[mod] += 1

    labels = [l.capitalize() for l in MODALITY_ORDER if l in modality_counts]
    values = [modality_counts[l.lower()] for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=SOFT_SEQUENCE[:len(labels)],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, "SLM Modality Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Modality")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_modality_distribution", output_format)


def figure_slm_status_distribution(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    statuses = Counter(normalized_status(m) for m in slms)
    order = ["Active", "Legacy", "Deprecated", "Unknown"]
    labels = [l for l in order if l in statuses] + [l for l in sorted(statuses) if l not in order]
    values = [statuses[l] for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=[STATUS_COLORS.get(l, PALETTE["slate"]) for l in labels],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, "SLM Status Distribution", show_title=show_title)
    fig.update_xaxes(title_text="Status")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_status_distribution", output_format)


def figure_slm_developer_param_heatmap(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    developers = top_developers(slms, limit=10)
    buckets = [b for b in SIZE_BUCKETS if b != "Unknown"] + ["Unknown"]
    matrix = []
    for dev in developers:
        params = [size_bucket(effective_params_billions(m)) for m in slms if m.get("developer", "Unknown") == dev]
        counts = Counter(params)
        matrix.append([counts.get(b, 0) for b in buckets])

    fig = go.Figure(go.Heatmap(
        z=matrix, x=buckets, y=developers,
        colorscale=SOFT_HEATMAP,
        text=matrix, texttemplate="%{text}",
        hovertemplate="Developer: %{y}<br>Bucket: %{x}<br>Count: %{z}<extra></extra>",
        colorbar=dict(title="Count"),
    ))
    apply_figure_theme(fig, "Developer by Parameter Bucket", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameter bucket")
    fig.update_yaxes(title_text="Developer")
    save_figure(fig, output_dir, "paper_slm_developer_param_heatmap", output_format)


def figure_slm_cumulative_releases(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    dates = sorted(str(m.get("release_date")) for m in slms if m.get("release_date"))
    cumulative = list(range(1, len(dates) + 1))

    fig = go.Figure(go.Scatter(
        x=dates, y=cumulative, mode="lines",
        line=dict(color=PALETTE["teal"], width=3),
        fill="tozeroy",
        fillcolor=color_with_alpha(PALETTE["teal"], 0.28),
    ))
    apply_figure_theme(fig, "Cumulative SLM Releases", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release date")
    fig.update_yaxes(title_text="Cumulative number of variants")
    save_figure(fig, output_dir, "paper_slm_cumulative_releases", output_format)


def figure_slm_release_timeline_by_developer(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    devs = top_developers(slms, limit=6)
    quarters = sorted(
        {q for q in (release_quarter(m) for m in slms) if q is not None},
        key=quarter_sort_key,
    )
    grouped: dict[str, Counter] = defaultdict(Counter)
    for model in slms:
        q = release_quarter(model)
        if q is None:
            continue
        dev = model.get("developer", "Unknown")
        key = dev if dev in devs else "Other"
        grouped[key][q] += 1

    fig = go.Figure()
    for idx, dev in enumerate(devs + ["Other"]):
        fig.add_trace(go.Bar(
            x=quarters,
            y=[grouped[dev].get(q, 0) for q in quarters],
            name=dev,
            marker_color=SOFT_SEQUENCE[idx % len(SOFT_SEQUENCE)],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, "SLM Release Timeline by Developer", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_release_timeline_by_developer", output_format)


def figure_slm_context_bucket_distribution(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    counts = Counter(context_bucket(m.get("context_window_tokens")) for m in slms)
    values = [counts.get(b, 0) for b in CONTEXT_BUCKETS]

    fig = go.Figure(go.Bar(
        x=CONTEXT_BUCKETS, y=values,
        marker_color=[CONTEXT_BUCKET_COLORS[b] for b in CONTEXT_BUCKETS],
        text=values, textposition="outside",
    ))
    apply_figure_theme(fig, "SLM Context-Window Buckets", show_title=show_title)
    fig.update_xaxes(title_text="Context bucket")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_context_bucket_distribution", output_format)


def figure_slm_family_treemap(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    developer_counts = Counter(m.get("developer", "Unknown") for m in slms)
    top_devs = {name for name, _ in developer_counts.most_common(10)}
    grouped: dict[str, Counter] = defaultdict(Counter)
    for model in slms:
        dev = model.get("developer", "Unknown")
        family = model.get("family", "Unknown")
        key = dev if dev in top_devs else "Other developers"
        grouped[key][family] += 1

    ids = []
    labels = []
    parents = []
    values = []
    colors = []

    dev_palette = [
        PALETTE["indigo"], PALETTE["teal"], PALETTE["amber"], PALETTE["coral"],
        PALETTE["sky"], PALETTE["plum"], PALETTE["mint"], PALETTE["peach"],
        PALETTE["ocean"], PALETTE["lavender"], PALETTE["slate"],
    ]

    for idx, dev in enumerate(sorted(grouped, key=lambda n: sum(grouped[n].values()), reverse=True)):
        dev_id = f"developer::{dev}"
        color = dev_palette[idx % len(dev_palette)]
        ids.append(dev_id)
        labels.append(dev)
        parents.append("")
        values.append(sum(grouped[dev].values()))
        colors.append(color)
        for family, count in grouped[dev].most_common():
            ids.append(f"{dev_id}::family::{family}")
            labels.append(family)
            parents.append(dev_id)
            values.append(count)
            colors.append(color)

    fig = go.Figure(go.Treemap(
        ids=ids, labels=labels, parents=parents, values=values,
        branchvalues="total",
        marker=dict(colors=colors, line=dict(color="white", width=1)),
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Variants: %{value}<extra></extra>",
        tiling=dict(pad=2),
        maxdepth=2,
    ))
    apply_figure_theme(fig, "SLM Ecosystem by Developer and Family", size="tall", show_title=show_title)
    save_figure(fig, output_dir, "paper_slm_family_treemap", output_format)


def figure_scale_buckets(
    slms: list[dict], llms: list[dict],
    output_dir: Path, show_title: bool, output_format: str,
) -> None:
    slm_counts = Counter(scale_bucket(effective_params_billions(m)) for m in slms)
    llm_counts = Counter(scale_bucket(effective_params_billions(m)) for m in llms)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=SCALE_BUCKETS,
        y=[slm_counts.get(b, 0) for b in SCALE_BUCKETS],
        name="SLMs", marker_color=PALETTE["teal"],
    ))
    fig.add_trace(go.Bar(
        x=SCALE_BUCKETS,
        y=[llm_counts.get(b, 0) for b in SCALE_BUCKETS],
        name="LLMs", marker_color=PALETTE["coral"],
    ))
    fig.update_layout(barmode="group")
    apply_figure_theme(fig, "Scale Separation Between SLM and LLM Inventories", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameter bucket")
    fig.update_yaxes(title_text="Model variants")
    save_figure(fig, output_dir, "paper_scale_buckets_slm_vs_llm", output_format)


# ===========================================================================
# New figures (7 additions)
# ===========================================================================

def figure_slm_moe_vs_dense(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    moe_models = [m for m in slms if is_moe(m)]
    dense_models = [m for m in slms if not is_moe(m)]

    categories = ["Count", "Median Total Params (B)", "Median Context (K)"]
    moe_total = [total_params_billions(m) for m in moe_models if total_params_billions(m) is not None]
    dense_total = [total_params_billions(m) for m in dense_models if total_params_billions(m) is not None]
    moe_ctx = [m["context_window_tokens"] / 1024 for m in moe_models if m.get("context_window_tokens")]
    dense_ctx = [m["context_window_tokens"] / 1024 for m in dense_models if m.get("context_window_tokens")]

    moe_values = [
        len(moe_models),
        round(median(moe_total), 1) if moe_total else 0,
        round(median(moe_ctx), 0) if moe_ctx else 0,
    ]
    dense_values = [
        len(dense_models),
        round(median(dense_total), 1) if dense_total else 0,
        round(median(dense_ctx), 0) if dense_ctx else 0,
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories, y=moe_values, name=f"MoE (n={len(moe_models)})",
        marker_color=PALETTE["amber"],
        text=[str(v) for v in moe_values], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=categories, y=dense_values, name=f"Dense (n={len(dense_models)})",
        marker_color=PALETTE["indigo"],
        text=[str(v) for v in dense_values], textposition="outside",
    ))
    fig.update_layout(barmode="group")
    apply_figure_theme(fig, "MoE vs Dense SLM Comparison", show_title=show_title)
    fig.update_yaxes(title_text="Value")
    save_figure(fig, output_dir, "paper_slm_moe_vs_dense", output_format)


def figure_slm_base_vs_instruct(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    years = sorted({y for y in (release_year(m) for m in slms) if y is not None})
    by_year: dict[int, Counter] = defaultdict(Counter)
    for model in slms:
        y = release_year(model)
        if y is not None:
            by_year[y][normalized_base_instruct(model)] += 1

    bi_order = ["Base", "Instruct", "Both", "Unknown"]
    bi_colors = {
        "Base": PALETTE["indigo"],
        "Instruct": PALETTE["teal"],
        "Both": PALETTE["amber"],
        "Unknown": PALETTE["slate"],
    }

    fig = go.Figure()
    for label in bi_order:
        fig.add_trace(go.Bar(
            x=[str(y) for y in years],
            y=[by_year[y].get(label, 0) for y in years],
            name=label, marker_color=bi_colors[label],
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, "SLM Base vs Instruct Releases by Year", show_title=show_title)
    fig.update_xaxes(title_text="Release year")
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_base_vs_instruct", output_format)


def figure_slm_benchmark_vs_params(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    points = []
    for model in slms:
        params = effective_params_billions(model)
        mmlu = parse_benchmark_value(model, "MMLU")
        if params is None or mmlu is None:
            continue
        points.append({
            "name": model.get("name", "Unknown"),
            "params": params,
            "mmlu": mmlu,
            "year": str(release_year(model) or "Unknown"),
            "group": modality_group(model),
        })

    if not points:
        print("  skipped paper_slm_benchmark_vs_params (no MMLU data)")
        return

    # Label top performers and smallest models with high scores
    labels = set()
    for row in sorted(points, key=lambda r: r["mmlu"], reverse=True)[:5]:
        labels.add(row["name"])
    for row in sorted(points, key=lambda r: r["params"])[:3]:
        labels.add(row["name"])

    fig = go.Figure()
    for year in sorted({r["year"] for r in points}):
        for group in ("Text-centric", "Multimodal", "Unknown"):
            subset = [r for r in points if r["year"] == year and r["group"] == group]
            if not subset:
                continue
            fig.add_trace(go.Scatter(
                x=[r["params"] for r in subset],
                y=[r["mmlu"] for r in subset],
                mode="markers+text",
                text=[r["name"] if r["name"] in labels else "" for r in subset],
                textposition="top center",
                textfont=ANNOTATION_FONT,
                marker=dict(
                    **MARKER_DEFAULTS,
                    color=YEAR_COLORS.get(year, PALETTE["slate"]),
                    symbol=SYMBOL_MAP.get(group, "circle"),
                ),
                name=f"{year} / {group}",
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    + f"Year: {year}<br>"
                    + "Params: %{x:.2f}B<br>"
                    + "MMLU: %{y:.1f}%<extra></extra>"
                ),
            ))

    apply_figure_theme(fig, f"SLM MMLU Score vs Parameters (n={len(points)})", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameters (billions)", type="log")
    fig.update_yaxes(title_text="MMLU score (%)")
    save_figure(fig, output_dir, "paper_slm_benchmark_vs_params", output_format)


def figure_slm_developer_diversity_timeline(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    entries: list[tuple[str, str]] = []
    for model in slms:
        q = release_quarter(model)
        if q is None:
            continue
        entries.append((q, model.get("developer", "Unknown")))

    quarters = sorted({q for q, _ in entries}, key=quarter_sort_key)
    seen: set[str] = set()
    cumulative: list[int] = []
    new_per_q: list[int] = []
    for q in quarters:
        devs_in_q = {dev for qq, dev in entries if qq == q}
        new = devs_in_q - seen
        seen |= devs_in_q
        cumulative.append(len(seen))
        new_per_q.append(len(new))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=quarters, y=cumulative, mode="lines+markers",
        name="Cumulative developers",
        line=dict(color=PALETTE["teal"], width=3),
        marker=dict(size=7),
        fill="tozeroy",
        fillcolor=color_with_alpha(PALETTE["teal"], 0.18),
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        x=quarters, y=new_per_q, name="New developers",
        marker_color=color_with_alpha(PALETTE["amber"], 0.7),
    ), secondary_y=True)

    apply_figure_theme(fig, "Developer Diversity in SLM Ecosystem", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text="Cumulative unique developers", secondary_y=False)
    fig.update_yaxes(title_text="New developers per quarter", secondary_y=True)
    save_figure(fig, output_dir, "paper_slm_developer_diversity_timeline", output_format)


def figure_slm_family_size_range(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    family_params: dict[str, list[float]] = defaultdict(list)
    for model in slms:
        p = effective_params_billions(model)
        if p is not None:
            family_params[model.get("family", "Unknown")].append(p)

    # Keep families with at least 2 variants
    families = sorted(
        [(f, vals) for f, vals in family_params.items() if len(vals) >= 2],
        key=lambda item: max(item[1]) - min(item[1]),
        reverse=True,
    )[:15]

    family_names = [f for f, _ in families]
    mins = [min(vals) for _, vals in families]
    maxs = [max(vals) for _, vals in families]
    medians = [round(median(vals), 2) for _, vals in families]

    fig = go.Figure()
    # Range bars
    for i, (name, vals) in enumerate(families):
        color = SOFT_SEQUENCE[i % len(SOFT_SEQUENCE)]
        fig.add_trace(go.Scatter(
            x=[min(vals), max(vals)],
            y=[name, name],
            mode="lines",
            line=dict(color=color, width=8),
            showlegend=False,
            hoverinfo="skip",
        ))
    # Min markers
    fig.add_trace(go.Scatter(
        x=mins, y=family_names, mode="markers",
        name="Min", marker=dict(size=10, color=PALETTE["sky"], symbol="triangle-left"),
    ))
    # Max markers
    fig.add_trace(go.Scatter(
        x=maxs, y=family_names, mode="markers",
        name="Max", marker=dict(size=10, color=PALETTE["coral"], symbol="triangle-right"),
    ))
    # Median markers
    fig.add_trace(go.Scatter(
        x=medians, y=family_names, mode="markers",
        name="Median", marker=dict(size=9, color=PALETTE["ink"], symbol="diamond"),
    ))

    apply_figure_theme(fig, "SLM Family Parameter Range (Top 15)", size="tall", show_title=show_title)
    fig.update_xaxes(title_text="Effective parameters (billions)", type="log")
    fig.update_yaxes(title_text="")
    save_figure(fig, output_dir, "paper_slm_family_size_range", output_format)


def figure_slm_multimodal_timeline(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    quarters = sorted(
        {q for q in (release_quarter(m) for m in slms) if q is not None},
        key=quarter_sort_key,
    )
    by_quarter: dict[str, Counter] = defaultdict(Counter)
    for model in slms:
        q = release_quarter(model)
        if q is None:
            continue
        by_quarter[q][modality_group(model)] += 1

    fig = go.Figure()
    for group, color in [("Text-centric", PALETTE["indigo"]), ("Multimodal", PALETTE["amber"])]:
        fig.add_trace(go.Bar(
            x=quarters,
            y=[by_quarter[q].get(group, 0) for q in quarters],
            name=group, marker_color=color,
        ))
    fig.update_layout(barmode="stack")
    apply_figure_theme(fig, "Rise of Multimodal SLMs", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release quarter", tickangle=-35)
    fig.update_yaxes(title_text="Number of SLM variants")
    save_figure(fig, output_dir, "paper_slm_multimodal_timeline", output_format)


def figure_slm_context_evolution_by_family(
    slms: list[dict], output_dir: Path, show_title: bool, output_format: str
) -> None:
    family_data: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for model in slms:
        date = model.get("release_date")
        ctx = model.get("context_window_tokens")
        if not date or not ctx:
            continue
        family_data[model.get("family", "Unknown")].append((str(date), int(ctx)))

    # Keep families with at least 2 data points and distinct context values
    eligible = []
    for family, data in family_data.items():
        ctx_values = {c for _, c in data}
        if len(data) >= 2 and len(ctx_values) >= 2:
            eligible.append((family, sorted(data)))

    # Sort by max context reached, take top 8
    eligible.sort(key=lambda item: max(c for _, c in item[1]), reverse=True)
    eligible = eligible[:8]

    fig = go.Figure()
    for idx, (family, data) in enumerate(eligible):
        dates = [d for d, _ in data]
        contexts = [c for _, c in data]
        fig.add_trace(go.Scatter(
            x=dates, y=contexts, mode="lines+markers",
            name=family,
            line=dict(color=SOFT_SEQUENCE[idx % len(SOFT_SEQUENCE)], width=2),
            marker=dict(size=7),
        ))

    apply_figure_theme(fig, "Context Window Evolution by SLM Family", size="wide", show_title=show_title)
    fig.update_xaxes(title_text="Release date")
    fig.update_yaxes(title_text="Context window (tokens)", type="log")
    save_figure(fig, output_dir, "paper_slm_context_evolution_by_family", output_format)


# ===========================================================================
# Audit & main
# ===========================================================================

def print_dataset_audit(slms: list[dict], llms: list[dict]) -> None:
    slm_context_known = sum(1 for m in slms if m.get("context_window_tokens"))
    llm_context_known = sum(1 for m in llms if m.get("context_window_tokens"))
    slm_over_limit = [m["name"] for m in slms if (effective_params_billions(m) or 0.0) > 20.0]
    raw_modalities = Counter(
        str(item).strip().lower()
        for m in slms for item in (m.get("modalities") or [])
    )
    slm_numeric_mmlu = 0
    for model in slms:
        if parse_benchmark_value(model, "MMLU") is not None:
            slm_numeric_mmlu += 1

    print("Dataset audit:")
    print(f"  SLMs: {len(slms)} variants; context available for {slm_context_known}")
    print(f"  LLMs: {len(llms)} variants; context available for {llm_context_known}")
    print(f"  SLMs above the stated 20B threshold: {len(slm_over_limit)}")
    if slm_over_limit:
        print("   ", ", ".join(slm_over_limit))
    print(
        "  Raw SLM modality labels:",
        ", ".join(f"{name}={count}" for name, count in raw_modalities.most_common()),
    )
    print(f"  SLM entries with numeric MMLU values: {slm_numeric_mmlu}")
    slm_moe = sum(1 for m in slms if is_moe(m))
    print(f"  SLM MoE models: {slm_moe}")
    bi_counts = Counter(normalized_base_instruct(m) for m in slms)
    print(f"  SLM base/instruct split: {dict(bi_counts)}")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pio.templates.default = DEFAULT_TEMPLATE

    database = load_database(input_path)
    slms = list(database.get("models", {}).get("slm", []))
    llms = list(database.get("models", {}).get("llm", []))

    print_dataset_audit(slms, llms)
    print("\nGenerating figures...")

    # Existing 13 (improved)
    figure_slm_releases_by_size(slms, output_dir, args.title, args.format)
    figure_slm_context_by_year(slms, output_dir, args.title, args.format)
    figure_slm_context_vs_size(slms, output_dir, args.title, args.format)
    figure_developer_portfolio(slms, output_dir, args.title, args.format)
    figure_slm_access_mode(slms, output_dir, args.title, args.format)
    figure_slm_license_posture(slms, output_dir, args.title, args.format)
    figure_slm_modality_distribution(slms, output_dir, args.title, args.format)
    figure_slm_status_distribution(slms, output_dir, args.title, args.format)
    figure_slm_developer_param_heatmap(slms, output_dir, args.title, args.format)
    figure_slm_cumulative_releases(slms, output_dir, args.title, args.format)
    figure_slm_release_timeline_by_developer(slms, output_dir, args.title, args.format)
    figure_slm_context_bucket_distribution(slms, output_dir, args.title, args.format)
    figure_slm_family_treemap(slms, output_dir, args.title, args.format)
    figure_scale_buckets(slms, llms, output_dir, args.title, args.format)

    # New 7
    figure_slm_moe_vs_dense(slms, output_dir, args.title, args.format)
    figure_slm_base_vs_instruct(slms, output_dir, args.title, args.format)
    figure_slm_benchmark_vs_params(slms, output_dir, args.title, args.format)
    figure_slm_developer_diversity_timeline(slms, output_dir, args.title, args.format)
    figure_slm_family_size_range(slms, output_dir, args.title, args.format)
    figure_slm_multimodal_timeline(slms, output_dir, args.title, args.format)
    figure_slm_context_evolution_by_family(slms, output_dir, args.title, args.format)

    generated = sorted(
        path.name
        for path in output_dir.glob(f"*.{args.format}")
        if path.name.startswith("paper_")
    )
    print(f"\nGenerated {len(generated)} paper figures in {output_dir.resolve()}:")
    for name in generated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
