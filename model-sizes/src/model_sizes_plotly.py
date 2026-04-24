#!/usr/bin/env python3
"""Interactive Plotly chart for LLM model size growth."""

from __future__ import annotations

import os

import pandas as pd
import plotly.graph_objects as go


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
    return pd.read_csv(csv_path, parse_dates=["date"]).sort_values("date")


def create_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for org in df["org"].unique():
        org_df = df[df["org"] == org]
        symbols = [
            "diamond-open" if row.unreleased else ("diamond" if row.estimated else "circle")
            for row in org_df.itertuples()
        ]
        hover = [
            f"<b>{row.name}</b><br>Date: {row.date.date()}<br>Org: {row.org}<br>"
            f"Params: {row.params_billions:g}B<br>Estimated: {row.estimated}<br>"
            f"Unreleased: {row.unreleased}<br>{row.note}"
            for row in org_df.itertuples()
        ]
        fig.add_trace(go.Scatter(
            x=org_df["date"],
            y=org_df["params_billions"],
            mode="markers",
            marker=dict(size=12, color=ORG_COLORS.get(org, "#6b7280"), symbol=symbols, line=dict(width=1, color="white")),
            name=org,
            text=hover,
            hoverinfo="text",
        ))

    for start, end, label, color in [
        ("2019-01-01", "2022-11-30", "Pre-ChatGPT", "rgba(96,165,250,0.10)"),
        ("2022-11-30", "2024-04-01", "Foundation models", "rgba(167,139,250,0.10)"),
        ("2024-04-01", "2025-01-01", "Open weights", "rgba(34,197,94,0.10)"),
        ("2025-01-01", "2026-07-01", "Reasoning & agents", "rgba(248,113,113,0.10)"),
    ]:
        x0 = pd.to_datetime(start)
        x1 = pd.to_datetime(end)
        fig.add_vrect(x0=x0, x1=x1, fillcolor=color, line_width=0)
        fig.add_annotation(x=x0 + (x1 - x0) / 2, y=8000, text=label, showarrow=False, font=dict(size=10, color="#666"))

    fig.update_layout(
        title="<b>LLM Model Sizes Over Time</b><br><sup>Disclosed counts vs. estimates and unreleased projections</sup>",
        xaxis_title="Release or projected date",
        yaxis=dict(title="Parameters (billions, log scale)", type="log"),
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", yanchor="bottom"),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="white",
        hovermode="closest",
        autosize=True,
        margin=dict(t=110, b=80, l=70, r=40),
    )
    fig.add_annotation(
        text="Footnote: 2023+ frontier parameter counts are often estimates. Open markers indicate unreleased or not publicly available models.",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.16,
        showarrow=False,
        font=dict(size=10, color="#666"),
    )
    return fig


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "output")
    os.makedirs(output_dir, exist_ok=True)
    fig = create_chart(load_data())
    fig.write_html(os.path.join(output_dir, "model_sizes_interactive.html"), include_plotlyjs="cdn")
    print("Saved model_sizes_interactive.html")


if __name__ == "__main__":
    main()
