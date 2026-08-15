"""Small offline checks for the v2 estimators and definition summary."""

import numpy as np
import pandas as pd

from polecoai.adoption_gap import (
    estimate_access_gap_model,
    estimate_two_part_models,
    summarize_frontline_definitions,
)


def synthetic_model_data(rows: int = 300) -> pd.DataFrame:
    random = np.random.default_rng(42)
    computer = random.normal(size=rows)
    physical = random.normal(size=rows)
    frontline = random.integers(0, 2, size=rows)
    latent = 0.7 * computer - 0.6 * physical + 0.2 * frontline
    probability = 1 / (1 + np.exp(-latent))
    any_use = random.binomial(1, probability)
    positive_use = np.exp(
        -2 + 0.25 * computer - 0.20 * physical + random.normal(0, 0.3, rows)
    )
    observed = np.where(any_use == 1, positive_use, 0)
    return pd.DataFrame(
        {
            "observed_exposure": observed,
            "any_ai_use": any_use,
            "log_wage": random.normal(11, 0.4, rows),
            "frontline_soc": frontline,
            "education_index": random.normal(5, 1, rows),
            "computer_use_score": computer,
            "physical_presence_index": physical,
            "customer_facing_index": random.normal(size=rows),
            "ai_access_gap": 0.7 - observed + random.normal(0, 0.05, rows),
        }
    )


def test_v2_estimators() -> None:
    data = synthetic_model_data()
    two_part = estimate_two_part_models(data)
    access_gap = estimate_access_gap_model(data)

    assert set(two_part["stage"]) == {
        "stage1_any_use_logit",
        "stage2_positive_use_ols",
    }
    assert int(two_part["n"].max()) == len(data)
    assert set(access_gap["term"]) >= {
        "computer_use_score",
        "physical_presence_index",
        "customer_facing_index",
    }


def test_frontline_definition_summary() -> None:
    data = pd.DataFrame(
        {
            "frontline_soc": [1, 1, 0, 0],
            "frontline_physical": [1, 0, 1, 0],
            "frontline_customer": [0, 1, 0, 1],
            "physical_presence_index": [4.0, 2.0, 3.0, 1.0],
            "customer_facing_index": [1.0, 4.0, 2.0, 3.0],
            "task_usage_pct": [10.0, 20.0, 30.0, 40.0],
            "frontline_origin_task_usage_pct": [10.0, 20.0, 0.0, 0.0],
            "calibrated_employment_pct": [25.0, 25.0, 25.0, 25.0],
        }
    )
    result = summarize_frontline_definitions(data).set_index("definition")
    baseline = result.loc["A_current_soc_groups"]
    assert baseline["usage_share_pct"] == 30.0
    assert baseline["employment_share_pct"] == 50.0
    assert baseline["representation_index"] == 0.6
