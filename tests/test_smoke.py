"""Synthetic-data smoke test for the core analysis pipeline."""

from pathlib import Path
import tempfile

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

from polecoai.analysis import (
    build_task_occupation_table,
    build_wage_dataset,
    calculate_representation,
    select_frontline_tasks,
)
from polecoai.plotting import plot_core_figures
from polecoai.regressions import estimate_wage_regressions


TASKS = [
    ("Answer customer questions about products and prices.", "41-2031.00", "Retail Salespersons"),
    ("Write and respond to customer emails.", "43-4051.00", "Customer Service Representatives"),
    ("Prepare sales reports and pricing analyses.", "41-1011.00", "First-Line Supervisors of Retail Sales Workers"),
    ("Develop and test software applications.", "15-1252.00", "Software Developers"),
    ("Debug computer programs.", "15-1252.00", "Software Developers"),
    ("Write marketing copy for products.", "27-3043.00", "Writers and Authors"),
    ("Plan menus and food presentation.", "35-1011.00", "Chefs and Head Cooks"),
    ("Schedule appointments for clients.", "43-6014.00", "Secretaries and Administrative Assistants"),
]

GROUP_TITLES = {
    "41": "Sales and Related",
    "43": "Office and Administrative Support",
    "15": "Computer and Mathematical",
    "27": "Arts and Media",
    "35": "Food Preparation and Serving",
    "39": "Personal Care and Service",
}


def synthetic_inputs() -> dict[str, pd.DataFrame]:
    """Return minimal in-memory inputs matching the initial release schema."""
    random = np.random.default_rng(0)
    return {
        "mappings": pd.DataFrame(
            {
                "task_name": [task[0] for task in TASKS],
                "pct": random.dirichlet(np.ones(len(TASKS))) * 100,
            }
        ),
        "statements": pd.DataFrame(
            {
                "O*NET-SOC Code": [task[1] for task in TASKS],
                "Title": [task[2] for task in TASKS],
                "Task": [task[0] for task in TASKS],
            }
        ),
        "soc": pd.DataFrame(
            {
                "Major Group": [f"{code}-0000" for code in GROUP_TITLES],
                "SOC or O*NET-SOC 2019 Title": list(GROUP_TITLES.values()),
            }
        ),
        "employment": pd.DataFrame(
            {
                "SOC or O*NET-SOC 2019 Title": list(GROUP_TITLES.values()),
                "bls_distribution": random.integers(
                    50_000, 3_000_000, len(GROUP_TITLES)
                ),
            }
        ),
        "wages": pd.DataFrame(
            {
                "SOCcode": [task[1] for task in TASKS],
                "MedianSalary": random.integers(30_000, 140_000, len(TASKS)),
            }
        ),
    }


def test_smoke_pipeline() -> None:
    """Run every core calculation and confirm all three figures are written."""
    inputs = synthetic_inputs()
    tasks = build_task_occupation_table(inputs)
    assert tasks["soc_code"].notna().all()

    representation = calculate_representation(inputs, tasks)
    frontline_tasks = select_frontline_tasks(tasks)
    wage_dataset = build_wage_dataset(inputs, tasks)
    regressions = estimate_wage_regressions(wage_dataset)

    assert not representation.empty
    assert not frontline_tasks.empty
    assert len(regressions) == 5

    with tempfile.TemporaryDirectory(prefix="frontline-smoke-") as temporary:
        output_dir = Path(temporary)
        plot_core_figures(
            representation, frontline_tasks, wage_dataset, output_dir
        )
        expected = {
            output_dir / "fig1_representation.png",
            output_dir / "fig2_frontline_tasks.png",
            output_dir / "fig3_wage_gradient.png",
        }
        assert all(path.exists() for path in expected)


if __name__ == "__main__":
    test_smoke_pipeline()
    print("PASS: isolated synthetic-data smoke test completed.")
