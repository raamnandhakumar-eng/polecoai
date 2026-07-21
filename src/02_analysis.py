"""
The Frontline Exposure Gap — analysis pipeline (matched to real AEI schemas).

Research question:
    How does real-world AI usage (Claude conversations mapped to O*NET
    tasks) compare to employment across frontline occupations -- retail
    sales, customer service, food service -- and which frontline tasks
    ARE being done with AI despite low overall adoption?

Run after 01_download_data.py:  python src/02_analysis.py
Outputs -> data/*.csv and figures/*.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "release_2025_02_10"
FIGS = ROOT / "figures"
OUT = ROOT / "results"

FRONTLINE_GROUPS = {
    "41": "Sales and Related",
    "43": "Office and Administrative Support",
    "35": "Food Preparation and Serving Related",
    "39": "Personal Care and Service",
}


def norm(s: pd.Series) -> pd.Series:
    return (
        s.astype(str).str.lower().str.strip()
        .str.replace(r"\s+", " ", regex=True).str.rstrip(".")
    )


def load():
    read = lambda n: pd.read_csv(DATA / n)
    return {
        "mappings": read("onet_task_mappings.csv"),      # task_name, pct
        "statements": read("onet_task_statements.csv"),  # O*NET-SOC Code, Title, Task
        "soc": read("SOC_Structure.csv"),                # Major Group, ..., 2019 Title
        "bls": read("bls_employment_may_2023.csv"),      # group title, bls_distribution
        "wage": read("wage_data.csv"),                   # SOCcode, MedianSalary, ...
    }


def group_names(soc: pd.DataFrame) -> pd.Series:
    """Map 2-digit major-group code -> group title."""
    mg = soc[soc["Major Group"].notna()].copy()
    mg["code2"] = mg["Major Group"].astype(str).str[:2]
    return mg.set_index("code2")["SOC or O*NET-SOC 2019 Title"]


def build_task_table(dfs) -> pd.DataFrame:
    m, s = dfs["mappings"].copy(), dfs["statements"].copy()
    m["task_key"] = norm(m["task_name"])
    s["task_key"] = norm(s["Task"])
    merged = m.merge(
        s[["task_key", "O*NET-SOC Code", "Title"]].drop_duplicates("task_key"),
        on="task_key", how="left",
    ).rename(columns={"O*NET-SOC Code": "soc_code", "Title": "occupation"})
    merged["major_group"] = merged["soc_code"].astype(str).str[:2]
    print(f"Task->SOC match rate: {merged['soc_code'].notna().mean():.1%} "
          f"({len(merged)} tasks)")
    return merged


def representation(dfs, tasks) -> pd.DataFrame:
    names = group_names(dfs["soc"])
    usage = (tasks.dropna(subset=["soc_code"])
             .groupby("major_group")["pct"].sum().rename("usage_pct"))
    usage = usage / usage.sum() * 100

    bls = dfs["bls"].copy()
    title_to_code = {v: k for k, v in names.items()}
    bls["code2"] = bls["SOC or O*NET-SOC 2019 Title"].map(title_to_code)
    emp = bls.dropna(subset=["code2"]).set_index("code2")["bls_distribution"]
    emp = (emp / emp.sum() * 100).rename("employment_pct")

    rep = pd.concat([usage, emp], axis=1).dropna()
    rep["representation_index"] = rep["usage_pct"] / rep["employment_pct"]
    rep["group_name"] = names.reindex(rep.index)
    rep = rep.sort_values("representation_index", ascending=False)
    rep.to_csv(OUT / "representation_by_group.csv")
    return rep


def frontline_tasks(tasks) -> pd.DataFrame:
    ft = (tasks[tasks["major_group"].isin(FRONTLINE_GROUPS)]
          .sort_values("pct", ascending=False).head(25).copy())
    ft["group"] = ft["major_group"].map(FRONTLINE_GROUPS)
    ft.to_csv(OUT / "frontline_tasks.csv", index=False)
    return ft


def wage_gradient(dfs, tasks) -> pd.DataFrame:
    w = dfs["wage"].copy()
    w["soc6"] = w["SOCcode"].astype(str).str[:7]
    w = (w.groupby("soc6", as_index=False)["MedianSalary"].median()
         .rename(columns={"MedianSalary": "median_wage"}))
    occ = (tasks.dropna(subset=["soc_code"])
           .assign(soc6=lambda d: d["soc_code"].astype(str).str[:7])
           .groupby("soc6")["pct"].sum().rename("usage_pct").reset_index())
    g = occ.merge(w, on="soc6", how="inner").dropna()
    g["frontline"] = g["soc6"].str[:2].isin(FRONTLINE_GROUPS)
    return g


def wage_regressions(wg: pd.DataFrame) -> pd.DataFrame:
    """Estimate the two paper specifications with HC1 robust standard errors."""
    y = np.log(wg["usage_pct"].to_numpy())
    log_wage = np.log(wg["median_wage"].to_numpy())
    frontline = wg["frontline"].astype(float).to_numpy()
    specifications = {
        "log_wage_only": (np.column_stack([np.ones(len(wg)), log_wage]),
                          ["intercept", "log_wage"]),
        "log_wage_frontline": (
            np.column_stack([np.ones(len(wg)), log_wage, frontline]),
            ["intercept", "log_wage", "frontline"]),
    }

    rows = []
    for model, (x, terms) in specifications.items():
        beta = np.linalg.solve(x.T @ x, x.T @ y)
        residual = y - x @ beta
        n, k = x.shape
        xtx_inv = np.linalg.inv(x.T @ x)
        meat = x.T @ ((residual ** 2)[:, None] * x)
        covariance_hc1 = (n / (n - k)) * xtx_inv @ meat @ xtx_inv
        se_hc1 = np.sqrt(np.diag(covariance_hc1))
        r_squared = 1 - ((residual @ residual)
                         / ((y - y.mean()) @ (y - y.mean())))
        for term, coefficient, standard_error in zip(terms, beta, se_hc1):
            rows.append({
                "model": model,
                "term": term,
                "coefficient": coefficient,
                "se_hc1": standard_error,
                "r_squared": r_squared,
                "n": n,
            })

    result = pd.DataFrame(rows)
    result.to_csv(OUT / "regression_usage_wage.csv", index=False)
    return result


def make_figures(rep, ft, wg):
    FIGS.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    r = rep.sort_values("usage_pct")
    labels = r["group_name"].fillna(r.index.to_series()).str.replace(
        " Occupations", "", regex=False).str.slice(0, 40)
    colors = ["#d97757" if i in FRONTLINE_GROUPS else "#9a9a9a" for i in r.index]
    ax.barh(labels, r["usage_pct"], color=colors, alpha=0.9, label="Claude usage share")
    ax.scatter(r["employment_pct"], labels, color="black", zorder=3, s=24,
               label="US employment share")
    ax.set_xlabel("Percent")
    ax.set_title("AI usage vs employment share by occupation group\n"
                 "(frontline groups in orange)")
    ax.legend(); fig.tight_layout()
    fig.savefig(FIGS / "fig1_representation.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 7))
    f = ft.sort_values("pct").tail(15)
    ax.barh(f["task_name"].str.slice(0, 62), f["pct"], color="#d97757")
    ax.set_xlabel("Share of Claude conversations (%)")
    ax.set_title("Top frontline (sales/admin/service) tasks done with AI")
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_frontline_tasks.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    base, fl = wg[~wg["frontline"]], wg[wg["frontline"]]
    ax.scatter(base["median_wage"], base["usage_pct"], s=14, alpha=0.35,
               color="#9a9a9a", label="Other occupations")
    ax.scatter(fl["median_wage"], fl["usage_pct"], s=28, alpha=0.9,
               color="#d97757", label="Frontline occupations")
    ax.set_xlabel("Median annual wage ($)"); ax.set_ylabel("Usage share (%), log scale")
    ax.set_yscale("log"); ax.legend()
    ax.set_title("AI usage vs wages: where frontline work sits")
    fig.tight_layout()
    fig.savefig(FIGS / "fig3_wage_gradient.png", dpi=200); plt.close(fig)


def main():
    dfs = load()
    tasks = build_task_table(dfs)
    rep = representation(dfs, tasks)
    ft = frontline_tasks(tasks)
    wg = wage_gradient(dfs, tasks)
    regressions = wage_regressions(wg)
    make_figures(rep, ft, wg)

    print("\n=== Headline numbers ===")
    pd.set_option("display.width", 140)
    cols = ["group_name", "usage_pct", "employment_pct", "representation_index"]
    print(rep[cols].round(2).to_string())
    print("\nFrontline usage total:",
          round(rep.loc[rep.index.isin(FRONTLINE_GROUPS), "usage_pct"].sum(), 2), "%")
    print("Frontline employment total:",
          round(rep.loc[rep.index.isin(FRONTLINE_GROUPS), "employment_pct"].sum(), 2), "%")
    print("\nTop 10 frontline tasks:")
    print(ft[["task_name", "occupation", "pct"]].head(10).to_string(index=False))
    print("\nOccupation-level wage regressions (HC1 standard errors):")
    print(regressions.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
