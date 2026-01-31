#!/usr/bin/env python3
"""
History of Compute & Intelligence: Training FLOPs for Key AI Milestones (1900-2026)
Publication-quality semi-log timeline visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os
import re


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

    # Handle speculative values
    if 'Speculative' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        return 1e27  # Default speculative

    # Handle "High compute" or similar vague terms
    if 'High compute' in value or value == 'Speculative':
        return 1e21

    # Handle proxy values
    if 'Proxy' in value:
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")
        if 'low' in value.lower():
            return 1e6
        return 1e3

    # Handle ranges like "1e24-1e25" or "~1e17-1e18"
    range_match = re.search(r'(\d+\.?\d*)e(\d+)[-–](\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
    if range_match:
        low = float(f"{range_match.group(1)}e{range_match.group(2)}")
        high = float(f"{range_match.group(3)}e{range_match.group(4)}")
        return np.sqrt(low * high)  # Geometric mean

    # Handle ">1e26" format
    if value.startswith('>'):
        match = re.search(r'(\d+\.?\d*)e(\d+)', value, re.IGNORECASE)
        if match:
            return float(f"{match.group(1)}e{match.group(2)}")

    # Handle "~few e23" format
    if 'few' in value.lower():
        match = re.search(r'e(\d+)', value, re.IGNORECASE)
        if match:
            return 3 * 10**int(match.group(1))

    # Handle "4e25 (Llama...)" format
    match = re.search(r'^~?(\d+\.?\d*)[eE](\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")

    # Handle scientific notation like "6.00E+17" or "3.14E+23"
    match = re.search(r'(\d+\.?\d*)[eE]\+?(\d+)', value)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")

    # Handle "~1e20+" format
    match = re.search(r'~?(\d+\.?\d*)e(\d+)\+?', value, re.IGNORECASE)
    if match:
        return float(f"{match.group(1)}e{match.group(2)}")

    return None


def get_primary_category(cat_str):
    """Get the primary category from potentially multiple categories."""
    if not cat_str:
        return 'Other'
    categories = cat_str.split(';')
    return categories[0].strip()


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


# Category color mapping
CATEGORY_COLORS = {
    'Hardware': '#E67E22',           # Orange
    'Theoretical Foundation': '#7F8C8D',  # Gray
    'AI Milestone': '#16A085',        # Teal
    'Model Release': '#8E44AD',       # Purple
    'Model/Architecture': '#9B59B6',  # Lighter purple
    'Dataset': '#27AE60',             # Green
    'Robotics': '#E74C3C',            # Red
    'AI Winter': '#BDC3C7',           # Light gray
    'Infrastructure': '#8B4513',      # Brown
    'Generative': '#FF69B4',          # Pink
    'Reasoning/Agentic': '#1D8348',   # Dark green
    'Quantum/Future Speculative': '#9B59B6',  # Purple
    'Speculative': '#9B59B6',         # Purple
    'Other': '#3498DB'                # Blue
}

# Impact to marker size mapping
IMPACT_SIZES = {
    'Transformative': 180,
    'Speculative Transformative': 160,
    'High': 100,
    'Speculative High': 80,
    'Medium': 50,
    'Low': 30
}


def get_short_label(event):
    """Extract short label for annotation."""
    # Key events to label
    labels = {
        'Vacuum Tube': 'Vacuum Tube',
        'Turing Machine': 'Turing Machine',
        'Shannon': 'Shannon',
        'ENIAC': 'ENIAC',
        'Transistor': 'Transistor',
        'Dartmouth': 'AI Born',
        'Perceptron': 'Perceptron',
        'Integrated Circuit': 'IC',
        'Moore': "Moore's Law",
        'Intel 4004': '4004',
        'First AI Winter': 'AI Winter I',
        'Backpropagation': 'Backprop',
        'Second AI Winter': 'AI Winter II',
        'Deep Blue': 'Deep Blue',
        'CUDA': 'CUDA',
        'ImageNet dataset': 'ImageNet',
        'AWS launch': 'AWS',
        'AlexNet': 'AlexNet',
        'DQN': 'DQN',
        'GANs': 'GANs',
        'AlphaGo': 'AlphaGo',
        'Transformers': 'Transformers',
        'GPT-1': 'GPT-1/BERT',
        'GPT-2': 'GPT-2',
        'GPT-3': 'GPT-3',
        'AlphaFold': 'AlphaFold',
        'DALL-E': 'DALL-E',
        'ChatGPT': 'ChatGPT',
        'Stable Diffusion': 'Stable Diff',
        'GPT-4': 'GPT-4',
        'Gemini 1.0': 'Gemini/Llama2',
        'Sora': 'Sora/Claude3/o1',
        'Llama 3.1': 'Llama 3.1',
        'Grok-3': 'Grok-3',
        'o3': 'o3/Claude4',
        'Quantum': 'Quantum',
        'Agentic AI': 'Agentic AI',
        'Optimus': 'Optimus',
        'Omni-modal': 'Omni-modal'
    }

    for key, label in labels.items():
        if key in event:
            return label
    return None


def create_timeline_plot(records):
    """Create the main timeline visualization."""

    # Set up the figure
    fig, ax = plt.subplots(figsize=(16, 10), dpi=150)

    # Set background
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('white')

    # Add era shading
    eras = [
        (1900, 1940, '#F5F5F5', 'Mechanical & Theoretical'),
        (1940, 1960, '#E8F4FD', 'Electronic Dawn'),
        (1960, 2000, '#E8F8E8', "Moore's Law Scaling"),
        (2000, 2012, '#FFF8E8', 'Parallel & Early Deep'),
        (2012, 2022, '#F0E8FF', 'Deep Learning Big Bang'),
        (2022, 2027, '#FFE8E8', 'Reasoning & Agentic Era')
    ]

    for start, end, color, label in eras:
        ax.axvspan(start, end, alpha=0.5, color=color, zorder=0)

    # Separate records with and without FLOPs
    records_with_flops = [r for r in records if r['flops'] is not None]
    records_without_flops = [r for r in records if r['flops'] is None]

    # Assign proxy values to records without FLOPs based on year
    for r in records_without_flops:
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

    all_records = records_with_flops + records_without_flops
    all_records.sort(key=lambda x: x['year'])

    # Extract data for plotting
    years = [r['year'] for r in all_records]
    flops = [r['flops'] for r in all_records]
    colors = [CATEGORY_COLORS.get(r['primary_category'], '#3498DB') for r in all_records]
    sizes = [IMPACT_SIZES.get(r['impact'], 50) for r in all_records]

    # Plot connecting line (thin) - split pre/post 2010 to show discontinuity
    # Pre-2010: dashed line (proxy values, not directly comparable)
    pre_2010 = [(y, f) for y, f, r in zip(years, flops, all_records) if r['year'] < 2010]
    post_2010 = [(y, f) for y, f, r in zip(years, flops, all_records) if r['year'] >= 2010]

    if pre_2010:
        pre_years, pre_flops = zip(*pre_2010)
        ax.plot(pre_years, pre_flops, '--', color='#2C3E50', alpha=0.25, linewidth=1, zorder=1)

    if post_2010:
        post_years, post_flops = zip(*post_2010)
        ax.plot(post_years, post_flops, '-', color='#2C3E50', alpha=0.4, linewidth=1.2, zorder=1)

    # Plot scatter points
    for i, r in enumerate(all_records):
        marker = 'o'
        edgecolor = 'white'
        alpha = 1.0

        # Special markers for speculative/future
        if 'Speculative' in r['impact'] or r['year'] >= 2026:
            marker = 'd'  # Diamond for speculative
            edgecolor = '#333333'
            alpha = 0.7

        # Special for AI Winter
        if 'Winter' in r['category']:
            marker = 'v'  # Triangle down

        ax.scatter(r['year'], r['flops'],
                   c=colors[i], s=sizes[i],
                   marker=marker, alpha=alpha,
                   edgecolors=edgecolor, linewidths=1.5,
                   zorder=3)

    # Add annotations for key events
    annotations = []
    for r in all_records:
        label = get_short_label(r['event'])
        if label:
            annotations.append({
                'year': r['year'],
                'flops': r['flops'],
                'label': label,
                'impact': r['impact']
            })

    # Add labels with smart positioning - custom offsets per label
    # Format: (x_offset, y_multiplier, rotation)
    # Negative x_offset = label to left of point
    label_positions = {
        'Vacuum Tube': (2, 3, 25),
        'Turing Machine': (2, 4, 30),
        'Shannon': (-8, 0.3, -30),
        'ENIAC': (2, 3, 25),
        'Transistor': (2, 4, 30),
        'AI Born': (2, 3, 25),
        'Perceptron': (-6, 0.4, -25),
        'IC': (2, 3, 25),
        "Moore's Law": (2, 3, 30),
        '4004': (-5, 0.4, -20),
        'AI Winter I': (2, 3, 25),
        'Backprop': (2, 4, 30),
        'AI Winter II': (-6, 0.3, -20),
        'Deep Blue': (2, 4, 30),
        'CUDA': (1, 4, 35),
        'ImageNet': (1, 3, 30),
        'AWS': (-5, 0.3, -25),
        'AlexNet': (1.5, 3, 35),
        'DQN': (-4, 0.3, -20),
        'GANs': (-5, 0.4, -25),
        'AlphaGo': (1, 3, 35),
        'Transformers': (-5, 0.3, -30),
        'GPT-1/BERT': (1, 3, 30),
        'GPT-2': (1, 2.5, 30),
        'GPT-3': (0.8, 2.5, 35),
        'AlphaFold': (-3.5, 0.35, -25),
        'DALL-E': (-3.5, 0.45, -20),
        'ChatGPT': (0.6, 3, 45),
        'Stable Diff': (-3.5, 0.25, -35),
        'GPT-4': (0.5, 2.2, 50),
        'Gemini/Llama2': None,  # Skip - covered by cluster label
        'Sora/Claude3/o1': (0.4, 2, 50),
        'Llama 3.1': None,  # Skip - covered by cluster label
        'Grok-3': (0.4, 1.8, 50),
        'o3/Claude4': (-1.8, 0.55, -40),
        'Quantum': (-3.5, 0.4, -30),
        'Agentic AI': (0.3, 1.6, 55),
        'Optimus': (-1.5, 0.6, -40),
        'Omni-modal': (0.3, 1.5, 55),
    }

    # Labels to skip (covered by cluster annotation)
    skip_labels = {'Gemini/Llama2', 'Llama 3.1'}

    for ann in annotations:
        # Skip labels covered by cluster annotation
        if ann['label'] in skip_labels:
            continue

        pos = label_positions.get(ann['label'], (1.5, 2.5, 30))
        if pos is None:
            continue

        x_offset, y_mult, rotation = pos

        fontsize = 8
        if 'Transformative' in ann['impact']:
            fontsize = 9

        ha = 'left' if x_offset >= 0 else 'right'

        ax.annotate(ann['label'],
                    xy=(ann['year'], ann['flops']),
                    xytext=(ann['year'] + x_offset, ann['flops'] * y_mult),
                    fontsize=fontsize,
                    ha=ha,
                    rotation=rotation,
                    alpha=0.85,
                    arrowprops=dict(arrowstyle='-', color='gray', alpha=0.4, lw=0.5),
                    zorder=4)

    # Configure axes
    ax.set_yscale('log')
    ax.set_xlim(1898, 2028)
    ax.set_ylim(1e1, 1e29)

    # X-axis configuration
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    major_ticks = range(1900, 2030, 10)
    minor_ticks = range(1900, 2030, 5)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.tick_params(axis='x', labelsize=11)

    # Y-axis configuration
    ax.set_ylabel('Total Training Compute (FLOPs, log₁₀)', fontsize=14, fontweight='bold')
    y_ticks = [10.0**i for i in range(0, 30, 3)]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'$10^{{{int(np.log10(float(y)))}}}$' for y in y_ticks], fontsize=10)
    ax.tick_params(axis='y', labelsize=10)

    # Grid
    ax.grid(True, which='major', axis='y', linestyle='-', alpha=0.3, color='gray')
    ax.grid(True, which='minor', axis='y', linestyle=':', alpha=0.2, color='gray')
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2, color='gray')

    # Title
    ax.set_title('History of Compute & Intelligence:\nTraining FLOPs for Key AI Milestones (1900–2026)',
                 fontsize=18, fontweight='bold', pad=20)

    # Add Moore's Law reference line (doubling every 2 years ≈ 0.15 log10/year)
    moore_years = np.array([1965, 2005])
    moore_start = 1e6  # Rough starting point
    moore_flops = moore_start * (2 ** ((moore_years - 1965) / 2))
    ax.plot(moore_years, moore_flops, '--', color='#E67E22', alpha=0.6, linewidth=2,
            label="Moore's Law trajectory")

    # Create legend
    # Category legend
    category_handles = []
    for cat, color in CATEGORY_COLORS.items():
        if any(r['primary_category'] == cat for r in all_records):
            category_handles.append(mpatches.Patch(color=color, label=cat))

    # Impact size legend
    size_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['Transformative']/3), label='Transformative'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['High']/3), label='High'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=np.sqrt(IMPACT_SIZES['Medium']/3), label='Medium'),
        Line2D([0], [0], marker='d', color='w', markerfacecolor='gray',
               markersize=8, label='Speculative', markeredgecolor='black')
    ]

    # Moore's Law line
    moore_handle = Line2D([0], [0], linestyle='--', color='#E67E22',
                          linewidth=2, label="Moore's Law")

    # Position legends
    leg1 = ax.legend(handles=category_handles, loc='upper left',
                     fontsize=8, title='Category', title_fontsize=9,
                     framealpha=0.9, bbox_to_anchor=(1.01, 1))
    ax.add_artist(leg1)

    leg2 = ax.legend(handles=size_handles + [moore_handle], loc='lower left',
                     fontsize=8, title='Impact / Type', title_fontsize=9,
                     framealpha=0.9, bbox_to_anchor=(1.01, 0))

    # Add era labels at top
    for start, end, color, label in eras:
        mid = (start + end) / 2
        ax.text(mid, 3e28, label, ha='center', va='bottom', fontsize=7,
                rotation=0, alpha=0.7, style='italic')

    # Add "2023-2025 Frontier Cluster" bracket annotation
    ax.annotate('', xy=(2022.8, 1e24), xytext=(2022.8, 5e26),
                arrowprops=dict(arrowstyle='-[, widthB=1.5', color='#666', lw=1.5))
    ax.text(2022.3, 7e24, '2023–25\nFrontier\nCluster\n(10²⁴–10²⁶)',
            fontsize=7, ha='right', va='center', color='#444', style='italic')

    # Add note box with data source credit
    note_text = ("Log scale: exponential growth appears as straight lines.\n"
                 "Pre-2010 values are rough proxies (ops/sec equivalents, not directly comparable).\n"
                 "Dashed line indicates proxy era; solid line = actual training compute.\n"
                 "Speculative 2026+ points marked with diamonds.\n"
                 "Sources: Epoch AI, Our World in Data, scaling reports. Estimates as of Jan 2026.")

    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray')
    ax.text(0.02, 0.02, note_text, transform=ax.transAxes, fontsize=7,
            verticalalignment='bottom', bbox=props, family='sans-serif')

    plt.tight_layout()
    plt.subplots_adjust(right=0.82)

    return fig, ax


def main():
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Load and parse data
    df = load_data()
    records = parse_data(df)
    print(f"Parsed {len(records)} records")

    # Create plot
    fig, ax = create_timeline_plot(records)

    # Save outputs
    fig.savefig(os.path.join(output_dir, 'ai_compute_timeline.png'), dpi=300,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: ai_compute_timeline.png (300 DPI)")

    fig.savefig(os.path.join(output_dir, 'ai_compute_timeline.svg'), format='svg',
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: ai_compute_timeline.svg")

    fig.savefig(os.path.join(output_dir, 'ai_compute_timeline_highres.png'), dpi=400,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: ai_compute_timeline_highres.png (400 DPI)")

    print("\nDone!")


if __name__ == '__main__':
    main()
