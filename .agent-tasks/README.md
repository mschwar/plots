# Agent Task Packages

5 parallel agents. Each brief is self-contained — agents start cold with no conversation context.

| # | File | Task | Intelligence needed | Files modified |
|---|------|------|--------------------|----|
| 1 | `agent1-data-freshness.md` | Update 3 CSVs with 2026 model data | **Haiku** — pure data entry | `ai-compute-timeline/data/ai_milestones.csv`, `adoption-timeline/data/tech_adoption.csv`, `energetic-scaling/data/ai_model_data.csv` |
| 2 | `agent2-homepage-site-upgrade.md` | Dark mode toggle, card stats, mobile layout, nav fix | **Sonnet** — CSS/JS/HTML | `shared/site.css`, `shared/site.js`, `index.html` |
| 3 | `agent3-model-sizes-d3-enhancements.md` | Add filter pills, toggles, fix label collisions, mobile | **Sonnet** — D3.js | `model-sizes/output/model_sizes_interactive.html` |
| 4 | `agent4-adoption-timeline-d3.md` | Full D3 rewrite of adoption timeline | **Sonnet** — D3.js | `adoption-timeline/output/adoption_timeline_interactive.html` |
| 5 | `agent5-compute-timeline-d3.md` | Full D3 rewrite of AI compute timeline (most complex) | **Opus** — complex D3 + data parsing | `ai-compute-timeline/output/ai_compute_timeline_interactive.html` |

## Parallelism notes
- Agents 1–5 touch **non-overlapping files** — all can run simultaneously
- Agent 2 modifies `index.html`; no other agent touches it
- Agent 1 modifies CSVs only; no other agent reads those CSVs at runtime
- Agents 4 and 5 each embed their data inline (not fetched from CSV), so Agent 1's CSV changes don't affect them — Agent 1 just keeps the source CSVs fresh for future rebuilds

## After all agents complete
1. Open `index.html` in browser — verify 6 cards, dark mode toggle works
2. Open each interactive HTML — verify dark theme consistency
3. `git add -A && git commit` with summary of all changes
4. `git push origin main` to deploy to GitHub Pages
