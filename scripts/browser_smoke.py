#!/usr/bin/env python3
"""Browser smoke harness for the homepage, dashboard, and one representative plot.

The script is intentionally stdlib-only so the repo has a non-UI pass/fail signal
without depending on Playwright or another browser automation runtime.

It validates the canonical smoke targets, prints a concise terminal report, and
can optionally write a self-contained HTML receipt for browser QA.
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path

from manifest_utils import ROOT

SMOKE_VIEWPORTS = [
    {"name": "desktop", "width": 1440, "height": 1200},
    {"name": "mobile", "width": 390, "height": 844},
]

SMOKE_TARGETS = [
    {
        "name": "homepage",
        "title": "Plots homepage",
        "path": "index.html",
        "checks": [
            'data-page="home"',
            "plots_manifest.json",
            "published entries",
        ],
    },
    {
        "name": "dashboard",
        "title": "Unified Dashboard",
        "path": "dashboard/index.html",
        "checks": [
            "dashboard.css",
            "dashboard.js",
            "dashboard-container",
        ],
    },
    {
        "name": "representative-plot",
        "title": "AI Compute Timeline",
        "path": "ai-compute-timeline/index.html",
        "checks": [
            "output/ai_compute_timeline_interactive.html",
            "output/ai_compute_timeline_highres.png",
            "output/ai_compute_timeline.svg",
        ],
    },
]


def _relative_url(root: Path, rel_path: str) -> str:
    return (root / rel_path).as_uri()


def evaluate_target(root: Path, target: dict) -> dict:
    path = root / target["path"]
    text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    missing = [needle for needle in target["checks"] if needle not in text]
    result = {
        "name": target["name"],
        "title": target["title"],
        "path": target["path"],
        "url": _relative_url(root, target["path"]),
        "file_exists": path.is_file(),
        "missing_checks": missing,
        "status": "pass" if path.is_file() and not missing else "fail",
        "viewports": SMOKE_VIEWPORTS,
    }
    return result


def run_smoke_checks(root: Path = ROOT) -> list[dict]:
    return [evaluate_target(root, target) for target in SMOKE_TARGETS]


def render_text_report(results: list[dict], root: Path) -> str:
    lines = [
        "Browser smoke harness",
        f"Root: {root}",
        "",
    ]
    for result in results:
        lines.append(f"[{result['status'].upper()}] {result['title']} -> {result['path']}")
        if result["missing_checks"]:
            for check in result["missing_checks"]:
                lines.append(f"  - missing: {check}")
        viewport_summary = ", ".join(
            f"{viewport['name']} {viewport['width']}x{viewport['height']}"
            for viewport in result["viewports"]
        )
        lines.append(f"  - browser viewports: {viewport_summary}")
    lines.append("")
    lines.append("Pass/fail: " + ("PASS" if all(result["status"] == "pass" for result in results) else "FAIL"))
    return "\n".join(lines)


def render_html_report(results: list[dict], root: Path) -> str:
    rows = []
    for result in results:
        missing = ", ".join(result["missing_checks"]) if result["missing_checks"] else "—"
        viewports = ", ".join(
            f"{vp['name']} {vp['width']}×{vp['height']}" for vp in result["viewports"]
        )
        rows.append(
            f"""<tr>
                <td>{escape(result['title'])}</td>
                <td><a href=\"{escape(result['url'])}\">{escape(result['path'])}</a></td>
                <td class=\"status-{escape(result['status'])}\">{escape(result['status'].upper())}</td>
                <td>{escape(viewports)}</td>
                <td>{escape(missing)}</td>
            </tr>"""
        )

    overall = "PASS" if all(result["status"] == "pass" for result in results) else "FAIL"
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Browser Smoke Receipt</title>
  <style>
    body {{ background: #0f1117; color: #e8eaf6; font-family: system-ui, sans-serif; padding: 32px; line-height: 1.5; }}
    a {{ color: #7dd3fc; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    th, td {{ border-bottom: 1px solid #2d3148; padding: 12px 10px; text-align: left; vertical-align: top; }}
    th {{ color: #cbd5e1; }}
    .status-pass {{ color: #4ade80; font-weight: 700; }}
    .status-fail {{ color: #f87171; font-weight: 700; }}
    .badge {{ display: inline-block; margin-left: 8px; padding: 2px 8px; border-radius: 999px; background: #1c1f2e; color: #cbd5e1; }}
  </style>
</head>
<body>
  <h1>Browser smoke receipt <span class=\"badge\">{overall}</span></h1>
  <p>Root: <code>{escape(str(root))}</code></p>
  <p>This receipt validates the canonical browser-smoke targets before opening them in a real browser session. Capture desktop and mobile screenshots for the three linked pages after this preflight passes.</p>
  <table>
    <thead>
      <tr><th>Target</th><th>Path</th><th>Status</th><th>Viewports</th><th>Missing checks</th></tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the browser smoke targets.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to validate.")
    parser.add_argument("--html", type=Path, help="Optional path for a browser-openable HTML receipt.")
    parser.add_argument("--json", dest="json_path", type=Path, help="Optional path for a JSON receipt.")
    args = parser.parse_args(argv)

    results = run_smoke_checks(args.root)
    ok = all(result["status"] == "pass" for result in results)

    print(render_text_report(results, args.root))

    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(render_html_report(results, args.root), encoding="utf-8")
        print(f"HTML receipt: {args.html}")

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps({"root": str(args.root), "results": results}, indent=2),
            encoding="utf-8",
        )
        print(f"JSON receipt: {args.json_path}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
