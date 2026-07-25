# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

Task-level evidence on observed AI use across U.S. occupations, using the Anthropic Economic Index, O*NET-SOC task statements, and BLS employment data.

**Headline finding:** Frontline occupations account for **31.7% of U.S. employment but only 11.1% of observed task-matched AI usage.** Excluding technical occupations classified under clerical codes reduces the administrative-support representation index from **0.645 to 0.338**. The estimated wage elasticity of usage is **0.38** with an HC1 standard error of **0.19**.

## Paper

- **Preprint (DOI):** https://doi.org/10.5281/zenodo.21522366
- **Read online:** https://raamnandhakumar-eng.github.io/polecoai/
- **PDF:** [`paper/paper.pdf`](paper/paper.pdf)

Sole-authored working paper. JEL: J23, J24, O33.

## Repository structure

```text
data/             Downloaded inputs, processed files, and the committed 2026 exposure subset
src/polecoai/     Analysis modules
scripts/          Download and rebuild commands
results/tables/   Generated tables
figures/          Generated figures
paper/            Paper website source and PDF
docs/             Method notes and result checks
tests/            Reproduction and smoke checks
```

## Reproduce the results

```bash
git clone https://github.com/raamnandhakumar-eng/polecoai.git
cd polecoai
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
make reproduce
```

The first run downloads the source data. Generated tables are written to `results/tables/`, figures to `figures/`, and the rebuilt paper to `paper/paper.pdf`.

Run the reported-result checks separately with:

```bash
python tests/test_reported_results.py
```

## Data

- **Anthropic Economic Index, `release_2025_02_10`** — task mappings, O*NET task statements, SOC structure, May 2023 BLS employment data, and wage data.
- **Anthropic Economic Index, `release_2025_09_15`** — the global task-level slice from the August 4–11, 2025 V3 usage file.
- **Anthropic AI Exposure Index, March 2026 release** — the committed frontline and computer/mathematical subset from `labor_market_impacts/job_exposure.csv`, stored in `data/reference/`.

The download script fetches the 2025 AEI files from `Anthropic/EconomicIndex` on Hugging Face. Files under `data/raw/` and `data/processed/` are not committed. Anthropic Economic Index data are distributed under CC BY 4.0. O*NET, BLS, and other third-party files retain their original terms.

## Robustness

The checks cover the SOC 43 taxonomy audit, shared-task splitting, February-to-August 2025 comparisons, occupation-level wage regressions, and direct assertions for the values reported in the paper. The four frontline representation indices are unchanged to three decimals under task splitting.

See [`docs/methodology.md`](docs/methodology.md) and [`docs/checks.md`](docs/checks.md).

## Limitations

- The data capture Claude usage, not all generative AI use.
- User occupation is inferred from task content rather than observed directly.
- Conversation share is not the same as work-time share or productivity.
- The February and August 2025 releases do not form a methodologically consistent panel.
- Employer-deployed AI may be underrepresented in consumer conversation data.
- The analysis is descriptive and does not identify causal effects on employment, wages, skills, or productivity.

## Citation

```bibtex
@techreport{nandhakumar2026frontline,
  author = {Nandhakumar, Sriramkrishnan},
  title = {The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data},
  year = {2026},
  type = {Working paper},
  doi = {10.5281/zenodo.21522366},
  url = {https://doi.org/10.5281/zenodo.21522366}
}
```

GitHub also reads [`CITATION.cff`](CITATION.cff) and provides a **Cite this repository** menu.

## Why I studied this

While running a manufacturing and retail business, I watched back-office work digitize quickly while production-floor and customer-facing work changed more slowly. This paper tests whether that divide appears across the U.S. workforce.

## License

- Code: [MIT](LICENSE)
- Manuscript text and original figures: [CC BY 4.0](LICENSE-CONTENT.md)
- Third-party data remain under their original licenses.

## Contact

Raam Nandhakumar — raam.nandhakumar@gmail.com
