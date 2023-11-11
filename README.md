# PyMC Workflow Analyzer

The PyMC Workflow Analyzer is a tool designed to statically analyze Python scripts or Jupyter notebooks to identify PyMC workflows. 
The goal is to provide data back to the deveopers so they understand library usage and can determine what is most useful to users.
It can process Python files, Python code as a string, or Jupyter notebooks from a local system or a URL.
See [Discourse](See https://discourse.pymc.io/t/extended-event-gathering-pymc-usage-information/13064) for the higher level discussion

## Features

- Analyze Python scripts or Jupyter notebooks containing PyMC workflows.
- Support for local files, Python code as strings, or files from URLs.
- Detailed reporting of the analysis.

## Requirements

- Python 3.6 or higher
- Requests library (`pip install requests`)
- Nbformat library (`pip install nbformat`)

## Usage

This script can analyze Python scripts or Jupyter notebooks to extract information about PyMC usage. It supports input directly from a file, a string of Python code, or a URL pointing to a Jupyter notebook or a raw Python script.

### Command-Line Usage

1. Clone the repository to your local machine.
2. Navigate to the directory containing the script.
3. Run the script using Python and provide the necessary arguments.

### Command Line Options

- `--file`: Path to the local Python script or Jupyter notebook to analyze (**Optional**).
- `--url`: URL pointing to a Python script or Jupyter notebook. Ensure this is the URL of the raw file.
- `--code`: A string of Python code to analyze.
- `--output`: Specify the path where the output report should be saved. If not provided, the report will be stored to `report.txt`

### Examples
Analyze a local Python file:
```sh
python main.py sample_script.py
```

Analyze a local Jupyter Notebook file:
```sh
python main.py sample_script.py
```

Analyze a local file and save the report to a specified path:
```sh
python main.py sample_script.ipynb --output /path/to/save/report.txt
```

Optional `--file` argument:
```sh
python main.py --file sample_script.ipynb
```

Analyze code from a direct URL Jupyter Notebook:
```sh
python main.py --url https://github.com/bwengals/hsgp/blob/main/cherry_blossoms_hsgp.ipynb
```

Analyze code from a direct URL containing Python code:
```sh
python main.py --url https://github.com/pymc-devs/pymc/blob/main/pymc/sampling/mcmc.py
```

Analyze a string of code and print the report to the console:
```sh
python main.py --code "import pymc as pm; model = pm.Model()"
```

### Output
The script generates a report that includes details about the PyMC functions used, their arguments, and other relevant information extracted from the static analysis of the code.

If the `--output` option is provided, the report will be saved to the specified path. Otherwise, it will be printed to the console and saved to `report.txt`.


### Python Script Usage

You can also import the `static_analyzer` function in your Python scripts:

```python
from pymc_workflow_analyzer import static_analyzer

# For local file analysis
report = static_analyzer("sample_script.py") #defaults source_type="file"

# For URL analysis
report = static_analyzer("https://raw.githubusercontent.com/user/repository/branch/file.ipynb", source_type="url")

# For analyzing code as a string
code = """
import pymc as pm
model = pm.Model()
"""
report = static_analyzer(code, source_type="code")

# Process the `report` as needed
```

## Contributing

Contributions, issues, and feature requests are welcome!
