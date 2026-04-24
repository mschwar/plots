#!/usr/bin/env python3
"""
Validate all plots: check meta.json fields match CSV headers, required files exist.
"""

import os
import json
import csv
import sys

PLOTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLOTS = [
    {
        'name': 'ai-compute-timeline',
        'csv': 'data/ai_milestones.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/ai_compute_timeline_interactive.html',
            'output/ai_compute_timeline_highres.png',
            'output/ai_compute_timeline.svg',
            'index.html',
        ]
    },
    {
        'name': 'adoption-timeline',
        'csv': 'data/tech_adoption.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/adoption_timeline_interactive.html',
            'output/adoption_timeline_highres.png',
            'output/adoption_timeline.svg',
            'index.html',
        ]
    },
    {
        'name': 'energetic-scaling',
        'csv': 'data/scaling_data.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/energetic_scaling_interactive.html',
            'output/energetic_scaling_highres.png',
            'output/energetic_scaling.svg',
            'index.html',
        ]
    },
    {
        'name': 'civilization-scaling',
        'csv': 'data/civilization_metrics.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/civilization_scaling_interactive.html',
            'output/civilization_scaling_highres.png',
            'output/civilization_scaling.svg',
            'index.html',
        ]
    },
    {
        'name': 'energy-leverage-per-person',
        'csv': 'data/energy_leverage_datapoints.csv',
        'meta': 'data/meta.json',
        'required_files': [
            'output/energy_leverage_interactive.html',
            'output/energy_leverage_highres.png',
            'output/energy_leverage.svg',
            'index.html',
        ]
    },
]


def validate_plot(plot_config):
    """Validate a single plot directory."""
    name = plot_config['name']
    plot_dir = os.path.join(PLOTS_DIR, name)
    errors = []
    warnings = []

    # Check directory exists
    if not os.path.isdir(plot_dir):
        errors.append(f"Directory not found: {name}/")
        return errors, warnings

    # Check required files
    for req_file in plot_config['required_files']:
        file_path = os.path.join(plot_dir, req_file)
        if not os.path.isfile(file_path):
            errors.append(f"Missing: {name}/{req_file}")

    # Check CSV exists
    csv_path = os.path.join(plot_dir, plot_config['csv'])
    if not os.path.isfile(csv_path):
        errors.append(f"Missing CSV: {name}/{plot_config['csv']}")
        return errors, warnings

    # Check meta.json exists
    meta_path = os.path.join(plot_dir, plot_config['meta'])
    if not os.path.isfile(meta_path):
        errors.append(f"Missing meta.json: {name}/{plot_config['meta']}")
        return errors, warnings

    # Load CSV headers
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            csv_headers = next(reader)
    except Exception as e:
        errors.append(f"CSV read error: {name}/{plot_config['csv']} - {e}")
        return errors, warnings

    # Load meta.json
    try:
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    except Exception as e:
        errors.append(f"meta.json parse error: {name}/{plot_config['meta']} - {e}")
        return errors, warnings

    # Check required meta.json fields
    required_meta_fields = ['title', 'description', 'sources']
    for field in required_meta_fields:
        if field not in meta:
            errors.append(f"Missing meta.json field '{field}' in {name}/")

    # Check fields vs CSV headers (if 'fields' exists in meta)
    if 'fields' in meta:
        meta_fields = set(meta['fields'].keys())
        csv_header_set = set(csv_headers)

        # Fields in meta but not in CSV
        extra_in_meta = meta_fields - csv_header_set
        if extra_in_meta:
            warnings.append(f"{name}: meta.json fields not in CSV: {extra_in_meta}")

        # Fields in CSV but not in meta (just a warning)
        extra_in_csv = csv_header_set - meta_fields
        if extra_in_csv:
            warnings.append(f"{name}: CSV headers not in meta.json: {extra_in_csv}")

    return errors, warnings


def main():
    print("=" * 60)
    print("Plots Validation")
    print("=" * 60)

    all_errors = []
    all_warnings = []

    for plot_config in PLOTS:
        name = plot_config['name']
        print(f"\nValidating: {name}/")
        errors, warnings = validate_plot(plot_config)

        if errors:
            all_errors.extend(errors)
            for e in errors:
                print(f"  ERROR: {e}")
        if warnings:
            all_warnings.extend(warnings)
            for w in warnings:
                print(f"  WARN:  {w}")
        if not errors and not warnings:
            print(f"  OK")

    print("\n" + "=" * 60)
    print(f"Summary: {len(all_errors)} errors, {len(all_warnings)} warnings")
    print("=" * 60)

    if all_errors:
        sys.exit(1)
    else:
        print("\nAll validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
