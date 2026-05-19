"""Tests for the browser smoke harness."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


def _load_browser_smoke():
    sys.path.insert(0, "scripts")
    import browser_smoke

    return browser_smoke


class TestBrowserSmokeTargets:
    def test_targets_are_canonical(self):
        browser_smoke = _load_browser_smoke()

        names = [target["name"] for target in browser_smoke.SMOKE_TARGETS]
        assert names == ["homepage", "dashboard", "representative-plot"]

        paths = [target["path"] for target in browser_smoke.SMOKE_TARGETS]
        assert paths == [
            "index.html",
            "dashboard/index.html",
            "ai-compute-timeline/index.html",
        ]

    def test_viewports_are_desktop_and_mobile(self):
        browser_smoke = _load_browser_smoke()

        viewport_names = [viewport["name"] for viewport in browser_smoke.SMOKE_VIEWPORTS]
        assert viewport_names == ["desktop", "mobile"]

    def test_run_smoke_checks_pass_for_repo_root(self, repo_root: Path):
        browser_smoke = _load_browser_smoke()

        results = browser_smoke.run_smoke_checks(repo_root)
        assert len(results) == 3
        assert all(result["status"] == "pass" for result in results)
        assert all(result["file_exists"] for result in results)

    def test_render_html_report_mentions_targets(self, repo_root: Path):
        browser_smoke = _load_browser_smoke()

        results = browser_smoke.run_smoke_checks(repo_root)
        html = browser_smoke.render_html_report(results, repo_root)

        assert "Browser smoke receipt" in html
        assert "homepage" in html
        assert "dashboard/index.html" in html
        assert "ai-compute-timeline/index.html" in html
        assert "PASS" in html
