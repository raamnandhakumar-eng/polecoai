"""Run the PolecoAI v2 adoption and access-gap extension."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from polecoai.adoption_gap import (
    build_adoption_dataset,
    estimate_access_gap_model,
    estimate_two_part_models,
    summarize_frontline_definitions,
)
from polecoai.config import (
    FIGURES_DIR,
    INITIAL_RELEASE_DIR,
    TABLES_DIR,
    V2_JOB_EXPOSURE,
    V2_ONET_CROSSWALK,
    V2_OEWS_DETAIL,
    V2_ONET_DATABASE,
    V2_THEORETICAL_EXPOSURE,
)


def make_figures(data: pd.DataFrame, definitions: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    complete = data.dropna(
        subset=["theoretical_exposure", "observed_exposure"]
    )
    fig, ax = plt.subplots(figsize=(8.5, 7))
    frontline = complete["frontline_soc"] == 1
    ax.scatter(
        complete.loc[~frontline, "theoretical_exposure"],
        complete.loc[~frontline, "observed_exposure"],
        color="#8b9693",
        alpha=0.62,
        s=28,
        label="Other occupations",
    )
    ax.scatter(
        complete.loc[frontline, "theoretical_exposure"],
        complete.loc[frontline, "observed_exposure"],
        color="#d97757",
        alpha=0.70,
        s=28,
        label="Current frontline SOC groups",
    )
    ax.plot([0, 1], [0, 1], color="black", linestyle="--", linewidth=1)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.01)
    ax.set_xlabel("Theoretical task exposure (GPTs-are-GPTs gamma)")
    ax.set_ylabel("Observed AI exposure (Anthropic Economic Index)")
    ax.set_title("Potential versus observed AI use by occupation")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig7_potential_observed_gap.png", dpi=200)
    plt.close(fig)

    labels = ["Current SOC", "High physical", "High customer"]
    positions = range(len(definitions))
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(
        [position - 0.18 for position in positions],
        definitions["usage_share_pct"],
        width=0.36,
        color="#d97757",
        label="Task-usage share",
    )
    ax.bar(
        [position + 0.18 for position in positions],
        definitions["employment_share_pct"],
        width=0.36,
        color="#8b9693",
        label="Employment share",
    )
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Share of U.S. total (%)")
    ax.set_title("The exposure gap under three frontline definitions")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig8_frontline_definitions.png", dpi=200)
    plt.close(fig)


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    data = build_adoption_dataset(
        observed_path=V2_JOB_EXPOSURE,
        theoretical_path=V2_THEORETICAL_EXPOSURE,
        oews_path=V2_OEWS_DETAIL,
        onet_path=V2_ONET_DATABASE,
        task_mappings_path=INITIAL_RELEASE_DIR / "onet_task_mappings.csv",
        task_statements_path=INITIAL_RELEASE_DIR / "onet_task_statements.csv",
        crosswalk_path=V2_ONET_CROSSWALK,
        group_employment_path=INITIAL_RELEASE_DIR / "bls_employment_may_2023.csv",
        soc_structure_path=INITIAL_RELEASE_DIR / "SOC_Structure.csv",
    )
    two_part = estimate_two_part_models(data)
    access_gap = estimate_access_gap_model(data)
    definitions = summarize_frontline_definitions(data)

    data.to_csv(TABLES_DIR / "v2_occupation_analysis.csv", index=False)
    two_part.to_csv(TABLES_DIR / "v2_two_part_models.csv", index=False)
    access_gap.to_csv(TABLES_DIR / "v2_access_gap_regression.csv", index=False)
    definitions.to_csv(
        TABLES_DIR / "v2_frontline_definitions.csv", index=False
    )
    make_figures(data, definitions)

    pd.set_option("display.width", 160)
    print("=== V2 coverage ===")
    print(
        "Observed-exposure occupations:",
        int(data["observed_exposure"].notna().sum()),
    )
    print(
        "Complete two-part sample:",
        int(
            data[
                [
                    "observed_exposure",
                    "log_wage",
                    "education_index",
                    "computer_use_score",
                    "physical_presence_index",
                ]
            ]
            .notna()
            .all(axis=1)
            .sum()
        ),
    )
    print("\n=== Two-part model ===")
    print(
        two_part[
            (two_part["estimate_type"] != "log_odds")
            & (two_part["term"] != "const")
        ][["stage", "estimate_type", "term", "estimate", "se_hc1", "p_value", "n"]]
        .round(4)
        .to_string(index=False)
    )
    print("\n=== Alternative frontline definitions ===")
    print(
        definitions[
            [
                "definition",
                "usage_share_pct",
                "employment_share_pct",
                "representation_index",
                "usage_minus_employment_pp",
                "n_inside",
            ]
        ]
        .round(3)
        .to_string(index=False)
    )
    print("\n=== Access-gap regression ===")
    print(access_gap.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
