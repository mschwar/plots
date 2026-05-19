#!/usr/bin/env python3
"""Repository-level validation for the plots atlas."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

for path in (ROOT, SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import build_all  # noqa: E402
import validate_all  # noqa: E402


REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "CURRENT_STATE.md",
    "LICENSE",
    "plots_manifest.json",
    "build_all.py",
    "requirements.txt",
    "scripts/browser_smoke.py",
    "scripts/validate_repo.py",
    "docs/agentic-overhaul/2026-05-audit.md",
    ".github/workflows/validate.yml",
]

REQUIRED_DIRECTORIES = [
    "scripts",
    "docs",
    "docs/agentic-overhaul",
    ".github",
    ".github/workflows",
]


def _check_repo_surface() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for rel in REQUIRED_DIRECTORIES:
        if not (ROOT / rel).is_dir():
            errors.append(f"Missing required directory: {rel}")

    if not callable(getattr(build_all, "main", None)):
        errors.append("build_all.py does not expose a callable main()")

    return errors, warnings


def _promote_freshness_warnings(warnings: list[str]) -> tuple[list[str], list[str]]:
    promoted: list[str] = []
    retained: list[str] = []
    for warning in warnings:
        if "output older than source/data" in warning:
            promoted.append(warning)
        else:
            retained.append(warning)
    return promoted, retained


def run_validation(*, check: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    surface_errors, surface_warnings = _check_repo_surface()
    errors.extend(surface_errors)
    warnings.extend(surface_warnings)

    manifest_errors, manifest_warnings = validate_all.validate_manifest()
    errors.extend(manifest_errors)
    warnings.extend(manifest_warnings)

    for entry in validate_all.plot_entries(ROOT, published_only=True):
        plot_errors, plot_warnings = validate_all.validate_plot(entry)
        if check:
            freshness_errors, plot_warnings = _promote_freshness_warnings(plot_warnings)
            errors.extend(freshness_errors)
        errors.extend(plot_errors)
        warnings.extend(plot_warnings)

    homepage_errors, homepage_warnings = validate_all.validate_homepage_and_readme()
    errors.extend(homepage_errors)
    warnings.extend(homepage_warnings)

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the plots repository.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail on stale generated outputs instead of only warning.",
    )
    args = parser.parse_args(argv)

    print("=" * 60)
    print("Repository Validation")
    print("=" * 60)

    errors, warnings = run_validation(check=args.check)

    if errors or warnings:
        print("\nRepository surface, manifest, plots, homepage, and README")
        if errors:
            for error in errors:
                print(f"  ERROR: {error}")
        if warnings:
            for warning in warnings:
                print(f"  WARN:  {warning}")
    else:
        print("\nRepository surface, manifest, plots, homepage, and README")
        print("  OK")

    print("\n" + "=" * 60)
    print(f"Summary: {len(errors)} errors, {len(warnings)} warnings")
    print("=" * 60)

    if errors:
        return 1

    print("\nRepository validation passed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
