"""Tests for cost-to-train plot structure, data, and generators."""

import csv
import json
import os
import subprocess

PLOT_DIR = "cost-to-train"
DATA_DIR = os.path.join(PLOT_DIR, "data")
OUTPUT_DIR = os.path.join(PLOT_DIR, "output")
SRC_DIR = os.path.join(PLOT_DIR, "src")


class TestDirectoryStructure:
    def test_plot_directory_exists(self):
        assert os.path.isdir(PLOT_DIR)

    def test_data_directory_exists(self):
        assert os.path.isdir(DATA_DIR)

    def test_output_directory_exists(self):
        assert os.path.isdir(OUTPUT_DIR)

    def test_src_directory_exists(self):
        assert os.path.isdir(SRC_DIR)

    def test_training_costs_csv_exists(self):
        assert os.path.isfile(os.path.join(DATA_DIR, "training_costs.csv"))

    def test_meta_json_exists(self):
        assert os.path.isfile(os.path.join(DATA_DIR, "meta.json"))

    def test_index_html_exists(self):
        assert os.path.isfile(os.path.join(PLOT_DIR, "index.html"))


class TestTrainingCostData:
    def test_csv_headers(self):
        with open(os.path.join(DATA_DIR, "training_costs.csv"), "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
        expected = ["Year", "Model", "Organization", "Training_FLOPs", "Cost_Million_USD",
                      "Dollar_per_FLOP", "Capability_Score", "Efficiency_Gain", "Notes"]
        assert headers == expected

    def test_costs_increase_over_time(self):
        with open(os.path.join(DATA_DIR, "training_costs.csv"), "r") as f:
            reader = csv.DictReader(f)
            costs = [(int(row["Year"]), float(row["Cost_Million_USD"])) for row in reader]
        # Later years should generally have higher costs
        assert costs[-1][1] > costs[0][1]

    def test_dollar_per_flop_decreases(self):
        with open(os.path.join(DATA_DIR, "training_costs.csv"), "r") as f:
            reader = csv.DictReader(f)
            dpfs = [float(row["Dollar_per_FLOP"]) for row in reader]
        # Efficiency improves over time
        assert dpfs[-1] < dpfs[0]


class TestMetaJson:
    def test_meta_json_valid(self):
        with open(os.path.join(DATA_DIR, "meta.json"), "r") as f:
            meta = json.load(f)
        assert isinstance(meta, dict)

    def test_fields_match_csv_headers(self):
        with open(os.path.join(DATA_DIR, "meta.json"), "r") as f:
            meta = json.load(f)
        meta_fields = set(meta["fields"].keys())
        with open(os.path.join(DATA_DIR, "training_costs.csv"), "r") as f:
            reader = csv.reader(f)
            csv_headers = set(next(reader))
        assert meta_fields == csv_headers


class TestMatplotlibGenerator:
    def test_generator_script_exists(self):
        assert os.path.isfile(os.path.join(SRC_DIR, "cost_to_train.py"))

    def test_generator_runs_and_creates_outputs(self):
        result = subprocess.run(
            ["python3", "cost_to_train.py"],
            cwd=SRC_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Generator failed: {result.stderr}"
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "cost_to_train_highres.png"))
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "cost_to_train.svg"))


class TestPlotlyGenerator:
    def test_plotly_generator_script_exists(self):
        assert os.path.isfile(os.path.join(SRC_DIR, "cost_to_train_plotly.py"))

    def test_plotly_generator_runs_and_creates_output(self):
        result = subprocess.run(
            ["python3", "cost_to_train_plotly.py"],
            cwd=SRC_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"Plotly generator failed: {result.stderr}"
        assert os.path.isfile(os.path.join(OUTPUT_DIR, "cost_to_train_interactive.html"))
