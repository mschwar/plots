# Current State

Audit date: 2026-05-19

This repo is a manifest-driven static atlas of plot pages, generated homepage content, generated README inventory text, a shared dashboard, a browser smoke harness, and Python-based plot generators. The manifest is the inventory source of truth; data and metadata live beside each plot; generated outputs live under each plot's `output/` directory.

## Confirmed Working Pieces

- The repository has a canonical manifest at `plots_manifest.json`.
- The root homepage, README inventory, and sitemap are generated from repo scripts.
- `build_all.py` now runs from the repository root.
- The repo-level validator exists at `scripts/validate_repo.py`.
- The test suite includes bootstrap smoke checks for the build and validator entrypoints.
- The shared accessibility and link-check scripts are present.
- The browser smoke harness exists at `scripts/browser_smoke.py`.
- The unified dashboard loads only local manifest/CSV files and no longer depends on a remote runtime CDN.


## Commands

Status below reflects the current local verification pass.

- `python -m pip install -r requirements.txt` - passed
- `uv run --with numpy --with pandas --with matplotlib --with plotly --with scipy python build_all.py` - passed and refreshed generated outputs
- `python scripts/generate_homepage.py` - passed
- `python scripts/generate_readme_links.py` - passed
- `python scripts/generate_sitemap.py` - passed
- `python scripts/validate_all.py` - passed
- `python scripts/validate_repo.py --check` - passed
- `python scripts/check_links.py` - passed
- `python scripts/check_accessibility_static.py` - passed
- `python scripts/browser_smoke.py` - passed for homepage, dashboard, and AI Compute Timeline
- Browser QA (desktop + mobile screenshots in `.gstack/qa-reports/screenshots/`) passed on homepage, dashboard, and AI Compute Timeline with no console errors
- `python -m pytest tests -q` - passed

## Important Files and Directories

- `plots_manifest.json`
- `build_all.py`
- `scripts/validate_repo.py`
- `scripts/validate_all.py`
- `scripts/generate_homepage.py`
- `scripts/generate_readme_links.py`
- `scripts/generate_sitemap.py`
- `shared/site.css`
- `shared/site.js`
- `dashboard/`
- `ai-compute-timeline/`
- `adoption-timeline/`
- `energetic-scaling/`
- `civilization-scaling/`
- `energy-leverage-per-person/`
- `model-sizes/`
- `ai-benchmark-progress/`
- `cost-to-train/`
- `docs/agentic-overhaul/2026-05-audit.md`

## Stale or Conflicting Docs and Metadata

- `CLAUDE.md` was stale and now points to `AGENTS.md`.
- `.agent-tasks/README.md` was archival and now points to `AGENTS.md`.
- `docs/plans/2026-04-24-three-next-level-plots.md` is historical and no longer matches the live repo shape.
- `scripts/validate_all.py` is the lower-level checker; it warns if outputs drift behind sources, while `scripts/validate_repo.py --check` treats that drift as an error.

## Known Risks

- The dashboard is offline-safe and loads local manifest/CSV assets instead of a remote D3 CDN.
- Some plot rows remain speculative or projection-based and should not be reworded into facts without source review.
- Generated outputs need to be rebuilt after data or source edits to stay fresh.
- The repo depends on the Python packages listed in `requirements.txt`.

## Immediate Next Moves

1. Use `python scripts/browser_smoke.py --html /tmp/browser-smoke/index.html` before browser QA for the homepage, dashboard, and AI Compute Timeline.
2. Follow `docs/agentic-overhaul/two-prompt-buildout-plan.md` for the next feature branch.
3. Run `python build_all.py` when changing data or plot generators.
4. Run `python scripts/validate_repo.py --check` after any substantive change.
5. Keep `CURRENT_STATE.md` and `docs/agentic-overhaul/2026-05-audit.md` up to date when the repo shape changes.

## Handoff Note

- Changed: the unified dashboard now loads only local assets and renders with inline SVG instead of a remote D3 CDN; the year parser now preserves zero-valued years and full-width year strings.
- Verified by: `python -m pytest tests/test_dashboard.py tests/test_dashboard_year_parsing.py tests/test_browser_smoke.py -q`, `python scripts/browser_smoke.py`, and browser QA screenshots on the live Pages site.
- Evidence: `.gstack/qa-reports/screenshots/dashboard-desktop.png`, `.gstack/qa-reports/screenshots/dashboard-mobile.png`, `.gstack/qa-reports/screenshots/homepage-desktop.png`.
- Next feature: provenance coverage for speculative rows.
