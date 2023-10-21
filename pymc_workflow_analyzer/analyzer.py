import ast
from typing import List, Dict, Any
from .parser import StaticParser


def static_analyzer(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Analyze a Python file statically.

    :param file_path: Path to the file to analyze.
    :return: A dictionary containing the report.
    """
    parser = StaticParser()
    try:
        with open(file_path, "r") as source_file:
            tree = ast.parse(source_file.read())
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You do not have the permission to read the file {file_path}.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: The file {file_path} contains syntax errors.\n{str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    parser.visit(tree)
    return parser.get_report()