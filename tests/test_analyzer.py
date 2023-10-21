import pytest
from pymc_workflow_analyzer.analyzer import static_analyzer

def test_analyze_script():
    script_path = 'sample_model.py'
    expected_repost = {
        "number_of_import_statements": 6,
        "imports": ["arviz", "matplotlib.pyplot", "numpy", "pandas", "pymc", "xarray"],
        "model": [{"name": "Model", "args": [], "kwargs": []}],
        "distributions": [
                {"name": "HalfCauchy", "args": ["sigma"], "kwargs": ["beta"]},
                {"name": "Normal", "args": ["Intercept", 0], "kwargs": ["sigma"]},
                {"name": "Normal", "args": ["slope", 0], "kwargs": ["sigma"]},
                {"name": "Normal", "args": ["y"], "kwargs": ["mu", "sigma", "observed"]}
        ],
        "samplers": [{"name": "sample", "args": [3000], "kwargs": []}],
        "math": [],
        "arviz": [{"name": "plot_trace", "args": ["idata"], "kwargs": ["figsize"]}]
    }
    analysis_report = static_analyzer(script_path)
    assert analysis_report == expected_repost
