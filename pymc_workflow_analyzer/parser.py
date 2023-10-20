import ast
from pymc.distributions import __all__ as pymc_distributions

class StaticParser(ast.NodeVisitor):
    def __init__(self):
        self.imported_names = {}  # Maps imported names to their original module (e.g., {"Normal": "pymc.distributions"})
        self.pymc_alias = None
        self.report_data = {
            "number_of_import_statements":0,
            "imports": [],
            "distributions": [],
            "samplers": [],
        }

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.name
            self.report_data["number_of_import_statements"] += 1
            self.report_data["imports"].append(name)  # Storing the imported library name
            if 'pymc' in name:
                self.pymc_alias = alias.asname or name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module_name = node.module
        self.report_data["number_of_import_statements"] += 1
        self.report_data["imports"].append(module_name)  # Storing the base module name of the import
        if module_name and 'pymc' in module_name:
            for alias in node.names:
                imported_as = alias.asname or alias.name
                self.imported_names[imported_as] = module_name
        self.generic_visit(node)

    def visit_Call(self, node):
        function_name = None

        # Extracting the function name
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id == self.pymc_alias:
                    function_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            function_name = node.func.id
            if function_name in self.imported_names:
                if 'pymc' in self.imported_names[function_name]:
                    function_name = node.func.id  # It's a PyMC function

        if function_name:
            # Check if it's a PyMC distribution
            if function_name in pymc_distributions and function_name not in self.report_data["distributions"]:
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
