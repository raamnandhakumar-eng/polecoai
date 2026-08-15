# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

Task-level evidence on observed AI use across U.S. occupations, using the Anthropic Economic Index, O*NET-SOC task statements, and BLS employment data.

**Headline finding:** Frontline occupations account for **31.7% of U.S. employment but only 11.1% of observed task-matched AI usage.** Excluding technical occupations classified under clerical codes reduces the administrative-support representation index from **0.645 to 0.338**. The estimated wage elasticity of usage is **0.38** with an HC1 standard error of **0.19**.

## Paper

- **Preprint (DOI):** https://doi.org/10.5281/zenodo.21522366
- **Read online:** https://raamnandhakumar-eng.github.io/polecoai/
- **PDF:** [`paper/paper.pdf`](paper/paper.pdf)

Sole-authored working paper. JEL: J23, J24, O33.

## v2 research extension

**Question:** Who has the potential to benefit from AI, who actually uses it,
and what explains the gap?

The v2 extension keeps the paper and its **31.7% vs 11.1%** headline intact.
It adds a two-part adoption model, two O*NET-based frontline definitions, and
a theoretical-minus-observed **AI access gap**.

- In the extensive-margin logit, a one-standard-deviation increase in computer
  use is associated with a **16.7 percentage-point** increase in the probability
  of any observed AI use. A one-standard-deviation increase in physical presence
  is associated with a **10.4 percentage-point decrease**. The model uses 732
  occupations and HC1 standard errors.
- The representation index remains below one under the current SOC definition
  (**0.351**), a high-physical-presence definition (**0.104**), and a
  high-customer-facing definition (**0.348**).
- The access-gap regression finds larger potential-minus-observed gaps in
  computer-intensive and customer-facing occupations. This is descriptive and
  does not identify a causal access barrier.

See [`docs/v2_extension.md`](docs/v2_extension.md) for definitions, estimates,
and limitations. The exact pre-extension version referenced in fellowship
materials remains available at
[`fellowship-submission-v1`](https://github.com/raamnandhakumar-eng/polecoai/tree/fellowship-submission-v1).

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
- **Anthropic AI Exposure Index, March 2026 release** — the committed five-group subset and the pinned full occupation file used by v2.
- **O*NET 30.2** — education, computer-use, physical-presence, and customer-facing measures.
- **May 2023 OEWS** — detailed occupation employment and wage controls.
- **GPTs-are-GPTs** — theoretical task exposure used for the v2 potential benchmark.

The download script fetches the 2025 AEI files and verifies the pinned v2 inputs
with SHA-256 hashes. Files under `data/raw/` and `data/processed/` are not
committed. Anthropic Economic Index data are distributed under CC BY 4.0.
O*NET, BLS, OpenAI, and other third-party files retain their original terms.

## Robustness

The checks cover the SOC 43 taxonomy audit, shared-task splitting,
February-to-August 2025 comparisons, occupation-level wage regressions, the v2
two-part model, all three frontline definitions, and the access-gap regression.
The four original frontline representation indices are unchanged to three
decimals under task splitting.

See [`docs/methodology.md`](docs/methodology.md) and [`docs/checks.md`](docs/checks.md).

## Limitations

- The data capture Claude usage, not all generative AI use.
- User occupation is inferred from task content rather than observed directly.
- Conversation share is not the same as work-time share or productivity.
- The February and August 2025 releases do not form a methodologically consistent panel.
- Employer-deployed AI may be underrepresented in consumer conversation data.
- The analysis is descriptive and does not identify causal effects on employment, wages, skills, or productivity.
- The v2 access gap compares measures built with different task universes and
  should be read as a benchmark, not a literal measure of denied tool access.

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
