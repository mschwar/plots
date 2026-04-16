# Agent 4 — Port Adoption Timeline to D3

## Goal
Replace the static Plotly interactive HTML (`adoption-timeline/output/adoption_timeline_interactive.html`) with a new, much better D3.js version. The existing Plotly version is mediocre. The new D3 version should match the visual quality of the model-sizes chart.

## Working directory
`/Users/mschwar/plots`

## Context
The adoption timeline shows time-to-50M-users for major technologies from 1957 to 2026. Y-axis = days (log scale), X-axis = year. The trend is exponential compression: 10 years → 60 days. 22 data points.

**Read these files before starting:**

1. `/Users/mschwar/plots/adoption-timeline/data/tech_adoption.csv` — the data (22 rows)
2. `/Users/mschwar/plots/model-sizes/output/model_sizes_interactive.html` — **use this as your visual template**. Copy its dark theme, font choices, tooltip style, era-band approach, and D3 patterns. The goal is a consistent visual language across both charts.
3. `/Users/mschwar/plots/adoption-timeline/output/adoption_timeline_interactive.html` — the current Plotly version (to understand what exists, then replace it)

## CSV Schema
```
Year,Event,Category,Days_to_Adoption,Impact
1957,FORTRAN Compiler (IBM),Software/Compiler,3650,High
2022,ChatGPT public launch,AI/Agentic,60,Transformative
```
Categories: Hardware, Software/Compiler, Internet/Web, Mobile, Social/Apps, Cloud/Infrastructure, AI/Agentic

---

## What to build

A self-contained D3 v7 HTML file saved to `adoption-timeline/output/adoption_timeline_interactive.html`.

### Visual spec

**Layout:** Single chart, ~1060px wide, ~540px tall. Same dark background (`#0f1117`) as model-sizes chart.

**Axes:**
- X: Year (1953–2032). Use `d3.scaleLinear` or `d3.scaleTime`.
- Y: Days to adoption, **log scale** (`d3.scaleLog`). Range: 7 days to 5000 days.
- Y-axis tick labels should be human-readable: "1 wk", "1 mo", "3 mo", "1 yr", "3 yr", "10 yr" (not raw numbers).

**Era bands** (same style as model-sizes — subtle dark fills with label at top):
- 1953–1990: "Pre-Internet"
- 1990–2005: "Web Era"
- 2005–2015: "Mobile Era"
- 2015–2032: "AI Era"

**Dots:**
- Color by Category (define your own color palette, harmonious with the model-sizes chart):
  - Hardware: `#60a5fa` (blue)
  - Software/Compiler: `#f59e0b` (amber)
  - Internet/Web: `#34d399` (green)
  - Mobile: `#a78bfa` (purple)
  - Social/Apps: `#f472b6` (pink)
  - Cloud/Infrastructure: `#94a3b8` (slate)
  - AI/Agentic: `#f87171` (red)
- Transformative impact → larger dot (r=9), High → r=7, Medium → r=5
- Speculative rows → dashed circle (same style as model-sizes)

**Trend line:**
A dashed exponential decay curve fit through the data (use `d3.line` with curve). Color: `#a78bfa` at 30% opacity. Show it from 1957 to 2032.

The trend equation (pre-computed): `days = 3650 * exp(-0.085 * (year - 1957))`

**Labels:**
Show labels for at least these key points (others optional):
- ARPANET (1969)
- WWW (1989)
- iPhone (2007)
- Instagram (2010)
- TikTok (2016)
- ChatGPT (2022)
- Projected agent (2026)

**Tooltip:**
On hover, show: Event name (bold, category color), Days value in human-readable form (e.g. "60 days" or "~10 years"), Category, Year, Impact.

**"Today" reference line:**
Vertical dashed line at 2026 labeled "Today (Apr 2026)" in muted text.

**Legend:**
Bottom row of colored dots + category names, same style as model-sizes legend.

**Annotation arrow:**
A curved SVG path annotation from ChatGPT dot pointing right with text: "60× compression\nsince ARPANET". Use `d3.annotate` or manual SVG paths.

### Key interaction
Same hover/mousemove/mouseout as model-sizes. No zoom needed.

---

## Technical requirements
- D3 v7 from CDN: `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js`
- Self-contained: all styles inline in `<style>`, all JS inline in `<script>`
- Data hardcoded inline (don't fetch the CSV — parse it inline as a JS array)
- Must work when opened as a local `file://` URL

## Done when
Save to `adoption-timeline/output/adoption_timeline_interactive.html`. Open it in a browser and verify:
- All 22 dots render correctly on log scale
- Hover tooltips work on every dot
- Era bands and trend line display
- Dark background consistent with model-sizes chart
- Labels are readable and don't overlap badly
