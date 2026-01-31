# Energetic Scaling: Biology vs. Technology

A publication-quality dual-panel log-log visualization comparing neural efficiency scaling in biology with compute efficiency scaling in technology.

![Energetic Scaling](output/energetic_scaling_highres.png)

## Interactive Version

Open [`output/energetic_scaling_interactive.html`](output/energetic_scaling_interactive.html) in your browser for an interactive version with hover tooltips.

## Key Insights

### Left Panel: Biological Allometry
- **Neurons per kg** vs. **body mass** reveals clade-specific scaling rules
- **Humans are outliers**: 86B neurons, Encephalization Quotient (EQ) ~7
- **Birds** achieve remarkable density (Goldcrest: 3.6×10¹⁰ neurons/kg)
- **Reptiles** have ~20x fewer neurons than endotherms at same body size
- Power-law slopes differ: mammals ~-0.3, primates flatter (linear scaling)

### Right Panel: Tech Scaling (Kurzweil-inspired)
- **Compute per dollar** has increased ~75 quadrillion-fold (1939–2024)
- Exponential trend continues: ~2x improvement per year
- **AI scaling explosion** post-2012 (AlexNet → GPT-4 → Grok-4)
- Training FLOPs grew from 10¹⁷ (AlexNet) to 10²⁶+ (frontier 2026)

## The Connection

Both panels reveal **power laws** (straight lines on log-log plots):
- Biology: Energy budget constrains neural investment; humans broke the curve
- Technology: Economic/physical limits drive exponential improvement; AI is the new outlier

| Domain | Scaling Rule | Outlier |
|--------|-------------|---------|
| Biology | Neurons/kg ~ Mass^(-0.3) | Human (EQ~7) |
| Tech | cps/$ ~ 2^(year/1.5) | AI FLOPs explosion |

## Data Sources

- **Neuronal scaling**: Herculano-Houzel et al. (comparative neuroanatomy)
- **Metabolic scaling**: Kleiber's Law (0.75 exponent)
- **Life History Theory**: Kaplan, Charnov (Ache/Tsimane forager data)
- **Tech price-performance**: Kurzweil (2024 update), NVIDIA specs
- **AI FLOPs**: Epoch AI, scaling reports

## Usage

### Requirements

```bash
pip install matplotlib numpy scipy plotly
```

### Generate Static Charts

```bash
cd src && python energetic_scaling.py
```

### Generate Interactive HTML

```bash
cd src && python energetic_scaling_plotly.py
```

## File Structure

```
energetic-scaling/
├── README.md
├── data/
│   └── scaling_data.csv
├── src/
│   ├── energetic_scaling.py
│   └── energetic_scaling_plotly.py
└── output/
    ├── energetic_scaling_highres.png
    ├── energetic_scaling.svg
    └── energetic_scaling_interactive.html
```

## Related Visualizations

- [AI Compute Timeline](../ai-compute-timeline/) – Training FLOPs growth over time
- [Adoption Timeline](../adoption-timeline/) – Time to mass adoption compression

Together, these three plots show:
1. **Compute growth** (AI Timeline) → enables scale
2. **Adoption compression** (Adoption Timeline) → accelerates deployment
3. **Efficiency scaling** (this plot) → fundamental limits and outliers

## License

MIT
