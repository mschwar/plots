#!/usr/bin/env python3
"""
Adoption Timeline – Static Matplotlib Version
Clean exports for PNG/SVG with minimal annotations (Kurzweil-simple)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

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
    'Transformative': 120,
    'Speculative Transformative': 100,
    'High': 70,
    'Medium': 50,
}

# Anchor labels for static export (minimal - only 4)
ANCHOR_LABELS = {
    1969: 'ARPANET',
    1989: 'WWW',
    2007: 'iPhone',
    2022: 'ChatGPT',
}


def load_data():
    """Load CSV data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'tech_adoption.csv')
    return pd.read_csv(csv_path)


def create_chart(df):
    """Create clean matplotlib chart."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#FAFAFA')

    df = df.sort_values('Year')

    # Subtle era shading
    eras = [
        (1955, 1990, '#F0F0F0'),
        (1990, 2005, '#E8F4FD'),
        (2005, 2015, '#F3E8FD'),
        (2015, 2030, '#FDE8E8'),
    ]
    for start, end, color in eras:
        ax.axvspan(start, end, alpha=0.4, color=color, zorder=0)

    # Connecting line
    ax.plot(df['Year'], df['Days_to_Adoption'],
            '-', color='#CCCCCC', linewidth=1, zorder=1)

    # Exponential trend (subtle)
    trend_years = np.linspace(1957, 2030, 100)
    k = np.log(3650 / 14) / (2026 - 1957)
    trend_days = 3650 * np.exp(-k * (trend_years - 1957))
    ax.plot(trend_years, trend_days, '--', color='#E67E22',
            linewidth=1.5, alpha=0.4, label='Trend', zorder=1)

    # Plot by category
    for cat in df['Category'].unique():
        cat_df = df[df['Category'] == cat]
        color = CATEGORY_COLORS.get(cat, '#7F8C8D')

        for _, row in cat_df.iterrows():
            size = IMPACT_SIZES.get(row['Impact'], 50)
            marker = 'd' if 'Speculative' in str(row['Impact']) or row['Year'] >= 2026 else 'o'
            ax.scatter(row['Year'], row['Days_to_Adoption'],
                      c=color, s=size, marker=marker,
                      edgecolors='white', linewidths=1.5, zorder=3)

    # Minimal anchor labels (only 4 key events)
    for year, label in ANCHOR_LABELS.items():
        matching = df[df['Year'] == year]
        if len(matching) > 0:
            row = matching.iloc[0]
            ax.annotate(label,
                       xy=(row['Year'], row['Days_to_Adoption']),
                       xytext=(0, 15), textcoords='offset points',
                       ha='center', va='bottom',
                       fontsize=8, fontweight='bold', color='#333',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                                edgecolor='none', alpha=0.8))

    # Log scale
    ax.set_yscale('log')

    # Human-readable Y-axis
    y_ticks = [14, 30, 90, 365, 1095, 3650]
    y_labels = ['2 wk', '1 mo', '3 mo', '1 yr', '3 yr', '10 yr']
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_ylim(10, 5000)

    # X-axis
    ax.set_xlim(1953, 2030)
    ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020])

    # Grid
    ax.grid(True, which='major', axis='y', linestyle='-', alpha=0.3)
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2)

    # Labels
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Time to ~50M Users', fontsize=11, fontweight='bold')
    ax.set_title('Time to Mass Adoption (1957–2026)',
                fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    return fig


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    df = load_data()
    print(f"Loaded {len(df)} records")

    fig = create_chart(df)

    # Save PNG
    png_path = os.path.join(output_dir, 'adoption_timeline.png')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path}")

    # Save high-res PNG
    highres_path = os.path.join(output_dir, 'adoption_timeline_highres.png')
    fig.savefig(highres_path, dpi=400, bbox_inches='tight', facecolor='white')
    print(f"Saved: {highres_path}")

    # Save SVG
    svg_path = os.path.join(output_dir, 'adoption_timeline.svg')
    fig.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white')
    print(f"Saved: {svg_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
