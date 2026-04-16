# Agent 5 — Port AI Compute Timeline to D3 (Complex)

## Goal
Replace the Plotly interactive at `ai-compute-timeline/output/ai_compute_timeline_interactive.html` with a high-quality D3.js version. This is the most complex chart in the repo — 51 data points spanning 10²–10²⁸ FLOPs across 120 years. Take it to the next level.

## Working directory
`/Users/mschwar/plots`

## Context
This chart is a semi-log timeline of AI compute milestones from 1900 to 2026+. It's the flagship visualization in the repo. The current Plotly version is functional but dated. The goal is a D3 chart that matches or exceeds the quality of the model-sizes chart.

**Read these files before starting:**

1. `/Users/mschwar/plots/ai-compute-timeline/data/ai_milestones.csv` — 51 rows, columns: `Year,Event,Category,Compute_FLOPs,Parameters,Impact`
2. `/Users/mschwar/plots/ai-compute-timeline/src/ai_compute_timeline.py` — the matplotlib version (read to understand the FLOPs parsing logic, category colors, era bands, label positions)
3. `/Users/mschwar/plots/model-sizes/output/model_sizes_interactive.html` — **visual template**. Match its dark theme, tooltip style, era-band approach, and D3 code patterns exactly.
4. `/Users/mschwar/plots/ai-compute-timeline/output/ai_compute_timeline_interactive.html` — current Plotly version (for reference, then replace)

---

## FLOPs parsing (critical)

The CSV's `Compute_FLOPs` column has messy values: `N/A`, `Proxy: ~5e2 ops/sec`, `~1e17-1e18`, `3.14E+23`, `Speculative 1e27+`, `High compute`, etc.

You must implement a JS parser. Logic (mirror the Python `parse_flops` function):

```js
function parseFlops(raw) {
    if (!raw || raw === 'N/A') return null;
    // Speculative: extract number
    const specMatch = raw.match(/(\d+\.?\d*)[eE]\+?(\d+)/);
    if (specMatch) return parseFloat(`${specMatch[1]}e${specMatch[2]}`);
    // Range: geometric mean  
    const rangeMatch = raw.match(/(\d+\.?\d*)[eE]\+?(\d+)[-–](\d+\.?\d*)[eE]\+?(\d+)/);
    if (rangeMatch) {
        const lo = parseFloat(`${rangeMatch[1]}e${rangeMatch[2]}`);
        const hi = parseFloat(`${rangeMatch[3]}e${rangeMatch[4]}`);
        return Math.sqrt(lo * hi);
    }
    // "High compute" → proxy
    if (/high compute/i.test(raw)) return 1e21;
    // Proxy: extract or use era-based fallback
    if (/proxy/i.test(raw)) { /* extract or null */ }
    return null;
}
```

For records where `parseFlops` returns null, assign a proxy based on year:
- year < 1945: 1e2
- year < 1960: 1e4  
- year < 1980: 1e6
- year < 2000: 1e8
- year < 2010: 1e10
- else: 1e12

Mark proxy records visually (smaller dot, lower opacity).

---

## What to build

A self-contained D3 v7 HTML file saved to `ai-compute-timeline/output/ai_compute_timeline_interactive.html`.

### Visual spec

**Layout:** 1060px wide, 600px tall. Same dark background (`#0f1117`) as model-sizes.

**Axes:**
- X: Year 1898–2028, linear scale
- Y: FLOPs, **log scale**, 10¹ to 10²⁹. Y-axis labels: `10³`, `10⁶`, `10⁹`, `10¹²`, `10¹⁵`, `10¹⁸`, `10²¹`, `10²⁴`, `10²⁷` (use superscript via HTML: `10<tspan baseline-shift="super" font-size="10">27</tspan>`)

**Era bands** (6 bands, subtle fills, labeled at top — same style as model-sizes):
- 1898–1940: "Mechanical Era" (`#1a1a2e`)
- 1940–1960: "Electronic Dawn" (`#1a2030`)
- 1960–2000: "Moore's Law Scaling" (`#1a2520`)
- 2000–2012: "Parallel & Early Deep" (`#2a1f10`)
- 2012–2022: "Deep Learning Era" (`#1f1a2e`)
- 2022–2028: "Reasoning & Agents" (`#2e1a1a`)

**Category colors** (from the Python source):
```js
const catColors = {
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
};
```

**Dot size by Impact:**
- Transformative: r=10
- High: r=7
- Medium: r=5
- Speculative: r=7, dashed stroke

**Connecting line:** Two segments:
- 1900–2010: dashed `#4b5563` at 25% opacity (proxy era)
- 2010–2028: solid `#6b7280` at 50% opacity

**Moore's Law reference line:**
Dashed orange line from (1965, 10⁶) to (2005, 10¹⁴). Label it "Moore's Law (2× / 2yr)".

**Labels:** Show labels for ~25 key events. Use the label map from the Python source (`get_short_label` function). Position them using the `label_positions` dict in the Python source as a starting guide. 

For labels: use a collision-avoidance strategy — after placing all labels, run 30 iterations of a simple Y-repulsion pass (nudge overlapping labels apart by their overlap amount). This is much better than hardcoded offsets.

**Annotations:**
- "2023–25 Frontier Cluster" bracket on the right side pointing to the dense cluster at 10²⁴–10²⁶
- Small note box (bottom-left): "Pre-2010 values are rough proxies. Dashed line = proxy era. ◆ = speculative."

**Tooltip:**
Show: Event name (bold), FLOPs value (formatted as `10^N`), Category, Year, Parameters (if available), Impact.

**Zoom/pan:**
Add `d3.zoom()` — the X range is 130 years wide and users want to zoom into recent years. On zoom, update both axes and reposition dots + labels. Add a "Reset zoom" button.

---

## Advanced features (if time allows)

**Timeline scrubber:** A range input below the chart that filters displayed dots to a year range. As user drags, dots outside the range fade out.

**Search box:** A text input that highlights dots whose event name matches.

---

## Technical requirements
- D3 v7 from CDN: `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js`
- Self-contained HTML: all CSS inline, all JS inline
- Data hardcoded as a JS array (parse from the CSV structure, don't fetch)
- Must work as local `file://` URL
- Smooth transitions on all state changes (200ms ease)

## Done when
Save to `ai-compute-timeline/output/ai_compute_timeline_interactive.html`. Open in browser and verify:
- All 51 dots render at correct FLOPs values
- Log scale Y-axis is correct (10² to 10²⁸)
- Hover tooltips work on every dot
- Zoom/pan works and Reset button restores original view
- Era bands and Moore's Law line display
- Dark background consistent with model-sizes chart
- No serious label collisions in the 2020–2026 cluster
