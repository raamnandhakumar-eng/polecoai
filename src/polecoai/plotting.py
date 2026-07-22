"""Figure generation for the core analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import FRONTLINE_GROUP_TITLES


def plot_core_figures(
    representation: pd.DataFrame,
    frontline_tasks: pd.DataFrame,
    wage_dataset: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Write Figures 1-3 without altering the underlying calculations."""
    output_dir.mkdir(exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 7))
    ordered = representation.sort_values("usage_pct")
    labels = (
        ordered["group_name"]
        .fillna(ordered.index.to_series())
        .str.replace(" Occupations", "", regex=False)
        .str.slice(0, 40)
    )
    colors = [
        "#d97757" if code in FRONTLINE_GROUP_TITLES else "#9a9a9a"
        for code in ordered.index
    ]
    axis.barh(
        labels,
        ordered["usage_pct"],
        color=colors,
        alpha=0.9,
        label="Claude usage share",
    )
    axis.scatter(
        ordered["employment_pct"],
        labels,
        color="black",
        zorder=3,
        s=24,
        label="US employment share",
    )
    axis.set_xlabel("Percent")
    axis.set_title(
        "AI usage vs employment share by occupation group\n"
        "(frontline groups in orange)"
    )
    axis.legend()
    figure.tight_layout()
    figure.savefig(output_dir / "fig1_representation.png", dpi=200)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(10, 7))
    ordered_tasks = frontline_tasks.sort_values("pct").tail(15)
    axis.barh(
        ordered_tasks["task_name"].str.slice(0, 62),
        ordered_tasks["pct"],
        color="#d97757",
    )
    axis.set_xlabel("Share of Claude conversations (%)")
    axis.set_title("Top frontline (sales/admin/service) tasks done with AI")
    figure.tight_layout()
    figure.savefig(output_dir / "fig2_frontline_tasks.png", dpi=200)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(8, 6))
    other = wage_dataset[~wage_dataset["frontline"]]
    frontline = wage_dataset[wage_dataset["frontline"]]
    axis.scatter(
        other["median_wage"],
        other["usage_pct"],
        s=14,
        alpha=0.35,
        color="#9a9a9a",
        label="Other occupations",
    )
    axis.scatter(
        frontline["median_wage"],
        frontline["usage_pct"],
        s=28,
        alpha=0.9,
        color="#d97757",
        label="Frontline occupations",
    )
    axis.set_xlabel("Median annual wage ($)")
    axis.set_ylabel("Usage share (%), log scale")
    axis.set_yscale("log")
    axis.legend()
    axis.set_title("AI usage vs wages: where frontline work sits")
    figure.tight_layout()
    figure.savefig(output_dir / "fig3_wage_gradient.png", dpi=200)
    plt.close(figure)
