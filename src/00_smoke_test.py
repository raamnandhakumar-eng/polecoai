"""Run the core pipeline against isolated synthetic fixtures.

The fixtures and generated outputs live in a temporary project directory, so
this test never overwrites the real data, figures, or results. Run:

    python src/00_smoke_test.py
"""
from pathlib import Path
import os
import runpy
import shutil
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ANALYSIS = ROOT / "src" / "02_analysis.py"

tasks = [
    ("Answer customer questions about products and prices.", "41-2031.00", "Retail Salespersons"),
    ("Write and respond to customer emails.", "43-4051.00", "Customer Service Representatives"),
    ("Prepare sales reports and pricing analyses.", "41-1011.00", "First-Line Supervisors of Retail Sales Workers"),
    ("Develop and test software applications.", "15-1252.00", "Software Developers"),
    ("Debug computer programs.", "15-1252.00", "Software Developers"),
    ("Write marketing copy for products.", "27-3043.00", "Writers and Authors"),
    ("Plan menus and food presentation.", "35-1011.00", "Chefs and Head Cooks"),
    ("Schedule appointments for clients.", "43-6014.00", "Secretaries and Administrative Assistants"),
]
groups = {"41": "Sales and Related", "43": "Office and Administrative Support",
          "15": "Computer and Mathematical", "27": "Arts and Media",
          "35": "Food Preparation and Serving", "39": "Personal Care and Service"}


def write_fixtures(data: Path) -> None:
    """Write a minimal set of inputs matching the release schema."""
    rng = np.random.default_rng(0)
    data.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({
        "task_name": [t[0] for t in tasks],
        "pct": rng.dirichlet(np.ones(len(tasks))) * 100,
    }).to_csv(data / "onet_task_mappings.csv", index=False)

    pd.DataFrame({
        "O*NET-SOC Code": [t[1] for t in tasks],
        "Title": [t[2] for t in tasks],
        "Task": [t[0] for t in tasks],
    }).to_csv(data / "onet_task_statements.csv", index=False)

    pd.DataFrame({
        "Major Group": [f"{g}-0000" for g in groups],
        "SOC or O*NET-SOC 2019 Title": list(groups.values()),
    }).to_csv(data / "SOC_Structure.csv", index=False)

    pd.DataFrame({
        "SOC or O*NET-SOC 2019 Title": list(groups.values()),
        "bls_distribution": rng.integers(50_000, 3_000_000, len(groups)),
    }).to_csv(data / "bls_employment_may_2023.csv", index=False)

    pd.DataFrame({
        "SOCcode": [t[1] for t in tasks],
        "MedianSalary": rng.integers(30_000, 140_000, len(tasks)),
    }).to_csv(data / "wage_data.csv", index=False)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="frontline-smoke-") as tmp:
        project = Path(tmp)
        (project / "src").mkdir()
        (project / "results").mkdir()
        (project / "figures").mkdir()
        shutil.copy2(SOURCE_ANALYSIS, project / "src" / "02_analysis.py")
        write_fixtures(project / "data" / "release_2025_02_10")
        os.environ["MPLCONFIGDIR"] = str(project / "matplotlib-cache")

        print(f"Synthetic fixtures written under {project}. Running pipeline...\n")
        runpy.run_path(str(project / "src" / "02_analysis.py"),
                       run_name="__main__")

        expected = {
            project / "results" / "representation_by_group.csv",
            project / "results" / "frontline_tasks.csv",
            project / "figures" / "fig1_representation.png",
            project / "figures" / "fig2_frontline_tasks.png",
            project / "figures" / "fig3_wage_gradient.png",
        }
        missing = sorted(str(path.relative_to(project)) for path in expected
                         if not path.exists())
        if missing:
            raise AssertionError(f"Smoke test did not create: {missing}")

    print("\nPASS: isolated synthetic-data smoke test completed.")


if __name__ == "__main__":
    main()
