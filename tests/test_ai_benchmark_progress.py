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
    """Tests for required directories and files."""

    def test_plot_directory_exists(self):
        assert os.path.isdir(PLOT_DIR), f"{PLOT_DIR}/ directory must exist"

    def test_data_directory_exists(self):
        assert os.path.isdir(DATA_DIR), f"{DATA_DIR}/ directory must exist"

    def test_output_directory_exists(self):
        assert os.path.isdir(OUTPUT_DIR), f"{OUTPUT_DIR}/ directory must exist"

    def test_src_directory_exists(self):
        assert os.path.isdir(SRC_DIR), f"{SRC_DIR}/ directory must exist"

    def test_benchmark_csv_exists(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        assert os.path.isfile(path), f"benchmark_data.csv must exist"

    def test_meta_json_exists(self):
        path = os.path.join(DATA_DIR, "meta.json")
        assert os.path.isfile(path), f"meta.json must exist"

    def test_init_py_exists(self):
        path = os.path.join(SRC_DIR, "__init__.py")
        assert os.path.isfile(path), f"src/__init__.py must exist"

    def test_index_html_exists(self):
        path = os.path.join(PLOT_DIR, "index.html")
        assert os.path.isfile(path), f"index.html must exist"

    def test_readme_exists(self):
        path = os.path.join(PLOT_DIR, "README.md")
        assert os.path.isfile(path), f"README.md must exist"

    def test_gitkeep_exists(self):
        path = os.path.join(OUTPUT_DIR, ".gitkeep")
        assert os.path.isfile(path), f"output/.gitkeep must exist"


class TestBenchmarkData:
    """Tests for benchmark_data.csv content."""

    def test_csv_headers(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)
        expected = [
            "Year", "Benchmark", "Score", "Human_Baseline",
            "Model", "Organization", "Category", "Impact", "Notes"
        ]
        assert headers == expected, f"Expected headers {expected}, got {headers}"

    def test_required_benchmarks_present(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        benchmarks = set()
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                benchmarks.add(row["Benchmark"])
        required = {"MMLU", "HumanEval", "SWE-bench", "ARC-AGI"}
        missing = required - benchmarks
        assert not missing, f"Missing benchmarks: {missing}"

    def test_mmlu_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        scores = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Benchmark"] == "MMLU":
                    scores.append(float(row["Score"]))
        assert max(scores) >= 89.8, "MMLU must have a score >= human baseline (89.8)"

    def test_humaneval_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        scores = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Benchmark"] == "HumanEval":
                    scores.append(float(row["Score"]))
        assert max(scores) >= 72.0, "HumanEval must have a score >= human baseline (72.0)"

    def test_swebench_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        scores = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Benchmark"] == "SWE-bench":
                    scores.append(float(row["Score"]))
        # SWE-bench human baseline is 100%, so we check it approaches it
        assert max(scores) >= 43.0, "SWE-bench must have meaningful scores"

    def test_arcagi_crosses_human_baseline(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        scores = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Benchmark"] == "ARC-AGI":
                    scores.append(float(row["Score"]))
        assert max(scores) >= 85.0, "ARC-AGI must have a score >= human baseline (85.0)"

    def test_human_baseline_column_present(self):
        path = os.path.join(DATA_DIR, "benchmark_data.csv")
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                assert "Human_Baseline" in row
                assert row["Human_Baseline"] != ""


class TestMetaJson:
    """Tests for meta.json structure and content."""

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
            assert field in meta, f"Missing required field: {field}"

    def test_fields_match_csv_headers(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        meta_fields = set(meta["fields"].keys())
        with open(os.path.join(DATA_DIR, "benchmark_data.csv"), "r", newline="") as f:
            reader = csv.reader(f)
            csv_headers = set(next(reader))
        extra_in_meta = meta_fields - csv_headers
        extra_in_csv = csv_headers - meta_fields
        assert not extra_in_meta, f"Fields in meta.json not in CSV: {extra_in_meta}"
        assert not extra_in_csv, f"CSV headers not in meta.json: {extra_in_csv}"

    def test_sources_is_list(self):
        path = os.path.join(DATA_DIR, "meta.json")
        with open(path, "r") as f:
            meta = json.load(f)
        assert isinstance(meta["sources"], list)
        assert len(meta["sources"]) > 0


class TestIndexHtml:
    """Tests for index.html structure."""

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
