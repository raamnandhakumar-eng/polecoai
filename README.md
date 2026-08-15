# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

Task-level evidence on observed AI use across U.S. occupations, using the Anthropic Economic Index, O*NET-SOC task statements, and BLS employment data.

**Headline finding:** Frontline occupations account for **31.7% of U.S. employment but only 11.1% of observed task-matched AI usage.** Excluding technical occupations classified under clerical codes reduces the administrative-support representation index from **0.645 to 0.338**. The estimated wage elasticity of usage is **0.38** with an HC1 standard error of **0.19**.

## Research versions

This repository contains the original working paper and a second-stage research
extension. Version 2 builds on Version 1. It does not replace or revise
the original paper or its headline results.

| Part | Focus | Main contribution | Status |
|---|---|---|---|
| **Version 1 paper** | Unequal observed AI adoption across occupations | Frontline representation indices, taxonomy audit, shared-task robustness, and wage regression | Working paper referenced in the fellowship application |
| **Version 2 extension** | Potential AI benefit versus observed use | Two-part adoption model, O*NET-based frontline definitions, and AI access-gap benchmark | Reproducible repository extension |

## Version 1: The original paper

**Question:** How much observed AI use reaches frontline occupations, relative
to their share of U.S. employment?

- **Preprint (DOI):** https://doi.org/10.5281/zenodo.21522366
- **Read online:** https://raamnandhakumar-eng.github.io/polecoai/
- **PDF:** [`paper/paper.pdf`](paper/paper.pdf)

Version 1 is a sole-authored working paper. JEL: J23, J24, O33.

### Version 1 findings

- Frontline occupations account for **31.7% of employment** but only **11.1% of
  observed task-matched AI usage**.
- The sales representation index is **0.26**. The administrative-support index
  falls from **0.645 to 0.338** after excluding technical occupations classified
  under clerical codes.
- Among occupations with positive usage and wage data, the estimated wage
  elasticity is **0.38** with an HC1 standard error of **0.19**.
- The taxonomy audit and shared-task robustness checks leave the main exposure
  gap intact.

The exact version referenced in fellowship materials remains available at
[`fellowship-submission-v1`](https://github.com/raamnandhakumar-eng/polecoai/tree/fellowship-submission-v1).

## Version 2: Adoption and access-gap extension

**Question:** Who has the potential to benefit from AI, who actually uses it,
and what explains the gap?

Version 2 keeps the Version 1 paper and its **31.7% vs 11.1%** headline intact.
It is currently a repository extension and is not yet included in the linked
Version 1 PDF.
It extends the analysis in three ways:

1. A two-part model first estimates the probability of any observed AI use,
   then estimates usage intensity among occupations with positive use.
2. Two O*NET-based definitions test whether the frontline gap persists for
   occupations with high physical presence or high customer interaction.
3. An AI access-gap benchmark compares theoretical task exposure with observed
   AI use and tests which occupation characteristics predict the difference.

### Version 2 findings

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

### Version 2 figures

#### Potential versus observed AI use

![Potential versus observed AI use by occupation](figures/fig7_potential_observed_gap.png)

*The access gap is the difference between theoretical task exposure and
observed AI use. Points above the diagonal have more observed use than the
theoretical benchmark; points below it have less.*

#### Exposure gap under three frontline definitions

![Employment and task-usage shares under three frontline definitions](figures/fig8_frontline_definitions.png)

*Frontline occupations remain underrepresented in observed AI use under the
current SOC definition and the physical-presence and customer-facing robustness
definitions.*

See [`docs/v2_extension.md`](docs/v2_extension.md) for definitions, estimates,
and limitations.

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

## Citation for Version 1

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
