"""Core task, occupation, and representation calculations."""

from collections.abc import Mapping

import pandas as pd

from .config import FRONTLINE_GROUP_TITLES
from .data import employment_shares, major_group_names, normalize_task_text


def build_task_occupation_table(
    inputs: Mapping[str, pd.DataFrame],
) -> pd.DataFrame:
    """Join AEI task shares to the first matching O*NET occupation."""
    mappings = inputs["mappings"].copy()
    statements = inputs["statements"].copy()
    mappings["task_key"] = normalize_task_text(mappings["task_name"])
    statements["task_key"] = normalize_task_text(statements["Task"])
    tasks = mappings.merge(
        statements[["task_key", "O*NET-SOC Code", "Title"]]
        .drop_duplicates("task_key"),
        on="task_key",
        how="left",
    ).rename(columns={"O*NET-SOC Code": "soc_code", "Title": "occupation"})
    tasks["major_group"] = tasks["soc_code"].astype(str).str[:2]
    return tasks


def calculate_representation(
    inputs: Mapping[str, pd.DataFrame],
    tasks: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate usage share, employment share, and their ratio by group."""
    group_names = major_group_names(inputs["soc"])
    usage = (
        tasks.dropna(subset=["soc_code"])
        .groupby("major_group")["pct"]
        .sum()
        .rename("usage_pct")
    )
    usage = usage / usage.sum() * 100
    employment = employment_shares(
        inputs["employment"], inputs["soc"]
    ).rename("employment_pct")

    representation = pd.concat([usage, employment], axis=1).dropna()
    representation["representation_index"] = (
        representation["usage_pct"] / representation["employment_pct"]
    )
    representation["group_name"] = group_names.reindex(representation.index)
    representation = representation.sort_values(
        "representation_index", ascending=False
    )
    representation.index.name = None
    return representation


def select_frontline_tasks(tasks: pd.DataFrame, limit: int = 25) -> pd.DataFrame:
    """Return the highest-share tasks mapped to the four frontline groups."""
    frontline = (
        tasks[tasks["major_group"].isin(FRONTLINE_GROUP_TITLES)]
        .sort_values("pct", ascending=False)
        .head(limit)
        .copy()
    )
    frontline["group"] = frontline["major_group"].map(FRONTLINE_GROUP_TITLES)
    return frontline


def build_wage_dataset(
    inputs: Mapping[str, pd.DataFrame],
    tasks: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate task usage to occupations and join occupation median wages."""
    wages = inputs["wages"].copy()
    wages["soc6"] = wages["SOCcode"].astype(str).str[:7]
    wages = (
        wages.groupby("soc6", as_index=False)["MedianSalary"]
        .median()
        .rename(columns={"MedianSalary": "median_wage"})
    )
    occupation_usage = (
        tasks.dropna(subset=["soc_code"])
        .assign(soc6=lambda frame: frame["soc_code"].astype(str).str[:7])
        .groupby("soc6")["pct"]
        .sum()
        .rename("usage_pct")
        .reset_index()
    )
    wage_dataset = occupation_usage.merge(wages, on="soc6", how="inner").dropna()
    wage_dataset["frontline"] = wage_dataset["soc6"].str[:2].isin(
        FRONTLINE_GROUP_TITLES
    )
    return wage_dataset
