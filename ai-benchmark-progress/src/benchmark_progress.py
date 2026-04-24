"""AI Benchmark Progress — static matplotlib generator.

Generates:
  - output/benchmark_progress_highres.png
  - output/benchmark_progress.svg
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Config
DPI = 150
OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "benchmark_data.csv"

# Colors per category
CATEGORY_COLORS = {
    "Knowledge": "#60a5fa",
    "Coding": "#34d399",
    "Agentic": "#f472b6",
    "Reasoning": "#a78bfa",
}


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df["Human_Baseline"] = pd.to_numeric(df["Human_Baseline"], errors="coerce")
    return df


def plot_benchmarks(df):
    benchmarks = df["Benchmark"].unique()
    n = len(benchmarks)
    fig, axes = plt.subplots(1, n, figsize=(4 * n + 2, 6), sharey=True)
    if n == 1:
        axes = [axes]
    fig.patch.set_facecolor("#0f1117")

    for ax, benchmark in zip(axes, benchmarks):
        ax.set_facecolor("#0f1117")
        bdf = df[df["Benchmark"] == benchmark].sort_values("Year")
        color = CATEGORY_COLORS.get(bdf["Category"].iloc[0], "#9ca3af")
        human = bdf["Human_Baseline"].iloc[0]

        # Plot scores
        ax.plot(
            bdf["Year"],
            bdf["Score"],
            marker="o",
            markersize=8,
            color=color,
            linewidth=2.5,
            zorder=3,
        )

        # Human baseline
        ax.axhline(
            y=human,
            color="#ef4444",
            linestyle="--",
            alpha=0.7,
            linewidth=1.5,
            zorder=2,
        )

        # Annotate crossing point (first score >= human baseline)
        crossed = bdf[bdf["Score"] >= human]
        if not crossed.empty:
            row = crossed.iloc[0]
            ax.annotate(
                f"{row['Model']}\n{int(row['Year'])}",
                xy=(row["Year"], row["Score"]),
                xytext=(8, 8),
                textcoords="offset points",
                fontsize=7,
                color=color,
                alpha=0.9,
                fontweight="bold",
            )

        ax.set_title(benchmark, color="#e8eaf6", fontsize=12, fontweight="bold", pad=10)
        ax.set_xlabel("Year", color="#6b7280", fontsize=10)
        ax.tick_params(colors="#6b7280", labelsize=9)
        ax.set_ylim(0, 105)
        ax.grid(True, alpha=0.15, color="#374151")
        for spine in ax.spines.values():
            spine.set_color("#2d3148")

    axes[0].set_ylabel("Score (%)", color="#d1d5db", fontsize=12)

    # Global title
    fig.suptitle(
        "AI Benchmark Progress: Crossing Human Baselines",
        color="#e8eaf6",
        fontsize=16,
        fontweight="bold",
        y=1.02,
    )

    # Legend
    legend_patches = [
        mpatches.Patch(color=color, label=cat)
        for cat, color in CATEGORY_COLORS.items()
    ]
    legend_patches.append(
        mpatches.Patch(color="#ef4444", label="Human Baseline")
    )
    fig.legend(
        handles=legend_patches,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=5,
        facecolor="#1c1f2e",
        edgecolor="#2d3148",
        labelcolor="#d1d5db",
        fontsize=9,
    )

    plt.tight_layout()
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = plot_benchmarks(df)

    fig.savefig(
        OUTPUT_DIR / "benchmark_progress_highres.png",
        dpi=DPI,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    fig.savefig(
        OUTPUT_DIR / "benchmark_progress.svg",
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    plt.close(fig)
    print("Generated: benchmark_progress_highres.png, benchmark_progress.svg")


if __name__ == "__main__":
    main()
