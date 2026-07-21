"""
Step 3: Extensions that make the paper.

  A. ROBUSTNESS  - drop technical occupations misclassified under SOC 43
                   (Bioinformatics Technicians, Computer Operators, etc.)
                   and recompute the frontline gap.
  B. TEMPORAL    - compare Feb 2025 vs Aug 2025 (AEI V3) task-level usage:
                   is the frontline gap closing as adoption spreads?
  C. COLLABORATION - within frontline tasks, is usage automation-style
                   (directive, feedback loop) or augmentation-style
                   (task iteration, learning, validation)? Compare to
                   computer/math occupations.

Run after 02_analysis.py:  python src/03_extensions.py
"""

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "release_2025_02_10"
V3 = ROOT / "data" / "v3_2025_08" / "global_task_data.csv"
FIGS = ROOT / "figures"
OUT = ROOT / "results"

FRONTLINE = {"41": "Sales", "43": "Office/Admin", "35": "Food Service",
             "39": "Personal Care"}
# SOC-43 occupations that are technical work misfiled under admin support
MISCLASSIFIED = {"43-9011.00", "43-9111.00", "43-9111.01", "43-9031.00"}
AUTOMATION = {"directive", "feedback loop"}
AUGMENTATION = {"task iteration", "learning", "validation"}


def norm(s: pd.Series) -> pd.Series:
    return (s.astype(str).str.lower().str.strip()
            .str.replace(r"\s+", " ", regex=True).str.rstrip("."))


def task_soc_map() -> pd.DataFrame:
    s = pd.read_csv(DATA / "onet_task_statements.csv")
    s["task_key"] = norm(s["Task"])
    return (s[["task_key", "O*NET-SOC Code", "Title"]]
            .drop_duplicates("task_key")
            .rename(columns={"O*NET-SOC Code": "soc_code", "Title": "occupation"}))


def employment_shares() -> pd.Series:
    soc = pd.read_csv(DATA / "SOC_Structure.csv")
    mg = soc[soc["Major Group"].notna()].copy()
    mg["code2"] = mg["Major Group"].astype(str).str[:2]
    names = mg.set_index("SOC or O*NET-SOC 2019 Title")["code2"]
    bls = pd.read_csv(DATA / "bls_employment_may_2023.csv")
    bls["code2"] = bls["SOC or O*NET-SOC 2019 Title"].map(names)
    emp = bls.dropna(subset=["code2"]).set_index("code2")["bls_distribution"]
    return emp / emp.sum() * 100


def usage_by_group(tasks: pd.DataFrame, pct_col: str,
                   exclude: set | None = None) -> pd.Series:
    t = tasks.dropna(subset=["soc_code"]).copy()
    if exclude:
        t = t[~t["soc_code"].isin(exclude)]
    u = t.groupby(t["soc_code"].str[:2])[pct_col].sum()
    return u / u.sum() * 100


# ---------- A. Robustness ----------
def robustness(feb: pd.DataFrame, emp: pd.Series) -> pd.DataFrame:
    base = usage_by_group(feb, "pct")
    strict = usage_by_group(feb, "pct", exclude=MISCLASSIFIED)
    rows = []
    for g, name in FRONTLINE.items():
        rows.append({
            "group": name,
            "usage_baseline": base.get(g, 0),
            "usage_strict": strict.get(g, 0),
            "employment": emp.get(g, float("nan")),
            "index_baseline": base.get(g, 0) / emp.get(g, 1),
            "index_strict": strict.get(g, 0) / emp.get(g, 1),
        })
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "robustness_misclassification.csv", index=False)
    return r


# ---------- B. Temporal ----------
def temporal(feb: pd.DataFrame, emp: pd.Series) -> pd.DataFrame:
    v3 = pd.read_csv(V3)
    aug = v3[(v3["facet"] == "onet_task") & (v3["variable"] == "onet_task_pct")]
    aug = aug[aug["cluster_name"].str.lower() != "none"].copy()
    aug["task_key"] = norm(aug["cluster_name"])
    aug = aug.merge(task_soc_map(), on="task_key", how="left")
    print(f"V3 task->SOC match rate: {aug['soc_code'].notna().mean():.1%} "
          f"({len(aug)} tasks)")

    u_feb = usage_by_group(feb, "pct")
    u_aug = usage_by_group(aug.rename(columns={"value": "pct"}), "pct")
    comp = pd.DataFrame({"feb_2025": u_feb, "aug_2025": u_aug,
                         "employment": emp}).dropna()
    comp["index_feb"] = comp["feb_2025"] / comp["employment"]
    comp["index_aug"] = comp["aug_2025"] / comp["employment"]
    comp["change_pp"] = comp["aug_2025"] - comp["feb_2025"]
    comp = comp.sort_values("index_aug", ascending=False)
    comp.to_csv(OUT / "temporal_feb_vs_aug_2025.csv")
    return comp


# ---------- C. Automation vs augmentation ----------
def collaboration_modes() -> pd.DataFrame:
    v3 = pd.read_csv(V3)
    tc = v3[(v3["facet"] == "onet_task::collaboration")
            & (v3["variable"] == "onet_task_collaboration_count")].copy()
    parts = tc["cluster_name"].str.rsplit("::", n=1, expand=True)
    tc["task"], tc["mode"] = parts[0], parts[1]
    tc = tc[tc["mode"].isin(AUTOMATION | AUGMENTATION)]
    tc["task_key"] = norm(tc["task"])
    tc = tc.merge(task_soc_map(), on="task_key", how="left").dropna(subset=["soc_code"])
    tc["code2"] = tc["soc_code"].str[:2]

    def label(code2: str) -> str:
        if code2 in FRONTLINE:
            return f"Frontline: {FRONTLINE[code2]}"
        if code2 == "15":
            return "Computer & Mathematical"
        return "All other"

    tc["bucket"] = tc["code2"].map(label)
    tc["is_auto"] = tc["mode"].isin(AUTOMATION)
    g = (tc.groupby("bucket")
         .apply(lambda d: pd.Series({
             "automation_share": d.loc[d["is_auto"], "value"].sum()
                                 / d["value"].sum() * 100,
             "conversations": d["value"].sum()}), include_groups=False)
         .sort_values("automation_share", ascending=False))
    g.to_csv(OUT / "automation_share_by_bucket.csv")
    return g


def make_figures(comp: pd.DataFrame, modes: pd.DataFrame) -> None:
    order = [g for g in comp.index if g in FRONTLINE] + ["15"]
    fig, ax = plt.subplots(figsize=(9, 6))
    x = range(len(order))
    labels = [FRONTLINE.get(g, "Computer/Math") for g in order]
    ax.bar([i - 0.2 for i in x], comp.loc[order, "index_feb"], width=0.4,
           color="#9a9a9a", label="Feb 2025")
    ax.bar([i + 0.2 for i in x], comp.loc[order, "index_aug"], width=0.4,
           color="#d97757", label="Aug 2025")
    ax.axhline(1, ls="--", c="black", lw=0.8)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_ylabel("Representation index (usage share / employment share)")
    ax.set_yscale("log")
    ax.set_title("Is the frontline gap closing? Feb vs Aug 2025")
    ax.legend(); fig.tight_layout()
    fig.savefig(FIGS / "fig4_temporal.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    m = modes.sort_values("automation_share")
    colors = ["#d97757" if b.startswith("Frontline") else "#9a9a9a"
              for b in m.index]
    ax.barh(m.index, m["automation_share"], color=colors)
    ax.axvline(50, ls="--", c="black", lw=0.8)
    ax.set_xlabel("Automation-style share of conversations (%)")
    ax.set_title("How AI is used when it reaches frontline tasks\n"
                 "(directive + feedback loop vs iteration/learning/validation)")
    fig.tight_layout()
    fig.savefig(FIGS / "fig5_automation_share.png", dpi=200); plt.close(fig)


def main() -> None:
    feb = pd.read_csv(DATA / "onet_task_mappings.csv")
    feb["task_key"] = norm(feb["task_name"])
    feb = feb.merge(task_soc_map(), on="task_key", how="left")
    emp = employment_shares()

    print("=== A. Robustness: excluding misclassified technical occupations ===")
    r = robustness(feb, emp)
    print(r.round(3).to_string(index=False))

    print("\n=== B. Temporal: Feb 2025 vs Aug 2025 ===")
    comp = temporal(feb, emp)
    keep = [g for g in comp.index if g in FRONTLINE or g == "15"]
    print(comp.loc[keep].round(3).to_string())

    print("\n=== C. Automation vs augmentation ===")
    modes = collaboration_modes()
    print(modes.round(1).to_string())

    make_figures(comp, modes)
    print(f"\nNew figures: fig4_temporal.png, fig5_automation_share.png -> {FIGS}")


if __name__ == "__main__":
    main()
