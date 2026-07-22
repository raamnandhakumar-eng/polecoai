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
data/processed/v3_2025_08/global_task_data.csv
data/reference/job_exposure_frontline_subset.csv
```

The reference exposure subset contains the five occupation groups used in the
February 2026 extension. Thirteen rows were checked against Anthropic’s public
`labor_market_impacts/job_exposure.csv`; see
[`docs/reproducibility.md`](../docs/reproducibility.md).

Source datasets retain their original licences. Anthropic Economic Index data
are distributed under CC BY 4.0. BLS and O*NET terms apply to their respective
files.
