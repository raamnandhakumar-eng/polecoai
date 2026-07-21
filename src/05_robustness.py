"""
Step 5: Referee-driven robustness checks.

  E. TASK SPLITTING (join robustness): 272 of 18,428 O*NET task statements
     (1.5%) appear under multiple occupations. The baseline pipeline assigns
     each task's usage to ONE occupation (first match). Here each shared
     task's usage share is split EQUALLY across all occupations listing it,
     and the representation index is recomputed.

  F. EMPLOYMENT WEIGHTING for the Feb 2026 exposure means: if a detailed
     OEWS national file is present at data/oews/oews_national_2023.csv
     (columns OCC_CODE, TOT_EMP -- the standard BLS national XLSX saved as
     CSV), group means are recomputed employment-weighted. Otherwise the
     script prints unweighted means with a warning.

Run: python src/05_robustness.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "release_2025_02_10"
EXPOSURE = ROOT / "data" / "labor_market_impacts_2026" / "job_exposure_frontline_subset.csv"
OEWS = ROOT / "data" / "oews" / "oews_national_2023.csv"
OUT = ROOT / "results"

FRONTLINE = {"41": "Sales", "43": "Office/Admin", "35": "Food Service",
             "39": "Personal Care"}
GROUPS = dict(FRONTLINE, **{"15": "Computer & Mathematical"})


def norm(s: pd.Series) -> pd.Series:
    return (s.astype(str).str.lower().str.strip()
            .str.replace(r"\s+", " ", regex=True).str.rstrip("."))


def employment_shares() -> pd.Series:
    soc = pd.read_csv(DATA / "SOC_Structure.csv")
    mg = soc[soc["Major Group"].notna()].copy()
    mg["code2"] = mg["Major Group"].astype(str).str[:2]
    names = mg.set_index("SOC or O*NET-SOC 2019 Title")["code2"]
    bls = pd.read_csv(DATA / "bls_employment_may_2023.csv")
    bls["code2"] = bls["SOC or O*NET-SOC 2019 Title"].map(names)
    emp = bls.dropna(subset=["code2"]).set_index("code2")["bls_distribution"]
    return emp / emp.sum() * 100


def task_split_robustness() -> pd.DataFrame:
    m = pd.read_csv(DATA / "onet_task_mappings.csv")
    s = pd.read_csv(DATA / "onet_task_statements.csv")
    m["task_key"] = norm(m["task_name"])
    s["task_key"] = norm(s["Task"])
    occs = s[["task_key", "O*NET-SOC Code"]].drop_duplicates()

    # Baseline: first match only
    base = m.merge(occs.drop_duplicates("task_key"), on="task_key", how="left")
    base_u = base.dropna(subset=["O*NET-SOC Code"]) \
        .groupby(base["O*NET-SOC Code"].str[:2])["pct"].sum()
    base_u = base_u / base_u.sum() * 100

    # Split: usage divided equally across all occupations sharing the task
    split = m.merge(occs, on="task_key", how="left")
    n_occ = split.groupby("task_key")["O*NET-SOC Code"].transform("count")
    split["pct_split"] = split["pct"] / n_occ
    split_u = split.dropna(subset=["O*NET-SOC Code"]) \
        .groupby(split["O*NET-SOC Code"].str[:2])["pct_split"].sum()
    split_u = split_u / split_u.sum() * 100

    emp = employment_shares()
    rows = []
    for g, name in GROUPS.items():
        rows.append({
            "group": name,
            "usage_first_match": round(base_u.get(g, 0), 3),
            "usage_split": round(split_u.get(g, 0), 3),
            "employment": round(emp.get(g, float("nan")), 3),
            "index_first_match": round(base_u.get(g, 0) / emp.get(g, 1), 3),
            "index_split": round(split_u.get(g, 0) / emp.get(g, 1), 3),
        })
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "robustness_task_split.csv", index=False)
    return r


def weighted_exposure_2026() -> pd.DataFrame | None:
    df = pd.read_csv(EXPOSURE)
    df["code2"] = df["occ_code"].str[:2]
    df["group"] = df["code2"].map(GROUPS)

    if not OEWS.exists():
        print("\n[F] OEWS detail file not found at data/oews/oews_national_2023.csv")
        print("    -> reporting UNWEIGHTED group means only. To run the")
        print("       employment-weighted version, download the May 2023")
        print("       national OEWS file from bls.gov/oes/tables.htm, save the")
        print("       all-occupations sheet as CSV with columns OCC_CODE,TOT_EMP,")
        print("       and re-run this script.")
        return None

    w = pd.read_csv(OEWS, dtype={"OCC_CODE": str})
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
    out.to_csv(OUT / "exposure_2026_weighted.csv")
    return out


def main() -> None:
    print("=== E. Task-splitting robustness (shared tasks split equally) ===")
    print(task_split_robustness().to_string(index=False))
    res = weighted_exposure_2026()
    if res is not None:
        print("\n=== F. Employment-weighted Feb 2026 exposure ===")
        print(res.to_string())


if __name__ == "__main__":
    main()
