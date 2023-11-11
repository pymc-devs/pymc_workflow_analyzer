# PyMC Examples: GLM - Linear regression
# https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_linear.html

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import xarray as xr

# Set up for data generation
RANDOM_SEED = 8927
rng = np.random.default_rng(RANDOM_SEED)
size = 200
true_intercept = 1
true_slope = 2

# Generate data
x = np.linspace(0, 1, size)
true_regression_line = true_intercept + true_slope * x
y = true_regression_line + rng.normal(scale=0.5, size=size)
data = pd.DataFrame(dict(x=x, y=y))

# Bayesian linear regression model specification
with pm.Model() as model:
    sigma = pm.HalfCauchy("sigma", beta=10)
    intercept = pm.Normal("Intercept", 0, sigma=20)
    slope = pm.Normal("slope", 0, sigma=20)
    likelihood = pm.Normal("y", mu=intercept + slope * x, sigma=sigma, observed=y)
    idata = pm.sample(3000)

# Plotting the trace
az.plot_trace(idata, figsize=(10, 7))
plt.show()
