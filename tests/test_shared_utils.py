"""Test shared utilities and data consistency across plots."""

import csv
from pathlib import Path

import pytest


class TestAdoptionTimelineData:
    """Tests for adoption-timeline plot data."""

    def test_csv_headers(self, repo_root):
        """Verify adoption-timeline CSV has expected headers."""
        csv_path = repo_root / "adoption-timeline" / "data" / "tech_adoption.csv"
        assert csv_path.exists(), f"CSV not found: {csv_path}"

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

        expected_required = {
            "Year",
            "Event",
            "Category",
            "Days_to_Adoption",
            "Impact",
            "adoption_metric_type",
            "comparability_level",
            "source_id",
            "confidence",
            "comparability_notes",
            "notes",
        }
        assert expected_required.issubset(set(headers)), f"Unexpected headers: {headers}"
