"""Tests for unified dashboard structure."""

import os

DASHBOARD_DIR = "dashboard"


class TestDashboardStructure:
    def test_dashboard_directory_exists(self):
        assert os.path.isdir(DASHBOARD_DIR)

    def test_index_html_exists(self):
        assert os.path.isfile(os.path.join(DASHBOARD_DIR, "index.html"))

    def test_dashboard_js_exists(self):
        assert os.path.isfile(os.path.join(DASHBOARD_DIR, "dashboard.js"))

    def test_dashboard_css_exists(self):
        assert os.path.isfile(os.path.join(DASHBOARD_DIR, "dashboard.css"))

    def test_index_html_links_d3(self):
        with open(os.path.join(DASHBOARD_DIR, "index.html"), "r") as f:
            content = f.read()
        assert "d3" in content.lower()

    def test_index_html_links_dashboard_js(self):
        with open(os.path.join(DASHBOARD_DIR, "index.html"), "r") as f:
            content = f.read()
        assert "dashboard.js" in content

    def test_index_html_links_dashboard_css(self):
        with open(os.path.join(DASHBOARD_DIR, "index.html"), "r") as f:
            content = f.read()
        assert "dashboard.css" in content

    def test_dashboard_js_references_csv_data(self):
        with open(os.path.join(DASHBOARD_DIR, "dashboard.js"), "r") as f:
            content = f.read()
        # Should reference at least one plot CSV
        assert ".csv" in content
