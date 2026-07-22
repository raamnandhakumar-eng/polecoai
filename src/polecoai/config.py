"""Project paths and occupational group definitions."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
INITIAL_RELEASE_DIR = RAW_DATA_DIR / "release_2025_02_10"
V3_RELEASE_DIR = RAW_DATA_DIR / "release_2025_09_15"
V3_PROCESSED_DIR = PROCESSED_DATA_DIR / "v3_2025_08"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"
FIGURES_DIR = PROJECT_ROOT / "figures"
PAPER_DIR = PROJECT_ROOT / "paper"

FRONTLINE_GROUPS = {
    "41": "Sales",
    "43": "Office/Admin",
    "35": "Food Service",
    "39": "Personal Care",
}

FRONTLINE_GROUP_TITLES = {
    "41": "Sales and Related",
    "43": "Office and Administrative Support",
    "35": "Food Preparation and Serving Related",
    "39": "Personal Care and Service",
}

ANALYSIS_GROUPS = {
    **FRONTLINE_GROUPS,
    "15": "Computer & Mathematical",
}
