#!/usr/bin/env python3
"""Validate manifest, plot files, data schemas, and generated site surfaces."""

from __future__ import annotations

import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from manifest_utils import (
    ALLOWED_CONFIDENCE,
    ALLOWED_STATUSES,
    REQUIRED_MANIFEST_FIELDS,
    ROOT,
    entry_path,
    load_manifest,
    plot_entries,
    published_entries,
)


PLOTS_DIR = str(ROOT)

SCHEMA_REQUIREMENTS = {
    "ai-compute-timeline": {
        "required": {
            "year",
            "event",
            "category",
            "value_numeric",
            "value_low",
            "value_high",
            "value_unit",
            "estimate_status",
            "source_id",
            "confidence",
            "display_label",
            "notes",
        },
        "numeric": {"year", "value_numeric", "value_low", "value_high"},
        "year": {"year"},
    },
    "adoption-timeline": {
        "required": {
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
        },
        "numeric": {"Year", "Days_to_Adoption"},
        "year": {"Year"},
    },
}

GENERIC_NUMERIC_PATTERNS = (
    "year",
    "years_ago",
    "metric_value",
    "days_to_adoption",
    "params_billions",
    "score",
    "baseline",
    "flops",
    "cost_million_usd",
    "dollar_per_flop",
    "capability_score",
    "efficiency_gain",
    "multiple_vs_metabolic",
    "watts",
    "energy_total",
    "energy_external",
)


class ImageAltParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        attr = dict(attrs)
        alt = attr.get("alt")
        src = attr.get("src", "(missing src)")
        if alt is None or not alt.strip():
            self.errors.append(f"Image missing alt text: {src}")


def _read_csv(path: Path) -> tuple[list[str], list[dict], list[str]]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            return reader.fieldnames or [], rows, errors
    except Exception as exc:
        return [], [], [f"CSV read error: {path.relative_to(ROOT)} - {exc}"]


def _parse_number(value: str | None) -> bool:
    if value is None or str(value).strip() == "":
        return True
    try:
        float(str(value).replace(",", ""))
        return True
    except ValueError:
        return False


def _validate_metadata(entry: dict, meta_path: Path, csv_headers: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel_meta = meta_path.relative_to(ROOT)

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"meta.json parse error: {rel_meta} - {exc}"], warnings

    for field in ("title", "description", "sources"):
        if field not in meta:
            errors.append(f"Missing meta.json field '{field}' in {entry['id']}/")

    sources = meta.get("sources", [])
    if not isinstance(sources, list) or not sources:
        errors.append(f"{entry['id']}: metadata sources must be a non-empty list")
    for source in sources:
        if not source.get("url"):
            errors.append(f"{entry['id']}: source missing url: {source.get('name', '(unnamed)')}")

    if "fields" in meta:
        meta_fields = set(meta["fields"].keys())
        csv_header_set = set(csv_headers)
        extra_in_meta = meta_fields - csv_header_set
        extra_in_csv = csv_header_set - meta_fields
        if extra_in_meta:
            warnings.append(f"{entry['id']}: meta.json fields not in CSV: {sorted(extra_in_meta)}")
        if extra_in_csv:
            warnings.append(f"{entry['id']}: CSV headers not in meta.json: {sorted(extra_in_csv)}")

    return errors, warnings


def _source_files_for(entry: dict) -> list[Path]:
    plot_dir = ROOT / entry["id"]
    sources = [entry_path(entry, "data"), entry_path(entry, "metadata")]
    src_dir = plot_dir / "src"
    if src_dir.exists():
        sources.extend(src_dir.glob("*.py"))
    return [path for path in sources if path.exists()]


def _outputs_for(entry: dict) -> list[Path]:
    keys = ["interactive", "png", "svg"]
    return [entry_path(entry, key) for key in keys if entry.get(key)]


def _validate_output_freshness(entry: dict) -> list[str]:
    warnings: list[str] = []
    outputs = _outputs_for(entry)
    sources = _source_files_for(entry)
    if not outputs or not sources:
        return warnings

    newest_source = max(path.stat().st_mtime for path in sources)
    for output in outputs:
        if output.exists() and output.stat().st_mtime < newest_source:
            warnings.append(
                f"{entry['id']}: output older than source/data: {output.relative_to(ROOT)}"
            )
    return warnings


def _numeric_columns(headers: set[str], required_config: dict | None) -> set[str]:
    numeric = set(required_config.get("numeric", set())) if required_config else set()
    for header in headers:
        normalized = header.lower()
        if any(pattern in normalized for pattern in GENERIC_NUMERIC_PATTERNS):
            numeric.add(header)
    return numeric


def _validate_csv_schema(entry: dict, headers: list[str], rows: list[dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    header_set = set(headers)
    schema = SCHEMA_REQUIREMENTS.get(entry["id"])

    if len(rows) < 2:
        errors.append(f"{entry['id']}: CSV must contain at least 2 data rows")

    if schema:
        missing = schema["required"] - header_set
        if missing:
            errors.append(f"{entry['id']}: CSV missing required columns: {sorted(missing)}")

    for column in _numeric_columns(header_set, schema):
        if column not in header_set:
            continue
        for row_num, row in enumerate(rows, start=2):
            if not _parse_number(row.get(column)):
                errors.append(f"{entry['id']}: non-numeric value in {column} at row {row_num}")
                break

    source_column = "source_id" if "source_id" in header_set else None
    status_column = "estimate_status" if "estimate_status" in header_set else None
    if source_column:
        for row_num, row in enumerate(rows, start=2):
            status = (row.get(status_column) or "").strip().lower()
            if status not in {"speculative", "projection"} and not (row.get(source_column) or "").strip():
                errors.append(f"{entry['id']}: source_id required for non-speculative row {row_num}")
                break

    return errors, warnings


def validate_manifest() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        entries = load_manifest(ROOT)
    except Exception as exc:
        return [f"Could not load plots_manifest.json: {exc}"], warnings

    seen_ids: set[str] = set()
    seen_orders: set[int] = set()
    for entry in entries:
        missing = REQUIRED_MANIFEST_FIELDS - set(entry)
        if missing:
            errors.append(f"Manifest entry missing fields: {entry.get('id', '(missing id)')} {sorted(missing)}")
        if entry.get("id") in seen_ids:
            errors.append(f"Duplicate manifest id: {entry.get('id')}")
        seen_ids.add(entry.get("id"))
        if entry.get("order") in seen_orders:
            errors.append(f"Duplicate manifest order: {entry.get('order')}")
        seen_orders.add(entry.get("order"))
        if entry.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{entry.get('id')}: invalid status {entry.get('status')}")
        if entry.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{entry.get('id')}: invalid confidence {entry.get('confidence')}")

    return errors, warnings


def validate_plot(plot_config: dict) -> tuple[list[str], list[str]]:
    """Validate a single plot manifest entry. Kept for test compatibility."""
    entry = plot_config
    errors: list[str] = []
    warnings: list[str] = []

    plot_dir = ROOT / entry["id"]
    if not plot_dir.is_dir():
        errors.append(f"Directory not found: {entry['id']}/")
        return errors, warnings

    required_files = [entry.get("interactive"), entry.get("png"), entry.get("svg"), entry.get("data"), entry.get("metadata"), entry.get("readme"), f"{entry['id']}/index.html"]
    for rel in [item for item in required_files if item]:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing: {rel}")

    csv_path = entry_path(entry, "data")
    headers, rows, csv_errors = _read_csv(csv_path)
    errors.extend(csv_errors)
    if not csv_errors:
        csv_schema_errors, csv_schema_warnings = _validate_csv_schema(entry, headers, rows)
        errors.extend(csv_schema_errors)
        warnings.extend(csv_schema_warnings)

    meta_path = entry_path(entry, "metadata")
    if meta_path.is_file() and headers:
        meta_errors, meta_warnings = _validate_metadata(entry, meta_path, headers)
        errors.extend(meta_errors)
        warnings.extend(meta_warnings)

    index_path = plot_dir / "index.html"
    if index_path.exists():
        parser = ImageAltParser()
        parser.feed(index_path.read_text(encoding="utf-8"))
        errors.extend(f"{entry['id']}: {err}" for err in parser.errors)

    warnings.extend(_validate_output_freshness(entry))
    return errors, warnings


def validate_homepage_and_readme() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    published = published_entries(ROOT)
    published_count = len(published)

    index_path = ROOT / "index.html"
    readme_path = ROOT / "README.md"
    index_html = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    match = re.search(r'data-published-count="(\d+)"', index_html)
    if not match:
        errors.append("Homepage missing data-published-count marker")
    elif int(match.group(1)) != published_count:
        errors.append(f"Homepage count {match.group(1)} does not match published manifest count {published_count}")

    for entry in published:
        if entry["title"] not in index_html:
            errors.append(f"Homepage missing published entry title: {entry['title']}")
        if entry["title"] not in readme:
            errors.append(f"README missing published entry title: {entry['title']}")

    parser = ImageAltParser()
    parser.feed(index_html)
    errors.extend(f"Homepage: {err}" for err in parser.errors)
    return errors, warnings


PLOTS = [
    {
        "name": entry["id"],
        "csv": str(Path(entry["data"]).relative_to(entry["id"])),
        "meta": str(Path(entry["metadata"]).relative_to(entry["id"])),
        "required_files": [
            str(Path(path).relative_to(entry["id"]))
            for path in (entry["interactive"], entry["png"], entry["svg"], f"{entry['id']}/index.html")
            if path
        ],
        **entry,
    }
    for entry in plot_entries(ROOT, published_only=True)
]


def main() -> None:
    print("=" * 60)
    print("Plots Validation")
    print("=" * 60)

    all_errors: list[str] = []
    all_warnings: list[str] = []

    manifest_errors, manifest_warnings = validate_manifest()
    all_errors.extend(manifest_errors)
    all_warnings.extend(manifest_warnings)
    print("\nValidating: plots_manifest.json")
    if manifest_errors or manifest_warnings:
        for error in manifest_errors:
            print(f"  ERROR: {error}")
        for warning in manifest_warnings:
            print(f"  WARN:  {warning}")
    else:
        print("  OK")

    for entry in plot_entries(ROOT, published_only=True):
        print(f"\nValidating: {entry['id']}/")
        errors, warnings = validate_plot(entry)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        if errors:
            for error in errors:
                print(f"  ERROR: {error}")
        if warnings:
            for warning in warnings:
                print(f"  WARN:  {warning}")
        if not errors and not warnings:
            print("  OK")

    print("\nValidating: homepage and README")
    errors, warnings = validate_homepage_and_readme()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    if errors:
        for error in errors:
            print(f"  ERROR: {error}")
    if warnings:
        for warning in warnings:
            print(f"  WARN:  {warning}")
    if not errors and not warnings:
        print("  OK")

    print("\n" + "=" * 60)
    print(f"Summary: {len(all_errors)} errors, {len(all_warnings)} warnings")
    print("=" * 60)

    if all_errors:
        sys.exit(1)
    print("\nAll validations passed!")
    sys.exit(0)


if __name__ == "__main__":
    main()
