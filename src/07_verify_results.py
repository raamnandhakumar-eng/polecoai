"""Assert the paper's headline values against the generated result tables.

Run after scripts 02-05:

    python src/07_verify_results.py
"""

from pathlib import Path
import hashlib
import math

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
EXPOSURE = (ROOT / "data" / "labor_market_impacts_2026"
            / "job_exposure_frontline_subset.csv")
V3_RAW = (ROOT / "data" / "release_2025_09_15" / "data" / "intermediate"
          / "aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv")
V3_SHA256 = "c8ef9c5eee0c42febc73e358ecc7d2358e0a0ce3b50122c0c15ae8ec569aceff"
FRONTLINE_CODES = {"41", "43", "35", "39"}

OFFICIAL_EXPOSURE_CHECKS = {
    "43-4051": ("Customer Service Representatives", 0.7011),
    "41-2011": ("Cashiers", 0.0846),
    "41-2031": ("Retail Salespersons", 0.3222),
    "15-1251": ("Computer Programmers", 0.7451),
    "15-1252": ("Software Developers", 0.2880),
    "35-9031": ("Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop", 0.0734),
    "39-6012": ("Concierges", 0.1875),
    "41-4012": ("Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products", 0.6279),
    "41-3041": ("Travel Agents", 0.4054),
    "43-9021": ("Data Entry Keyers", 0.6707),
    "43-4171": ("Receptionists and Information Clerks", 0.4338),
    "43-6014": ("Secretaries and Administrative Assistants, Except Legal, Medical, and Executive", 0.4528),
    "43-9111": ("Statistical Assistants", 0.5099),
}


def close(actual: float, expected: float, tolerance: float = 1e-9) -> None:
    if not math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance):
        raise AssertionError(f"expected {expected}, got {actual}")


def verify_representation() -> None:
    frame = pd.read_csv(RESULTS / "representation_by_group.csv", dtype={0: str})
    code_col = frame.columns[0]
    frame[code_col] = frame[code_col].astype(str).str.zfill(2)
    frontline = frame[frame[code_col].isin(FRONTLINE_CODES)]
    close(frontline["usage_pct"].sum(), 11.129672930844415)
    close(frontline["employment_pct"].sum(), 31.742760326095082)
    sales = frame.loc[frame[code_col] == "41", "representation_index"].iloc[0]
    close(sales, 0.257578501849144)
    print("PASS 02: frontline usage 11.13%; employment 31.74%; Sales index 0.26")


def verify_extensions() -> None:
    frame = pd.read_csv(RESULTS / "robustness_misclassification.csv")
    admin = frame.loc[frame["group"] == "Office/Admin"].iloc[0]
    close(admin["index_baseline"], 0.6445694655484034)
    close(admin["index_strict"], 0.3378358852874682)
    print("PASS 03: Office/Admin index 0.645 -> 0.338")


def verify_wage_regressions() -> None:
    frame = pd.read_csv(RESULTS / "regression_usage_wage.csv")
    indexed = frame.set_index(["model", "term"])
    checks = {
        ("log_wage_only", "log_wage"): (0.38378931, 0.18484632),
        ("log_wage_frontline", "log_wage"): (0.40791872, 0.20632653),
        ("log_wage_frontline", "frontline"): (0.18565227, 0.19010712),
    }
    for key, (coefficient, se_hc1) in checks.items():
        row = indexed.loc[key]
        close(float(row["coefficient"]), coefficient, tolerance=1e-7)
        close(float(row["se_hc1"]), se_hc1, tolerance=1e-7)
        if int(row["n"]) != 585:
            raise AssertionError(f"{key}: expected n=585, got {row['n']}")
    print("PASS wage regressions: 0.38 (0.19), 0.41 (0.21), frontline 0.19 (0.19)")


def verify_task_split() -> None:
    frame = pd.read_csv(RESULTS / "robustness_task_split.csv")
    frontline = frame[frame["group"].isin(
        ["Sales", "Office/Admin", "Food Service", "Personal Care"])]
    if not (frontline["index_first_match"] == frontline["index_split"]).all():
        raise AssertionError("one or more frontline indices changed under task splitting")
    print("PASS 05: all four frontline indices unchanged under task splitting")


def verify_latest_exposure() -> None:
    frame = pd.read_csv(EXPOSURE, dtype={"occ_code": str}).set_index("occ_code")
    for code, (title, expected) in OFFICIAL_EXPOSURE_CHECKS.items():
        if code not in frame.index:
            raise AssertionError(f"missing occupation {code}")
        row = frame.loc[code]
        if row["title"] != title:
            raise AssertionError(f"{code}: expected title {title!r}, got {row['title']!r}")
        close(float(row["observed_exposure"]), expected)
    print("PASS 04: Customer Service Representatives 0.7011")
    print("PASS official spot-check: 3 requested + 10 additional rows")


def verify_official_v3() -> None:
    if not V3_RAW.exists():
        raise AssertionError(f"official V3 source missing: {V3_RAW}")
    digest = hashlib.sha256(V3_RAW.read_bytes()).hexdigest()
    if digest != V3_SHA256:
        raise AssertionError(f"official V3 SHA-256 mismatch: {digest}")
    print(f"PASS official V3 SHA-256: {digest}")


def main() -> None:
    verify_representation()
    verify_extensions()
    verify_wage_regressions()
    verify_task_split()
    verify_latest_exposure()
    verify_official_v3()
    print("\nALL REQUESTED NUMERIC CHECKS PASSED")


if __name__ == "__main__":
    main()
