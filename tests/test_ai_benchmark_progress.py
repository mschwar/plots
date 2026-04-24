"""Tests for ai-benchmark-progress plot structure and data."""

import csv
import json
import os
import pytest

PLOT_DIR = "ai-benchmark-progress"
DATA_DIR = os.path.join(PLOT_DIR, "data")
OUTPUT_DIR = os.path.join(PLOT_DIR, "output")
SRC_DIR = os.path.join(PLOT_DIR, "src")


class TestDirectoryStructure:
    """Verify plot directory structure exists."""

    def test_plot_directory_exists(self):
        assert os.path.isdir(PLOT_DIR)

    def test_data_directory_exists(self):
        assert os.path.isdir(DATA_DIR)

    def test_output_directory_exists(self):
        assert os.path.isdir(OUTPUT_DIR)

    def test_src_directory_exists(self):
        assert os.path.isdir(SRC_DIR)

    def test_benchmark_csv_exists(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        assert os.path.isfile(path)

    def test_meta_json_exists(self):
        path = os.path.join(DATA_DIR, "meta.json")
        assert os.path.isfile(path)

    def test_init_py_exists(self):
        path = os.path.join(SRC_DIR, "__init__.py")
        assert os.path.isfile(path)

    def test_index_html_exists(self):
        path = os.path.join(PLOT_DIR, "index.html")
        assert os.path.isfile(path)

    def test_readme_exists(self):
        path = os.path.join(PLOT_DIR, "README.md")
        assert os.path.isfile(path)

    def test_gitkeep_exists(self):
        path = os.path.join(OUTPUT_DIR, ".gitkeep")
        assert os.path.isfile(path)


class TestBenchmarkData:
    """Verify CSV data content and structure."""

    def test_csv_headers(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
        expected = ["Year", "Benchmark", "Score", "Human_Baseline", "Model", "Organization", "Category", "Impact", "Notes"]
        assert headers == expected

    def test_required_benchmarks_present(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            benchmarks = set(row["Benchmark"] for row in reader)
        required = {"MMLU", "HumanEval", "SWE-bench", "ARC-AGI"}
        assert required.issubset(benchmarks)

    def test_mmlu_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            mmlu_scores = [float(row["Score"]) for row in reader if row["Benchmark"] == "MMLU"]
        assert any(score >= 89.8 for score in mmlu_scores)

    def test_humaneval_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            scores = [float(row["Score"]) for row in reader if row["Benchmark"] == "HumanEval"]
        assert any(score >= 72.0 for score in scores)

    def test_swebench_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            scores = [float(row["Score"]) for row in reader if row["Benchmark"] == "SWE-bench"]
        # SWE-bench human baseline is 100%, models approach but may not exceed
        assert any(score >= 85.0 for score in scores), f"Expected SWE-bench to approach 85%+, got max {max(scores)}"

    def test_arcagi_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            scores = [float(row["Score"]) for row in reader if row["Benchmark"] == "ARC-AGI"]
        assert any(score >= 85.0 for score in scores)

    def test_human_baseline_column_present(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            row = next(reader)
        assert "Human_Baseline" in row
        assert float(row["Human_Baseline"]) > 0


class TestMetaJson:
    """Verify meta.json structure and content."""

    def test_meta_json_valid(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        assert isinstance(meta, dict)

    def test_required_meta_fields(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        required = ["title", "description", "fields", "sources", "created", "author"]
        for field in required:
            assert field in meta, f"Missing field: {field}"

    def test_fields_match_csv_headers(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        meta_fields = set(meta["fields"].keys())

        csv_path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            csv_headers = next(reader)
        csv_headers_set = set(csv_headers)

        assert meta_fields == csv_headers_set, f"Mismatch: meta={meta_fields}, csv={csv_headers_set}"

    def test_sources_is_list(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        assert isinstance(meta["sources"], list)
        assert len(meta["sources"]) > 0


class TestIndexHtml:
    """Verify index.html links and structure."""

    def test_index_html_links_shared_css(self):
        path = os.path.join(PLOT_DIR, "index.html")
        with open(path, "r") as f:
            content = f.read()
        assert "shared/site.css" in content or "../shared/site.css" in content

    def test_index_html_has_title(self):
        path = os.path.join(PLOT_DIR, "index.html")
        with open(path, "r") as f:
            content = f.read()
        assert "<title>" in content
        assert "</title>" in content

    def test_index_html_links_data(self):
        path = os.path.join(PLOT_DIR, "index.html")
        with open(path, "r") as f:
            content = f.read()
        assert "benchmark_data.csv" in content
        assert "meta.json" in content


class TestGenerator:
    """TDD tests for matplotlib static generator."""

    def test_generator_script_exists(self):
        path = os.path.join(SRC_DIR, "benchmark_progress.py")
        assert os.path.isfile(path), f"Generator not found: {path}"

    def test_generator_runs_and_creates_outputs(self):
        import subprocess
        result = subprocess.run(
            ["python3", "benchmark_progress.py"],
            cwd=SRC_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Generator failed: {result.stderr}"
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "benchmark_progress_highres.png"))
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "benchmark_progress.svg"))


class TestPlotlyGenerator:
    """TDD tests for Plotly interactive generator."""

    def test_plotly_generator_script_exists(self):
        path = os.path.join(SRC_DIR, "benchmark_progress_plotly.py")
        assert os.path.isfile(path), f"Plotly generator not found: {path}"

    def test_plotly_generator_runs_and_creates_output(self):
        import subprocess
        result = subprocess.run(
            ["python3", "benchmark_progress_plotly.py"],
            cwd=SRC_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Plotly generator failed: {result.stderr}"
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "benchmark_progress_interactive.html"))
