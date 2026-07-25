# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

**Sriramkrishnan Nandhakumar**  
Boston University Questrom School of Business, MBA 2026  
Working paper, revised July 2026

Code and files for a working paper on observed AI use in frontline occupations.

[Paper webpage](https://raamnandhakumar-eng.github.io/polecoai/) · [PDF](paper/paper.pdf) · [Method notes](docs/methodology.md) · [Result checks](docs/checks.md)

## Requirements

- Python 3.10 or later
- `make`
- internet access for source-data downloads

## Install and run

```bash
git clone https://github.com/raamnandhakumar-eng/polecoai.git
cd polecoai
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
make reproduce
```

## Outputs

- tables: `results/tables/`
- figures: `figures/`
- paper: `paper/paper.pdf`

## Checks

```bash
python tests/test_reported_results.py
```

The checked values are listed in [`docs/checks.md`](docs/checks.md).

## Limits

- The data capture Claude usage, not all generative AI use.
- User occupation is inferred from task content rather than directly observed.
- Conversation share is not equivalent to work-time share or productivity.
- Employer-deployed systems may be underrepresented in consumer usage data.
- The February and August 2025 releases do not form a methodologically consistent panel.
- The February 2026 exposure measure is not directly comparable with the 2025 usage-share series.

## Citation

> Nandhakumar, S. (2026). *The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data*. Working paper. https://github.com/raamnandhakumar-eng/polecoai

Code is released under the [MIT License](LICENSE). Source datasets retain their original licenses. Anthropic Economic Index data are distributed under CC BY 4.0.
