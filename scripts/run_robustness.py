"""
Step 5: Referee-driven robustness checks.

  E. TASK SPLITTING (join robustness): 272 of 18,428 O*NET task statements
     (1.5%) appear under multiple occupations. The baseline pipeline assigns
     each task's usage to ONE occupation (first match). Here each shared
     task's usage share is split EQUALLY across all occupations listing it,
     and the representation index is recomputed.

  F. EMPLOYMENT WEIGHTING for the Feb 2026 exposure means: if a detailed
     OEWS national file is present at data/raw/oews/oews_national_2023.csv
     (columns OCC_CODE, TOT_EMP -- the standard BLS national XLSX saved as
     CSV), group means are recomputed employment-weighted. Otherwise the
     script prints unweighted means with a warning.

Run: python scripts/run_robustness.py
"""

import pandas as pd

from polecoai.config import (
    ANALYSIS_GROUPS,
    INITIAL_RELEASE_DIR,
    RAW_DATA_DIR,
    REFERENCE_DATA_DIR,
    TABLES_DIR,
)
from polecoai.data import (
    employment_shares,
    load_initial_release,
    normalize_task_text,
)

EXPOSURE_DATA = REFERENCE_DATA_DIR / "job_exposure_frontline_subset.csv"
OEWS_DATA = RAW_DATA_DIR / "oews" / "oews_national_2023.csv"


def task_split_robustness() -> pd.DataFrame:
    mappings = pd.read_csv(INITIAL_RELEASE_DIR / "onet_task_mappings.csv")
    statements = pd.read_csv(INITIAL_RELEASE_DIR / "onet_task_statements.csv")
    mappings["task_key"] = normalize_task_text(mappings["task_name"])
    statements["task_key"] = normalize_task_text(statements["Task"])
    occupations = statements[["task_key", "O*NET-SOC Code"]].drop_duplicates()

    # Baseline: first match only
    base = mappings.merge(
        occupations.drop_duplicates("task_key"), on="task_key", how="left"
    )
    base_u = base.dropna(subset=["O*NET-SOC Code"]) \
        .groupby(base["O*NET-SOC Code"].str[:2])["pct"].sum()
    base_u = base_u / base_u.sum() * 100

    # Split: usage divided equally across all occupations sharing the task
    split = mappings.merge(occupations, on="task_key", how="left")
    n_occ = split.groupby("task_key")["O*NET-SOC Code"].transform("count")
    split["pct_split"] = split["pct"] / n_occ
    split_u = split.dropna(subset=["O*NET-SOC Code"]) \
        .groupby(split["O*NET-SOC Code"].str[:2])["pct_split"].sum()
    split_u = split_u / split_u.sum() * 100

    inputs = load_initial_release()
    emp = employment_shares(inputs["employment"], inputs["soc"])
    rows = []
    for g, name in ANALYSIS_GROUPS.items():
        rows.append({
            "group": name,
            "usage_first_match": round(base_u.get(g, 0), 3),
            "usage_split": round(split_u.get(g, 0), 3),
            "employment": round(emp.get(g, float("nan")), 3),
            "index_first_match": round(base_u.get(g, 0) / emp.get(g, 1), 3),
            "index_split": round(split_u.get(g, 0) / emp.get(g, 1), 3),
        })
    r = pd.DataFrame(rows)
    r.to_csv(TABLES_DIR / "robustness_task_split.csv", index=False)
    return r


def weighted_exposure_2026() -> pd.DataFrame | None:
    df = pd.read_csv(EXPOSURE_DATA)
    df["code2"] = df["occ_code"].str[:2]
    df["group"] = df["code2"].map(ANALYSIS_GROUPS)

    if not OEWS_DATA.exists():
        print("\n[F] OEWS detail file not found at data/raw/oews/oews_national_2023.csv")
        print("    -> reporting UNWEIGHTED group means only. To run the")
        print("       employment-weighted version, download the May 2023")
        print("       national OEWS file from bls.gov/oes/tables.htm, save the")
        print("       all-occupations sheet as CSV with columns OCC_CODE,TOT_EMP,")
        print("       and re-run this script.")
        return None

    w = pd.read_csv(OEWS_DATA, dtype={"OCC_CODE": str})
    w["TOT_EMP"] = pd.to_numeric(
        w["TOT_EMP"].astype(str).str.replace(",", ""), errors="coerce")
    g = df.merge(w[["OCC_CODE", "TOT_EMP"]], left_on="occ_code",
                 right_on="OCC_CODE", how="left")
    matched = g["TOT_EMP"].notna().mean()
    print(f"\n[F] OEWS match rate: {matched:.1%}")
    out = (g.dropna(subset=["TOT_EMP"]).groupby("group")
           .apply(lambda d: pd.Series({
               "weighted_mean": (d["observed_exposure"] * d["TOT_EMP"]).sum()
                                / d["TOT_EMP"].sum(),
               "unweighted_mean": d["observed_exposure"].mean(),
               "employment": d["TOT_EMP"].sum()}), include_groups=False)
           .round(3))
    out.to_csv(TABLES_DIR / "exposure_2026_weighted.csv")
    return out


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    print("=== E. Task-splitting robustness (shared tasks split equally) ===")
    print(task_split_robustness().to_string(index=False))
    res = weighted_exposure_2026()
    if res is not None:
        print("\n=== F. Employment-weighted Feb 2026 exposure ===")
        print(res.to_string())


if __name__ == "__main__":
    main()
