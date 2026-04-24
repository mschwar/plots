#!/usr/bin/env python3
"""Interactive AI compute timeline with speculative filtering."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go


STATUS_SYMBOLS = {
    "observed": "circle",
    "estimated": "circle-open",
    "proxy": "square",
    "projection": "triangle-up",
    "speculative": "diamond",
}

STATUS_COLORS = {
    "observed": "#2563eb",
    "estimated": "#7c3aed",
    "proxy": "#64748b",
    "projection": "#f59e0b",
    "speculative": "#dc2626",
}


def load_data() -> pd.DataFrame:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), "data", "ai_milestones.csv")
    df = pd.read_csv(csv_path)
    for column in ("value_numeric", "value_low", "value_high"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df.sort_values("year")


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


def create_chart(df: pd.DataFrame) -> go.Figure:
    df = df.copy()
    df["plot_value"] = df.apply(plotted_value, axis=1)

    fig = go.Figure()

    for start, end, label, color in [
        (1900, 2012, "historical foundations", "rgba(148,163,184,0.12)"),
        (2012, 2022, "deep learning scaling", "rgba(124,58,237,0.10)"),
        (2022, 2026, "current frontier", "rgba(59,130,246,0.10)"),
        (2026, 2027, "speculative", "rgba(220,38,38,0.12)"),
    ]:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, line_width=0, annotation_text=label, annotation_position="top")

    for status in ["observed", "estimated", "proxy", "projection", "speculative"]:
        status_df = df[df["estimate_status"] == status]
        if status_df.empty:
            continue
        visible = True if status != "speculative" else "legendonly"
        hover = [
            f"<b>{row.event}</b><br>Year: {row.year}<br>"
            f"Value: {row.value_numeric if pd.notna(row.value_numeric) else 'context marker'}<br>"
            f"Unit: {row.value_unit}<br>Status: {row.estimate_status}<br>"
            f"Confidence: {row.confidence}<br>Source: {row.source_id or 'none'}<br>{row.notes}"
            for row in status_df.itertuples()
        ]
        fig.add_trace(go.Scatter(
            x=status_df["year"],
            y=status_df["plot_value"],
            mode="markers",
            marker=dict(
                size=12,
                color=STATUS_COLORS[status],
                symbol=STATUS_SYMBOLS[status],
                line=dict(width=1.2, color="white"),
            ),
            name=status.title(),
            text=hover,
            hoverinfo="text",
            visible=visible,
        ))

        bounded = status_df.dropna(subset=["value_low", "value_high"])
        if not bounded.empty:
            for _, row in bounded.iterrows():
                fig.add_shape(
                    type="line",
                    x0=row["year"],
                    x1=row["year"],
                    y0=row["value_low"],
                    y1=row["value_high"],
                    line=dict(color="rgba(30,41,59,0.25)", width=1),
                )

    label_df = df[df["display_label"].notna()].copy()
    label_df = label_df[label_df["display_label"].astype(str).str.strip() != ""]
    label_df = label_df.sort_values("plot_value", ascending=False).head(14)
    for _, row in label_df.iterrows():
        fig.add_annotation(
            x=row["year"],
            y=row["plot_value"],
            text=row["display_label"],
            showarrow=True,
            arrowhead=0,
            arrowwidth=1,
            arrowcolor="rgba(100,100,100,0.45)",
            ax=20,
            ay=-28,
            font=dict(size=9),
            bgcolor="rgba(255,255,255,0.85)",
        )

    fig.add_vline(x=2022, line_dash="dash", line_color="#64748b")
    fig.add_vline(x=2026, line_dash="dash", line_color="#dc2626")

    fig.update_layout(
        title="<b>AI Compute Timeline</b><br><sup>Training FLOPs, proxies, estimates, and speculative projections separated structurally</sup>",
        xaxis=dict(title="Year", range=[1898, 2028], dtick=10),
        yaxis=dict(title="Value (log scale; see hover for unit)", type="log", range=[1, 29]),
        legend=dict(orientation="h", y=1.03, x=0.5, xanchor="center", yanchor="bottom"),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="white",
        hovermode="closest",
        autosize=True,
        margin=dict(t=120, b=90, l=80, r=40),
    )
    fig.add_annotation(
        text="Footnote: speculative rows are hidden by default in the legend. Toggle 'Speculative' to show future projections. Ops/sec proxies are not training FLOPs.",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.14,
        showarrow=False,
        font=dict(size=10, color="#666"),
    )
    return fig


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "output")
    os.makedirs(output_dir, exist_ok=True)
    fig = create_chart(load_data())
    fig.write_html(os.path.join(output_dir, "ai_compute_timeline_interactive.html"), include_plotlyjs="cdn")
    print("Saved ai_compute_timeline_interactive.html")


if __name__ == "__main__":
    main()
