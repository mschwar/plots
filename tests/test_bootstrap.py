"""Smoke tests for repo bootstrap entrypoints."""

import sys


def test_build_all_importable():
    import build_all

    assert callable(build_all.main)


def test_validate_repo_importable():
    sys.path.insert(0, "scripts")
    import validate_repo

    assert callable(validate_repo.main)
