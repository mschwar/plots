"""Tests for the plot validator structure and importability."""

import pytest


class TestValidatorStructure:
    """Tests that validate_all.py can be imported and has the expected structure."""

    def test_import_validate_all(self):
        """Verify validate_all can be imported as a module."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all
        assert validate_all is not None

    def test_plots_list_exists_and_is_list(self):
        """Verify PLOTS is defined and is a non-empty list."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        assert hasattr(validate_all, "PLOTS")
        assert isinstance(validate_all.PLOTS, list)
        assert len(validate_all.PLOTS) > 0

    def test_plots_entries_have_required_keys(self):
        """Verify each PLOTS entry has the required config keys."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        required_keys = {"name", "csv", "meta", "required_files"}
        for plot_config in validate_all.PLOTS:
            assert isinstance(plot_config, dict)
            assert required_keys.issubset(plot_config.keys())
            assert isinstance(plot_config["name"], str)
            assert isinstance(plot_config["csv"], str)
            assert isinstance(plot_config["meta"], str)
            assert isinstance(plot_config["required_files"], list)

    def test_validate_plot_callable(self):
        """Verify validate_plot is a callable function."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        assert hasattr(validate_all, "validate_plot")
        assert callable(validate_all.validate_plot)

    def test_validate_plot_accepts_plot_config(self):
        """Verify validate_plot accepts a plot config dict and returns (errors, warnings)."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        # Use first plot config; it may error (dir might not exist in test env) but must not raise
        plot_config = validate_all.PLOTS[0]
        errors, warnings = validate_all.validate_plot(plot_config)
        assert isinstance(errors, list)
        assert isinstance(warnings, list)

    def test_plot_names_are_unique(self):
        """Verify all plot names in PLOTS are unique."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        names = [p["name"] for p in validate_all.PLOTS]
        assert len(names) == len(set(names)), f"Duplicate plot names: {names}"

    def test_main_function_exists(self):
        """Verify main() function exists and is callable."""
        import sys
        sys.path.insert(0, "scripts")
        import validate_all

        assert hasattr(validate_all, "main")
        assert callable(validate_all.main)
