"""Download the Anthropic Economic Index inputs used by the analysis.

    pip install -r requirements.txt
    python scripts/download_data.py

Fetches from Hugging Face (Anthropic/EconomicIndex, CC-BY 4.0):
  1. release_2025_02_10  -- initial release: task mappings, O*NET statements,
                            SOC structure, BLS employment, wages
  2. The V3 raw usage file (Aug 4-11, 2025) from release_2025_09_15, from
     which we extract the GLOBAL task-level slice used in run_extensions.py.
"""

import hashlib
from pathlib import Path

import httpx
import pandas as pd
from huggingface_hub import hf_hub_download, snapshot_download

from polecoai.config import (
    INITIAL_RELEASE_DIR,
    RAW_DATA_DIR,
    V2_JOB_EXPOSURE,
    V2_OEWS_DETAIL,
    V2_ONET_CROSSWALK,
    V2_ONET_DATABASE,
    V2_SOURCE_DIR,
    V2_THEORETICAL_EXPOSURE,
    V3_PROCESSED_DIR,
    V3_RELEASE_DIR,
)

V3_NAME = "aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"

V2_SOURCES: dict[Path, tuple[str, str]] = {
    V2_JOB_EXPOSURE: (
        "https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/"
        "2ea58ff75e4247d26810c37f10c179edc2466cac/"
        "labor_market_impacts/job_exposure.csv",
        "4f0a3adf5feeb2ec5f5d02ab18cc5e851a2a4b8470bde84c0c9335017be12d68",
    ),
    V2_THEORETICAL_EXPOSURE: (
        "https://raw.githubusercontent.com/openai/GPTs-are-GPTs/"
        "0471612fef3cc22b74fb884d27bff9dbd3770582/data/occ_level.csv",
        "40c74f53de40aec91c0017d80690cbba915f83a8bb414bcf2f884692f1749acb",
    ),
    V2_ONET_DATABASE: (
        "https://www.onetcenter.org/dl_files/database/db_30_2_text.zip",
        "b5479271931796b838f7173dc0f673a9ec961b7833ac87168fd11e92e7453741",
    ),
    V2_OEWS_DETAIL: (
        "https://www.bls.gov/oes/special.requests/oesm23nat.zip",
        "8ce5e8277c3ba68a19f468fec9b4da21170593d5ad9693a813f1afc04c80efa2",
    ),
    V2_ONET_CROSSWALK: (
        "https://www.onetcenter.org/taxonomy/2019/walk/"
        "2010_to_2019_Crosswalk.csv?fmt=csv",
        "8f026a33134bfde5770308d1c6117cf70d9dd41c2b3467e6dd271d65bdeecc5a",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_verified(url: str, path: Path, expected_sha256: str) -> None:
    """Download a pinned public input and reject silent source changes."""
    if path.exists() and sha256(path) == expected_sha256:
        print(f"Verified cached v2 source: {path.name}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    timeout = httpx.Timeout(180, connect=30)
    with httpx.stream(
        "GET", url, follow_redirects=True, timeout=timeout
    ) as response:
        response.raise_for_status()
        with temporary.open("wb") as destination:
            for chunk in response.iter_bytes():
                destination.write(chunk)
    temporary.replace(path)
    actual = sha256(path)
    if actual != expected_sha256:
        raise ValueError(
            f"SHA-256 mismatch for {path.name}: {actual} != {expected_sha256}"
        )
    print(f"Downloaded and verified v2 source: {path.name}")


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Initial release
    initial_dir = INITIAL_RELEASE_DIR
    required_initial = {
        "onet_task_mappings.csv", "onet_task_statements.csv",
        "SOC_Structure.csv", "bls_employment_may_2023.csv", "wage_data.csv",
    }
    if not all((initial_dir / name).exists() for name in required_initial):
        snapshot_download(
            repo_id="Anthropic/EconomicIndex", repo_type="dataset",
            # Only CSV inputs are required. Downloading the whole folder also
            # fetches large, unused plot images and can stall constrained runners.
            allow_patterns=["release_2025_02_10/*.csv"],
            local_dir=RAW_DATA_DIR,
        )
    else:
        print("Initial release inputs already present; resuming download.")
    print("Initial release downloaded:")
    for f in sorted(INITIAL_RELEASE_DIR.glob("*.csv")):
        print("  -", f.name)

    # 2. V3 raw file. Use the repository's documented exact path so the
    #    downloader does not need to scan the full dataset tree.
    v3_local = V3_RELEASE_DIR / "data" / "intermediate" / V3_NAME
    if v3_local.exists():
        v3_path = v3_local
        print(f"Official V3 raw file already present; resuming: {v3_path}")
    else:
        v3_path = hf_hub_download(
            repo_id="Anthropic/EconomicIndex", repo_type="dataset",
            filename=f"release_2025_09_15/data/intermediate/{V3_NAME}",
            local_dir=RAW_DATA_DIR,
        )
    raw = pd.read_csv(v3_path)
    V3_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    global_tasks = raw[
        (raw["geo_id"] == "GLOBAL")
        & raw["facet"].isin(["onet_task", "onet_task::collaboration"])
    ]
    output_path = V3_PROCESSED_DIR / "global_task_data.csv"
    global_tasks.to_csv(output_path, index=False)
    print(
        f"V3 global task slice extracted: {len(global_tasks)} rows "
        f"-> {output_path}"
    )

    # 3. Pinned occupation-level sources for the v2 adoption-gap extension.
    V2_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for path, (url, expected_sha256) in V2_SOURCES.items():
        download_verified(url, path, expected_sha256)


if __name__ == "__main__":
    main()
