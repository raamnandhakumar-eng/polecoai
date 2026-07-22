"""
Step 4: The latest evidence — Anthropic's Feb 2026 observed-exposure scores
(labor_market_impacts/job_exposure.csv, AI Exposure Index release, Mar 2026).

observed_exposure = share of an occupation's tasks with meaningful observed
AI penetration in Feb 2026 data. This script analyzes the frontline groups
(SOC 35, 39, 41, 43) against computer/math (15):

  D1. Persistence: distribution of exposure by group one year after the
      baseline — does the frontline gap survive into 2026?
  D2. Polarization: within frontline groups, which occupations are exposed?

Run: python scripts/run_latest_exposure.py
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from polecoai.config import FIGURES_DIR, REFERENCE_DATA_DIR, TABLES_DIR

EXPOSURE_DATA = REFERENCE_DATA_DIR / "job_exposure_frontline_subset.csv"
EXPOSURE_GROUPS = {
    "15": "Computer & Mathematical",
    "41": "Sales",
    "43": "Office/Admin Support",
    "35": "Food Service",
    "39": "Personal Care & Service",
}


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    exposure = pd.read_csv(EXPOSURE_DATA)
    exposure["group"] = exposure["occ_code"].str[:2].map(EXPOSURE_GROUPS)

    summary = (exposure.groupby("group")["observed_exposure"]
               .agg(mean="mean", median="median",
                    zero_share=lambda s: (s == 0).mean(),
                    max="max", n="count")
               .loc[list(EXPOSURE_GROUPS.values())].round(3))
    summary.to_csv(TABLES_DIR / "exposure_2026_by_group.csv")
    print("=== D1. Observed exposure by group, Feb 2026 ===")
    print(summary.to_string())

    frontline = exposure[exposure["group"] != "Computer & Mathematical"]
    print("\n=== D2. Most vs least exposed frontline occupations ===")
    print("\nTop 10:")
    print(frontline.nlargest(10, "observed_exposure")[["title", "observed_exposure"]]
          .to_string(index=False))
    print(f"\nFrontline occupations with ZERO observed exposure: "
          f"{(frontline['observed_exposure'] == 0).sum()} of {len(frontline)} "
          f"({(frontline['observed_exposure'] == 0).mean():.0%})")

    # Figure: strip/dot plot of exposure by group
    fig, ax = plt.subplots(figsize=(10, 6))
    order = ["Computer & Mathematical", "Office/Admin Support", "Sales",
             "Personal Care & Service", "Food Service"]
    for i, g in enumerate(order):
        vals = exposure.loc[exposure["group"] == g, "observed_exposure"]
        color = "#9a9a9a" if g == "Computer & Mathematical" else "#d97757"
        ax.scatter(vals, [i] * len(vals), alpha=0.6, s=30, color=color)
        ax.scatter(vals.mean(), i, marker="|", s=500, color="black", zorder=3)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_xlabel("Observed AI exposure (share of tasks with meaningful penetration), Feb 2026")
    ax.set_title("One year on, the gap persists — and frontline exposure is polarized\n"
                 "(dots = occupations; bar = group mean; source: AEI labor market impacts)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig6_exposure_2026.png", dpi=200)
    plt.close(fig)
    print(f"\nFigure -> {FIGURES_DIR / 'fig6_exposure_2026.png'}")


if __name__ == "__main__":
    main()
