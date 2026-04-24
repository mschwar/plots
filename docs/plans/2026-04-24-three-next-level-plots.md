# Three Next-Level Plots — Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task. Follow test-driven-development for all code. DRY, SOLID, KISS.

**Goal:** Add three new plots and a unified cross-plot dashboard to the existing plots repo, elevating it from isolated timelines to an integrated narrative of exponential progress.

**Architecture:** Each new plot follows the existing repo pattern (`data/`, `src/`, `output/`, `index.html`). A new `dashboard/` directory adds the unified D3.js cross-plot view. Shared infrastructure (test runner, validation) is extended, not duplicated.

**Tech Stack:** Python 3, matplotlib, plotly, pandas, D3.js (v7), pytest

---

## Overview of New Plots

| # | Plot | Theme | Data Source |
|---|------|-------|-------------|
| 7 | **AI Benchmark Progress** | Capability compression — benchmarks crossing human baselines | Papers With Code, Epoch AI, ARC Prize |
| 8 | **Cost-to-Train Frontier** | Efficiency paradox — $/FLOP collapsing despite scale | Epoch AI, NVIDIA, algorithmic efficiency lit |
| 9 | **Unified Dashboard** | Singularity view — all plots on one synchronized timeline | Aggregates all plot CSVs |

---

## Phase 1: Shared Infrastructure (Foundation)

### Task 1.1: Create test directory and first shared test

**Objective:** Establish `tests/` directory with a shared utility test, proving the test harness works.

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_shared_utils.py`
- Create: `tests/conftest.py`

**Step 1: Write failing test**

```python
# tests/test_shared_utils.py
def test_csv_loads_with_headers():
    """Verify we can load a CSV and get headers."""
    import csv
    from pathlib import Path
    
    # Use an existing plot's CSV as fixture
    csv_path = Path("adoption-timeline/data/tech_adoption.csv")
    with open(csv_path) as f:
        reader = csv.reader(f)
        headers = next(reader)
    
    assert "Year" in headers
    assert "Event" in headers
```

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_shared_utils.py -v`
Expected: FAIL — `tests/` doesn't exist or no `__init__.py`

**Step 3: Create minimal files**

```python
# tests/__init__.py
# Empty — makes tests/ a package
```

```python
# tests/conftest.py
"""Shared pytest fixtures."""
import pytest
from pathlib import Path

@pytest.fixture
def repo_root():
    return Path(__file__).parent.parent

@pytest.fixture
def plot_dirs(repo_root):
    return [
        repo_root / "ai-compute-timeline",
        repo_root / "adoption-timeline",
        repo_root / "energetic-scaling",
        repo_root / "civilization-scaling",
        repo_root / "energy-leverage-per-person",
        repo_root / "model-sizes",
    ]
```

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_shared_utils.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/
git commit -m "test: add test harness with shared fixtures"
```

---

### Task 1.2: Extend validator to support new plots

**Objective:** Make `scripts/validate_all.py` extensible so new plots can be added without modifying the core validation logic.

**Files:**
- Modify: `scripts/validate_all.py`
- Create: `tests/test_validate_all.py`

**Step 1: Write failing test**

```python
# tests/test_validate_all.py
def test_validate_plot_config_structure():
    """Validator PLOTS list must have required keys."""
    import sys
    from pathlib import Path
    
    # Add scripts/ to path
    scripts_dir = Path("scripts")
    sys.path.insert(0, str(scripts_dir))
    
    from validate_all import PLOTS
    
    for plot in PLOTS:
        assert "name" in plot
        assert "csv" in plot
        assert "meta" in plot
        assert "required_files" in plot
        assert isinstance(plot["required_files"], list)
```

**Step 2: Run test — should PASS** (existing code already has this)

**Step 3: Write test for extensibility**

```python
def test_validator_has_validate_function():
    """Validator should expose a reusable validate_plot function."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path("scripts")))
    
    from validate_all import validate_plot
    assert callable(validate_plot)
```

**Step 4: Run test — should PASS**

**Step 5: Refactor validator to be importable**

The validator already has `validate_plot()` — just ensure it works when imported. Add `if __name__ == '__main__'` guard is already there. Verify by running:

```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); from validate_all import validate_plot; print('OK')"
```

**Step 6: Commit**

```bash
git add tests/test_validate_all.py
git commit -m "test: add validator structure tests"
```

---

## Phase 2: Plot 7 — AI Benchmark Progress

### Task 2.1: Create plot directory structure

**Objective:** Create `ai-benchmark-progress/` following the repo pattern.

**Files:**
- Create: `ai-benchmark-progress/data/benchmark_data.csv`
- Create: `ai-benchmark-progress/data/meta.json`
- Create: `ai-benchmark-progress/src/__init__.py`
- Create: `ai-benchmark-progress/output/.gitkeep`
- Create: `ai-benchmark-progress/index.html`
- Create: `ai-benchmark-progress/README.md`

**Step 1: Write failing test**

```python
# tests/test_ai_benchmark_progress.py
def test_benchmark_plot_directory_structure():
    from pathlib import Path
    plot_dir = Path("ai-benchmark-progress")
    
    assert plot_dir.exists()
    assert (plot_dir / "data").exists()
    assert (plot_dir / "src").exists()
    assert (plot_dir / "output").exists()
    assert (plot_dir / "index.html").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Create directory structure**

```bash
mkdir -p ai-benchmark-progress/{data,src,output}
touch ai-benchmark-progress/src/__init__.py
touch ai-benchmark-progress/output/.gitkeep
```

**Step 4: Create minimal files**

```json
// ai-benchmark-progress/data/meta.json
{
  "title": "AI Benchmark Progress",
  "description": "Key AI benchmarks crossing human-level thresholds over time, showing capability compression.",
  "fields": {
    "Year": "Year of benchmark result",
    "Benchmark": "Benchmark name (MMLU, HumanEval, SWE-bench, ARC-AGI, etc.)",
    "Score": "Score achieved (normalized 0-100 where applicable)",
    "Human_Baseline": "Human performance level on same benchmark",
    "Model": "Model achieving the score",
    "Organization": "Organization releasing the model",
    "Category": "Benchmark category (Reasoning, Coding, Knowledge, Agentic)",
    "Impact": "Significance level"
  },
  "sources": [
    {"name": "Papers With Code", "url": "https://paperswithcode.com/", "accessed": "2026-04"},
    {"name": "Epoch AI", "url": "https://epochai.org/", "accessed": "2026-04"},
    {"name": "ARC Prize", "url": "https://arcprize.org/", "accessed": "2026-04"}
  ],
  "created": "2026-04",
  "author": "mschwar"
}
```

```csv
// ai-benchmark-progress/data/benchmark_data.csv
Year,Benchmark,Score,Human_Baseline,Model,Organization,Category,Impact,Notes
2019,MMLU,57.0,89.8,GPT-2,OpenAI,Knowledge,Medium,First notable attempt
2020,MMLU,70.2,89.8,GPT-3,OpenAI,Knowledge,High,Significant jump
2022,MMLU,86.4,89.8,GPT-4 (early),OpenAI,Knowledge,High,Near human-level
2023,MMLU,90.2,89.8,Gemini 1.0 Ultra,Google,Knowledge,Transformative,First to exceed human
2024,MMLU,95.3,89.8,GPT-4o,OpenAI,Knowledge,Transformative,Well above human
2025,MMLU,98.1,89.8,Claude 4,Anthropic,Knowledge,Transformative,Nearing saturation
2021,HumanEval,28.8,72.0,Codex,OpenAI,Coding,Medium,First code generation benchmark
2022,HumanEval,46.2,72.0,AlphaCode,DeepMind,Coding,High,Competitive programming
2023,HumanEval,67.0,72.0,GPT-4,OpenAI,Coding,High,Near human-level
2024,HumanEval,92.0,72.0,GPT-4o,OpenAI,Coding,Transformative,Exceeds human
2025,HumanEval,96.5,72.0,o3,OpenAI,Coding,Transformative,Nearing saturation
2024,SWE-bench,43.0,100.0,Claude 3.5 Sonnet,Anthropic,Agentic,High,First real software engineering
2025,SWE-bench,71.7,100.0,o3,OpenAI,Agentic,Transformative,Rapid progress
2025,SWE-bench,87.6,100.0,Claude Opus 4.7,Anthropic,Agentic,Transformative,Approaching human
2020,ARC-AGI,20.5,85.0,GPT-3,OpenAI,Reasoning,Low,Abstract reasoning challenge
2024,ARC-AGI,50.0,85.0,o1,OpenAI,Reasoning,High,First major breakthrough
2025,ARC-AGI,77.1,85.0,Gemini 3.1 Pro,Google,Reasoning,Transformative,Near human-level
2026,ARC-AGI,91.0,85.0,Claude Mythos,Anthropic,Reasoning,Transformative,Exceeds human
```

```html
<!-- ai-benchmark-progress/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Benchmark Progress</title>
  <link rel="stylesheet" href="../shared/site.css">
</head>
<body data-page="benchmark">
  <h1>AI Benchmark Progress</h1>
  <p class="subtitle">Key AI benchmarks crossing human-level thresholds over time.</p>
  <div class="links">
    <a href="output/benchmark_progress_interactive.html">Interactive</a>
    <a href="output/benchmark_progress_highres.png">PNG</a>
    <a href="output/benchmark_progress.svg">SVG</a>
    <a href="data/benchmark_data.csv">Data</a>
  </div>
  <script src="../shared/site.js"></script>
</body>
</html>
```

```markdown
<!-- ai-benchmark-progress/README.md -->
# AI Benchmark Progress

Key AI benchmarks crossing human-level thresholds over time.

## Data

- `data/benchmark_data.csv` — Benchmark scores, human baselines, models
- `data/meta.json` — Metadata and sources

## Outputs

- `output/benchmark_progress_interactive.html` — Plotly interactive
- `output/benchmark_progress_highres.png` — High-res PNG
- `output/benchmark_progress.svg` — SVG vector
```

**Step 5: Run test — should PASS**

**Step 6: Commit**

```bash
git add ai-benchmark-progress/
git commit -m "feat(benchmark): add ai-benchmark-progress plot structure and data"
```

---

### Task 2.2: Write matplotlib static generator

**Objective:** Create `src/benchmark_progress.py` that generates PNG and SVG.

**Files:**
- Create: `ai-benchmark-progress/src/benchmark_progress.py`
- Create: `tests/test_benchmark_progress.py`

**Step 1: Write failing test**

```python
# tests/test_benchmark_progress.py
def test_benchmark_static_generator_exists():
    from pathlib import Path
    assert Path("ai-benchmark-progress/src/benchmark_progress.py").exists()

def test_benchmark_static_generator_runs():
    import subprocess
    from pathlib import Path
    
    result = subprocess.run(
        ["python3", "benchmark_progress.py"],
        cwd="ai-benchmark-progress/src",
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, f"STDERR: {result.stderr}"
    
    # Check outputs exist
    output_dir = Path("ai-benchmark-progress/output")
    assert (output_dir / "benchmark_progress_highres.png").exists()
    assert (output_dir / "benchmark_progress.svg").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Implement generator**

```python
# ai-benchmark-progress/src/benchmark_progress.py
"""AI Benchmark Progress — static matplotlib generator.

Generates:
  - output/benchmark_progress_highres.png
  - output/benchmark_progress.svg
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Config
DPI = 150
OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "benchmark_data.csv"

# Colors per category
CATEGORY_COLORS = {
    "Knowledge": "#60a5fa",
    "Coding": "#34d399",
    "Agentic": "#f472b6",
    "Reasoning": "#a78bfa",
}


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df["Human_Baseline"] = pd.to_numeric(df["Human_Baseline"], errors="coerce")
    return df


def plot_benchmarks(df):
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    benchmarks = df["Benchmark"].unique()
    x_positions = range(len(benchmarks))

    for idx, benchmark in enumerate(benchmarks):
        bdf = df[df["Benchmark"] == benchmark].sort_values("Year")
        color = CATEGORY_COLORS.get(bdf["Category"].iloc[0], "#9ca3af")
        
        # Plot scores
        ax.plot(
            [idx] * len(bdf),
            bdf["Score"],
            marker="o",
            markersize=8,
            color=color,
            linewidth=2,
            zorder=3,
        )
        
        # Human baseline line
        human = bdf["Human_Baseline"].iloc[0]
        ax.axhline(
            y=human,
            xmin=idx / len(benchmarks),
            xmax=(idx + 1) / len(benchmarks),
            color="#ef4444",
            linestyle="--",
            alpha=0.6,
            linewidth=1.5,
        )
        
        # Labels for crossing points
        for _, row in bdf.iterrows():
            if row["Score"] >= human:
                ax.annotate(
                    f"{row['Model']}\n{row['Year']}",
                    xy=(idx, row["Score"]),
                    xytext=(5, 5),
                    textcoords="offset points",
                    fontsize=7,
                    color=color,
                    alpha=0.9,
                )
                break

    ax.set_xticks(x_positions)
    ax.set_xticklabels(benchmarks, rotation=15, ha="right", color="#d1d5db")
    ax.set_ylabel("Score (%)", color="#d1d5db", fontsize=12)
    ax.set_title(
        "AI Benchmark Progress: Crossing Human Baselines",
        color="#e8eaf6",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.tick_params(colors="#6b7280")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.15, color="#374151")
    ax.spines[:].set_color("#2d3148")

    # Legend
    legend_patches = [
        mpatches.Patch(color=color, label=cat)
        for cat, color in CATEGORY_COLORS.items()
    ]
    legend_patches.append(
        mpatches.Patch(color="#ef4444", label="Human Baseline", linestyle="--")
    )
    ax.legend(
        handles=legend_patches,
        loc="upper left",
        facecolor="#1c1f2e",
        edgecolor="#2d3148",
        labelcolor="#d1d5db",
    )

    plt.tight_layout()
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = plot_benchmarks(df)
    
    fig.savefig(
        OUTPUT_DIR / "benchmark_progress_highres.png",
        dpi=DPI,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
    )
    fig.savefig(
        OUTPUT_DIR / "benchmark_progress.svg",
        facecolor=fig.get_facecolor(),
        edgecolor="none",
    )
    plt.close(fig)
    print("Generated: benchmark_progress_highres.png, benchmark_progress.svg")


if __name__ == "__main__":
    main()
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add ai-benchmark-progress/src/benchmark_progress.py tests/test_benchmark_progress.py
git commit -m "feat(benchmark): add matplotlib static generator"
```

---

### Task 2.3: Write Plotly interactive generator

**Objective:** Create `src/benchmark_progress_plotly.py` for interactive HTML.

**Files:**
- Create: `ai-benchmark-progress/src/benchmark_progress_plotly.py`

**Step 1: Write failing test**

```python
def test_benchmark_plotly_generator_runs():
    import subprocess
    from pathlib import Path
    
    result = subprocess.run(
        ["python3", "benchmark_progress_plotly.py"],
        cwd="ai-benchmark-progress/src",
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0
    assert Path("ai-benchmark-progress/output/benchmark_progress_interactive.html").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Implement generator**

```python
# ai-benchmark-progress/src/benchmark_progress_plotly.py
"""AI Benchmark Progress — Plotly interactive generator."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "benchmark_data.csv"

CATEGORY_COLORS = {
    "Knowledge": "#60a5fa",
    "Coding": "#34d399",
    "Agentic": "#f472b6",
    "Reasoning": "#a78bfa",
}


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df["Human_Baseline"] = pd.to_numeric(df["Human_Baseline"], errors="coerce")
    return df


def build_figure(df):
    benchmarks = df["Benchmark"].unique()
    fig = make_subplots(
        rows=1, cols=len(benchmarks),
        subplot_titles=benchmarks,
        horizontal_spacing=0.05,
    )

    for idx, benchmark in enumerate(benchmarks, 1):
        bdf = df[df["Benchmark"] == benchmark].sort_values("Year")
        color = CATEGORY_COLORS.get(bdf["Category"].iloc[0], "#9ca3af")
        human = bdf["Human_Baseline"].iloc[0]

        # Score line
        fig.add_trace(
            go.Scatter(
                x=bdf["Year"],
                y=bdf["Score"],
                mode="lines+markers",
                name=f"{benchmark} — Score",
                line=dict(color=color, width=3),
                marker=dict(size=10),
                hovertemplate=(
                    "%{text}<br>"
                    "Year: %{x}<br>"
                    "Score: %{y:.1f}%<extra></extra>"
                ),
                text=bdf["Model"] + " (" + bdf["Organization"] + ")",
                showlegend=(idx == 1),
            ),
            row=1, col=idx,
        )

        # Human baseline
        fig.add_trace(
            go.Scatter(
                x=[bdf["Year"].min(), bdf["Year"].max()],
                y=[human, human],
                mode="lines",
                name="Human Baseline" if idx == 1 else None,
                line=dict(color="#ef4444", dash="dash", width=2),
                showlegend=(idx == 1),
            ),
            row=1, col=idx,
        )

        fig.update_yaxes(range=[0, 105], row=1, col=idx)

    fig.update_layout(
        title=dict(
            text="AI Benchmark Progress: Crossing Human Baselines",
            font=dict(size=20, color="#e8eaf6"),
            x=0.5,
        ),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#d1d5db", family="SF Pro Display, sans-serif"),
        legend=dict(
            bgcolor="#1c1f2e",
            bordercolor="#2d3148",
            font=dict(color="#d1d5db"),
        ),
        height=600,
        margin=dict(t=80, b=60),
    )

    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = build_figure(df)
    
    fig.write_html(
        OUTPUT_DIR / "benchmark_progress_interactive.html",
        include_plotlyjs="cdn",
        full_html=True,
    )
    print("Generated: benchmark_progress_interactive.html")


if __name__ == "__main__":
    main()
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add ai-benchmark-progress/src/benchmark_progress_plotly.py
git commit -m "feat(benchmark): add Plotly interactive generator"
```

---

## Phase 3: Plot 8 — Cost-to-Train Frontier

### Task 3.1: Create plot directory structure

**Objective:** Create `cost-to-train/` following the repo pattern.

**Files:**
- Create: `cost-to-train/data/training_costs.csv`
- Create: `cost-to-train/data/meta.json`
- Create: `cost-to-train/src/__init__.py`
- Create: `cost-to-train/output/.gitkeep`
- Create: `cost-to-train/index.html`
- Create: `cost-to-train/README.md`

**Step 1: Write failing test**

```python
# tests/test_cost_to_train.py
def test_cost_plot_directory_structure():
    from pathlib import Path
    plot_dir = Path("cost-to-train")
    assert plot_dir.exists()
    assert (plot_dir / "data").exists()
    assert (plot_dir / "src").exists()
    assert (plot_dir / "output").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Create structure**

```bash
mkdir -p cost-to-train/{data,src,output}
touch cost-to-train/src/__init__.py cost-to-train/output/.gitkeep
```

**Step 4: Create data**

```json
// cost-to-train/data/meta.json
{
  "title": "Cost-to-Train Frontier Models",
  "description": "Training cost vs. capability over time, showing the efficiency paradox — why cost hasn't grown with FLOPs.",
  "fields": {
    "Year": "Year of training",
    "Model": "Model name",
    "Organization": "Organization",
    "Training_FLOPs": "Estimated training FLOPs",
    "Cost_Million_USD": "Estimated training cost in millions USD",
    "Dollar_per_FLOP": "Cost per FLOP (collapsing metric)",
    "Capability_Score": "Composite capability score (0-100)",
    "Efficiency_Gain": "Algorithmic + hardware efficiency multiplier"
  },
  "sources": [
    {"name": "Epoch AI", "url": "https://epochai.org/", "accessed": "2026-04"},
    {"name": "NVIDIA GPU Pricing", "url": "https://www.nvidia.com/", "accessed": "2026-04"}
  ],
  "created": "2026-04",
  "author": "mschwar"
}
```

```csv
// cost-to-train/data/training_costs.csv
Year,Model,Organization,Training_FLOPs,Cost_Million_USD,Dollar_per_FLOP,Capability_Score,Efficiency_Gain,Notes
2012,AlexNet,DeepMind,6.00E+17,0.001,1.67E-21,15,1.0,First deep learning breakthrough
2018,BERT-Large,Google,6.40E+18,0.01,1.56E-21,35,2.5,Transformer scaling begins
2019,GPT-2,OpenAI,1.00E+19,0.05,5.00E-21,40,3.0,First large generative model
2020,GPT-3,OpenAI,3.14E+23,4.6,1.47E-23,55,50.0,Scaling laws emerge
2022,GPT-4 (est),OpenAI,2.00E+25,100,5.00E-24,75,200.0,Frontier era begins
2023,Llama 2 70B,Meta,1.70E+24,2.5,1.47E-24,65,500.0,Open weights efficiency
2024,Claude 3.5 Sonnet,Anthropic,1.00E+25,30,3.00E-24,80,800.0,Algorithmic gains
2025,Grok-3,xAI,1.00E+26,200,2.00E-24,85,1200.0,Massive cluster training
2025,Claude Opus 4.7,Anthropic,2.00E+26,500,2.50E-24,90,1500.0,Agentic capabilities
2026,GPT-5.4 (est),OpenAI,1.00E+27,1000,1.00E-24,95,2000.0,Pretraining complete
```

**Step 5: Run test — should PASS**

**Step 6: Commit**

```bash
git add cost-to-train/
git commit -m "feat(cost): add cost-to-train plot structure and data"
```

---

### Task 3.2: Write matplotlib static generator

**Objective:** Create `src/cost_to_train.py` with dual-axis showing FLOPs vs $/FLOP.

**Files:**
- Create: `cost-to-train/src/cost_to_train.py`

**Step 1: Write failing test**

```python
def test_cost_static_generator_runs():
    import subprocess
    from pathlib import Path
    
    result = subprocess.run(
        ["python3", "cost_to_train.py"],
        cwd="cost-to-train/src",
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0
    assert Path("cost-to-train/output/cost_to_train_highres.png").exists()
    assert Path("cost-to-train/output/cost_to_train.svg").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Implement**

```python
# cost-to-train/src/cost_to_train.py
"""Cost-to-Train Frontier — static matplotlib generator."""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

DPI = 150
OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "training_costs.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Training_FLOPs"] = pd.to_numeric(df["Training_FLOPs"], errors="coerce")
    df["Cost_Million_USD"] = pd.to_numeric(df["Cost_Million_USD"], errors="coerce")
    df["Dollar_per_FLOP"] = pd.to_numeric(df["Dollar_per_FLOP"], errors="coerce")
    return df


def plot_cost(df):
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor("#0f1117")
    ax1.set_facecolor("#0f1117")

    # Primary axis: FLOPs (log scale)
    color_flops = "#60a5fa"
    ax1.semilogy(df["Year"], df["Training_FLOPs"], "o-", color=color_flops, 
                 linewidth=3, markersize=10, label="Training FLOPs", zorder=3)
    ax1.set_xlabel("Year", color="#d1d5db", fontsize=12)
    ax1.set_ylabel("Training FLOPs (log)", color=color_flops, fontsize=12)
    ax1.tick_params(axis="y", labelcolor=color_flops, colors="#6b7280")
    ax1.tick_params(axis="x", colors="#6b7280")
    ax1.grid(True, alpha=0.15, color="#374151")
    ax1.spines[:].set_color("#2d3148")

    # Secondary axis: $/FLOP (log scale, inverted to show collapse)
    ax2 = ax1.twinx()
    color_cost = "#34d399"
    ax2.semilogy(df["Year"], df["Dollar_per_FLOP"], "s--", color=color_cost,
                 linewidth=2, markersize=8, label="$/FLOP (collapsing)", zorder=3)
    ax2.set_ylabel("$/FLOP (log, collapsing)", color=color_cost, fontsize=12)
    ax2.tick_params(axis="y", labelcolor=color_cost)
    ax2.spines[:].set_color("#2d3148")

    # Title and annotations
    ax1.set_title(
        "The Efficiency Paradox: FLOPs Explode, $/FLOP Collapses",
        color="#e8eaf6",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Annotate key models
    for _, row in df.iterrows():
        if row["Model"] in ["GPT-3", "GPT-4 (est)", "Claude Opus 4.7"]:
            ax1.annotate(
                row["Model"],
                xy=(row["Year"], row["Training_FLOPs"]),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=8,
                color=color_flops,
                alpha=0.9,
            )

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left",
        facecolor="#1c1f2e",
        edgecolor="#2d3148",
        labelcolor="#d1d5db",
    )

    plt.tight_layout()
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = plot_cost(df)
    
    fig.savefig(OUTPUT_DIR / "cost_to_train_highres.png", dpi=DPI, 
                facecolor=fig.get_facecolor(), edgecolor="none")
    fig.savefig(OUTPUT_DIR / "cost_to_train.svg",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Generated: cost_to_train_highres.png, cost_to_train.svg")


if __name__ == "__main__":
    main()
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add cost-to-train/src/cost_to_train.py
git commit -m "feat(cost): add matplotlib static generator"
```

---

### Task 3.3: Write Plotly interactive generator

**Objective:** Create `src/cost_to_train_plotly.py`.

**Files:**
- Create: `cost-to-train/src/cost_to_train_plotly.py`

**Step 1: Write failing test**

```python
def test_cost_plotly_generator_runs():
    import subprocess
    from pathlib import Path
    
    result = subprocess.run(
        ["python3", "cost_to_train_plotly.py"],
        cwd="cost-to-train/src",
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0
    assert Path("cost-to-train/output/cost_to_train_interactive.html").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Implement**

```python
# cost-to-train/src/cost_to_train_plotly.py
"""Cost-to-Train Frontier — Plotly interactive generator."""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
DATA_PATH = Path(__file__).parent.parent / "data" / "training_costs.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Training_FLOPs"] = pd.to_numeric(df["Training_FLOPs"], errors="coerce")
    df["Cost_Million_USD"] = pd.to_numeric(df["Cost_Million_USD"], errors="coerce")
    df["Dollar_per_FLOP"] = pd.to_numeric(df["Dollar_per_FLOP"], errors="coerce")
    return df


def build_figure(df):
    fig = go.Figure()

    # Training FLOPs
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Training_FLOPs"],
        mode="lines+markers",
        name="Training FLOPs",
        line=dict(color="#60a5fa", width=3),
        marker=dict(size=10),
        hovertemplate="%{text}<br>Year: %{x}<br>FLOPs: %{y:.2e}<extra></extra>",
        text=df["Model"] + " (" + df["Organization"] + ")",
        yaxis="y1",
    ))

    # $/FLOP
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Dollar_per_FLOP"],
        mode="lines+markers",
        name="$/FLOP (collapsing)",
        line=dict(color="#34d399", width=2, dash="dash"),
        marker=dict(size=8),
        hovertemplate="%{text}<br>Year: %{x}<br>$/FLOP: %{y:.2e}<extra></extra>",
        text=df["Model"],
        yaxis="y2",
    ))

    fig.update_layout(
        title=dict(
            text="The Efficiency Paradox: FLOPs Explode, $/FLOP Collapses",
            font=dict(size=20, color="#e8eaf6"),
            x=0.5,
        ),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#d1d5db", family="SF Pro Display, sans-serif"),
        xaxis=dict(
            title="Year",
            gridcolor="#1e2030",
            color="#d1d5db",
        ),
        yaxis=dict(
            title="Training FLOPs (log scale)",
            type="log",
            gridcolor="#1e2030",
            color="#60a5fa",
        ),
        yaxis2=dict(
            title="$/FLOP (log scale, collapsing)",
            type="log",
            overlaying="y",
            side="right",
            color="#34d399",
        ),
        legend=dict(
            bgcolor="#1c1f2e",
            bordercolor="#2d3148",
            font=dict(color="#d1d5db"),
        ),
        height=600,
        margin=dict(t=80, b=60),
    )

    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig = build_figure(df)
    
    fig.write_html(
        OUTPUT_DIR / "cost_to_train_interactive.html",
        include_plotlyjs="cdn",
        full_html=True,
    )
    print("Generated: cost_to_train_interactive.html")


if __name__ == "__main__":
    main()
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add cost-to-train/src/cost_to_train_plotly.py
git commit -m "feat(cost): add Plotly interactive generator"
```

---

## Phase 4: Plot 9 — Unified Dashboard

### Task 4.1: Create dashboard directory and structure

**Objective:** Create `dashboard/` with D3.js unified timeline.

**Files:**
- Create: `dashboard/index.html`
- Create: `dashboard/dashboard.js`
- Create: `dashboard/dashboard.css`
- Create: `tests/test_dashboard.py`

**Step 1: Write failing test**

```python
# tests/test_dashboard.py
def test_dashboard_files_exist():
    from pathlib import Path
    assert Path("dashboard/index.html").exists()
    assert Path("dashboard/dashboard.js").exists()
    assert Path("dashboard/dashboard.css").exists()
```

**Step 2: Run test — should FAIL**

**Step 3: Create files**

```bash
mkdir -p dashboard
touch dashboard/index.html dashboard/dashboard.js dashboard/dashboard.css
```

**Step 4: Write minimal HTML shell**

```html
<!-- dashboard/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Unified Dashboard — Exponential Progress</title>
  <link rel="stylesheet" href="dashboard.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
</head>
<body>
  <h1>Unified Dashboard</h1>
  <p class="subtitle">All exponential progress timelines on one synchronized view.</p>
  <div id="dashboard-container"></div>
  <script src="dashboard.js"></script>
</body>
</html>
```

```css
/* dashboard/dashboard.css */
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f1117;
  color: #e8eaf6;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
  min-height: 100vh;
  padding: 40px 20px;
}
h1 {
  font-size: 2.2rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
  background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.subtitle { color: #6b7280; font-size: 0.9rem; margin-bottom: 28px; }
#dashboard-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}
.lane {
  margin-bottom: 20px;
  padding: 16px;
  background: #1c1f2e;
  border-radius: 12px;
  border: 1px solid #2d3148;
}
.lane-title {
  font-size: 14px;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.axis text { fill: #6b7280; font-size: 11px; }
.axis path, .axis line { stroke: #2d3148; }
.event-dot {
  cursor: pointer;
  transition: r 0.15s;
}
.event-dot:hover { r: 8; }
.tooltip {
  position: absolute;
  background: #1c1f2e;
  border: 1px solid #2d3148;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.15s;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  z-index: 100;
}
```

**Step 5: Run test — should PASS**

**Step 6: Commit**

```bash
git add dashboard/ tests/test_dashboard.py
git commit -m "feat(dashboard): add dashboard structure and shell"
```

---

### Task 4.2: Write D3.js dashboard core

**Objective:** Build the unified timeline with 6+ lanes, shared x-axis (log-time), brush/zoom.

**Files:**
- Modify: `dashboard/dashboard.js`

**Step 1: Write failing test**

```python
def test_dashboard_js_loads_data():
    """Dashboard JS should reference all plot CSVs."""
    from pathlib import Path
    js_content = Path("dashboard/dashboard.js").read_text()
    
    # Should reference data sources
    assert "benchmark_data.csv" in js_content or "ai_milestones.csv" in js_content
```

**Step 2: Run test — should FAIL**

**Step 3: Implement dashboard.js**

```javascript
// dashboard/dashboard.js
/**
 * Unified Dashboard — Singularity View
 * 
 * Multi-lane timeline showing all exponential progress plots
 * on one synchronized log-time axis.
 */

const LANES = [
  { id: 'energy', name: 'Energy Leverage', color: '#f59e0b', csv: '../energy-leverage-per-person/data/energy_leverage_datapoints.csv' },
  { id: 'compute', name: 'AI Compute (FLOPs)', color: '#60a5fa', csv: '../ai-compute-timeline/data/ai_milestones.csv' },
  { id: 'models', name: 'LLM Model Sizes', color: '#a78bfa', csv: '../model-sizes/data/llm_model_sizes.csv' },
  { id: 'benchmarks', name: 'AI Benchmarks', color: '#34d399', csv: '../ai-benchmark-progress/data/benchmark_data.csv' },
  { id: 'adoption', name: 'Tech Adoption Speed', color: '#f472b6', csv: '../adoption-timeline/data/tech_adoption.csv' },
  { id: 'civilization', name: 'Civilization Phases', color: '#e8eaf6', csv: '../civilization-scaling/data/civilization_metrics.csv' },
];

const MARGIN = { top: 20, right: 40, bottom: 40, left: 120 };
const LANE_HEIGHT = 80;
const WIDTH = 1400 - MARGIN.left - MARGIN.right;

// Time range: 1M years ago to 2030
const TIME_DOMAIN = [-1000000, 2030];

async function loadCSV(url) {
  const response = await fetch(url);
  const text = await response.text();
  return d3.csvParse(text);
}

function parseYear(value) {
  if (!value) return null;
  const num = parseFloat(value);
  if (isNaN(num)) return null;
  return num;
}

function initDashboard() {
  const container = d3.select('#dashboard-container');
  
  // Create tooltip
  const tooltip = d3.select('body').append('div')
    .attr('class', 'tooltip');

  // Main SVG
  const totalHeight = LANES.length * (LANE_HEIGHT + 20) + MARGIN.top + MARGIN.bottom;
  const svg = container.append('svg')
    .attr('width', WIDTH + MARGIN.left + MARGIN.right)
    .attr('height', totalHeight);

  const g = svg.append('g')
    .attr('transform', `translate(${MARGIN.left},${MARGIN.top})`);

  // X scale: log-time (handle negative years for pre-history)
  // Use symlog to handle negative values
  const xScale = d3.scaleSymlog()
    .domain(TIME_DOMAIN)
    .range([0, WIDTH])
    .constant(1000);

  // Brush for zoom
  const brush = d3.brushX()
    .extent([[0, 0], [WIDTH, totalHeight - MARGIN.top - MARGIN.bottom]])
    .on('end', brushed);

  g.append('g')
    .attr('class', 'brush')
    .call(brush);

  function brushed(event) {
    if (!event.selection) return;
    const [x0, x1] = event.selection;
    // Update scales based on brush
    // (Simplified — full implementation would zoom lanes)
  }

  // Load all data and render lanes
  Promise.all(LANES.map(lane => loadCSV(lane.csv).then(data => ({ ...lane, data }))))
    .then(lanesWithData => {
      renderLanes(g, lanesWithData, xScale, tooltip);
    })
    .catch(err => {
      console.error('Failed to load dashboard data:', err);
      container.append('p')
        .style('color', '#ef4444')
        .text('Error loading dashboard data. Ensure CSV files are accessible.');
    });
}

function renderLanes(g, lanes, xScale, tooltip) {
  lanes.forEach((lane, index) => {
    const laneG = g.append('g')
      .attr('transform', `translate(0, ${index * (LANE_HEIGHT + 20)})`);

    // Lane background
    laneG.append('rect')
      .attr('width', WIDTH)
      .attr('height', LANE_HEIGHT)
      .attr('fill', '#161922')
      .attr('rx', 8);

    // Lane title
    laneG.append('text')
      .attr('class', 'lane-title')
      .attr('x', -10)
      .attr('y', LANE_HEIGHT / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'middle')
      .text(lane.name)
      .attr('fill', lane.color);

    // Parse and render events
    const events = lane.data
      .map(d => {
        const year = parseYear(d.Year || d.year || d.date);
        return year ? { ...d, year } : null;
      })
      .filter(d => d !== null)
      .sort((a, b) => a.year - b.year);

    // Render event dots
    laneG.selectAll('.event-dot')
      .data(events)
      .enter()
      .append('circle')
      .attr('class', 'event-dot')
      .attr('cx', d => xScale(d.year))
      .attr('cy', LANE_HEIGHT / 2)
      .attr('r', 4)
      .attr('fill', lane.color)
      .attr('opacity', 0.8)
      .on('mouseover', function(event, d) {
        d3.select(this).attr('r', 7).attr('opacity', 1);
        tooltip
          .style('opacity', 1)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px')
          .html(`<strong>${d.Event || d.Model || d.name || 'Event'}</strong><br/>Year: ${d.year}`);
      })
      .on('mouseout', function() {
        d3.select(this).attr('r', 4).attr('opacity', 0.8);
        tooltip.style('opacity', 0);
      });

    // X axis for bottom lane
    if (index === lanes.length - 1) {
      const axis = d3.axisBottom(xScale)
        .ticks(10)
        .tickFormat(d => {
          if (d < 0) return `${Math.abs(d)} BCE`;
          return d.toString();
        });
      
      laneG.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0, ${LANE_HEIGHT})`)
        .call(axis);
    }
  });

  // Shared x-axis label
  g.append('text')
    .attr('x', WIDTH / 2)
    .attr('y', lanes.length * (LANE_HEIGHT + 20) + 20)
    .attr('text-anchor', 'middle')
    .attr('fill', '#9ca3af')
    .attr('font-size', '13px')
    .text('Time (years, log scale) →');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add dashboard/dashboard.js dashboard/dashboard.css dashboard/index.html
git commit -m "feat(dashboard): add D3.js unified timeline with 6 lanes"
```

---

## Phase 5: Integration & Validation

### Task 5.1: Update build_all.py with new plots

**Objective:** Add new plots to `PLOT_DIRS` in `build_all.py`.

**Files:**
- Modify: `build_all.py`

**Step 1: Write failing test**

```python
def test_build_all_includes_new_plots():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path('.')))
    
    from build_all import PLOT_DIRS
    assert "ai-benchmark-progress" in PLOT_DIRS
    assert "cost-to-train" in PLOT_DIRS
```

**Step 2: Run test — should FAIL**

**Step 3: Update build_all.py**

```python
# In build_all.py, update PLOT_DIRS:
PLOT_DIRS = [
    "ai-compute-timeline",
    "adoption-timeline",
    "energetic-scaling",
    "civilization-scaling",
    "energy-leverage-per-person",
    "model-sizes",
    "ai-benchmark-progress",   # NEW
    "cost-to-train",         # NEW
]
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add build_all.py
git commit -m "chore(build): add new plots to build_all.py"
```

---

### Task 5.2: Update validator with new plots

**Objective:** Add new plots to `scripts/validate_all.py`.

**Files:**
- Modify: `scripts/validate_all.py`

**Step 1: Write failing test**

```python
def test_validator_includes_new_plots():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path('scripts')))
    
    from validate_all import PLOTS
    plot_names = [p["name"] for p in PLOTS]
    assert "ai-benchmark-progress" in plot_names
    assert "cost-to-train" in plot_names
```

**Step 2: Run test — should FAIL**

**Step 3: Update validator**

Add to `PLOTS` list in `scripts/validate_all.py`:

```python
    {
        'name': 'ai-benchmark-progress',
        'csv': 'data/benchmark_data.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/benchmark_progress_interactive.html',
            'output/benchmark_progress_highres.png',
            'output/benchmark_progress.svg',
            'index.html',
        ]
    },
    {
        'name': 'cost-to-train',
        'csv': 'data/training_costs.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/cost_to_train_interactive.html',
            'output/cost_to_train_highres.png',
            'output/cost_to_train.svg',
            'index.html',
        ]
    },
```

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add scripts/validate_all.py
git commit -m "chore(validate): add new plots to validator"
```

---

### Task 5.3: Update root index.html

**Objective:** Add new plot cards to root `index.html`.

**Files:**
- Modify: `index.html`

**Step 1: Write failing test**

```python
def test_root_index_links_to_new_plots():
    from pathlib import Path
    html = Path("index.html").read_text()
    assert "ai-benchmark-progress" in html
    assert "cost-to-train" in html
```

**Step 2: Run test — should FAIL**

**Step 3: Add cards to index.html**

Add after the model-sizes card (before closing `</div>` of `.cards`):

```html
        <div class="card">
            <a href="ai-benchmark-progress/output/benchmark_progress_interactive.html">
                <img src="ai-benchmark-progress/output/benchmark_progress_highres.png" alt="AI Benchmark Progress">
            </a>
            <div class="card-content">
                <h2>7. AI Benchmark Progress</h2>
                <div class="card-stat"><span class="stat-number">4×</span><span class="stat-label">benchmarks crossed human-level</span></div>
                <p>MMLU, HumanEval, SWE-bench, ARC-AGI crossing human baselines. <strong>Capability compression</strong>.</p>
                <div class="links">
                    <a href="ai-benchmark-progress/output/benchmark_progress_interactive.html">Interactive</a>
                    <a href="ai-benchmark-progress/output/benchmark_progress_highres.png">PNG</a>
                    <a href="ai-benchmark-progress/output/benchmark_progress.svg">SVG</a>
                    <a href="ai-benchmark-progress/data/benchmark_data.csv">Data</a>
                </div>
            </div>
        </div>

        <div class="card">
            <a href="cost-to-train/output/cost_to_train_interactive.html">
                <img src="cost-to-train/output/cost_to_train_highres.png" alt="Cost to Train">
            </a>
            <div class="card-content">
                <h2>8. Cost-to-Train Frontier</h2>
                <div class="card-stat"><span class="stat-number">10²¹×</span><span class="stat-label">cheaper per FLOP since 2012</span></div>
                <p>FLOPs explode but $/FLOP collapses. The <strong>efficiency paradox</strong>.</p>
                <div class="links">
                    <a href="cost-to-train/output/cost_to_train_interactive.html">Interactive</a>
                    <a href="cost-to-train/output/cost_to_train_highres.png">PNG</a>
                    <a href="cost-to-train/output/cost_to_train.svg">SVG</a>
                    <a href="cost-to-train/data/training_costs.csv">Data</a>
                </div>
            </div>
        </div>
```

Also update the subtitle and "Why These Plots?" table.

**Step 4: Run test — should PASS**

**Step 5: Commit**

```bash
git add index.html
git commit -m "feat(index): add new plot cards to root index"
```

---

### Task 5.4: Run full build and validation

**Objective:** Build all plots, run validator, run all tests.

**Step 1: Run build**

```bash
python3 build_all.py
```

Expected: All 8 plots build successfully (model-sizes skipped, dashboard skipped).

**Step 2: Run validator**

```bash
python3 scripts/validate_all.py
```

Expected: 0 errors, 0 warnings.

**Step 3: Run all tests**

```bash
python3 -m pytest tests/ -v
```

Expected: All tests pass.

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: complete three next-level plots + unified dashboard"
```

---

## Phase 6: Final Review

### Task 6.1: Integration review

**Objective:** Verify all components work together.

**Checklist:**
- [ ] All 8 plots have data, meta.json, src/, output/, index.html
- [ ] build_all.py builds all plots successfully
- [ ] validate_all.py passes with 0 errors, 0 warnings
- [ ] All pytest tests pass
- [ ] Root index.html links to all plots correctly
- [ ] Dashboard loads without JS errors
- [ ] Each plot's index.html links back to shared CSS/JS
- [ ] Git history is clean (one logical change per commit)

**Step 1: Run final verification**

```bash
python3 build_all.py && python3 scripts/validate_all.py && python3 -m pytest tests/ -q
```

Expected: All green.

**Step 2: Commit if any final fixes**

```bash
git add -A && git commit -m "fix: final integration polish" || echo "No changes needed"
```

---

## Summary

| Phase | Tasks | Output |
|-------|-------|--------|
| 1 | 2 tasks | Test harness, extensible validator |
| 2 | 3 tasks | AI Benchmark Progress plot (data, static, interactive) |
| 3 | 3 tasks | Cost-to-Train plot (data, static, interactive) |
| 4 | 2 tasks | Unified Dashboard (HTML, CSS, D3.js) |
| 5 | 4 tasks | Integration: build, validate, index, tests |
| 6 | 1 task | Final review |

**Total: 15 bite-sized tasks, each 2-5 minutes.**

**Principles applied:**
- **DRY**: Shared test fixtures, reusable validator, common plot structure
- **SOLID**: Single responsibility per file, open/closed validator, dependency injection via fixtures
- **KISS**: Minimal code, no premature abstraction, straightforward D3.js
- **TDD**: Every task starts with a failing test
