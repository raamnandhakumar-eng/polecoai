"""
Step 4: The latest evidence — Anthropic's Feb 2026 observed-exposure scores
(labor_market_impacts/job_exposure.csv, AI Exposure Index release, Mar 2026).

observed_exposure = share of an occupation's tasks with meaningful observed
AI penetration in Feb 2026 data. This script analyzes the frontline groups
(SOC 35, 39, 41, 43) against computer/math (15):

  D1. Persistence: distribution of exposure by group one year after the
      baseline — does the frontline gap survive into 2026?
  D2. Polarization: within frontline groups, which occupations are exposed?

Run: python src/04_latest_exposure.py
"""

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "labor_market_impacts_2026" / "job_exposure_frontline_subset.csv"
FIGS = ROOT / "figures"
OUT = ROOT / "results"

GROUPS = {"15": "Computer & Mathematical", "41": "Sales",
          "43": "Office/Admin Support", "35": "Food Service",
          "39": "Personal Care & Service"}


def main() -> None:
    df = pd.read_csv(DATA)
    df["group"] = df["occ_code"].str[:2].map(GROUPS)

    summary = (df.groupby("group")["observed_exposure"]
               .agg(mean="mean", median="median",
                    zero_share=lambda s: (s == 0).mean(),
                    max="max", n="count")
               .loc[list(GROUPS.values())].round(3))
    summary.to_csv(OUT / "exposure_2026_by_group.csv")
    print("=== D1. Observed exposure by group, Feb 2026 ===")
    print(summary.to_string())

    fl = df[df["group"] != "Computer & Mathematical"]
    print("\n=== D2. Most vs least exposed frontline occupations ===")
    print("\nTop 10:")
    print(fl.nlargest(10, "observed_exposure")[["title", "observed_exposure"]]
          .to_string(index=False))
    print(f"\nFrontline occupations with ZERO observed exposure: "
          f"{(fl['observed_exposure'] == 0).sum()} of {len(fl)} "
          f"({(fl['observed_exposure'] == 0).mean():.0%})")

    # Figure: strip/dot plot of exposure by group
    fig, ax = plt.subplots(figsize=(10, 6))
    order = ["Computer & Mathematical", "Office/Admin Support", "Sales",
             "Personal Care & Service", "Food Service"]
    for i, g in enumerate(order):
        vals = df.loc[df["group"] == g, "observed_exposure"]
        color = "#9a9a9a" if g == "Computer & Mathematical" else "#d97757"
        ax.scatter(vals, [i] * len(vals), alpha=0.6, s=30, color=color)
        ax.scatter(vals.mean(), i, marker="|", s=500, color="black", zorder=3)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_xlabel("Observed AI exposure (share of tasks with meaningful penetration), Feb 2026")
    ax.set_title("One year on, the gap persists — and frontline exposure is polarized\n"
                 "(dots = occupations; bar = group mean; source: AEI labor market impacts)")
    # annotate the outliers
    for occ, y in [("Customer Service Reps (0.70)", 1), ("Data Entry Keyers (0.67)", 1),
                   ("Retail Salespersons (0.32)", 2), ("Computer Programmers (0.75)", 0)]:
        pass  # annotations kept minimal; occupations named in text
    fig.tight_layout()
    fig.savefig(FIGS / "fig6_exposure_2026.png", dpi=200)
    plt.close(fig)
    print(f"\nFigure -> {FIGS / 'fig6_exposure_2026.png'}")


if __name__ == "__main__":
    main()
