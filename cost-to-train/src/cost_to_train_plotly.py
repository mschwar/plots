"""Cost-to-Train Frontier — Plotly interactive generator."""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "training_costs.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Training_FLOPs"] = pd.to_numeric(df["Training_FLOPs"], errors="coerce")
    df["Cost_Million_USD"] = pd.to_numeric(df["Cost_Million_USD"], errors="coerce")
    df["Dollar_per_FLOP"] = pd.to_numeric(df["Dollar_per_FLOP"], errors="coerce")
    return df


def build_figure(df):
    fig = go.Figure()

    # Training FLOPs
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Training_FLOPs"],
        mode="lines+markers",
        name="Training FLOPs",
        line=dict(color="#60a5fa", width=3),
        marker=dict(size=10),
        hovertemplate="%{text}<br>Year: %{x}<br>FLOPs: %{y:.2e}<extra></extra>",
        text=df["Model"] + " (" + df["Organization"] + ")",
        yaxis="y1",
    ))

    # $/FLOP
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Dollar_per_FLOP"],
        mode="lines+markers",
        name="$/FLOP (collapsing)",
        line=dict(color="#34d399", width=2, dash="dash"),
        marker=dict(size=8),
        hovertemplate="%{text}<br>Year: %{x}<br>$/FLOP: %{y:.2e}<extra></extra>",
        text=df["Model"],
        yaxis="y2",
    ))

    fig.update_layout(
        title=dict(
            text="The Efficiency Paradox: FLOPs Explode, $/FLOP Collapses",
            font=dict(size=20, color="#e8eaf6"),
            x=0.5,
        ),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#d1d5db", family="SF Pro Display, sans-serif"),
        xaxis=dict(
            title="Year",
            gridcolor="#1e2030",
            color="#d1d5db",
        ),
        yaxis=dict(
            title="Training FLOPs (log scale)",
            type="log",
            gridcolor="#1e2030",
            color="#60a5fa",
        ),
        yaxis2=dict(
            title="$/FLOP (log scale, collapsing)",
            type="log",
            overlaying="y",
            side="right",
            color="#34d399",
        ),
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
        OUTPUT_DIR / "cost_to_train_interactive.html",
        include_plotlyjs="cdn",
        full_html=True,
    )
    print("Generated: cost_to_train_interactive.html")


if __name__ == "__main__":
    main()
