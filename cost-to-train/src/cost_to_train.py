"""Cost-to-Train Frontier — static matplotlib generator."""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DPI = 150
OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "training_costs.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Training_FLOPs"] = pd.to_numeric(df["Training_FLOPs"], errors="coerce")
    df["Cost_Million_USD"] = pd.to_numeric(df["Cost_Million_USD"], errors="coerce")
    df["Dollar_per_FLOP"] = pd.to_numeric(df["Dollar_per_FLOP"], errors="coerce")
    return df


def plot_cost(df):
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor("#0f1117")
    ax1.set_facecolor("#0f1117")

    # Primary axis: FLOPs (log scale)
    color_flops = "#60a5fa"
    ax1.semilogy(df["Year"], df["Training_FLOPs"], "o-", color=color_flops,
                 linewidth=3, markersize=10, label="Training FLOPs", zorder=3)
    ax1.set_xlabel("Year", color="#d1d5db", fontsize=12)
    ax1.set_ylabel("Training FLOPs (log)", color=color_flops, fontsize=12)
    ax1.tick_params(axis="y", labelcolor=color_flops, colors="#6b7280")
    ax1.tick_params(axis="x", colors="#6b7280")
    ax1.grid(True, alpha=0.15, color="#374151")
    ax1.spines[:].set_color("#2d3148")

    # Secondary axis: $/FLOP (log scale)
    ax2 = ax1.twinx()
    color_cost = "#34d399"
    ax2.semilogy(df["Year"], df["Dollar_per_FLOP"], "s--", color=color_cost,
                 linewidth=2, markersize=8, label="$/FLOP (collapsing)", zorder=3)
    ax2.set_ylabel("$/FLOP (log, collapsing)", color=color_cost, fontsize=12)
    ax2.tick_params(axis="y", labelcolor=color_cost)
    ax2.spines[:].set_color("#2d3148")

    # Title
    ax1.set_title(
        "The Efficiency Paradox: FLOPs Explode, $/FLOP Collapses",
        color="#e8eaf6",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Annotate key models
    for _, row in df.iterrows():
        if row["Model"] in ["GPT-3", "GPT-4 (est)", "Claude Opus 4.7"]:
            ax1.annotate(
                row["Model"],
                xy=(row["Year"], row["Training_FLOPs"]),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=8,
                color=color_flops,
                alpha=0.9,
            )

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left",
        facecolor="#1c1f2e",
        edgecolor="#2d3148",
        labelcolor="#d1d5db",
    )

    plt.tight_layout()
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = plot_cost(df)

    fig.savefig(OUTPUT_DIR / "cost_to_train_highres.png", dpi=DPI,
                facecolor=fig.get_facecolor(), edgecolor="none")
    fig.savefig(OUTPUT_DIR / "cost_to_train.svg",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Generated: cost_to_train_highres.png, cost_to_train.svg")


if __name__ == "__main__":
    main()
