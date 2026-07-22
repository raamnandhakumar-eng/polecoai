"""Data-loading and occupational-mapping utilities shared across analyses."""

from collections.abc import Mapping

import pandas as pd

from .config import INITIAL_RELEASE_DIR


def normalize_task_text(series: pd.Series) -> pd.Series:
    """Normalize task statements for exact text joins across AEI files."""
    return (
        series.astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.rstrip(".")
    )


def load_initial_release() -> Mapping[str, pd.DataFrame]:
    """Load the five initial-release inputs used throughout the project."""
    filenames = {
        "mappings": "onet_task_mappings.csv",
        "statements": "onet_task_statements.csv",
        "soc": "SOC_Structure.csv",
        "employment": "bls_employment_may_2023.csv",
        "wages": "wage_data.csv",
    }
    return {
        name: pd.read_csv(INITIAL_RELEASE_DIR / filename)
        for name, filename in filenames.items()
    }


def major_group_names(soc_structure: pd.DataFrame) -> pd.Series:
    """Return a mapping from two-digit SOC major-group code to title."""
    major_groups = soc_structure[soc_structure["Major Group"].notna()].copy()
    major_groups["major_group"] = major_groups["Major Group"].astype(str).str[:2]
    return major_groups.set_index("major_group")["SOC or O*NET-SOC 2019 Title"]


def employment_shares(
    employment: pd.DataFrame,
    soc_structure: pd.DataFrame,
) -> pd.Series:
    """Calculate national employment shares by two-digit SOC major group."""
    group_names = major_group_names(soc_structure)
    title_to_code = {title: code for code, title in group_names.items()}
    employment = employment.copy()
    employment["major_group"] = employment[
        "SOC or O*NET-SOC 2019 Title"
    ].map(title_to_code)
    shares = (
        employment.dropna(subset=["major_group"])
        .set_index("major_group")["bls_distribution"]
    )
    return shares / shares.sum() * 100
