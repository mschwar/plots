# Agent 3 — Model Sizes: D3 Chart Enhancements

## Goal
Enhance the existing D3.js interactive chart at `/Users/mschwar/plots/model-sizes/output/model_sizes_interactive.html`. Add filter controls, fix label collisions, and improve usability. This is pure HTML/CSS/D3 JavaScript work — no Python.

## Working directory
`/Users/mschwar/plots`

## Context
The model-sizes chart is a standalone self-contained D3 v7 visualization showing LLM parameter counts (2019–2026) on a log-scale scatter plot. It already works well. We want to make it significantly more interactive and polished.

**Read this file first — it's the only file you'll modify:**
`/Users/mschwar/plots/model-sizes/output/model_sizes_interactive.html`

The data is inline in the JS as a `const models = [...]` array. Each model has: `name`, `date`, `params`, `org`, `estimated`, `unreleased`, `note`. The chart uses D3 scales, dots, labels, and tooltips.

---

## Task 3A: Org filter pill buttons

Add a row of pill toggle buttons above the chart — one per org. Clicking toggles that org's dots + labels on/off. "All" button resets.

**Implementation:**
1. After `const orgs = [...]` (which already exists in the legend code), insert a filter bar div into `#chart-container` above the SVG.
2. Style: horizontal flex row, each pill has `background: transparent`, `border: 1px solid <org-color>`, `border-radius: 20px`, `padding: 4px 12px`, `color: <org-color>`, `cursor: pointer`. Active pills have `background: <org-color>20` (20% opacity fill). 
3. State: maintain a `Set` of active orgs (start with all active). On pill click: toggle org in/out of the set, then update dot opacity (inactive = 0.08) and label opacity (inactive = 0).
4. Add an "All" pill at the start that re-activates everything.

```js
// Example structure (adapt to fit the existing code style)
const filterState = new Set(orgs);

const filterBar = d3.select("#chart-container")
    .insert("div", "svg")  // insert before SVG
    .style("display", "flex")
    .style("flex-wrap", "wrap")
    .style("gap", "8px")
    .style("margin-bottom", "16px")
    .style("padding", "0 4px");

// "All" pill
filterBar.append("button")
    .text("All")
    .style("/* pill styles */")
    .on("click", () => { orgs.forEach(o => filterState.add(o)); updateFilter(); });

// Per-org pills
orgs.forEach(org => {
    filterBar.append("button")
        .text(org)
        .style("border-color", orgColors[org] || "#9ca3af")
        .style("color", orgColors[org] || "#9ca3af")
        .on("click", function() {
            if (filterState.has(org)) filterState.delete(org);
            else filterState.add(org);
            updateFilter();
        });
});

function updateFilter() {
    d3.selectAll(".dot").style("opacity", d => filterState.has(d.org) ? 0.88 : 0.06);
    d3.selectAll(".label").style("opacity", d => filterState.has(d.org) ? 1 : 0);
    // update pill active states
}
```

**Note:** For this to work, the `.datum(d)` must be set on the labels too — check the existing code. If labels don't have datum, add `datum(d)` to the label append calls so `filterState.has(d.org)` works on them.

---

## Task 3B: Estimated/unreleased toggle

Add two checkbox toggles below the filter bar:
- `☐ Hide estimated` — when checked, fade out all dots where `d.estimated === true`
- `☐ Hide unreleased` — when checked, fade out all dots where `d.unreleased === true`

Style them as small toggle switches using CSS (no external libraries).

When both a filter pill AND a hide-estimated toggle are active, use the more restrictive rule (AND logic).

---

## Task 3C: Fix label collisions

Currently some labels overlap (especially in the 2023–2024 cluster). Implement a simple force-separation pass:

After all labels are placed, run 20 iterations of a 1D repulsion pass on the Y positions of labels that share a similar X coordinate (within 40px):

```js
// After labels are rendered, collect their bounding boxes and nudge
const labelEls = svg.selectAll(".label").nodes();
// For each pair within 40px X-distance, push Y apart if they overlap
// This is a simple greedy pass, not full force simulation
```

Alternatively — and simpler — just audit the `labelOffsets` object and fix the worst collisions manually by adjusting offset values. The main clusters to fix:
- LLaMA 2, LLaMA 3, LLaMA 3.1, Claude Opus 4.6 all cluster around 70–405B in 2023–2024
- Claude Opus 4.7 and Claude 3.7 Sonnet are close
- DeepSeek V3 and DeepSeek R1 have the same params and nearly the same date

---

## Task 3D: Year marker lines

Add subtle vertical tick marks at Jan 1 of each year (2019–2026) on the X axis, with the year label — currently the x-axis only has the D3 auto-ticks which may not align cleanly with Jan 1. Ensure tick labels show every year from 2019–2026.

---

## Task 3E: Mobile responsiveness

The chart currently has a fixed pixel width. Make it responsive:
- Change `const width = Math.min(1060, window.innerWidth - 40) - margin.left - margin.right;` to also recalculate on `window.resize`
- Add `max-width: 100%; height: auto;` to the SVG element
- On screens < 600px, hide text labels entirely (only show dots + tooltips)

---

## Design constraints
- Keep the dark background (`#0f1117`) and the existing color palette
- Don't add any new external CDN dependencies beyond D3 v7 (already loaded)
- Tooltips must still work after all changes
- The file is self-contained — all JS/CSS is inline

## Done when
- Filter pills render above the chart and correctly toggle dots/labels
- Estimated + unreleased toggles work
- Worst label collisions are fixed
- Chart is mobile-responsive
- Open the file in a browser and verify visually before reporting done
