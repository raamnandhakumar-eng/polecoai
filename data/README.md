# Data

The repository does not commit the full Anthropic Economic Index releases.
Run `python scripts/download_data.py` to retrieve the required source files.

## Directories

- `raw/`: downloaded source files, excluded from Git.
- `processed/`: generated intermediate files, excluded from Git.
- `reference/`: small, committed reference inputs required by the analysis.

## Source layout after download

```text
data/raw/release_2025_02_10/
data/raw/release_2025_09_15/
data/raw/v2_sources/
data/processed/v3_2025_08/global_task_data.csv
data/reference/job_exposure_frontline_subset.csv
```

The v2 source folder contains pinned copies of the full Anthropic occupation
exposure file, GPTs-are-GPTs task-capability scores, O*NET 30.2, the O*NET 2010
to 2019 crosswalk, and detailed May 2023 OEWS data. The download script verifies
each file against a committed SHA-256 value.

The committed reference exposure subset contains the five occupation groups
used in the February 2026 extension. Thirteen rows were checked against the
full Anthropic file; see [`docs/checks.md`](../docs/checks.md).

Source datasets retain their original licences. Anthropic Economic Index data
are distributed under CC BY 4.0. BLS and O*NET terms apply to their respective
files.
