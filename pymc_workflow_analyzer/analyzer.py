import ast
from .parser import StaticParser

def static_analyze(file_path):
    parser = StaticParser()
    try:
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
    except (FileNotFoundError, PermissionError, SyntaxError):
        raise  # Re-throwing the exception to be caught in main.py
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise

    parser.visit(tree)
    return parser.report()
