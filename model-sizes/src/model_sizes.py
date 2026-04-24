#!/usr/bin/env python3
"""Static chart for LLM model size growth."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd


ORG_COLORS = {
    "OpenAI": "#2563eb",
    "Google": "#16a34a",
    "Meta": "#7c3aed",
    "Anthropic": "#dc2626",
    "Mistral": "#ea580c",
    "DeepSeek": "#0891b2",
}


def load_data() -> pd.DataFrame:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), "data", "llm_model_sizes.csv")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25
    return df.sort_values("date")


def create_chart(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#FAFAFA")

    eras = [
        (2019, 2022.9, "#E8F4FD", "Pre-ChatGPT"),
        (2022.9, 2024.2, "#F0E8FF", "Foundation models"),
        (2024.2, 2025.1, "#E8F8E8", "Open weights"),
        (2025.1, 2026.5, "#FFE8E8", "Reasoning & agents"),
    ]
    for start, end, color, label in eras:
        ax.axvspan(start, end, color=color, alpha=0.45, zorder=0)
        ax.text((start + end) / 2, 7500, label, ha="center", va="top", fontsize=8, color="#555")

    for _, row in df.iterrows():
        color = ORG_COLORS.get(row["org"], "#6b7280")
        marker = "D" if bool(row["estimated"]) else "o"
        alpha = 0.55 if bool(row["estimated"]) else 0.9
        edge = "#111827" if bool(row["unreleased"]) else "white"
        ax.scatter(row["year"], row["params_billions"], s=95, c=color, marker=marker,
                   alpha=alpha, edgecolors=edge, linewidths=1.4, zorder=3)

    labels = {
        "GPT-2", "GPT-3", "ChatGPT", "GPT-4", "LLaMA 3.1 405B",
        "DeepSeek R1", "Claude Opus 4.7", "GPT Spud"
    }
    for _, row in df.iterrows():
        if row["name"] in labels:
            ax.annotate(
                row["name"],
                xy=(row["year"], row["params_billions"]),
                xytext=(4, 8),
                textcoords="offset points",
                fontsize=8,
                arrowprops=dict(arrowstyle="-", color="#777", lw=0.5),
            )

    ax.set_yscale("log")
    ax.set_xlim(2018.8, 2026.55)
    ax.set_ylim(1, 10000)
    ax.set_xlabel("Year", fontweight="bold")
    ax.set_ylabel("Parameters (billions, log scale)", fontweight="bold")
    ax.set_title("LLM Model Sizes Over Time\nDisclosed counts vs. estimates and unreleased projections", fontweight="bold", pad=14)
    ax.grid(True, which="major", axis="y", alpha=0.25)
    ax.grid(True, which="major", axis="x", alpha=0.15)

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#6b7280", markeredgecolor="white", markersize=8, label="Disclosed"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="#6b7280", markeredgecolor="white", markersize=8, label="Estimated"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="#6b7280", markeredgecolor="#111827", markersize=8, label="Unreleased"),
    ]
    ax.legend(handles=handles, loc="lower right", framealpha=0.9)
    ax.text(
        0.01,
        0.02,
        "Footnote: frontier labs generally stopped disclosing parameter counts after GPT-3. 2023+ points are estimates unless marked otherwise.",
        transform=ax.transAxes,
        fontsize=8,
        color="#555",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#ddd", alpha=0.9),
    )

    plt.tight_layout()
    return fig


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "output")
    os.makedirs(output_dir, exist_ok=True)

    fig = create_chart(load_data())
    fig.savefig(os.path.join(output_dir, "model_sizes.png"), dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(output_dir, "model_sizes_highres.png"), dpi=400, bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(output_dir, "model_sizes.svg"), format="svg", bbox_inches="tight", facecolor="white")
    print("Saved model-sizes static outputs")


if __name__ == "__main__":
    main()
