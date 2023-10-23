import pytest
import textwrap
from pymc_workflow_analyzer.analyzer import static_analyzer

def test_analyze_script():
    script_path = 'sample_model.py'
    expected_repost = {
        "number_of_import_statements": 6,
        "imports": ["arviz", "matplotlib.pyplot", "numpy", "pandas", "pymc", "xarray"],
        "model": [{"name": "Model", "args": 0, "kwargs": []}],
        "distributions": [
                {"name": "HalfCauchy", "args": 1, "kwargs": ["beta"]},
                {"name": "Normal", "args": 2, "kwargs": ["sigma"]},
                {"name": "Normal", "args": 2, "kwargs": ["sigma"]},
                {"name": "Normal", "args": 1, "kwargs": ["mu", "sigma", "observed"]}
        ],
        "samplers": [{"name": "sample", "args": 1, "kwargs": []}],
        "math": [],
        "arviz": [{"name": "plot_trace", "args": 1, "kwargs": ["figsize"]}],
        "pymc_experimental": []
    }
    analysis_report = static_analyzer(script_path, source_type="file")
    assert analysis_report == expected_repost


def test_import_statement():
    script = textwrap.dedent("""
        import pymc
        import pymc as pm
        from pymc import math
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
        "arviz": [],
        "pymc_experimental": []
    }
    
    analysis_report = static_analyzer(script, source_type="code")
    assert analysis_report == expected_repost


def test_function_calls():
    script = textwrap.dedent("""
        import pymc
        import pymc as pm
        from pymc import math
        from pymc import math as pymc_math
        from pymc.math import eq
        from pymc.math import eq as equals

        result = pymc.math.eq(1, 1)
        result = pm.math.eq(2, 2)
        result = math.eq(3, 3)
        result = pymc_math.eq(4, 4)
        result = eq(5, 5)
        result = equals(6, 6)
    """)
    expected_repost = {
        "number_of_import_statements": 2,
        "imports": ["pymc", "pymc.math"],
        "model": [],
        "distributions": [],
        "samplers": [],
        "math": [
                {"name": "eq", "args": 2, "kwargs": []},
                {"name": "eq", "args": 2, "kwargs": []},
                {"name": "eq", "args": 2, "kwargs": []},
                {"name": "eq", "args": 2, "kwargs": []},
                {"name": "eq", "args": 2, "kwargs": []},
                {"name": "eq", "args": 2, "kwargs": []}
        ],
        "arviz": [],
        "pymc_experimental": []
    }
    
    analysis_report = static_analyzer(script, source_type="code")
    assert analysis_report == expected_repost
