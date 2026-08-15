"""Occupation-level adoption, alternative-frontline, and access-gap models."""

from collections.abc import Iterable
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .config import FRONTLINE_GROUPS
from .data import employment_shares, normalize_task_text


ONET_MEMBERS = {
    "activities": "db_30_2_text/Work Activities.txt",
    "context": "db_30_2_text/Work Context.txt",
    "education": "db_30_2_text/Education, Training, and Experience.txt",
}

PHYSICAL_CONTEXT = [
    "Spend Time Standing",
    "Spend Time Walking or Running",
    "Outdoors, Exposed to All Weather Conditions",
    "Indoors, Not Environmentally Controlled",
]

CUSTOMER_CONTEXT = [
    "Contact With Others",
    "Face-to-Face Discussions with Individuals and Within Teams",
    "Deal With External Customers or the Public in General",
]

CONTINUOUS_TWO_PART = [
    "log_wage",
    "education_index",
    "computer_use_score",
    "physical_presence_index",
]

TWO_PART_TERMS = [
    "log_wage",
    "frontline_soc",
    "education_index",
    "computer_use_score",
    "physical_presence_index",
]

ACCESS_GAP_TERMS = [
    *TWO_PART_TERMS,
    "customer_facing_index",
]


def normalize_occ_code(series: pd.Series) -> pd.Series:
    """Collapse O*NET detailed codes to their six-digit SOC base."""
    return series.astype(str).str.strip().str.replace(r"\.\d+$", "", regex=True)


def _read_onet_member(path: Path, member: str) -> pd.DataFrame:
    with ZipFile(path) as archive:
        return pd.read_csv(archive.open(member), sep="\t", encoding="latin-1")


def _descriptor_wide(
    data: pd.DataFrame,
    names: Iterable[str],
    scale_id: str,
) -> pd.DataFrame:
    selected = data[
        (data["Scale ID"] == scale_id) & data["Element Name"].isin(names)
    ].copy()
    selected["occ_code"] = normalize_occ_code(selected["O*NET-SOC Code"])
    selected["Data Value"] = pd.to_numeric(
        selected["Data Value"], errors="coerce"
    )
    return (
        selected.groupby(["occ_code", "Element Name"], as_index=False)[
            "Data Value"
        ]
        .mean()
        .pivot(index="occ_code", columns="Element Name", values="Data Value")
        .reset_index()
    )


def build_onet_controls(path: Path) -> pd.DataFrame:
    """Build transparent O*NET education, computer, and work-context measures."""
    activities = _read_onet_member(path, ONET_MEMBERS["activities"])
    context = _read_onet_member(path, ONET_MEMBERS["context"])
    education = _read_onet_member(path, ONET_MEMBERS["education"])

    computer = _descriptor_wide(
        activities, ["Working with Computers"], scale_id="IM"
    ).rename(columns={"Working with Computers": "computer_use_score"})

    context_wide = _descriptor_wide(
        context, PHYSICAL_CONTEXT + CUSTOMER_CONTEXT, scale_id="CX"
    )
    context_wide["physical_presence_index"] = context_wide[
        PHYSICAL_CONTEXT
    ].mean(axis=1, skipna=False)
    context_wide["customer_facing_index"] = context_wide[
        CUSTOMER_CONTEXT
    ].mean(axis=1, skipna=False)

    required = education[
        (education["Element Name"] == "Required Level of Education")
        & (education["Scale ID"] == "RL")
    ].copy()
    required["occ_code"] = normalize_occ_code(required["O*NET-SOC Code"])
    required["Category"] = pd.to_numeric(required["Category"], errors="coerce")
    required["Data Value"] = pd.to_numeric(
        required["Data Value"], errors="coerce"
    )

    def expected_category(group: pd.DataFrame) -> float:
        weights = group["Data Value"].to_numpy()
        categories = group["Category"].to_numpy()
        if not np.isfinite(weights).all() or weights.sum() <= 0:
            return float("nan")
        return float(np.average(categories, weights=weights))

    education_index = (
        required.groupby("occ_code")
        .apply(expected_category, include_groups=False)
        .rename("education_index")
        .reset_index()
    )

    controls = computer.merge(
        context_wide[
            ["occ_code", "physical_presence_index", "customer_facing_index"]
        ],
        on="occ_code",
        how="outer",
    ).merge(education_index, on="occ_code", how="outer")
    return controls


def build_theoretical_exposure(path: Path) -> pd.DataFrame:
    """Aggregate GPTs-are-GPTs task capability scores to six-digit SOC codes."""
    data = pd.read_csv(path)
    data["occ_code"] = normalize_occ_code(data["O*NET-SOC Code"])
    return (
        data.groupby("occ_code", as_index=False)
        .agg(
            theoretical_exposure=("dv_rating_gamma", "mean"),
            human_theoretical_exposure=("human_rating_gamma", "mean"),
        )
    )


def build_oews_controls(path: Path) -> pd.DataFrame:
    """Return May 2023 OEWS employment and wage controls by detailed SOC."""
    with ZipFile(path) as archive:
        member = next(
            name for name in archive.namelist() if name.endswith(".xlsx")
        )
        with archive.open(member) as workbook:
            data = pd.read_excel(workbook)
    data = data[data["O_GROUP"].astype(str).str.lower() == "detailed"].copy()
    data["occ_code"] = normalize_occ_code(data["OCC_CODE"])
    data["annual_mean_wage"] = pd.to_numeric(data["A_MEAN"], errors="coerce")
    data["total_employment"] = pd.to_numeric(data["TOT_EMP"], errors="coerce")
    return (
        data.groupby("occ_code", as_index=False)
        .agg(
            annual_mean_wage=("annual_mean_wage", "max"),
            total_employment=("total_employment", "max"),
        )
    )


def build_task_usage(
    mappings_path: Path,
    statements_path: Path,
    crosswalk_path: Path,
) -> pd.DataFrame:
    """Crosswalk February 2025 task usage from O*NET-SOC 2010 to 2019."""
    mappings = pd.read_csv(mappings_path)
    statements = pd.read_csv(statements_path)
    mappings["task_key"] = normalize_task_text(mappings["task_name"])
    statements["task_key"] = normalize_task_text(statements["Task"])
    task_codes = (
        statements[["task_key", "O*NET-SOC Code"]]
        .drop_duplicates("task_key")
        .rename(columns={"O*NET-SOC Code": "old_onet_code"})
    )
    tasks = mappings.merge(task_codes, on="task_key", how="left").dropna(
        subset=["old_onet_code"]
    )
    old_usage = tasks.groupby("old_onet_code", as_index=False)["pct"].sum()
    crosswalk = pd.read_csv(crosswalk_path)[
        ["O*NET-SOC 2010 Code", "O*NET-SOC 2019 Code"]
    ].rename(
        columns={
            "O*NET-SOC 2010 Code": "old_onet_code",
            "O*NET-SOC 2019 Code": "new_onet_code",
        }
    )
    split = old_usage.merge(crosswalk, on="old_onet_code", how="left")
    split["new_onet_code"] = split["new_onet_code"].fillna(
        split["old_onet_code"]
    )
    targets = split.groupby("old_onet_code")["new_onet_code"].transform(
        "nunique"
    )
    split["task_usage_pct"] = split["pct"] / targets
    split["frontline_origin_task_usage_pct"] = np.where(
        split["old_onet_code"].str[:2].isin(FRONTLINE_GROUPS),
        split["task_usage_pct"],
        0,
    )
    split["occ_code"] = normalize_occ_code(split["new_onet_code"])
    usage = split.groupby("occ_code", as_index=False).agg(
        task_usage_pct=("task_usage_pct", "sum"),
        frontline_origin_task_usage_pct=(
            "frontline_origin_task_usage_pct",
            "sum",
        ),
    )
    normalization = 100 / usage["task_usage_pct"].sum()
    usage["task_usage_pct"] *= normalization
    usage["frontline_origin_task_usage_pct"] *= normalization
    return usage


def build_adoption_dataset(
    observed_path: Path,
    theoretical_path: Path,
    oews_path: Path,
    onet_path: Path,
    task_mappings_path: Path,
    task_statements_path: Path,
    crosswalk_path: Path,
    group_employment_path: Path,
    soc_structure_path: Path,
) -> pd.DataFrame:
    """Merge observed use, theoretical capability, wages, and O*NET controls."""
    observed = pd.read_csv(observed_path).rename(
        columns={"title": "occupation_title"}
    )
    observed["occ_code"] = normalize_occ_code(observed["occ_code"])
    data = (
        observed.merge(
            build_theoretical_exposure(theoretical_path),
            on="occ_code",
            how="outer",
        )
        .merge(build_oews_controls(oews_path), on="occ_code", how="outer")
        .merge(build_onet_controls(onet_path), on="occ_code", how="outer")
        .merge(
            build_task_usage(
                task_mappings_path, task_statements_path, crosswalk_path
            ),
            on="occ_code",
            how="outer",
        )
    )
    data["major_group"] = data["occ_code"].str[:2]
    data["frontline_soc"] = data["major_group"].isin(
        FRONTLINE_GROUPS
    ).astype(int)
    data["task_usage_pct"] = data["task_usage_pct"].fillna(0)
    data["frontline_origin_task_usage_pct"] = data[
        "frontline_origin_task_usage_pct"
    ].fillna(0)
    group_employment = employment_shares(
        pd.read_csv(group_employment_path),
        pd.read_csv(soc_structure_path),
    )
    available_group_employment = data.groupby("major_group")[
        "total_employment"
    ].transform("sum")
    data["calibrated_employment_pct"] = (
        data["total_employment"]
        / available_group_employment
        * data["major_group"].map(group_employment)
    )
    data["any_ai_use"] = np.where(
        data["observed_exposure"].notna(),
        (data["observed_exposure"] > 0).astype(float),
        np.nan,
    )
    data["log_wage"] = np.log(data["annual_mean_wage"])
    data["ai_access_gap"] = (
        data["theoretical_exposure"] - data["observed_exposure"]
    )

    for index, name in [
        ("physical_presence_index", "frontline_physical"),
        ("customer_facing_index", "frontline_customer"),
    ]:
        threshold = data[index].quantile(0.75)
        data[name] = np.where(data[index].notna(), (data[index] >= threshold), np.nan)

    return data.sort_values("occ_code").reset_index(drop=True)


def _standardized_design(
    data: pd.DataFrame,
    terms: list[str],
    continuous: list[str],
) -> tuple[pd.DataFrame, dict[str, tuple[float, float]]]:
    design = data[terms].astype(float).copy()
    scales: dict[str, tuple[float, float]] = {}
    for term in continuous:
        mean = float(design[term].mean())
        standard_deviation = float(design[term].std(ddof=0))
        if standard_deviation == 0:
            raise ValueError(f"cannot standardize constant predictor: {term}")
        design[term] = (design[term] - mean) / standard_deviation
        scales[term] = (mean, standard_deviation)
    return sm.add_constant(design, has_constant="add"), scales


def estimate_two_part_models(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate a logit extensive margin and positive-use log-OLS intensity."""
    required = ["observed_exposure", "any_ai_use", *TWO_PART_TERMS]
    sample = data.dropna(subset=required).copy()
    design, _ = _standardized_design(
        sample, TWO_PART_TERMS, CONTINUOUS_TWO_PART
    )

    stage1 = sm.Logit(sample["any_ai_use"], design).fit(
        disp=False, maxiter=200, cov_type="HC1"
    )
    stage1_ci = stage1.conf_int()
    rows = []
    for term in design.columns:
        rows.append(
            {
                "stage": "stage1_any_use_logit",
                "estimate_type": "log_odds",
                "term": term,
                "estimate": stage1.params[term],
                "se_hc1": stage1.bse[term],
                "p_value": stage1.pvalues[term],
                "ci_low": stage1_ci.loc[term, 0],
                "ci_high": stage1_ci.loc[term, 1],
                "fit_statistic": stage1.prsquared,
                "n": int(stage1.nobs),
            }
        )

    marginal = stage1.get_margeff(at="overall", method="dydx")
    marginal_frame = marginal.summary_frame()
    for term, result in marginal_frame.iterrows():
        rows.append(
            {
                "stage": "stage1_any_use_logit",
                "estimate_type": "average_marginal_effect",
                "term": term,
                "estimate": result["dy/dx"],
                "se_hc1": result["Std. Err."],
                "p_value": result["Pr(>|z|)"],
                "ci_low": result["Conf. Int. Low"],
                "ci_high": result["Cont. Int. Hi."],
                "fit_statistic": stage1.prsquared,
                "n": int(stage1.nobs),
            }
        )

    positive = sample["observed_exposure"] > 0
    stage2 = sm.OLS(
        np.log(sample.loc[positive, "observed_exposure"]),
        design.loc[positive],
    ).fit(cov_type="HC1")
    stage2_ci = stage2.conf_int()
    for term in design.columns:
        rows.append(
            {
                "stage": "stage2_positive_use_ols",
                "estimate_type": "log_intensity_coefficient",
                "term": term,
                "estimate": stage2.params[term],
                "se_hc1": stage2.bse[term],
                "p_value": stage2.pvalues[term],
                "ci_low": stage2_ci.loc[term, 0],
                "ci_high": stage2_ci.loc[term, 1],
                "fit_statistic": stage2.rsquared,
                "n": int(stage2.nobs),
            }
        )
    return pd.DataFrame(rows)


def estimate_access_gap_model(data: pd.DataFrame) -> pd.DataFrame:
    """Regress the theoretical-minus-observed access gap on job features."""
    required = ["ai_access_gap", *ACCESS_GAP_TERMS]
    sample = data.dropna(subset=required).copy()
    continuous = [
        term for term in ACCESS_GAP_TERMS if term != "frontline_soc"
    ]
    design, _ = _standardized_design(sample, ACCESS_GAP_TERMS, continuous)
    model = sm.OLS(sample["ai_access_gap"], design).fit(cov_type="HC1")
    confidence = model.conf_int()
    return pd.DataFrame(
        {
            "term": design.columns,
            "coefficient": model.params,
            "se_hc1": model.bse,
            "p_value": model.pvalues,
            "ci_low": confidence[0],
            "ci_high": confidence[1],
            "r_squared": model.rsquared,
            "n": int(model.nobs),
        }
    ).reset_index(drop=True)


def summarize_frontline_definitions(data: pd.DataFrame) -> pd.DataFrame:
    """Recalculate task-usage representation under three frontline definitions."""
    definitions = {
        "A_current_soc_groups": "frontline_soc",
        "B_high_physical_presence": "frontline_physical",
        "C_high_customer_facing": "frontline_customer",
    }
    rows = []
    for label, column in definitions.items():
        sample = data.dropna(subset=[column, "task_usage_pct"]).copy()
        sample[column] = sample[column].astype(bool)
        threshold = np.nan
        if column == "frontline_physical":
            threshold = data["physical_presence_index"].quantile(0.75)
        elif column == "frontline_customer":
            threshold = data["customer_facing_index"].quantile(0.75)

        inside = sample[column]
        usage_coverage = sample["task_usage_pct"].sum()
        employment_coverage = sample["calibrated_employment_pct"].sum()
        if column == "frontline_soc":
            inside_usage = sample["frontline_origin_task_usage_pct"].sum()
        else:
            inside_usage = sample.loc[inside, "task_usage_pct"].sum()
        usage_share = inside_usage / usage_coverage * 100
        employment_share = (
            sample.loc[inside, "calibrated_employment_pct"].sum()
            / employment_coverage
            * 100
        )
        rows.append(
            {
                "definition": label,
                "threshold": threshold,
                "usage_share_pct": usage_share,
                "employment_share_pct": employment_share,
                "representation_index": usage_share / employment_share,
                "usage_minus_employment_pp": usage_share - employment_share,
                "usage_coverage_pct": usage_coverage,
                "employment_coverage_pct": employment_coverage,
                "n_inside": int(inside.sum()),
                "n_outside": int((~inside).sum()),
            }
        )
    return pd.DataFrame(rows)
