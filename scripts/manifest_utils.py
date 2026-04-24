"""Shared helpers for the manifest-driven plots site."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "plots_manifest.json"

ALLOWED_STATUSES = {"published", "draft", "archived"}
ALLOWED_CONFIDENCE = {"high", "medium", "mixed", "speculative"}
REQUIRED_MANIFEST_FIELDS = {
    "id",
    "order",
    "status",
    "title",
    "short_title",
    "description",
    "hero_stat",
    "interactive",
    "png",
    "svg",
    "data",
    "metadata",
    "readme",
    "confidence",
}


def load_manifest(root: Path | None = None) -> list[dict]:
    """Load and sort the root plots manifest."""
    manifest_path = (root or ROOT) / "plots_manifest.json"
    with manifest_path.open("r", encoding="utf-8") as f:
        entries = json.load(f)
    return sorted(entries, key=lambda entry: entry["order"])


def published_entries(root: Path | None = None) -> list[dict]:
    """Return published manifest entries in display order."""
    return [entry for entry in load_manifest(root) if entry["status"] == "published"]


def plot_entries(root: Path | None = None, *, published_only: bool = False) -> list[dict]:
    """Return plot entries, optionally excluding drafts and archived entries."""
    entries = published_entries(root) if published_only else load_manifest(root)
    return [entry for entry in entries if entry.get("kind", "plot") == "plot"]


def entry_path(entry: dict, key: str, root: Path | None = None) -> Path:
    """Resolve a manifest path field to an absolute path."""
    return (root or ROOT) / entry[key]
