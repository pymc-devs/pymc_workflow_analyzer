import ast

#TODO: fix these to include all functions name
from pymc.distributions import __all__ as pymc_distributions
from pymc.math import __all__ as pymc_math
from pymc.model.core import __all__ as core_models
from pymc.model.transform.conditioning import __all__ as conditioning_models
from pymc.model.fgraph import __all__ as fgraph_models

from arviz.plots import __all__ as arviz_plots

pymc_models = list(core_models) + list(conditioning_models) + list(fgraph_models)

pymc_samplers = [
    "sample", "sample_prior_predictive", "sample_posterior_predictive", "sample_posterior_predictive_w",
    "sample_blackjax_nuts", "sample_numpyro_nuts", "init_nuts", "draw", "NUTS", "HamiltonianMC", 
    "BinaryGibbsMetropolis", "BinaryMetropolis", "CategoricalGibbsMetropolis", "CauchyProposal", 
    "DEMetropolis", "DEMetropolisZ", "LaplaceProposal", "Metropolis", "MultivariateNormalProposal", 
    "NormalProposal", "PoissonProposal", "UniformProposal", "CompoundStep", "Slice",
]

pymc_experimentals = [
    "MarginalModel", "ModelBuilder", "fit", "GenExtreme", "GeneralizedPoisson", "DiscreteMarkovChain",
    "R2D2M2CP", "histogram_approximation", "bspline_interpolation", "prior_from_idata", 
    "PytensorRepresentation", "PyMCStateSpace", "StandardFilter", "UnivariateFilter", "SteadyStateFilter",
    "KalmanSmoother", "SingleTimeseriesFilter", "CholeskyFilter", "LinearGaussianStateSpace", "BayesianVARMAX"
]


class StaticParser(ast.NodeVisitor):
    """
    A class to parse a Python script and extract information about PyMC usage.
    """
    def __init__(self):
        self.imported_names = {}  # Maps imported names to their original module (e.g., {"Normal": "pymc"})
        self.alias_name = []
        self.report = {
            "number_of_import_statements": 0,
            "imports": [],
            "model": [],
            "distributions": [],
            "samplers": [],
            "math": [],
            "arviz": [],
            "pymc_experimental": [],
        }
        
    def visit_Import(self, node):
        """
        Visit an Import node and extract information about the imported library.

        :param node: The Import node to visit.
        """
        for alias in node.names:
            name = alias.name
            asname = alias.asname if alias.asname else name
            self.imported_names[asname] = name # Note: Store the alias as a key
            
            if name not in self.report["imports"]:
                self.report["number_of_import_statements"] += 1
                self.report["imports"].append(name)  # Storing the imported library name
            if 'pymc' in name or 'arviz' in name or 'pymc_experimental' in name:
                self.alias_name.append(alias.asname or name)
                
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """
        Visit an ImportFrom node and extract information about the imported library.

        :param node: The ImportFrom node to visit.
        """
        module_name = node.module
        if module_name not in self.report["imports"]:
            self.report["number_of_import_statements"] += 1
            self.report["imports"].append(module_name)  # Storing the base module name of the import
        if module_name and ('pymc' in module_name or 'arviz' in module_name or 'pymc_experimental' in module_name):
            for alias in node.names:
                name = alias.name
                asname = alias.asname if alias.asname else name
                # Construct a full path for the imported function/class
                full_name = f"{module_name}.{name}" if module_name else name
                self.imported_names[asname] = full_name
        self.generic_visit(node)

    def extract_function_path(self, node):
        """
        Recursively extract the full function path from a nested AST node.

        :param node: The AST node to extract the path from.
        :return: A string representing the full path (e.g., "pymc.math.eq").
        """
        if isinstance(node, ast.Attribute):
            return self.extract_function_path(node.value) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return node.id
        else:
            return ''  # Non-handleable node
        
    def visit_Call(self, node):
        """
        Visit a Call node and extract information about the PyMC function being called.

        :param node: The Call node to visit.
        """
        full_function_path = self.extract_function_path(node.func)
        # First, check if the function is called by its alias
        if full_function_path in self.imported_names:
            full_function_path = self.imported_names[full_function_path]
        
        function_name = None
        # Checking if the function path starts with a known PyMC alias or imported name
        for alias, module in self.imported_names.items():
            if full_function_path.startswith(alias):
                if 'pymc' in module or 'arviz' in module or 'pymc_experimental' in module:
                    function_name = full_function_path.split('.')[-1]  # Extract the actual function name
                    break

        if function_name:
            args = len(node.args)
            kwargs = [keyword.arg for keyword in node.keywords]
            function_info = {"name": function_name, "args": args, "kwargs": kwargs}
            
            if function_name in pymc_models:
                self.report["model"].append(function_info)
            elif function_name in pymc_distributions:
                self.report["distributions"].append(function_info)
            elif function_name in pymc_samplers:
                self.report["samplers"].append(function_info)
            elif function_name in pymc_math:
                self.report["math"].append(function_info)
            elif function_name in arviz_plots:
                self.report["arviz"].append(function_info)
            elif function_name in pymc_experimentals:
                self.report["pymc_experimental"].append(function_info)

        # continue the visit to other nodes in the syntax tree
        self.generic_visit(node)

    def get_report(self):
        """
        Get the report generated by the parser.

        :return: The report generated by the parser.
        """
        return self.report
