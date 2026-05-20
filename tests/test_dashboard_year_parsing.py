"""Regression tests for dashboard year parsing."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

DASHBOARD_JS = Path("dashboard/dashboard.js")


def _extract_function(source: str, signature: str) -> str:
    start = source.index(signature)
    brace_depth = 0
    end = None

    for index in range(start, len(source)):
        char = source[index]
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
            if brace_depth == 0:
                end = index + 1
                break

    assert end is not None, f"Could not extract function for {signature}"
    return source[start:end]


def test_parse_year_preserves_zero_and_full_year_values():
    """Regression: ISSUE-PR3 — parseYear treated 0 as falsy and truncated long years.

    Found by /qa on 2026-05-20
    Report: .gstack/qa-reports/qa-report-plots-2026-05-20.md
    """

    source = DASHBOARD_JS.read_text()
    parse_year = _extract_function(source, "function parseYear(row) {")

    cases = [
        {"row": {"year": 0}, "expected": 0},
        {"row": {"Year": 12345}, "expected": 12345},
        {"row": {"date": "2024-01-01"}, "expected": 2024},
        {"row": {"Years_Ago": 2}, "expected": 2024},
        {"row": {"year": ""}, "expected": None},
    ]

    script = "\n".join(
        [
            parse_year,
            f"const cases = {json.dumps([case['row'] for case in cases])};",
            "const results = cases.map((row) => parseYear(row));",
            "process.stdout.write(JSON.stringify(results));",
        ]
    )

    completed = subprocess.run(
        ["node", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(completed.stdout) == [case["expected"] for case in cases]
