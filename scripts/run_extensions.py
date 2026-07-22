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

Run after run_analysis.py:  python scripts/run_extensions.py
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from polecoai.config import (
    FIGURES_DIR,
    FRONTLINE_GROUPS,
    INITIAL_RELEASE_DIR,
    TABLES_DIR,
    V3_PROCESSED_DIR,
)
from polecoai.data import (
    employment_shares as calculate_employment_shares,
    load_initial_release,
    normalize_task_text,
)

V3_TASKS = V3_PROCESSED_DIR / "global_task_data.csv"
# SOC-43 occupations that are technical work misfiled under admin support
MISCLASSIFIED = {"43-9011.00", "43-9111.00", "43-9111.01", "43-9031.00"}
AUTOMATION = {"directive", "feedback loop"}
AUGMENTATION = {"task iteration", "learning", "validation"}


def task_occupation_map() -> pd.DataFrame:
    statements = pd.read_csv(INITIAL_RELEASE_DIR / "onet_task_statements.csv")
    statements["task_key"] = normalize_task_text(statements["Task"])
    return (statements[["task_key", "O*NET-SOC Code", "Title"]]
            .drop_duplicates("task_key")
            .rename(columns={"O*NET-SOC Code": "soc_code", "Title": "occupation"}))


def employment_shares() -> pd.Series:
    inputs = load_initial_release()
    return calculate_employment_shares(inputs["employment"], inputs["soc"])


def usage_by_group(tasks: pd.DataFrame, pct_col: str,
                   exclude: set | None = None) -> pd.Series:
    included_tasks = tasks.dropna(subset=["soc_code"]).copy()
    if exclude:
        included_tasks = included_tasks[~included_tasks["soc_code"].isin(exclude)]
    usage = included_tasks.groupby(
        included_tasks["soc_code"].str[:2]
    )[pct_col].sum()
    return usage / usage.sum() * 100


# ---------- A. Robustness ----------
def robustness(feb: pd.DataFrame, emp: pd.Series) -> pd.DataFrame:
    baseline_usage = usage_by_group(feb, "pct")
    strict_usage = usage_by_group(feb, "pct", exclude=MISCLASSIFIED)
    rows = []
    for g, name in FRONTLINE_GROUPS.items():
        rows.append({
            "group": name,
            "usage_baseline": baseline_usage.get(g, 0),
            "usage_strict": strict_usage.get(g, 0),
            "employment": emp.get(g, float("nan")),
            "index_baseline": baseline_usage.get(g, 0) / emp.get(g, 1),
            "index_strict": strict_usage.get(g, 0) / emp.get(g, 1),
        })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES_DIR / "robustness_misclassification.csv", index=False)
    return result


# ---------- B. Temporal ----------
def temporal(feb: pd.DataFrame, emp: pd.Series) -> pd.DataFrame:
    v3_data = pd.read_csv(V3_TASKS)
    august_tasks = v3_data[
        (v3_data["facet"] == "onet_task")
        & (v3_data["variable"] == "onet_task_pct")
    ]
    august_tasks = august_tasks[
        august_tasks["cluster_name"].str.lower() != "none"
    ].copy()
    august_tasks["task_key"] = normalize_task_text(august_tasks["cluster_name"])
    august_tasks = august_tasks.merge(
        task_occupation_map(), on="task_key", how="left"
    )
    print(
        f"V3 task->SOC match rate: {august_tasks['soc_code'].notna().mean():.1%} "
        f"({len(august_tasks)} tasks)"
    )

    february_usage = usage_by_group(feb, "pct")
    august_usage = usage_by_group(
        august_tasks.rename(columns={"value": "pct"}), "pct"
    )
    comparison = pd.DataFrame(
        {
            "feb_2025": february_usage,
            "aug_2025": august_usage,
            "employment": emp,
        }
    ).dropna()
    comparison["index_feb"] = comparison["feb_2025"] / comparison["employment"]
    comparison["index_aug"] = comparison["aug_2025"] / comparison["employment"]
    comparison["change_pp"] = comparison["aug_2025"] - comparison["feb_2025"]
    comparison = comparison.sort_values("index_aug", ascending=False)
    comparison.to_csv(TABLES_DIR / "temporal_feb_vs_aug_2025.csv")
    return comparison


# ---------- C. Automation vs augmentation ----------
def collaboration_modes() -> pd.DataFrame:
    v3_data = pd.read_csv(V3_TASKS)
    conversations = v3_data[
        (v3_data["facet"] == "onet_task::collaboration")
        & (v3_data["variable"] == "onet_task_collaboration_count")
    ].copy()
    parts = conversations["cluster_name"].str.rsplit("::", n=1, expand=True)
    conversations["task"], conversations["mode"] = parts[0], parts[1]
    conversations = conversations[
        conversations["mode"].isin(AUTOMATION | AUGMENTATION)
    ]
    conversations["task_key"] = normalize_task_text(conversations["task"])
    conversations = conversations.merge(
        task_occupation_map(), on="task_key", how="left"
    ).dropna(subset=["soc_code"])
    conversations["code2"] = conversations["soc_code"].str[:2]

    def label(code2: str) -> str:
        if code2 in FRONTLINE_GROUPS:
            return f"Frontline: {FRONTLINE_GROUPS[code2]}"
        if code2 == "15":
            return "Computer & Mathematical"
        return "All other"

    conversations["bucket"] = conversations["code2"].map(label)
    conversations["is_auto"] = conversations["mode"].isin(AUTOMATION)
    summary = (conversations.groupby("bucket")
         .apply(lambda d: pd.Series({
             "automation_share": d.loc[d["is_auto"], "value"].sum()
                                 / d["value"].sum() * 100,
             "conversations": d["value"].sum()}), include_groups=False)
         .sort_values("automation_share", ascending=False))
    summary.to_csv(TABLES_DIR / "automation_share_by_bucket.csv")
    return summary


def make_figures(comp: pd.DataFrame, modes: pd.DataFrame) -> None:
    order = [g for g in comp.index if g in FRONTLINE_GROUPS] + ["15"]
    fig, ax = plt.subplots(figsize=(9, 6))
    x = range(len(order))
    labels = [FRONTLINE_GROUPS.get(g, "Computer/Math") for g in order]
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
    fig.savefig(FIGURES_DIR / "fig4_temporal.png", dpi=200); plt.close(fig)

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
    fig.savefig(FIGURES_DIR / "fig5_automation_share.png", dpi=200); plt.close(fig)


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    feb = pd.read_csv(INITIAL_RELEASE_DIR / "onet_task_mappings.csv")
    feb["task_key"] = normalize_task_text(feb["task_name"])
    feb = feb.merge(task_occupation_map(), on="task_key", how="left")
    emp = employment_shares()

    print("=== A. Robustness: excluding misclassified technical occupations ===")
    r = robustness(feb, emp)
    print(r.round(3).to_string(index=False))

    print("\n=== B. Temporal: Feb 2025 vs Aug 2025 ===")
    comp = temporal(feb, emp)
    keep = [g for g in comp.index if g in FRONTLINE_GROUPS or g == "15"]
    print(comp.loc[keep].round(3).to_string())

    print("\n=== C. Automation vs augmentation ===")
    modes = collaboration_modes()
    print(modes.round(1).to_string())

    make_figures(comp, modes)
    print(
        "\nNew figures: fig4_temporal.png, fig5_automation_share.png "
        f"-> {FIGURES_DIR}"
    )


if __name__ == "__main__":
    main()
