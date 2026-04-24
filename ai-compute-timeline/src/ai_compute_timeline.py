#!/usr/bin/env python3
"""Static AI compute timeline with separated estimate statuses."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


STATUS_STYLES = {
    "observed": {"marker": "o", "alpha": 0.9, "label": "Observed"},
    "estimated": {"marker": "o", "alpha": 0.75, "label": "Estimated"},
    "proxy": {"marker": "s", "alpha": 0.55, "label": "Proxy"},
    "projection": {"marker": "^", "alpha": 0.5, "label": "Projection"},
    "speculative": {"marker": "D", "alpha": 0.45, "label": "Speculative"},
}

CATEGORY_COLORS = {
    "Hardware": "#E67E22",
    "Theoretical Foundation": "#7F8C8D",
    "AI Milestone": "#16A085",
    "Model Release": "#8E44AD",
    "Model/Architecture": "#9B59B6",
    "Dataset": "#27AE60",
    "Robotics": "#E74C3C",
    "AI Winter": "#BDC3C7",
    "Infrastructure": "#8B4513",
    "Generative": "#FF69B4",
    "Reasoning/Agentic": "#1D8348",
    "Quantum/Future Speculative": "#9B59B6",
    "Speculative": "#9B59B6",
}


def load_data() -> pd.DataFrame:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), "data", "ai_milestones.csv")
    df = pd.read_csv(csv_path)
    for column in ("value_numeric", "value_low", "value_high"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def primary_category(value: str) -> str:
    return str(value).split(";")[0].strip()


def plotted_value(row: pd.Series) -> float:
    if np.isfinite(row["value_numeric"]):
        return row["value_numeric"]
    year = row["year"]
    if year < 1945:
        return 1e2
    if year < 1960:
        return 1e4
    if year < 1980:
        return 1e6
    if year < 2000:
        return 1e8
    if year < 2012:
        return 1e10
    return 1e12


def plot_panel(ax, df: pd.DataFrame, title: str, xlim: tuple[int, int], label_limit: int) -> None:
    panel = df[(df["year"] >= xlim[0]) & (df["year"] <= xlim[1])].copy()
    panel["plot_value"] = panel.apply(plotted_value, axis=1)

    ax.set_facecolor("#FAFAFA")
    ax.axvspan(xlim[0], min(2022, xlim[1]), color="#F0F0F0", alpha=0.35, zorder=0)
    if xlim[1] >= 2022:
        ax.axvspan(2022, min(2026, xlim[1]), color="#F0E8FF", alpha=0.35, zorder=0)
        ax.axvspan(2026, xlim[1], color="#FFE8E8", alpha=0.45, zorder=0)
        ax.axvline(2022, color="#666", linestyle="--", linewidth=1)
        ax.axvline(2026, color="#b91c1c", linestyle="--", linewidth=1)
        ax.text(2022.15, 3e28, "current frontier", fontsize=8, color="#555")
        ax.text(2026.05, 3e28, "speculative", fontsize=8, color="#8a1f1f")

    for status, style in STATUS_STYLES.items():
        status_df = panel[panel["estimate_status"] == status]
        if status_df.empty:
            continue
        colors = [CATEGORY_COLORS.get(primary_category(cat), "#3498DB") for cat in status_df["category"]]
        ax.scatter(
            status_df["year"],
            status_df["plot_value"],
            c=colors,
            s=95,
            marker=style["marker"],
            alpha=style["alpha"],
            edgecolors="white",
            linewidths=1.2,
            label=style["label"],
            zorder=3,
        )
        bounded = status_df.dropna(subset=["value_low", "value_high"])
        if not bounded.empty:
            ax.vlines(
                bounded["year"],
                bounded["value_low"],
                bounded["value_high"],
                colors="#444",
                alpha=0.25,
                linewidth=1.5,
                zorder=2,
            )

    label_rows = panel.dropna(subset=["display_label"])
    label_rows = label_rows[label_rows["display_label"].astype(str).str.strip() != ""]
    label_rows = label_rows.sort_values("plot_value", ascending=False).head(label_limit)
    for _, row in label_rows.iterrows():
        ax.annotate(
            row["display_label"],
            xy=(row["year"], row["plot_value"]),
            xytext=(4, 8),
            textcoords="offset points",
            fontsize=8,
            arrowprops=dict(arrowstyle="-", color="#777", lw=0.5, alpha=0.5),
        )

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_yscale("log")
    ax.set_xlim(*xlim)
    ax.set_ylim(1e1, 1e29)
    ax.grid(True, which="major", axis="y", alpha=0.25)
    ax.grid(True, which="major", axis="x", alpha=0.15)


def create_chart(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=150, sharey=True)
    fig.patch.set_facecolor("white")

    plot_panel(axes[0], df, "1900-2011: historical foundations and proxies", (1900, 2011), 12)
    plot_panel(axes[1], df, "2012-2026: frontier training compute", (2012, 2027), 10)

    axes[0].set_ylabel("Value (log scale; unit depends on marker)", fontweight="bold")
    for ax in axes:
        ax.set_xlabel("Year", fontweight="bold")

    handles = [
        Line2D([0], [0], marker=style["marker"], color="w", markerfacecolor="#6b7280",
               markeredgecolor="white", markersize=8, label=style["label"])
        for style in STATUS_STYLES.values()
    ]
    fig.legend(handles=handles, loc="upper center", ncol=5, frameon=False, bbox_to_anchor=(0.5, 0.98))
    fig.suptitle("AI Compute Timeline", fontsize=18, fontweight="bold", y=1.04)
    fig.text(
        0.5,
        0.01,
        "Footnote: training FLOPs, ops/sec proxies, no-unit milestones, estimates, projections, and speculative rows are separated by marker and data fields. Dense labels are moved into hover text in the interactive chart.",
        ha="center",
        fontsize=8,
        color="#555",
    )
    plt.tight_layout(rect=[0, 0.04, 1, 0.93])
    return fig


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "output")
    os.makedirs(output_dir, exist_ok=True)
    fig = create_chart(load_data())
    fig.savefig(os.path.join(output_dir, "ai_compute_timeline.png"), dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(output_dir, "ai_compute_timeline_highres.png"), dpi=400, bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(output_dir, "ai_compute_timeline.svg"), format="svg", bbox_inches="tight", facecolor="white")
    print("Saved AI compute static outputs")


if __name__ == "__main__":
    main()
