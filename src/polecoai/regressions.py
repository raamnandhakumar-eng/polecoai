"""Occupation-level regression specifications reported in the paper."""

import numpy as np
import pandas as pd


def estimate_wage_regressions(wage_dataset: pd.DataFrame) -> pd.DataFrame:
    """Estimate both OLS specifications with HC1 standard errors."""
    log_usage = np.log(wage_dataset["usage_pct"].to_numpy())
    log_wage = np.log(wage_dataset["median_wage"].to_numpy())
    frontline = wage_dataset["frontline"].astype(float).to_numpy()
    specifications = {
        "log_wage_only": (
            np.column_stack([np.ones(len(wage_dataset)), log_wage]),
            ["intercept", "log_wage"],
        ),
        "log_wage_frontline": (
            np.column_stack([np.ones(len(wage_dataset)), log_wage, frontline]),
            ["intercept", "log_wage", "frontline"],
        ),
    }

    rows = []
    for model, (design, terms) in specifications.items():
        coefficients = np.linalg.solve(
            design.T @ design, design.T @ log_usage
        )
        residuals = log_usage - design @ coefficients
        observations, parameters = design.shape
        inverse_cross_product = np.linalg.inv(design.T @ design)
        meat = design.T @ ((residuals ** 2)[:, None] * design)
        covariance_hc1 = (
            observations / (observations - parameters)
        ) * inverse_cross_product @ meat @ inverse_cross_product
        standard_errors = np.sqrt(np.diag(covariance_hc1))
        r_squared = 1 - (
            (residuals @ residuals)
            / ((log_usage - log_usage.mean()) @ (log_usage - log_usage.mean()))
        )
        for term, coefficient, standard_error in zip(
            terms, coefficients, standard_errors
        ):
            rows.append(
                {
                    "model": model,
                    "term": term,
                    "coefficient": coefficient,
                    "se_hc1": standard_error,
                    "r_squared": r_squared,
                    "n": observations,
                }
            )
    return pd.DataFrame(rows)
