# Agent 1 — Data Freshness (CSV Updates)

## Goal
Update three CSV data files in `/Users/mschwar/plots` to include 2026 frontier AI models. No code changes — only data files.

## Working directory
`/Users/mschwar/plots`

## Context
This is a repo of 6 interactive data visualizations. Three plots have CSV data that needs to be updated with models released in 2025–2026. Today is April 16, 2026.

---

## Task 1A: `ai-compute-timeline/data/ai_milestones.csv`

Read `/Users/mschwar/plots/ai-compute-timeline/data/ai_milestones.csv` first.

The CSV has columns: `Year,Event,Category,Compute_FLOPs,Parameters,Impact`

**Add these rows** (insert in year order — rows are roughly chronological):

```
2025,LLaMA 4 Scout (Meta) - 109B MoE open-weights model,Model Release,4e25 (est.),109B total / 17B active,High
2026,Gemini 3.1 Pro (Google) - 77.1% ARC-AGI-2; 2× prior gen; 1M context,Model Release,Speculative 1e26-5e26,N/A (est. ~2T),Transformative
2026,GPT-5.4 (OpenAI) - Released Mar 5 2026; native multimodal; 1M context,Model Release,Speculative 1e26,N/A (est. ~600B),High
2026,Claude Opus 4.7 (Anthropic) - 87.6% SWE-bench Verified; released Apr 16 2026,Reasoning/Agentic,Speculative 1e26,N/A (est. ~800B),Transformative
2026,Claude Mythos Preview (Anthropic) - Invite-only; 73% expert cyber tasks; inflection point,Reasoning/Agentic,Speculative 2e26+,N/A (est. ~3T),Speculative Transformative
2026,GPT Spud / GPT-5.5 (OpenAI) - Pretraining complete Mar 24 2026; in safety eval; ~5-6T MoE,Model Release,Speculative 5e27+,N/A (est. ~5T),Speculative Transformative
```

Also **update** the existing 2026 rows that are speculative/generic to be more specific. The existing rows for 2026 say things like "Agentic AI & recursive self-improvement loops emerge at scale" — leave those, just add the new model-specific rows.

Update the note at the bottom of the existing `note_text` string in the Python source? No — that's in `src/`, not the CSV. Just update the CSV.

---

## Task 1B: `adoption-timeline/data/tech_adoption.csv`

Read `/Users/mschwar/plots/adoption-timeline/data/tech_adoption.csv` first.

The CSV has columns: `Year,Event,Category,Days_to_Adoption,Impact`

**Context:** Days_to_Adoption = approximate days for the technology to reach ~50M users.

**Add these rows** (in year order):

```
2026,GPT-5.4 (OpenAI) public release,AI/Agentic,21,Transformative
2026,Gemini 3.1 Pro public preview (Google),AI/Agentic,30,High
2026,Claude Opus 4.7 (Anthropic) — released Apr 16 2026,AI/Agentic,21,High
```

Also update the existing 2025 row "Agentic AI tools scale (Devin-like)" — change `Days_to_Adoption` from 30 to 21 (adoption is accelerating faster than the original projection) and note this in a comment if the CSV format supports it (it doesn't — just change the number).

---

## Task 1C: `energetic-scaling/data/ai_model_data.csv`

Read `/Users/mschwar/plots/energetic-scaling/data/ai_model_data.csv` first to understand column schema before adding anything.

Add recent frontier models (2025-2026) following the existing schema exactly. If there's a cost_per_megaflop or efficiency column, use estimates from industry pricing: GPT-5.4 costs $2.50/1M input tokens, Opus 4.7 costs $5/1M input tokens, Gemini 3.1 Pro costs $2/1M input tokens.

---

## Constraints
- Do NOT modify any Python `.py` files
- Do NOT modify any `.html` files
- Do NOT modify `meta.json` files — those are updated manually
- Make sure CSV rows have the exact same number of commas/columns as existing rows
- Preserve the existing row order (append new rows at the bottom or insert in year order — whatever the existing file uses)

## Done when
All three CSVs have been read, updated with new rows, and saved. Report back: how many rows were added to each file.
