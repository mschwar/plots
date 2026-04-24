#!/usr/bin/env python3
"""Generate README.md from the manifest inventory."""

from __future__ import annotations

from manifest_utils import ROOT, published_entries


def _entry_section(entry: dict) -> str:
    links = [f"- **Interactive**: [{entry['title']}]({entry['interactive']})"]
    if entry.get("png"):
        links.append(f"- **Static**: [PNG]({entry['png']}) | [SVG]({entry['svg']})")
    links.append(f"- **Data**: [{entry['data']}]({entry['data']})")
    links.append(f"- **Metadata**: [{entry['metadata']}]({entry['metadata']})")
    if entry.get("readme"):
        links.append(f"- **Details**: [{entry['id']}/]({entry['id']}/)")
    return f"""## {entry['order']}. {entry['title']}

{entry['description']}

Hero stat: **{entry['hero_stat']}**. Data confidence: **{entry['confidence']}**.

{chr(10).join(links)}
"""


def render_readme(entries: list[dict]) -> str:
    quick_links = "\n".join(
        f"- [{entry['title']}]({entry['interactive']})" for entry in entries
    )
    sections = "\n---\n\n".join(_entry_section(entry) for entry in entries)
    count = len(entries)
    return f"""# Exponential Progress Atlas

Interactive timelines showing how compute, energy, coordination, memory, and adoption compound into civilizational acceleration.

The root inventory is [`plots_manifest.json`](plots_manifest.json). Homepage cards, README links, build ordering, dashboard lanes, and validation all read from that manifest.

## Published Inventory ({count})

{quick_links}

---

{sections}

---

## Data Contracts

- `ai-compute-timeline/data/ai_milestones.csv` uses normalized fields: `year,event,category,value_numeric,value_low,value_high,value_unit,estimate_status,source_id,confidence,display_label,notes`.
- `adoption-timeline/data/tech_adoption.csv` includes `adoption_metric_type`, `comparability_level`, `source_id`, `confidence`, and notes so unlike adoption proxies are not treated as perfectly comparable.
- Energetic Scaling keeps comparison-level data in `scaling_data.csv` and splits clean source contracts into `biology_neural_scaling.csv`, `hardware_efficiency.csv`, `ai_training_flops.csv`, and `foraging_lht.csv`.

## Repository Structure

Each plot should follow this structure:

```text
<plot-name>/
├── index.html
├── data/
│   ├── <slug>.csv
│   └── meta.json
├── output/
│   ├── *_interactive.html
│   ├── *_highres.png
│   └── *.svg
├── src/
│   ├── *.py
│   └── *_plotly.py
└── README.md
```

## Development

```bash
python -m pip install -r requirements.txt
python build_all.py
python scripts/generate_homepage.py
python scripts/generate_readme_links.py
python scripts/validate_all.py
python scripts/check_links.py
python scripts/check_accessibility_static.py
```

## Adding a New Plot

1. Create the standard plot directory structure.
2. Add data, metadata, generator scripts, output paths, and README.
3. Add the entry to `plots_manifest.json` with `status: "draft"` until outputs and sources pass validation.
4. Run the build, generators, validators, link checker, and accessibility checker.
5. Change `status` to `"published"` only when the plot should appear on the homepage and dashboard.

## Deployment

GitHub Pages deploys should run the same validation commands in CI before publishing. A failed build, broken relative link, missing alt text, stale output, or manifest mismatch should block deployment.

## License

MIT
"""


def main() -> None:
    (ROOT / "README.md").write_text(render_readme(published_entries(ROOT)), encoding="utf-8")


if __name__ == "__main__":
    main()
