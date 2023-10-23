import ast
import sys
from .parser import StaticParser


def static_analyzer(input_source, source_type="file"):
    """
    Analyze a Python file or script content statically.

    :param input_source: Path to the file to analyze or string containing script.
    :param source_type: Type of the input_source: "file" or "string".
    :return: A dictionary containing the report.
    """
    parser = StaticParser()
    try:
        if source_type == "file":
            with open(input_source, "r") as source_file:
                tree = ast.parse(source_file.read())
        elif source_type == "string":
            tree = ast.parse(input_source)
        else:
            print("Error: The source_type must be 'file' or 'string'.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The file {input_source} does not exist.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You do not have the permission to read the file {input_source}.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: The script contains syntax errors.\n{str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    parser.visit(tree)
    return parser.get_report()
