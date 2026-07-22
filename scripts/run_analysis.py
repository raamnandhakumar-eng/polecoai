"""Run the core representation, task, wage, and regression analyses."""

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from polecoai.analysis import (
    build_task_occupation_table,
    build_wage_dataset,
    calculate_representation,
    select_frontline_tasks,
)
from polecoai.config import FIGURES_DIR, FRONTLINE_GROUP_TITLES, TABLES_DIR
from polecoai.data import load_initial_release
from polecoai.plotting import plot_core_figures
from polecoai.regressions import estimate_wage_regressions


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_initial_release()
    tasks = build_task_occupation_table(inputs)
    match_rate = tasks["soc_code"].notna().mean()
    print(f"Task->SOC match rate: {match_rate:.1%} ({len(tasks)} tasks)")

    representation = calculate_representation(inputs, tasks)
    frontline_tasks = select_frontline_tasks(tasks)
    wage_dataset = build_wage_dataset(inputs, tasks)
    regressions = estimate_wage_regressions(wage_dataset)

    representation.to_csv(TABLES_DIR / "representation_by_group.csv")
    frontline_tasks.to_csv(TABLES_DIR / "frontline_tasks.csv", index=False)
    regressions.to_csv(TABLES_DIR / "regression_usage_wage.csv", index=False)
    plot_core_figures(
        representation, frontline_tasks, wage_dataset, FIGURES_DIR
    )

    print("\n=== Headline numbers ===")
    pd.set_option("display.width", 140)
    columns = [
        "group_name",
        "usage_pct",
        "employment_pct",
        "representation_index",
    ]
    print(representation[columns].round(2).to_string())
    frontline_rows = representation.index.isin(FRONTLINE_GROUP_TITLES)
    print(
        "\nFrontline usage total:",
        round(representation.loc[frontline_rows, "usage_pct"].sum(), 2),
        "%",
    )
    print(
        "Frontline employment total:",
        round(representation.loc[frontline_rows, "employment_pct"].sum(), 2),
        "%",
    )
    print("\nTop 10 frontline tasks:")
    print(
        frontline_tasks[["task_name", "occupation", "pct"]]
        .head(10)
        .to_string(index=False)
    )
    print("\nOccupation-level wage regressions (HC1 standard errors):")
    print(regressions.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
