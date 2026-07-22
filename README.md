# The Frontline Exposure Gap

Code and data documentation for **“The Frontline Exposure Gap: Evidence on AI
Adoption in Retail and Service Occupations from Task-Level Usage Data.”**

**Author:** Sriramkrishnan Nandhakumar  
**Contact:** raam.nandhakumar@gmail.com  
**Paper:** [Markdown](paper/paper.md) · [PDF](paper/paper.pdf)

![AI usage and employment share by occupation group](figures/fig1_representation.png)

## Abstract

This project measures realized AI use in frontline service occupations using
the Anthropic Economic Index, O*NET task statements, and US occupational
employment data. Sales, administrative support, food service, and personal
care account for 31.74% of US employment but 11.13% of task-matched Claude
usage. The analysis examines occupational classification, changes between the
February and August 2025 releases, collaboration modes, wage patterns, and
occupation-level observed exposure through February 2026.

## Research question

How does observed AI use compare with employment across frontline occupations,
and what distinguishes the frontline tasks and occupations in which AI use is
already present?

## Motivation

Studies of generative AI often estimate productivity effects after a tool has
been introduced. This project instead examines where observed use appears in
the occupational distribution. The distinction matters because gains within
AI-using tasks can coexist with unequal adoption across occupations.

## Data and methodology

The analysis combines:

- Anthropic Economic Index task-level usage data from February 2025;
- the September 2025 release covering an August 2025 usage window;
- O*NET task statements, occupation codes, and wages;
- BLS Occupational Employment and Wage Statistics; and
- Anthropic’s February 2026 occupation-level observed-exposure measure.

For occupation group \(g\), the representation index is

\[R_g = \frac{\text{usage share}_g}{\text{employment share}_g}.\]

An index of 1 indicates usage proportional to employment. The study is
descriptive and does not estimate a causal effect. Details are in
[docs/methodology.md](docs/methodology.md).

## Main findings

1. The four frontline groups account for **11.13% of usage** and **31.74% of
   employment**. Their representation indices are 0.645 for administrative
   support, 0.258 for sales, 0.229 for personal care, and 0.061 for food
   service. Computer and mathematical occupations have an index of 10.944.
2. Excluding four technical occupations classified under administrative
   support reduces that group’s index from **0.645 to 0.338**. The other
   frontline indices change by no more than 0.01.
3. Splitting shared O*NET tasks equally across listing occupations leaves all
   four frontline indices unchanged to three decimal places. The
   computer/mathematical index moves from 10.944 to 10.918.
4. Between the February and August 2025 releases, administrative support,
   sales, and personal care rise modestly, while food service falls from 0.061
   to 0.045. Differences in release methodology limit temporal interpretation.
5. Automation-style conversations account for 62.7% of classified frontline
   administrative usage, compared with 58.1% in computer/mathematical
   occupations and 43.0% across other occupations.
6. In the February 2026 exposure data, 44 of 112 frontline occupations have
   zero observed exposure. Customer Service Representatives score 0.7011,
   compared with 0.0846 for Cashiers and 0.3222 for Retail Salespersons.

The committed values are in [results/tables](results/tables) and are checked by
[tests/test_reported_results.py](tests/test_reported_results.py).

## Repository structure

```text
src/polecoai/    shared analysis, data, regression, and plotting functions
scripts/         executable analysis and paper-build commands
data/            data provenance, ignored raw/processed data, reference subset
results/tables/  generated CSV tables reported in the paper
figures/         generated figures
paper/           current paper source, PDF, and notes
docs/            methodology, data dictionary, and reproducibility record
tests/           synthetic smoke test and reported-result assertions
```

## Installation

Python 3.12 was used for the verified run.

```bash
git clone https://github.com/raamnandhakumar-eng/polecoai.git
cd polecoai
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Reproducing the results

Run the complete pipeline:

```bash
make reproduce
```

Or run each stage directly:

```bash
python scripts/download_data.py
python scripts/run_analysis.py
python scripts/run_extensions.py
python scripts/run_robustness.py
python scripts/run_latest_exposure.py
python tests/test_reported_results.py
python scripts/build_paper.py
```

The download script retrieves the source files from
`Anthropic/EconomicIndex` on Hugging Face. Raw and intermediate data are not
committed. Generated tables and figures are committed so the reported results
can be inspected without rerunning the pipeline.

For a download-free code check:

```bash
python tests/test_smoke.py
```

## Limitations

- AEI records Claude usage rather than all AI use.
- Task content is mapped to occupations; the user’s occupation is not observed.
- Conversation share is not equivalent to work-time share or productivity.
- The February and August 2025 releases use different classification pipelines
  and task universes.
- The February 2026 group means are unweighted across occupations unless a
  detailed OEWS employment file is supplied.

The paper discusses the direction and interpretation of each limitation.

## Citation

Citation metadata are available in [CITATION.cff](CITATION.cff). A plain-text
citation is:

> Nandhakumar, S. (2026). *The Frontline Exposure Gap: Evidence on AI
> Adoption in Retail and Service Occupations from Task-Level Usage Data*.
> https://github.com/raamnandhakumar-eng/polecoai

## Acknowledgements

This project uses public data from the Anthropic Economic Index, the US Bureau
of Labor Statistics, and the US Department of Labor’s O*NET program. Their
inclusion does not imply endorsement of this analysis.

## License

Code is released under the [MIT License](LICENSE). Source datasets retain their
original licences; Anthropic Economic Index data are distributed under
CC BY 4.0.
