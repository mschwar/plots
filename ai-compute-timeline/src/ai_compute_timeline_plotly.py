#!/usr/bin/env python3
"""
History of Compute & Intelligence: Training FLOPs for Key AI Milestones (1900-2026)
Interactive Plotly version with hover tooltips
"""

import numpy as np
import pandas as pd
import os
import re

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")


def load_data():
    """Load data from CSV file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'ai_milestones.csv')
    return pd.read_csv(csv_path)


def parse_flops(value):
    """Convert FLOPs string to numeric value."""
    if not value or value == 'N/A':
        return None
    value = str(value).strip()
    if 'Speculative' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        return 1e27
    if 'High compute' in value or value == 'Speculative':
        return 1e21
    if 'Proxy' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        if 'low' in value.lower():
            return 1e6
        return 1e3
    range_match = re.search(r'(\d+\.?\d*)e(\d+)[-–](\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
    if range_match:
        low = float(f"{range_match.group(1)}e{range_match.group(2)}")
        high = float(f"{range_match.group(3)}e{range_match.group(4)}")
        return np.sqrt(low * high)
    if value.startswith('>'):
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
    if 'few' in value.lower():
        match = re.search(r'e(\d+)', value, re.IGNORECASE)
        if match:
            return 3 * 10**int(match.group(1))
    match = re.search(r'^~?(\d+\.?\d*)[eE](\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    match = re.search(r'(\d+\.?\d*)[eE]\+?(\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    match = re.search(r'~?(\d+\.?\d*)e(\d+)\+?', value, re.IGNORECASE)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")
    return None


def get_primary_category(cat_str):
    if not cat_str:
        return 'Other'
    return cat_str.split(';')[0].strip()


def parse_data(df):
    """Parse DataFrame into structured format."""
    records = []
    for _, row in df.iterrows():
        year = int(row['Year'])
        record = {
            'year': year,
            'event': str(row['Event']),
            'category': str(row['Category']),
            'flops_raw': str(row['Compute_FLOPs']),
            'parameters': str(row['Parameters']) if pd.notna(row['Parameters']) else 'N/A',
            'impact': str(row['Impact']) if pd.notna(row['Impact']) else 'Medium'
        }
        record['flops'] = parse_flops(record['flops_raw'])
        record['primary_category'] = get_primary_category(record['category'])
        records.append(record)
    return records


CATEGORY_COLORS = {
    'Hardware': '#E67E22',
    'Theoretical Foundation': '#7F8C8D',
    'AI Milestone': '#16A085',
    'Model Release': '#8E44AD',
    'Model/Architecture': '#9B59B6',
    'Dataset': '#27AE60',
    'Robotics': '#E74C3C',
    'AI Winter': '#BDC3C7',
    'Infrastructure': '#8B4513',
    'Generative': '#FF69B4',
    'Reasoning/Agentic': '#1D8348',
    'Quantum/Future Speculative': '#9B59B6',
    'Speculative': '#9B59B6',
    'Other': '#3498DB'
}

IMPACT_SIZES = {
    'Transformative': 22,
    'Speculative Transformative': 18,
    'High': 14,
    'Speculative High': 12,
    'Medium': 10,
    'Low': 8
}


def create_plotly_chart(records):
    # Assign proxy values for records without FLOPs
    for r in records:
        if r['flops'] is None:
            if r['year'] < 1945:
                r['flops'] = 1e2
            elif r['year'] < 1960:
                r['flops'] = 1e4
            elif r['year'] < 1980:
                r['flops'] = 1e6
            elif r['year'] < 2000:
                r['flops'] = 1e8
            elif r['year'] < 2010:
                r['flops'] = 1e10
            else:
                r['flops'] = 1e12

    records.sort(key=lambda x: x['year'])

    fig = go.Figure()

    # Add era shading as shapes
    eras = [
        (1900, 1940, 'rgba(200,200,200,0.2)', 'Mechanical & Theoretical'),
        (1940, 1960, 'rgba(100,150,220,0.2)', 'Electronic Dawn'),
        (1960, 2000, 'rgba(100,200,100,0.2)', "Moore's Law Scaling"),
        (2000, 2012, 'rgba(255,200,100,0.2)', 'Parallel & Early Deep'),
        (2012, 2022, 'rgba(180,150,220,0.2)', 'Deep Learning Big Bang'),
        (2022, 2027, 'rgba(255,150,150,0.2)', 'Reasoning & Agentic Era')
    ]

    for start, end, color, label in eras:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, line_width=0,
                      annotation_text=label, annotation_position="top",
                      annotation_font_size=10, annotation_font_color="gray")

    # Add connecting line - split pre/post 2010 to show discontinuity
    pre_2010 = [(r['year'], r['flops']) for r in records if r['year'] < 2010]
    post_2010 = [(r['year'], r['flops']) for r in records if r['year'] >= 2010]

    if pre_2010:
        pre_years, pre_flops = zip(*pre_2010)
        fig.add_trace(go.Scatter(
            x=pre_years, y=pre_flops, mode='lines',
            line=dict(color='rgba(50,50,50,0.25)', width=1, dash='dash'),
            showlegend=False, hoverinfo='skip', name='Pre-2010 (proxy)'
        ))

    if post_2010:
        post_years, post_flops = zip(*post_2010)
        fig.add_trace(go.Scatter(
            x=post_years, y=post_flops, mode='lines',
            line=dict(color='rgba(50,50,50,0.4)', width=1.5),
            showlegend=False, hoverinfo='skip', name='Post-2010 (actual)'
        ))

    # Group records by category for legend
    categories = {}
    for r in records:
        cat = r['primary_category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    # Add scatter points by category
    for cat, cat_records in categories.items():
        color = CATEGORY_COLORS.get(cat, '#3498DB')

        x_vals = [r['year'] for r in cat_records]
        y_vals = [r['flops'] for r in cat_records]
        sizes = [IMPACT_SIZES.get(r['impact'], 10) for r in cat_records]
        symbols = ['diamond' if 'Speculative' in r['impact'] or r['year'] >= 2026
                   else ('triangle-down' if 'Winter' in r['category'] else 'circle')
                   for r in cat_records]

        hover_texts = [
            f"<b>{r['event'][:60]}...</b><br>" +
            f"Year: {int(r['year'])}<br>" +
            f"Category: {r['category']}<br>" +
            f"Compute: {r['flops_raw']}<br>" +
            f"Parameters: {r['parameters']}<br>" +
            f"Impact: {r['impact']}"
            for r in cat_records
        ]

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(
                size=sizes, color=color,
                symbol=symbols[0] if len(set(symbols)) == 1 else symbols,
                line=dict(width=1, color='white')
            ),
            name=cat,
            text=hover_texts,
            hoverinfo='text'
        ))

    # Add Moore's Law reference line
    moore_years = np.linspace(1965, 2005, 100)
    moore_start = 1e6
    moore_flops = moore_start * np.power(2, (moore_years - 1965) / 2)
    fig.add_trace(go.Scatter(
        x=moore_years, y=moore_flops, mode='lines',
        line=dict(color='#E67E22', width=2, dash='dash'),
        name="Moore's Law trajectory",
        hoverinfo='skip'
    ))

    # Add key event annotations
    key_events = [
        (1936, 'Turing Machine'), (1945, 'ENIAC'), (1947, 'Transistor'),
        (1956, 'AI Born'), (1965, "Moore's Law"), (1997, 'Deep Blue'),
        (2007, 'CUDA'), (2009, 'ImageNet'), (2012, 'AlexNet'),
        (2016, 'AlphaGo'), (2017, 'Transformers'), (2020, 'GPT-3'),
        (2022, 'ChatGPT'), (2023, 'GPT-4'), (2025, 'Grok-3')
    ]

    for r in records:
        for yr, lbl in key_events:
            if abs(r['year'] - yr) < 0.5 and lbl in r['event']:
                fig.add_annotation(
                    x=r['year'], y=r['flops'],
                    text=lbl, showarrow=True,
                    arrowhead=0, arrowsize=0.5, arrowwidth=1,
                    arrowcolor='gray',
                    ax=30, ay=-40,
                    font=dict(size=9, color='#333'),
                    bgcolor='rgba(255,255,255,0.8)',
                    borderpad=2
                )
                break

    # Layout configuration
    fig.update_layout(
        title=dict(
            text='<b>History of Compute & Intelligence</b><br>' +
                 '<sup>Training FLOPs for Key AI Milestones (1900–2026)</sup>',
            x=0.5, font=dict(size=20)
        ),
        xaxis=dict(
            title='Year', range=[1898, 2028],
            tickmode='linear', tick0=1900, dtick=10,
            gridcolor='rgba(128,128,128,0.2)',
            minor=dict(tickmode='linear', tick0=1900, dtick=5)
        ),
        yaxis=dict(
            title='Total Training Compute (FLOPs, log₁₀)',
            type='log', range=[1, 29],
            gridcolor='rgba(128,128,128,0.3)',
            tickformat='.0e'
        ),
        legend=dict(
            title='Category',
            yanchor='top', y=0.99, xanchor='left', x=1.02,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=1400, height=800,
        margin=dict(r=200, t=100, b=80),
        hovermode='closest'
    )

    # Add frontier cluster bracket annotation
    fig.add_annotation(
        x=2022.5, y=3e25,
        text="<b>2023–25 Frontier Cluster</b><br>(10²⁴–10²⁶ FLOPs)",
        showarrow=False,
        font=dict(size=10, color='#444'),
        bgcolor='rgba(255,255,255,0.85)',
        borderpad=4,
        xanchor='right'
    )

    # Add note
    fig.add_annotation(
        text="Log scale: exponential growth appears as straight lines.<br>" +
             "Pre-2010 values are rough proxies (ops/sec, not directly comparable).<br>" +
             "Speculative 2026+ points marked with diamonds.<br>" +
             "Sources: Epoch AI, Our World in Data. Estimates as of Jan 2026.",
        xref='paper', yref='paper', x=0.01, y=0.01,
        showarrow=False, font=dict(size=9, color='#666'),
        bgcolor='rgba(255,255,255,0.9)', borderpad=5,
        align='left'
    )

    return fig


def main():
    if not PLOTLY_AVAILABLE:
        print("Please install plotly: pip install plotly")
        return

    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Load and parse data
    df = load_data()
    records = parse_data(df)
    print(f"Parsed {len(records)} records")

    fig = create_plotly_chart(records)

    # Save as interactive HTML
    html_path = os.path.join(output_dir, 'ai_compute_timeline_interactive.html')
    fig.write_html(html_path)
    print(f"Saved: {html_path}")

    # Save as static image (requires kaleido)
    try:
        png_path = os.path.join(output_dir, 'ai_compute_timeline_plotly.png')
        fig.write_image(png_path, scale=2)
        print(f"Saved: {png_path}")
    except Exception:
        print("Note: Static image export requires kaleido: pip install kaleido")

    print("\nDone!")


if __name__ == '__main__':
    main()
