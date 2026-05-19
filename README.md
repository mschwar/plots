# Exponential Progress Atlas

Interactive timelines showing how compute, energy, coordination, memory, and adoption compound into civilizational acceleration.

The root inventory is [`plots_manifest.json`](plots_manifest.json). Homepage cards, README links, build ordering, dashboard lanes, and validation all read from that manifest.

## Published Inventory (9)

- [AI Compute Timeline](ai-compute-timeline/output/ai_compute_timeline_interactive.html)
- [Adoption Timeline](adoption-timeline/output/adoption_timeline_interactive.html)
- [Energetic Scaling](energetic-scaling/output/energetic_scaling_interactive.html)
- [Civilization Scaling](civilization-scaling/output/civilization_scaling_interactive.html)
- [Energy Leverage](energy-leverage-per-person/output/energy_leverage_interactive.html)
- [Model Sizes](model-sizes/output/model_sizes_interactive.html)
- [AI Benchmark Progress](ai-benchmark-progress/output/benchmark_progress_interactive.html)
- [Cost to Train](cost-to-train/output/cost_to_train_interactive.html)
- [Unified Dashboard](dashboard/index.html)

---

## 1. AI Compute Timeline

Training compute from early electronic computing to frontier AI, with proxies and speculative projections labeled separately.

Hero stat: **10^27+ FLOPs**. Data confidence: **mixed**.

- **Interactive**: [AI Compute Timeline](ai-compute-timeline/output/ai_compute_timeline_interactive.html)
- **Static**: [PNG](ai-compute-timeline/output/ai_compute_timeline_highres.png) | [SVG](ai-compute-timeline/output/ai_compute_timeline.svg)
- **Data**: [ai-compute-timeline/data/ai_milestones.csv](ai-compute-timeline/data/ai_milestones.csv)
- **Metadata**: [ai-compute-timeline/data/meta.json](ai-compute-timeline/data/meta.json)
- **Details**: [ai-compute-timeline/](ai-compute-timeline/)

---

## 2. Adoption Timeline

Time-to-scale proxies across computing, connectivity, mobile, cloud, and AI paradigms.

Hero stat: **60x faster**. Data confidence: **mixed**.

- **Interactive**: [Adoption Timeline](adoption-timeline/output/adoption_timeline_interactive.html)
- **Static**: [PNG](adoption-timeline/output/adoption_timeline_highres.png) | [SVG](adoption-timeline/output/adoption_timeline.svg)
- **Data**: [adoption-timeline/data/tech_adoption.csv](adoption-timeline/data/tech_adoption.csv)
- **Metadata**: [adoption-timeline/data/meta.json](adoption-timeline/data/meta.json)
- **Details**: [adoption-timeline/](adoption-timeline/)

---

## 3. Energetic Scaling

Biology, hardware efficiency, AI training compute, and foraging energetics compared with clean source datasets.

Hero stat: **10^6x+ efficiency**. Data confidence: **mixed**.

- **Interactive**: [Energetic Scaling](energetic-scaling/output/energetic_scaling_interactive.html)
- **Static**: [PNG](energetic-scaling/output/energetic_scaling_highres.png) | [SVG](energetic-scaling/output/energetic_scaling.svg)
- **Data**: [energetic-scaling/data/scaling_data.csv](energetic-scaling/data/scaling_data.csv)
- **Metadata**: [energetic-scaling/data/meta.json](energetic-scaling/data/meta.json)
- **Details**: [energetic-scaling/](energetic-scaling/)

---

## 4. Civilization Scaling

Five civilizational lanes: energy, coordination, memory, replication, and latency over log-time.

Hero stat: **5 lanes**. Data confidence: **mixed**.

- **Interactive**: [Civilization Scaling](civilization-scaling/output/civilization_scaling_interactive.html)
- **Static**: [PNG](civilization-scaling/output/civilization_scaling_highres.png) | [SVG](civilization-scaling/output/civilization_scaling.svg)
- **Data**: [civilization-scaling/data/civilization_metrics.csv](civilization-scaling/data/civilization_metrics.csv)
- **Metadata**: [civilization-scaling/data/meta.json](civilization-scaling/data/meta.json)
- **Details**: [civilization-scaling/](civilization-scaling/)

---

## 5. Energy Leverage

Per-person energy command relative to the metabolic baseline, with period anchors labeled explicitly.

Hero stat: **17x body energy**. Data confidence: **high**.

- **Interactive**: [Energy Leverage](energy-leverage-per-person/output/energy_leverage_interactive.html)
- **Static**: [PNG](energy-leverage-per-person/output/energy_leverage_highres.png) | [SVG](energy-leverage-per-person/output/energy_leverage.svg)
- **Data**: [energy-leverage-per-person/data/energy_leverage_datapoints.csv](energy-leverage-per-person/data/energy_leverage_datapoints.csv)
- **Metadata**: [energy-leverage-per-person/data/meta.json](energy-leverage-per-person/data/meta.json)
- **Details**: [energy-leverage-per-person/](energy-leverage-per-person/)

---

## 6. Model Sizes

Language model parameter counts over time, separating disclosed counts from estimates and unreleased projections.

Hero stat: **1.5B -> 5T params**. Data confidence: **speculative**.

- **Interactive**: [Model Sizes](model-sizes/output/model_sizes_interactive.html)
- **Static**: [PNG](model-sizes/output/model_sizes_highres.png) | [SVG](model-sizes/output/model_sizes.svg)
- **Data**: [model-sizes/data/llm_model_sizes.csv](model-sizes/data/llm_model_sizes.csv)
- **Metadata**: [model-sizes/data/meta.json](model-sizes/data/meta.json)
- **Details**: [model-sizes/](model-sizes/)

---

## 7. AI Benchmark Progress

Benchmark progress against human baselines across knowledge, coding, software engineering, and reasoning tasks.

Hero stat: **4 benchmark lanes**. Data confidence: **mixed**.

- **Interactive**: [AI Benchmark Progress](ai-benchmark-progress/output/benchmark_progress_interactive.html)
- **Static**: [PNG](ai-benchmark-progress/output/benchmark_progress_highres.png) | [SVG](ai-benchmark-progress/output/benchmark_progress.svg)
- **Data**: [ai-benchmark-progress/data/benchmark_data.csv](ai-benchmark-progress/data/benchmark_data.csv)
- **Metadata**: [ai-benchmark-progress/data/meta.json](ai-benchmark-progress/data/meta.json)
- **Details**: [ai-benchmark-progress/](ai-benchmark-progress/)

---

## 8. Cost to Train

Training cost, FLOPs, and capability over time, showing the efficiency paradox at the frontier.

Hero stat: **$/FLOP collapse**. Data confidence: **mixed**.

- **Interactive**: [Cost to Train](cost-to-train/output/cost_to_train_interactive.html)
- **Static**: [PNG](cost-to-train/output/cost_to_train_highres.png) | [SVG](cost-to-train/output/cost_to_train.svg)
- **Data**: [cost-to-train/data/training_costs.csv](cost-to-train/data/training_costs.csv)
- **Metadata**: [cost-to-train/data/meta.json](cost-to-train/data/meta.json)
- **Details**: [cost-to-train/](cost-to-train/)

---

## 9. Unified Dashboard

A synchronized overview of the atlas inventory using the same manifest as the homepage, README, build, and validator.

Hero stat: **9 atlas entries**. Data confidence: **mixed**.

- **Interactive**: [Unified Dashboard](dashboard/index.html)
- **Data**: [plots_manifest.json](plots_manifest.json)
- **Metadata**: [plots_manifest.json](plots_manifest.json)
- **Details**: [dashboard/](dashboard/)


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
python scripts/generate_sitemap.py
python scripts/validate_repo.py --check
python scripts/check_links.py
python scripts/check_accessibility_static.py
python -m pytest tests -q
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
