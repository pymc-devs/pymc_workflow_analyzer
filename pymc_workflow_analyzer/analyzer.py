import ast
import sys
import json
import requests
import nbformat
from .parser import StaticParser

def fetch_content_from_url(url):
    """
    Fetch content from a URL.

    :param url: URL pointing to a Python script or Jupyter notebook.
    :return: Content as a string.
    """
    try:
        if 'github.com' in url and '/blob/' in url:
            url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Check if the content seems to be HTML
        if content.strip().startswith('<!DOCTYPE html>') or '<html' in content:
            print("Error: The URL seems to be pointing to an HTML page, not a raw Python script or Jupyter notebook. "
                  "Please provide a URL pointing to the raw content. "
                  "For files on GitHub, you can get the raw URL by clicking on the 'Raw' button.")
            sys.exit(1)
        else:
            # Check if the content is JSON and not what we expect
            try:
                content_json = json.loads(content)
                if 'payload' in content_json or 'items' in content_json:  # or other checks to identify it's not a raw code file
                    print("Error: The URL seems to be pointing to a JSON API or a structured data endpoint, not a raw Python script or Jupyter notebook. "
                          "Please provide a URL pointing to the raw content. "
                          "For files on GitHub, you can get the raw URL by clicking on the 'Raw' button.")
                    sys.exit(1)
            except json.JSONDecodeError:
                # It's not JSON, so it's likely the raw content of a file, proceed accordingly
                pass

            return content

    except requests.RequestException as e:
        print(f"Error: Unable to retrieve content from URL.\n{str(e)}")
        sys.exit(1)

def extract_code_from_notebook(notebook_content):
    """
    Extract Python code from a Jupyter notebook's content.

    :param notebook_content: Jupyter notebook content as a string.
    :return: Python code extracted from the notebook.
    """
    try:
        notebook_json = json.loads(notebook_content)
        notebook = nbformat.reads(json.dumps(notebook_json), as_version=4)
        code = ""
        for cell in notebook.cells:
            if cell.cell_type == "code":
                code += cell.source + "\n"
        return code
    except json.JSONDecodeError:
        print("Error: The provided content does not appear to be in JSON format. "
              "If you're providing a URL, please ensure it's a direct link to the raw file content, "
              "such as the 'Raw' content view from a GitHub repository or Gist.")
        sys.exit(1)
    except nbformat.reader.NotJSONError:
        print("Error: The provided content does not appear to be a valid Jupyter notebook. "
              "Please ensure the file is a proper '.ipynb' file and the URL is pointing to its raw content.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while parsing the notebook content.\n{str(e)}")
        sys.exit(1)

def static_analyzer(input_source, source_type="file"):
    """
    Analyze a Python file, script content, or Jupyter notebook statically.

    :param input_source: Path to the file to analyze, string containing script, or URL to a Jupyter notebook.
    :param source_type: Type of the input_source: "file", "string", or "url".
    :return: A dictionary containing the report.
    """
    parser = StaticParser()
    try:
        if source_type == "file":
            with open(input_source, "r") as source_file:
                if input_source.endswith(".ipynb"):
                    code = extract_code_from_notebook(source_file.read())
                    tree = ast.parse(code)
                else:
                    tree = ast.parse(source_file.read())
        elif source_type == "code":
            tree = ast.parse(input_source)
        elif source_type == "url":
            content = fetch_content_from_url(input_source)
            if input_source.endswith(".ipynb"):
                code = extract_code_from_notebook(content)
                tree = ast.parse(code)
            else:
                # Assuming it's a Python script if it's not a notebook
                tree = ast.parse(content)
        else:
            print("Error: The source_type must be 'file', 'string', or 'url'.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The file {input_source} does not exist.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You do not have the permission to read the file {input_source}.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: The script contains syntax errors.\nPlease provide a valid Python script or URL\n{str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    parser.visit(tree)
    return parser.get_report()
