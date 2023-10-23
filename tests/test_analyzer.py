import pytest
import textwrap
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


def test_import_statement():
    script = textwrap.dedent("""
        import pymc
        from pymc import math
        import pymc as pm
        from pymc import math as pymc_math
        from pymc.math import eq
        from pymc.math import eq as equals
    """)
    expected_repost = {
        "number_of_import_statements": 2,
        "imports": ["pymc", "pymc.math"],
        "model": [],
        "distributions": [],
        "samplers": [],
        "math": [],
        "arviz": []
    }
    
    analysis_report = static_analyzer(script, source_type="string")
    assert analysis_report == expected_repost
