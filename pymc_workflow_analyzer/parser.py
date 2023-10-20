import ast
from pymc.distributions import __all__ as pymc_distributions

class StaticParser(ast.NodeVisitor):
    def __init__(self):
        self.report_data = {
            "imports": [],
            "distributions": [],
            "samplers": [],
        }

    def visit_Import(self, node):
        for alias in node.names:
            self.report_data["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.report_data["imports"].append(node.module)
        self.generic_visit(node)

    def visit_Call(self, node):
        function_name = None

        # Extracting the function name
        if isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            function_name = node.func.id

        # Check if it's a PyMC distribution
        if function_name in pymc_distributions:
            if function_name not in self.report_data["distributions"]:
                self.report_data["distributions"].append(function_name)

        # If it's a PyMC sampling function, we handle it separately
        elif function_name in ["sample"]:
            sampler_info = {"name": function_name, "args": [], "keywords": []}

            # Extracting positional arguments
            for arg in node.args:
                sampler_info["args"].append(ast.dump(arg))

            # Extracting keyword arguments
            for kw in node.keywords:
                sampler_info["keywords"].append((kw.arg, ast.dump(kw.value)))

            self.report_data["samplers"].append(sampler_info)

        # continue the visit to other nodes in the syntax tree
        self.generic_visit(node)

    def report(self):
        return self.report_data
