"""AI Benchmark Progress — Plotly interactive generator."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "benchmark_data.csv"

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


def build_figure(df):
    benchmarks = df["Benchmark"].unique()
    fig = make_subplots(
        rows=1, cols=len(benchmarks),
        subplot_titles=benchmarks,
        horizontal_spacing=0.05,
    )

    for idx, benchmark in enumerate(benchmarks, 1):
        bdf = df[df["Benchmark"] == benchmark].sort_values("Year")
        color = CATEGORY_COLORS.get(bdf["Category"].iloc[0], "#9ca3af")
        human = bdf["Human_Baseline"].iloc[0]

        # Score line
        fig.add_trace(
            go.Scatter(
                x=bdf["Year"],
                y=bdf["Score"],
                mode="lines+markers",
                name=f"{benchmark} — Score",
                line=dict(color=color, width=3),
                marker=dict(size=10),
                hovertemplate=(
                    "%{text}<br>"
                    "Year: %{x}<br>"
                    "Score: %{y:.1f}%<extra></extra>"
                ),
                text=bdf["Model"] + " (" + bdf["Organization"] + ")",
                showlegend=(idx == 1),
            ),
            row=1, col=idx,
        )

        # Human baseline
        fig.add_trace(
            go.Scatter(
                x=[bdf["Year"].min(), bdf["Year"].max()],
                y=[human, human],
                mode="lines",
                name="Human Baseline" if idx == 1 else None,
                line=dict(color="#ef4444", dash="dash", width=2),
                showlegend=(idx == 1),
            ),
            row=1, col=idx,
        )

        fig.update_yaxes(range=[0, 105], row=1, col=idx)

    fig.update_layout(
        title=dict(
            text="AI Benchmark Progress: Crossing Human Baselines",
            font=dict(size=20, color="#e8eaf6"),
            x=0.5,
        ),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#d1d5db", family="SF Pro Display, sans-serif"),
        legend=dict(
            bgcolor="#1c1f2e",
            bordercolor="#2d3148",
            font=dict(color="#d1d5db"),
        ),
        height=600,
        margin=dict(t=80, b=60),
    )

    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = build_figure(df)

    fig.write_html(
        OUTPUT_DIR / "benchmark_progress_interactive.html",
        include_plotlyjs="cdn",
        full_html=True,
    )
    print("Generated: benchmark_progress_interactive.html")


if __name__ == "__main__":
    main()
