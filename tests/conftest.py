"""Shared pytest fixtures for the plots test suite."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Return the repository root directory."""
    # This file lives at tests/conftest.py, so parent is repo root
    return Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def plot_dirs(repo_root: Path) -> dict[str, Path]:
    """Return a mapping of plot names to their directory paths."""
    plots = [
        "ai-compute-timeline",
        "adoption-timeline",
        "energetic-scaling",
        "civilization-scaling",
        "energy-leverage-per-person",
        "model-sizes",
    ]
    return {name: repo_root / name for name in plots}
