"""
Step 1: Download the Anthropic Economic Index data used in this project.

    pip install -r requirements.txt
    python src/01_download_data.py

Fetches from Hugging Face (Anthropic/EconomicIndex, CC-BY 4.0):
  1. release_2025_02_10  -- initial release: task mappings, O*NET statements,
                            SOC structure, BLS employment, wages
  2. The V3 raw usage file (Aug 4-11, 2025) from release_2025_09_15, from
     which we extract the GLOBAL task-level slice used in 03_extensions.py
"""

from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download, snapshot_download

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
V3_NAME = "aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"


def main() -> None:
    DATA.mkdir(exist_ok=True)

    # 1. Initial release
    initial_dir = DATA / "release_2025_02_10"
    required_initial = {
        "onet_task_mappings.csv", "onet_task_statements.csv",
        "SOC_Structure.csv", "bls_employment_may_2023.csv", "wage_data.csv",
    }
    if not all((initial_dir / name).exists() for name in required_initial):
        snapshot_download(
            repo_id="Anthropic/EconomicIndex", repo_type="dataset",
            # Only CSV inputs are required. Downloading the whole folder also
            # fetches large, unused plot images and can stall constrained runners.
            allow_patterns=["release_2025_02_10/*.csv"], local_dir=DATA,
        )
    else:
        print("Initial release inputs already present; resuming download.")
    print("Initial release downloaded:")
    for f in sorted((DATA / "release_2025_02_10").glob("*.csv")):
        print("  -", f.name)

    # 2. V3 raw file. Use the repository's documented exact path so the
    #    downloader does not need to scan the full dataset tree.
    v3_local = DATA / "release_2025_09_15" / "data" / "intermediate" / V3_NAME
    if v3_local.exists():
        v3_path = v3_local
        print(f"Official V3 raw file already present; resuming: {v3_path}")
    else:
        v3_path = hf_hub_download(
            repo_id="Anthropic/EconomicIndex", repo_type="dataset",
            filename=f"release_2025_09_15/data/intermediate/{V3_NAME}",
            local_dir=DATA,
        )
    raw = pd.read_csv(v3_path)
    out_dir = DATA / "v3_2025_08"
    out_dir.mkdir(exist_ok=True)
    g = raw[(raw["geo_id"] == "GLOBAL")
            & (raw["facet"].isin(["onet_task", "onet_task::collaboration"]))]
    g.to_csv(out_dir / "global_task_data.csv", index=False)
    print(f"V3 global task slice extracted: {len(g)} rows "
          f"-> {out_dir / 'global_task_data.csv'}")


if __name__ == "__main__":
    main()
