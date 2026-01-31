#!/usr/bin/env python3
"""
Adoption Timeline – Time to ~50M Users (1957–2026)
Kurzweil-simple: minimal canvas noise, hover-first, one core idea
"""

import numpy as np
import pandas as pd
import os

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")


# Category colors
CATEGORY_COLORS = {
    'Hardware': '#3498DB',
    'Software/Compiler': '#E67E22',
    'Internet/Web': '#27AE60',
    'Mobile': '#9B59B6',
    'Social/Apps': '#FF69B4',
    'Cloud/Infrastructure': '#8B4513',
    'AI/Agentic': '#E74C3C',
}

# Impact → marker size
IMPACT_SIZES = {
    'Transformative': 18,
    'Speculative Transformative': 16,
    'High': 12,
    'Medium': 9,
}

# Only these get always-visible labels (4-6 anchors)
ANCHOR_LABELS = ['ARPANET', 'WWW', 'iPhone', 'ChatGPT']


def load_data():
    """Load CSV data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'tech_adoption.csv')
    return pd.read_csv(csv_path)


def days_to_readable(days):
    """Convert days to human-readable format."""
    if days >= 3650:
        return f"~{days // 365} years"
    elif days >= 365:
        years = days / 365
        return f"~{years:.1f} years"
    elif days >= 30:
        months = days / 30
        return f"~{months:.0f} months"
    else:
        return f"{days} days"


def create_chart(df, export_mode=False):
    """
    Create Plotly chart.
    export_mode=True: minimal annotations for clean PNG/SVG export.
    """
    fig = go.Figure()

    # Sort by year
    df = df.sort_values('Year')

    # Subtle era shading (very light, no text labels in export mode)
    eras = [
        (1955, 1990, 'rgba(200,200,200,0.15)'),
        (1990, 2005, 'rgba(100,150,220,0.12)'),
        (2005, 2015, 'rgba(180,150,220,0.12)'),
        (2015, 2030, 'rgba(255,150,150,0.15)'),
    ]
    for start, end, color in eras:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, line_width=0)

    # Connecting line (subtle)
    fig.add_trace(go.Scatter(
        x=df['Year'], y=df['Days_to_Adoption'],
        mode='lines',
        line=dict(color='rgba(100,100,100,0.25)', width=1.5),
        showlegend=False, hoverinfo='skip'
    ))

    # Exponential trend line (subtle dashed)
    trend_years = np.linspace(1957, 2030, 100)
    k = np.log(3650 / 14) / (2026 - 1957)
    trend_days = 3650 * np.exp(-k * (trend_years - 1957))
    fig.add_trace(go.Scatter(
        x=trend_years, y=trend_days,
        mode='lines',
        line=dict(color='rgba(230,126,34,0.4)', width=1.5, dash='dash'),
        name='Trend (visual guide)',
        hovertemplate='Exponential fit<br>Year: %{x:.0f}<br>Days: %{y:.0f}<extra></extra>'
    ))

    # Group by category for legend
    for cat in df['Category'].unique():
        cat_df = df[df['Category'] == cat]
        color = CATEGORY_COLORS.get(cat, '#7F8C8D')

        sizes = [IMPACT_SIZES.get(imp, 10) for imp in cat_df['Impact']]
        symbols = ['diamond' if 'Speculative' in str(imp) or yr >= 2026 else 'circle'
                   for imp, yr in zip(cat_df['Impact'], cat_df['Year'])]

        # Rich hover template
        hover_texts = [
            f"<b>{row['Event']}</b><br>"
            f"Year: {row['Year']}<br>"
            f"Time to 50M: <b>{days_to_readable(row['Days_to_Adoption'])}</b><br>"
            f"Category: {row['Category']}<br>"
            f"Impact: {row['Impact']}"
            for _, row in cat_df.iterrows()
        ]

        fig.add_trace(go.Scatter(
            x=cat_df['Year'], y=cat_df['Days_to_Adoption'],
            mode='markers',
            marker=dict(
                size=sizes,
                color=color,
                symbol=symbols,
                line=dict(width=1.5, color='white')
            ),
            name=cat,
            text=hover_texts,
            hoverinfo='text'
        ))

    # Always-visible anchor labels (only 4-6 key events)
    if not export_mode:
        for _, row in df.iterrows():
            # Check if this event should have an anchor label
            is_anchor = any(anchor in row['Event'] for anchor in ANCHOR_LABELS)
            if is_anchor:
                # Short label
                label = row['Event'].split('(')[0].split('/')[0].strip()
                if 'World Wide Web' in row['Event']:
                    label = 'WWW'
                elif 'ARPANET' in row['Event']:
                    label = 'ARPANET'
                elif 'iPhone' in row['Event']:
                    label = 'iPhone'
                elif 'ChatGPT' in row['Event']:
                    label = 'ChatGPT'

                fig.add_annotation(
                    x=row['Year'], y=row['Days_to_Adoption'],
                    text=label,
                    showarrow=True,
                    arrowhead=0,
                    arrowsize=0.5,
                    arrowwidth=1,
                    arrowcolor='rgba(100,100,100,0.5)',
                    ax=0 if row['Year'] > 2000 else 20,
                    ay=-30,
                    font=dict(size=10, color='#333'),
                    bgcolor='rgba(255,255,255,0.85)',
                    borderpad=3
                )

    # Human-readable Y-axis ticks
    y_tickvals = [14, 30, 90, 365, 1095, 3650]
    y_ticktext = ['2 wk', '1 mo', '3 mo', '1 yr', '3 yr', '10 yr']

    fig.update_layout(
        title=dict(
            text='<b>Time to Mass Adoption</b><br>'
                 '<sup>Days to ~50M Users (1957–2026)</sup>',
            x=0.5,
            font=dict(size=18)
        ),
        xaxis=dict(
            title='Year',
            range=[1953, 2030],
            tickmode='linear', tick0=1960, dtick=10,
            gridcolor='rgba(128,128,128,0.15)'
        ),
        yaxis=dict(
            title='Days to ~50M Users',
            type='log',
            range=[1, 4],
            gridcolor='rgba(128,128,128,0.2)',
            tickvals=y_tickvals,
            ticktext=y_ticktext
        ),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='center', x=0.5,
            font=dict(size=9),
            itemsizing='constant'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=900 if export_mode else 1000,
        height=550 if export_mode else 600,
        margin=dict(t=100, b=80, l=60, r=40),
        hovermode='closest'
    )

    # Caption below chart (not inside canvas)
    if not export_mode:
        fig.add_annotation(
            text="Adoption times compressed from ~10 years (1957) to ~60 days (ChatGPT). "
                 "Trend line is visual guide, not causal model. "
                 "Sources: Statista, Asymco, Epoch AI.",
            xref='paper', yref='paper',
            x=0.5, y=-0.12,
            showarrow=False,
            font=dict(size=9, color='#666'),
            align='center'
        )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Please install plotly: pip install plotly")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    df = load_data()
    print(f"Loaded {len(df)} records")

    # Interactive version
    fig = create_chart(df, export_mode=False)
    html_path = os.path.join(output_dir, 'adoption_timeline_interactive.html')
    fig.write_html(html_path)
    print(f"Saved: {html_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
