#!/usr/bin/env python3
"""
Energetic Scaling: Brain/Neural Efficiency vs. Size in Biology
and Compute Efficiency vs. Scale in Technology

Dual-panel log-log visualization comparing biological allometry with tech scaling laws.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from scipy import stats
import os

# ============================================================================
# BIOLOGICAL DATA: Neural scaling
# ============================================================================
bio_data = [
    # (Entity, Body_Mass_kg, Total_Neurons, Neurons_per_kg, Group, Impact, Notes)
    ("Crocodile", 90, 8.3e7, 9.22e5, "Reptiles", "Low", "Low neuron density"),
    ("Goldcrest", 0.0045, 1.64e8, 3.64e10, "Birds", "High", "Smallest bird, high density"),
    ("Corvid/Rook", 0.5, 2e9, 4e9, "Birds", "High", "Primate-like forebrain"),
    ("Mouse", 0.02, 7.1e7, 3.55e9, "Mammals", "Medium", "Rodent baseline"),
    ("Elephant", 4000, 2.57e11, 6.43e7, "Mammals", "High", "Large absolute, low per kg"),
    ("Human", 70, 8.6e10, 1.23e9, "Primates", "Transformative", "EQ~7, 86B neurons"),
    ("Marmoset", 0.3, 1.4e9, 4.67e9, "Primates", "High", "Linear primate scaling"),
    # Additional data points for better trend lines
    ("Rat", 0.3, 2e8, 6.67e8, "Mammals", "Medium", "Rodent"),
    ("Cat", 4, 7.6e8, 1.9e8, "Mammals", "Medium", "Carnivore"),
    ("Dog", 15, 5.3e8, 3.5e7, "Mammals", "Medium", "Carnivore"),
    ("Macaque", 7, 6.4e9, 9.14e8, "Primates", "High", "Old World monkey"),
    ("Chimpanzee", 50, 2.8e10, 5.6e8, "Primates", "High", "Great ape"),
    ("Parrot (African Grey)", 0.4, 3e9, 7.5e9, "Birds", "High", "High cognition"),
    ("Pigeon", 0.35, 3.1e8, 8.86e8, "Birds", "Medium", "Common bird"),
    ("Lizard", 0.1, 1e7, 1e8, "Reptiles", "Low", "Small reptile"),
]

# ============================================================================
# TECH DATA: Compute efficiency scaling (Kurzweil-inspired)
# ============================================================================
tech_data = [
    # (Entity, Year, CPS_per_Dollar, Category, Impact, Notes)
    ("Zeus II 1939", 1939, 6.5e-6, "Hardware", "Low", "Early baseline"),
    ("ENIAC 1945", 1945, 1e-4, "Hardware", "Medium", "Vacuum tube era"),
    ("UNIVAC 1951", 1951, 1e-3, "Hardware", "Medium", "Commercial computer"),
    ("IBM 7090 1959", 1959, 0.1, "Hardware", "Medium", "Transistor mainframe"),
    ("Intel 4004 1971", 1971, 10, "Hardware", "High", "Microprocessor start"),
    ("Intel 8086 1978", 1978, 100, "Hardware", "Medium", "PC era begins"),
    ("Intel 386 1985", 1985, 1e4, "Hardware", "Medium", "32-bit era"),
    ("Pentium 1993", 1993, 1e6, "Hardware", "Medium", "CISC dominance"),
    ("Pentium 4 2000", 2000, 1e8, "Hardware", "Medium", "GHz race"),
    ("Core i7 2008", 2008, 1e9, "Hardware", "High", "Multi-core era"),
    ("NVIDIA V100 2017", 2017, 1e10, "Hardware", "High", "GPU compute"),
    ("NVIDIA A100 2020", 2020, 5e10, "Hardware", "High", "AI accelerator"),
    ("NVIDIA B200 2024", 2024, 5e11, "Hardware", "Transformative", "75 quadrillion-fold"),
    ("Projected 2026", 2026, 2e12, "Hardware", "High", "Kurzweil trajectory"),
]

# AI model FLOPs (for secondary view)
ai_flops = [
    ("AlexNet 2012", 2012, 6e17, "High"),
    ("GPT-2 2019", 2019, 1e19, "High"),
    ("GPT-3 2020", 2020, 3.14e23, "Transformative"),
    ("GPT-4 2023", 2023, 2e25, "Transformative"),
    ("Grok-4 2026", 2026, 5e26, "Transformative"),
]

# ============================================================================
# COLOR SCHEMES
# ============================================================================
BIO_COLORS = {
    "Reptiles": "#7F8C8D",      # Gray
    "Birds": "#27AE60",          # Green
    "Mammals": "#3498DB",        # Blue
    "Primates": "#9B59B6",       # Purple
}

TECH_COLORS = {
    "Hardware": "#E67E22",       # Orange
    "AI": "#E74C3C",             # Red
}

IMPACT_SIZES = {
    "Transformative": 250,
    "High": 150,
    "Medium": 80,
    "Low": 50,
}


def create_dual_panel_plot():
    """Create the dual-panel visualization."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), dpi=150)
    fig.patch.set_facecolor('white')

    # ========================================================================
    # LEFT PANEL: Biological Allometry
    # ========================================================================
    ax1.set_facecolor('#FAFAFA')

    # Plot by group
    for entity, mass, neurons, per_kg, group, impact, notes in bio_data:
        color = BIO_COLORS.get(group, '#333')
        size = IMPACT_SIZES.get(impact, 80)

        # Plot neurons per kg vs body mass
        marker = 'o'
        edgecolor = 'white'
        alpha = 1.0

        if entity == "Human":
            marker = '*'
            size = 400
            edgecolor = '#C0392B'

        ax1.scatter(mass, per_kg, c=color, s=size, marker=marker,
                   alpha=alpha, edgecolors=edgecolor, linewidths=1.5, zorder=3)

    # Add trend lines
    # Mammals trend (excluding human outlier)
    mammal_data = [(m, pk) for e, m, n, pk, g, i, no in bio_data
                   if g == "Mammals"]
    if len(mammal_data) >= 2:
        m_mass, m_pk = zip(*mammal_data)
        log_m, log_pk = np.log10(m_mass), np.log10(m_pk)
        slope, intercept, r, p, se = stats.linregress(log_m, log_pk)
        x_fit = np.logspace(-2, 4, 100)
        y_fit = 10**(intercept + slope * np.log10(x_fit))
        ax1.plot(x_fit, y_fit, '--', color=BIO_COLORS["Mammals"], alpha=0.5,
                linewidth=2, label=f'Mammals (slope={slope:.2f})')

    # Primates trend
    primate_data = [(m, pk) for e, m, n, pk, g, i, no in bio_data
                    if g == "Primates"]
    if len(primate_data) >= 2:
        p_mass, p_pk = zip(*primate_data)
        log_m, log_pk = np.log10(p_mass), np.log10(p_pk)
        slope, intercept, r, p, se = stats.linregress(log_m, log_pk)
        x_fit = np.logspace(-1, 2, 100)
        y_fit = 10**(intercept + slope * np.log10(x_fit))
        ax1.plot(x_fit, y_fit, '--', color=BIO_COLORS["Primates"], alpha=0.5,
                linewidth=2, label=f'Primates (slope={slope:.2f})')

    # Add labels for key entities
    labels_bio = {
        "Human": (1.5, 1.5, "Human\n(86B neurons, EQ~7)"),
        "Elephant": (0.3, 0.4, "Elephant"),
        "Goldcrest": (2, 2, "Goldcrest\n(smallest bird)"),
        "Corvid/Rook": (2, 1.5, "Corvid"),
        "Mouse": (2, 0.5, "Mouse"),
        "Crocodile": (0.3, 2, "Crocodile"),
    }

    for entity, mass, neurons, per_kg, group, impact, notes in bio_data:
        if entity in labels_bio:
            x_mult, y_mult, label = labels_bio[entity]
            fontsize = 9 if entity == "Human" else 8
            weight = 'bold' if entity == "Human" else 'normal'
            ax1.annotate(label, xy=(mass, per_kg),
                        xytext=(mass * x_mult, per_kg * y_mult),
                        fontsize=fontsize, fontweight=weight,
                        arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5, lw=0.5),
                        ha='left', va='bottom')

    # Reference line: Kleiber's law slope (~0.75 for metabolism)
    x_ref = np.logspace(-3, 4, 100)
    # Typical neuron/kg vs mass has negative slope around -0.3 to -0.5
    ax1.plot(x_ref, 5e9 * x_ref**(-0.3), ':', color='gray', alpha=0.4, linewidth=1.5,
            label='Reference slope -0.3')

    # Shaded region for endothermy advantage
    ax1.axhspan(1e9, 1e11, alpha=0.1, color='#E74C3C', zorder=0)
    ax1.text(0.001, 3e10, 'Endotherm\nadvantage zone', fontsize=8,
            style='italic', alpha=0.6, color='#E74C3C')

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(1e-3, 1e4)
    ax1.set_ylim(1e5, 1e11)
    ax1.set_xlabel('Body Mass (kg)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Neurons per kg Body Mass', fontsize=13, fontweight='bold')
    ax1.set_title('Biological Allometry:\nNeural Efficiency vs. Body Size',
                 fontsize=14, fontweight='bold', pad=15)

    ax1.grid(True, which='major', linestyle='-', alpha=0.3)
    ax1.grid(True, which='minor', linestyle=':', alpha=0.15)

    # Legend for biology
    bio_handles = [mpatches.Patch(color=c, label=g) for g, c in BIO_COLORS.items()]
    bio_handles.append(Line2D([0], [0], marker='*', color='w', markerfacecolor='#9B59B6',
                              markersize=15, label='Human (outlier)'))
    ax1.legend(handles=bio_handles, loc='lower left', fontsize=8, framealpha=0.9)

    # ========================================================================
    # RIGHT PANEL: Tech Scaling
    # ========================================================================
    ax2.set_facecolor('#FAFAFA')

    # Plot hardware efficiency over time
    for entity, year, cps, category, impact, notes in tech_data:
        color = TECH_COLORS.get(category, '#333')
        size = IMPACT_SIZES.get(impact, 80)
        marker = 'o'
        edgecolor = 'white'

        if "B200" in entity or "2026" in entity:
            marker = 's'
            edgecolor = '#C0392B'

        ax2.scatter(year, cps, c=color, s=size, marker=marker,
                   alpha=0.9, edgecolors=edgecolor, linewidths=1.5, zorder=3)

    # Add exponential trend line (Kurzweil)
    years = np.array([d[1] for d in tech_data])
    cps = np.array([d[2] for d in tech_data])
    log_cps = np.log10(cps)

    slope, intercept, r, p, se = stats.linregress(years, log_cps)
    x_fit = np.linspace(1935, 2030, 100)
    y_fit = 10**(intercept + slope * x_fit)
    ax2.plot(x_fit, y_fit, '--', color='#E67E22', alpha=0.6, linewidth=2,
            label=f'Kurzweil trend\n(~{10**slope:.1f}x/year)')

    # Add AI FLOPs as secondary series (different y-scale implied)
    # We'll plot them as a secondary visual with different markers
    ax2_twin = ax2.twinx()
    for entity, year, flops, impact in ai_flops:
        size = IMPACT_SIZES.get(impact, 80)
        ax2_twin.scatter(year, flops, c=TECH_COLORS["AI"], s=size, marker='d',
                        alpha=0.7, edgecolors='white', linewidths=1, zorder=2)

    ax2_twin.set_yscale('log')
    ax2_twin.set_ylim(1e15, 1e28)
    ax2_twin.set_ylabel('Training FLOPs (AI models)', fontsize=11, color=TECH_COLORS["AI"], alpha=0.7)
    ax2_twin.tick_params(axis='y', labelcolor=TECH_COLORS["AI"], labelsize=9)

    # Labels for key tech milestones
    labels_tech = {
        "Zeus II 1939": (-5, 3, "Zeus II\n(1939)"),
        "ENIAC 1945": (3, 2, "ENIAC"),
        "Intel 4004 1971": (3, 2, "Intel 4004"),
        "NVIDIA B200 2024": (2, 0.3, "NVIDIA B200\n(75 quadrillion-fold)"),
        "Projected 2026": (2, 2, "2026\nprojected"),
    }

    for entity, year, cps, category, impact, notes in tech_data:
        if entity in labels_tech:
            x_off, y_mult, label = labels_tech[entity]
            fontsize = 9 if "B200" in entity else 8
            weight = 'bold' if "B200" in entity else 'normal'
            ax2.annotate(label, xy=(year, cps),
                        xytext=(year + x_off, cps * y_mult),
                        fontsize=fontsize, fontweight=weight,
                        arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5, lw=0.5),
                        ha='left', va='bottom')

    # Add AI labels
    for entity, year, flops, impact in ai_flops:
        if "GPT-3" in entity or "Grok" in entity:
            label = entity.split()[0]
            ax2_twin.annotate(label, xy=(year, flops),
                             xytext=(year + 1, flops * 2),
                             fontsize=8, color=TECH_COLORS["AI"],
                             arrowprops=dict(arrowstyle='-', color=TECH_COLORS["AI"],
                                           alpha=0.4, lw=0.5))

    # Shaded region for AI explosion
    ax2.axvspan(2012, 2030, alpha=0.1, color='#E74C3C', zorder=0)
    ax2.text(2015, 1e-5, 'AI Scaling\nExplosion', fontsize=9,
            style='italic', alpha=0.6, color='#E74C3C')

    ax2.set_yscale('log')
    ax2.set_xlim(1935, 2030)
    ax2.set_ylim(1e-7, 1e13)
    ax2.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Compute per Dollar (cps/$)', fontsize=13, fontweight='bold')
    ax2.set_title('Tech Scaling (Kurzweil-inspired):\nCompute Efficiency vs. Time',
                 fontsize=14, fontweight='bold', pad=15)

    ax2.grid(True, which='major', linestyle='-', alpha=0.3)
    ax2.grid(True, which='minor', linestyle=':', alpha=0.15)

    # Legend for tech
    tech_handles = [
        mpatches.Patch(color=TECH_COLORS["Hardware"], label='Hardware (cps/$)'),
        Line2D([0], [0], marker='d', color='w', markerfacecolor=TECH_COLORS["AI"],
               markersize=10, label='AI Models (FLOPs)'),
        Line2D([0], [0], linestyle='--', color='#E67E22', linewidth=2, label='Kurzweil trend'),
    ]
    ax2.legend(handles=tech_handles, loc='upper left', fontsize=8, framealpha=0.9)

    # ========================================================================
    # MAIN TITLE & FOOTNOTE
    # ========================================================================
    fig.suptitle('Energetic Scaling: Neural Efficiency (Biology) vs. Compute Efficiency (Technology)',
                fontsize=18, fontweight='bold', y=0.98)

    footnote = ("Log-log plots reveal power laws (straight lines = scaling rules). "
                "Biology: Neurons/kg vs. body mass shows clade differences; humans outlier (EQ~7). "
                "Tech: Compute/$ vs. time mirrors Kurzweil's exponential (~75 quadrillion-fold 1939–2024).\n"
                "Inspired by: Kleiber (metabolic 0.75), Herculano-Houzel (neuronal scaling), "
                "Kaplan/Charnov (LHT Ache/Tsimane). Estimates as of Jan 2026.")

    fig.text(0.5, 0.02, footnote, ha='center', fontsize=8, style='italic',
            wrap=True, alpha=0.7)

    plt.tight_layout(rect=[0, 0.06, 1, 0.95])

    return fig


def main():
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Create plot
    fig = create_dual_panel_plot()
    print("Created dual-panel energetic scaling plot")

    # Save outputs
    fig.savefig(os.path.join(output_dir, 'energetic_scaling.png'), dpi=300,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: energetic_scaling.png (300 DPI)")

    fig.savefig(os.path.join(output_dir, 'energetic_scaling.svg'), format='svg',
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: energetic_scaling.svg")

    fig.savefig(os.path.join(output_dir, 'energetic_scaling_highres.png'), dpi=400,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved: energetic_scaling_highres.png (400 DPI)")

    print("\nDone!")


if __name__ == '__main__':
    main()
