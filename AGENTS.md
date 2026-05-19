# AGENTS.md

## Orientation

This repo is a manifest-driven static atlas of plots and dashboards. Start here, in this order:

1. `CURRENT_STATE.md`
2. `plots_manifest.json`
3. `README.md`
4. `docs/agentic-overhaul/2026-05-audit.md`
5. The plot directory you plan to touch

The manifest is the source of truth for inventory, order, and published status. The generated homepage, README inventory, sitemap, and validation all read from it.

## Canonical Sources

- `plots_manifest.json`: inventory, order, status, canonical links
- `<plot>/data/*.csv`: source data
- `<plot>/data/meta.json`: provenance, field descriptions, and source list
- `<plot>/src/*.py`: plot generators
- `shared/site.css` and `shared/site.js`: shared site chrome
- `dashboard/`: hand-authored cross-plot dashboard
- `scripts/generate_homepage.py`, `scripts/generate_readme_links.py`, `scripts/generate_sitemap.py`: generated site surfaces
- `scripts/validate_repo.py`: repo-level validation entrypoint
- `CURRENT_STATE.md`: current truth snapshot for humans and agents

## Generated vs Hand-Authored

Generated and should not be edited by hand when a generator exists:

- `README.md`
- `index.html`
- `sitemap.xml`
- each plot's `output/*`

Hand-authored and should be edited directly:

- `plots_manifest.json`
- all CSV and `meta.json` sources
- all `src/*.py` generators
- `shared/site.css`
- `shared/site.js`
- `dashboard/index.html`
- `dashboard/dashboard.js`
- `dashboard/dashboard.css`
- `AGENTS.md`
- `CURRENT_STATE.md`
- `docs/agentic-overhaul/2026-05-audit.md`

Historical or archival:

- `CLAUDE.md`
- `.agent-tasks/`
- `docs/plans/`

## Commands

Run these before and after changes as appropriate:

```bash
python -m pip install -r requirements.txt
python build_all.py
python scripts/generate_homepage.py
python scripts/generate_readme_links.py
python scripts/generate_sitemap.py
python scripts/validate_repo.py --check
python scripts/check_links.py
python scripts/check_accessibility_static.py
python -m pytest tests -q
```

Use `python scripts/validate_repo.py --check` as the canonical validation command for this repo.

## Data and Provenance

- CSVs are the source of truth for plotted data.
- Keep `meta.json` `fields` keys aligned with CSV headers.
- Every non-speculative row should carry provenance through `source_id` or the equivalent schema field.
- Speculative or projection rows must remain labeled as such.
- Do not invent citations, dates, or source claims. If a claim cannot be verified locally, mark it as unresolved.

## Accessibility and Documentation

- Keep image `alt` text present and specific.
- Keep interactive links and controls accessible by name.
- Update `CURRENT_STATE.md` when repo shape or command status changes.
- Update the generator sources, not the generated `README.md` or homepage HTML, when inventory text changes.

## Safe Change Rules

- Use `apply_patch` for edits.
- Keep changes small and reviewable.
- Do not hand-edit generated artifacts when a generator exists.
- Do not rename plot directories or manifest IDs without a coordinated migration.
- Do not introduce a new framework or build system unless the repo already needs it.
- Use `sys.executable` in subprocess tests and helper scripts. Avoid hardcoding `python3`.

## Known Traps

- `build_all.py` runs from the repo root and needs the `scripts/` helper import path.
- `validate_repo.py --check` is the strict validator; `validate_all.py` is the lower-level plot checker.
- `model-sizes/` has source generators now; the old no-src note in `CLAUDE.md` is stale.
- `dashboard/` is hand-authored and not produced by `build_all.py`.
- `.agent-tasks/` and `docs/plans/` contain historical briefs that may be out of date. Treat them as context, not instructions.
