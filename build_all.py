#!/usr/bin/env python3
"""
Build All Plots
Regenerates all static and interactive visualizations from source.
"""

import os
import sys
import subprocess
from pathlib import Path

# Plot directories (order matters for dependencies)
PLOT_DIRS = [
    "ai-compute-timeline",
    "adoption-timeline",
    "energetic-scaling",
    "civilization-scaling",
    "energy-leverage-per-person",
]


def run_script(script_path: Path, plot_name: str) -> bool:
    """Run a Python script with proper working directory."""
    script_name = script_path.name
    src_dir = script_path.parent

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=src_dir,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return True
        else:
            print(f"    STDERR: {result.stderr[:200]}" if result.stderr else "")
            return False

    except subprocess.TimeoutExpired:
        print(f"    Timeout after 120s")
        return False
    except Exception as e:
        print(f"    Error: {e}")
        return False


def build_plot(plot_dir: Path) -> tuple[int, int]:
    """Build all scripts in a plot's src/ directory."""
    src_dir = plot_dir / "src"
    if not src_dir.exists():
        return 0, 0

    scripts = sorted(src_dir.glob("*.py"))
    success = 0
    failed = 0

    for script in scripts:
        script_name = script.name
        result = run_script(script, plot_dir.name)

        if result:
            print(f"  {script_name}: OK")
            success += 1
        else:
            print(f"  {script_name}: FAIL")
            failed += 1

    return success, failed


def main():
    print("=" * 60)
    print("Building All Plots")
    print("=" * 60)

    root = Path(__file__).parent
    total_success = 0
    total_failed = 0

    for plot_name in PLOT_DIRS:
        plot_dir = root / plot_name

        if not plot_dir.exists():
            print(f"\n{plot_name}/: NOT FOUND")
            continue

        src_dir = plot_dir / "src"
        if not src_dir.exists():
            print(f"\n{plot_name}/: no src/ directory")
            continue

        print(f"\n{plot_name}/")
        success, failed = build_plot(plot_dir)
        total_success += success
        total_failed += failed

    print("\n" + "=" * 60)
    print(f"Summary: {total_success} succeeded, {total_failed} failed")
    print("=" * 60)

    if total_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
