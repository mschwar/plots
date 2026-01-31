#!/usr/bin/env python3
"""
Energetic Scaling: Brain/Neural Efficiency vs. Size in Biology
and Compute Efficiency vs. Scale in Technology

Interactive Plotly version with hover tooltips.
"""

import numpy as np
import os

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not installed. Run: pip install plotly")

# ============================================================================
# BIOLOGICAL DATA
# ============================================================================
bio_data = [
    {"entity": "Crocodile", "mass": 90, "neurons": 8.3e7, "per_kg": 9.22e5,
     "group": "Reptiles", "impact": "Low", "notes": "Low neuron density; ~20x fewer than endotherms"},
    {"entity": "Goldcrest", "mass": 0.0045, "neurons": 1.64e8, "per_kg": 3.64e10,
     "group": "Birds", "impact": "High", "notes": "Smallest bird, extreme density"},
    {"entity": "Corvid/Rook", "mass": 0.5, "neurons": 2e9, "per_kg": 4e9,
     "group": "Birds", "impact": "High", "notes": "Primate-like forebrain neurons"},
    {"entity": "Parrot (African Grey)", "mass": 0.4, "neurons": 3e9, "per_kg": 7.5e9,
     "group": "Birds", "impact": "High", "notes": "High cognition, tool use"},
    {"entity": "Pigeon", "mass": 0.35, "neurons": 3.1e8, "per_kg": 8.86e8,
     "group": "Birds", "impact": "Medium", "notes": "Common bird baseline"},
    {"entity": "Mouse", "mass": 0.02, "neurons": 7.1e7, "per_kg": 3.55e9,
     "group": "Mammals", "impact": "Medium", "notes": "Rodent baseline"},
    {"entity": "Rat", "mass": 0.3, "neurons": 2e8, "per_kg": 6.67e8,
     "group": "Mammals", "impact": "Medium", "notes": "Rodent"},
    {"entity": "Cat", "mass": 4, "neurons": 7.6e8, "per_kg": 1.9e8,
     "group": "Mammals", "impact": "Medium", "notes": "Carnivore"},
    {"entity": "Dog", "mass": 15, "neurons": 5.3e8, "per_kg": 3.5e7,
     "group": "Mammals", "impact": "Medium", "notes": "Carnivore"},
    {"entity": "Elephant", "mass": 4000, "neurons": 2.57e11, "per_kg": 6.43e7,
     "group": "Mammals", "impact": "High", "notes": "Largest land mammal; 257B neurons but low density"},
    {"entity": "Marmoset", "mass": 0.3, "neurons": 1.4e9, "per_kg": 4.67e9,
     "group": "Primates", "impact": "High", "notes": "Small primate, linear scaling"},
    {"entity": "Macaque", "mass": 7, "neurons": 6.4e9, "per_kg": 9.14e8,
     "group": "Primates", "impact": "High", "notes": "Old World monkey"},
    {"entity": "Chimpanzee", "mass": 50, "neurons": 2.8e10, "per_kg": 5.6e8,
     "group": "Primates", "impact": "High", "notes": "Great ape, closest relative"},
    {"entity": "Human", "mass": 70, "neurons": 8.6e10, "per_kg": 1.23e9,
     "group": "Primates", "impact": "Transformative", "notes": "86B neurons, EQ~7 (outlier)"},
    {"entity": "Lizard", "mass": 0.1, "neurons": 1e7, "per_kg": 1e8,
     "group": "Reptiles", "impact": "Low", "notes": "Small reptile baseline"},
]

# ============================================================================
# TECH DATA
# ============================================================================
tech_data = [
    {"entity": "Zeus II 1939", "year": 1939, "cps": 6.5e-6, "category": "Hardware",
     "impact": "Low", "notes": "Kurzweil baseline; relay computer"},
    {"entity": "ENIAC 1945", "year": 1945, "cps": 1e-4, "category": "Hardware",
     "impact": "Medium", "notes": "Vacuum tube era"},
    {"entity": "UNIVAC 1951", "year": 1951, "cps": 1e-3, "category": "Hardware",
     "impact": "Medium", "notes": "First commercial computer"},
    {"entity": "IBM 7090 1959", "year": 1959, "cps": 0.1, "category": "Hardware",
     "impact": "Medium", "notes": "Transistor mainframe"},
    {"entity": "Intel 4004 1971", "year": 1971, "cps": 10, "category": "Hardware",
     "impact": "High", "notes": "First microprocessor"},
    {"entity": "Intel 8086 1978", "year": 1978, "cps": 100, "category": "Hardware",
     "impact": "Medium", "notes": "PC architecture foundation"},
    {"entity": "Intel 386 1985", "year": 1985, "cps": 1e4, "category": "Hardware",
     "impact": "Medium", "notes": "32-bit era"},
    {"entity": "Pentium 1993", "year": 1993, "cps": 1e6, "category": "Hardware",
     "impact": "Medium", "notes": "Superscalar x86"},
    {"entity": "Pentium 4 2000", "year": 2000, "cps": 1e8, "category": "Hardware",
     "impact": "Medium", "notes": "GHz race peak"},
    {"entity": "Core i7 2008", "year": 2008, "cps": 1e9, "category": "Hardware",
     "impact": "High", "notes": "Multi-core era"},
    {"entity": "NVIDIA V100 2017", "year": 2017, "cps": 1e10, "category": "Hardware",
     "impact": "High", "notes": "GPU for deep learning"},
    {"entity": "NVIDIA A100 2020", "year": 2020, "cps": 5e10, "category": "Hardware",
     "impact": "High", "notes": "AI accelerator"},
    {"entity": "NVIDIA B200 2024", "year": 2024, "cps": 5e11, "category": "Hardware",
     "impact": "Transformative", "notes": "~75 quadrillion-fold increase since 1939"},
    {"entity": "Projected 2026", "year": 2026, "cps": 2e12, "category": "Hardware",
     "impact": "High", "notes": "Kurzweil trajectory projection"},
]

ai_data = [
    {"entity": "AlexNet 2012", "year": 2012, "flops": 6e17, "impact": "High",
     "notes": "Deep learning breakthrough; ImageNet"},
    {"entity": "GPT-2 2019", "year": 2019, "flops": 1e19, "impact": "High",
     "notes": "Emergent scaling behaviors"},
    {"entity": "GPT-3 2020", "year": 2020, "flops": 3.14e23, "impact": "Transformative",
     "notes": "175B params; few-shot learning"},
    {"entity": "GPT-4 2023", "year": 2023, "flops": 2e25, "impact": "Transformative",
     "notes": "Multimodal frontier"},
    {"entity": "Grok-4 2026", "year": 2026, "flops": 5e26, "impact": "Transformative",
     "notes": "Projected frontier model"},
]

BIO_COLORS = {
    "Reptiles": "#7F8C8D",
    "Birds": "#27AE60",
    "Mammals": "#3498DB",
    "Primates": "#9B59B6",
}

TECH_COLORS = {
    "Hardware": "#E67E22",
    "AI": "#E74C3C",
}

IMPACT_SIZES = {
    "Transformative": 22,
    "High": 14,
    "Medium": 10,
    "Low": 7,
}


def create_plotly_chart():
    """Create interactive dual-panel Plotly chart."""

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            '<b>Biological Allometry</b><br><sup>Neural Efficiency vs. Body Size</sup>',
            '<b>Tech Scaling (Kurzweil-inspired)</b><br><sup>Compute Efficiency vs. Time</sup>'
        ),
        horizontal_spacing=0.12
    )

    # ========================================================================
    # LEFT PANEL: Biology
    # ========================================================================
    for group in ["Reptiles", "Birds", "Mammals", "Primates"]:
        group_data = [d for d in bio_data if d["group"] == group]
        if not group_data:
            continue

        x = [d["mass"] for d in group_data]
        y = [d["per_kg"] for d in group_data]
        sizes = [IMPACT_SIZES.get(d["impact"], 10) for d in group_data]
        color = BIO_COLORS[group]

        hover_texts = [
            f"<b>{d['entity']}</b><br>" +
            f"Body Mass: {d['mass']:.4g} kg<br>" +
            f"Total Neurons: {d['neurons']:.2e}<br>" +
            f"Neurons/kg: {d['per_kg']:.2e}<br>" +
            f"Group: {d['group']}<br>" +
            f"Impact: {d['impact']}<br>" +
            f"<i>{d['notes']}</i>"
            for d in group_data
        ]

        # Special marker for Human
        symbols = ['star' if d['entity'] == 'Human' else 'circle' for d in group_data]
        marker_sizes = [s * 1.5 if d['entity'] == 'Human' else s for s, d in zip(sizes, group_data)]

        fig.add_trace(go.Scatter(
            x=x, y=y, mode='markers',
            marker=dict(size=marker_sizes, color=color, symbol=symbols,
                       line=dict(width=1, color='white')),
            name=group, text=hover_texts, hoverinfo='text',
            legendgroup='bio', legendgrouptitle_text='Biology'
        ), row=1, col=1)

    # Add trend line for mammals
    mammal_data = [d for d in bio_data if d["group"] == "Mammals"]
    if len(mammal_data) >= 2:
        log_x = np.log10([d["mass"] for d in mammal_data])
        log_y = np.log10([d["per_kg"] for d in mammal_data])
        from scipy import stats
        slope, intercept, _, _, _ = stats.linregress(log_x, log_y)
        x_fit = np.logspace(-2, 4, 50)
        y_fit = 10**(intercept + slope * np.log10(x_fit))
        fig.add_trace(go.Scatter(
            x=x_fit, y=y_fit, mode='lines',
            line=dict(color=BIO_COLORS["Mammals"], dash='dash', width=2),
            name=f'Mammals trend (slope={slope:.2f})',
            hoverinfo='skip', legendgroup='bio'
        ), row=1, col=1)

    # ========================================================================
    # RIGHT PANEL: Tech
    # ========================================================================
    # Hardware data
    x_hw = [d["year"] for d in tech_data]
    y_hw = [d["cps"] for d in tech_data]
    sizes_hw = [IMPACT_SIZES.get(d["impact"], 10) for d in tech_data]

    hover_hw = [
        f"<b>{d['entity']}</b><br>" +
        f"Year: {d['year']}<br>" +
        f"Compute/$ (cps): {d['cps']:.2e}<br>" +
        f"Impact: {d['impact']}<br>" +
        f"<i>{d['notes']}</i>"
        for d in tech_data
    ]

    fig.add_trace(go.Scatter(
        x=x_hw, y=y_hw, mode='markers',
        marker=dict(size=sizes_hw, color=TECH_COLORS["Hardware"],
                   line=dict(width=1, color='white')),
        name='Hardware (cps/$)', text=hover_hw, hoverinfo='text',
        legendgroup='tech', legendgrouptitle_text='Technology'
    ), row=1, col=2)

    # Kurzweil trend line
    from scipy import stats
    years = np.array([d["year"] for d in tech_data])
    log_cps = np.log10([d["cps"] for d in tech_data])
    slope, intercept, _, _, _ = stats.linregress(years, log_cps)
    x_fit = np.linspace(1935, 2030, 50)
    y_fit = 10**(intercept + slope * x_fit)

    fig.add_trace(go.Scatter(
        x=x_fit, y=y_fit, mode='lines',
        line=dict(color=TECH_COLORS["Hardware"], dash='dash', width=2),
        name=f'Kurzweil trend (~{10**slope:.1f}x/yr)',
        hoverinfo='skip', legendgroup='tech'
    ), row=1, col=2)

    # AI FLOPs (secondary y-axis style - we'll use annotations)
    x_ai = [d["year"] for d in ai_data]
    y_ai = [d["flops"] for d in ai_data]
    sizes_ai = [IMPACT_SIZES.get(d["impact"], 10) for d in ai_data]

    hover_ai = [
        f"<b>{d['entity']}</b><br>" +
        f"Year: {d['year']}<br>" +
        f"Training FLOPs: {d['flops']:.2e}<br>" +
        f"Impact: {d['impact']}<br>" +
        f"<i>{d['notes']}</i>"
        for d in ai_data
    ]

    # Add AI data on secondary y-axis (we'll fake it by scaling)
    # Map FLOPs to cps/$ scale for visual placement
    y_ai_scaled = [f * 1e-12 for f in y_ai]  # Scale down to fit on same visual

    fig.add_trace(go.Scatter(
        x=x_ai, y=y_ai_scaled, mode='markers',
        marker=dict(size=sizes_ai, color=TECH_COLORS["AI"], symbol='diamond',
                   line=dict(width=1, color='white')),
        name='AI Models (FLOPs)', text=hover_ai, hoverinfo='text',
        legendgroup='tech', yaxis='y4'
    ), row=1, col=2)

    # ========================================================================
    # LAYOUT
    # ========================================================================
    fig.update_xaxes(type='log', title_text='Body Mass (kg)', row=1, col=1,
                    gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(type='log', title_text='Neurons per kg Body Mass', row=1, col=1,
                    gridcolor='rgba(128,128,128,0.2)')

    fig.update_xaxes(title_text='Year', row=1, col=2, range=[1935, 2030],
                    gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(type='log', title_text='Compute per Dollar (cps/$)', row=1, col=2,
                    gridcolor='rgba(128,128,128,0.2)')

    # Add shaded regions
    fig.add_vrect(x0=2012, x1=2030, fillcolor='rgba(231,76,60,0.1)',
                 line_width=0, row=1, col=2)

    fig.update_layout(
        title=dict(
            text='<b>Energetic Scaling</b><br>' +
                 '<sup>Neural Efficiency (Biology) vs. Compute Efficiency (Technology)</sup>',
            x=0.5, font=dict(size=20)
        ),
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='white',
        width=1500, height=700,
        margin=dict(t=120, b=150),
        hovermode='closest'
    )

    # Footnote
    fig.add_annotation(
        text="Log-log plots reveal power laws. Biology: Neurons/kg shows clade differences; humans outlier (EQ~7). " +
             "Tech: cps/$ mirrors Kurzweil's ~75 quadrillion-fold increase (1939–2024).<br>" +
             "Sources: Herculano-Houzel (neuronal), Kleiber (metabolic 0.75), Kaplan/Charnov (LHT), Kurzweil. Jan 2026.",
        xref='paper', yref='paper', x=0.5, y=-0.18,
        showarrow=False, font=dict(size=10, color='#666'),
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

    fig = create_plotly_chart()
    print("Created interactive energetic scaling chart")

    output_path = os.path.join(output_dir, 'energetic_scaling_interactive.html')
    fig.write_html(output_path)
    print(f"Saved: {output_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
