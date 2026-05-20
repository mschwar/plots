"""Tests for unified dashboard structure."""

from pathlib import Path

DASHBOARD_DIR = Path("dashboard")


class TestDashboardStructure:
    def test_dashboard_directory_exists(self):
        assert DASHBOARD_DIR.is_dir()

    def test_index_html_exists(self):
        assert (DASHBOARD_DIR / "index.html").is_file()

    def test_dashboard_js_exists(self):
        assert (DASHBOARD_DIR / "dashboard.js").is_file()

    def test_dashboard_css_exists(self):
        assert (DASHBOARD_DIR / "dashboard.css").is_file()

    def test_index_html_uses_only_local_assets(self):
        content = (DASHBOARD_DIR / "index.html").read_text()
        lowered = content.lower()
        assert "https://" not in lowered
        assert "http://" not in lowered
        assert "dashboard.js" in content
        assert "dashboard.css" in content
        assert "offline-safe" in lowered

    def test_dashboard_js_references_csv_data(self):
        content = (DASHBOARD_DIR / "dashboard.js").read_text()
        # Should reference the manifest and local CSV loading path.
        assert "plots_manifest.json" in content
        assert "loadCSV" in content
        assert "../" in content
