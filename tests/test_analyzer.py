import pytest
from pymc_workflow_analyzer.analyzer import static_analyze
from pymc_workflow_analyzer.report import static_report_generator, save_report

def test_analyze_script():
    script_path = 'sample_model.py'
    expected_result = {
        'imports': ['arviz', 'matplotlib.pyplot', 'numpy', 'pandas', 'pymc', 'xarray'], 
        'distributions': ['HalfCauchy', 'Normal'],
        'samplers': [{'name': 'sample', 'args': ['Constant(value=3000)'], 'keywords': []}]
    }
    
    result = static_analyze(script_path)
    assert result == expected_result
