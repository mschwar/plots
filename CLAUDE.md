# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Rebuild all plots (runs all src/*.py scripts)
python build_all.py

# Rebuild a single plot
cd <plot-name>/src
python <slug>.py             # Static PNG/SVG (matplotlib)
python <slug>_plotly.py      # Interactive HTML (Plotly)

# Validate all plots (checks required files, meta.json vs CSV headers)
python scripts/validate_all.py
```

## Architecture

Each plot is a self-contained directory:

```
<plot-name>/
├── data/<slug>.csv       # Source data (edit here to update content)
├── data/meta.json        # title, description, fields, sources — must stay in sync with CSV headers
├── src/<slug>.py         # matplotlib static generator → output/*.png, *.svg
├── src/<slug>_plotly.py  # Plotly interactive generator → output/*_interactive.html
├── output/               # Generated artifacts (not hand-edited)
└── index.html            # Plot landing page (links shared/site.css via ../)
```

`shared/site.css` and `shared/site.js` are referenced by all `index.html` files. `site.js` injects the nav bar.

`model-sizes` is the exception: it has no `src/` Python scripts. Its `output/model_sizes_interactive.html` is a standalone D3 visualization — edit it directly.

`build_all.py` skips plots with no `src/` directory, so `model-sizes` is silently skipped.

### Adding a new plot

1. Create `<plot-name>/` following the structure above.
2. Add an entry to `PLOT_DIRS` in `build_all.py`.
3. Add a validation config to `PLOTS` in `scripts/validate_all.py`.
4. Add a link in the root `index.html` and `README.md`.

### Data conventions

- CSVs are the source of truth. `meta.json` `fields` keys must match CSV headers or validation warns.
- Plotly outputs use CDN (`include_plotlyjs='cdn'`) to avoid large embedded JS.
- Static images use matplotlib with high DPI (`dpi=150`+).
