# The Frontline Exposure Gap

**Frontline occupations — retail sales, admin support, food service, personal
care — hold 31.7% of US employment but only 11.1% of real-world AI usage.
The gap is larger than official occupation codes suggest, it did not close
between February and August 2025, and when AI does reach frontline tasks, it
is used to automate rather than augment.**

Empirical analysis of the [Anthropic Economic Index](https://www.anthropic.com/news/the-anthropic-economic-index)
(AEI): millions of Claude conversations mapped to O*NET tasks, joined here to
BLS employment and O*NET wage data.

![Usage vs employment by occupation group](figures/fig1_representation.png)

## Findings

**1. The gap.** AI usage concentrates in computer/mathematical occupations
(37% of usage, 3.4% of employment — representation index 10.9). Frontline
groups sit far below parity: admin support 0.64, sales 0.26, personal care
0.23, food service 0.06 (`results/representation_by_group.csv`).

**2. The gap is understated by the taxonomy.** The strongest-looking
frontline group (admin support) is roughly half technical work misfiled under
SOC 43 — Bioinformatics Technicians, Computer Operators, Statistical
Assistants. Excluding them cuts its index from 0.65 to **0.34**; other
frontline groups barely move, a clean placebo
(`results/robustness_misclassification.csv`).

**3. The gap is not closing.** Comparing the Feb 2025 release to the Aug 2025
(V3) release, frontline representation was roughly flat and food service
*fell* (0.061 → 0.045). Adoption deepened where it was already deep
(`results/temporal_feb_vs_aug_2025.csv`). Caveat: the releases use different
classification pipelines; this comparison is indicative, and measuring the
trend properly is an open problem discussed in the paper.

![Temporal comparison](figures/fig4_temporal.png)

**4. When AI reaches frontline work, it automates.** Frontline admin tasks
show 62.7% automation-style usage (directive + feedback loop) — *higher than
software tasks* (58.1%) and well above other occupations (43.0%)
(`results/automation_share_by_bucket.csv`). The tasks that do penetrate
frontline work are its embedded information tasks: customer correspondence,
policy Q&A, scheduling — the back-office edges, not the customer-facing core.

![Automation vs augmentation](figures/fig5_automation_share.png)

**5. One year on (Feb 2026): the gap persists — and polarizes.** Using
Anthropic's newest observed-exposure scores (AI Exposure Index, March 2026
release), 39% of frontline occupations show *zero* observed exposure and food
service averages 0.01 — yet Customer Service Representatives score **0.70**,
among the highest in the entire economy, rivaling Computer Programmers (0.75).
The fault line runs between information-mediated and physically co-present
service work, not between "frontline" and "professional"
(`results/exposure_2026_by_group.csv`, `figures/fig6_exposure_2026.png`).

## Reproduce

```bash
pip install -r requirements.txt
python src/01_download_data.py   # fetches AEI data from Hugging Face (CC-BY 4.0)
python src/02_analysis.py        # core indices, tasks, wages, and HC1 regressions
python src/03_extensions.py      # robustness, temporal, automation vs augmentation
python src/05_robustness.py      # shared-task assignment and optional OEWS weighting
python src/04_latest_exposure.py # Feb 2026 exposure: persistence + polarization
python src/07_verify_results.py  # assert every headline number
python src/06_make_pdf.py        # rebuild writeup/paper.pdf
```

Outputs: tables in `results/`, figures in `figures/`. A synthetic-data smoke
test (`src/00_smoke_test.py`) verifies the pipeline in an isolated temporary
folder without downloading or overwriting the official inputs. The completed
manual and automated audit is recorded in [`VERIFICATION.md`](VERIFICATION.md).

## Repository

```
src/         download + analysis pipeline (Python, pandas/matplotlib)
results/     generated tables (committed for convenience)
figures/     generated figures
writeup/     working paper draft and findings summary
```

## Data & citation

- Anthropic Economic Index (CC-BY 4.0): Handa et al., *Which Economic Tasks
  are Performed with AI? Evidence from Millions of Claude Conversations*,
  arXiv:2503.04761; AEI V3 release (Sept 2025).
- Employment: US Bureau of Labor Statistics, OES May 2023.
- Task taxonomy: O*NET / SOC, US Department of Labor.

Code: MIT. Paper author: Sriramkrishnan Nandhakumar
(raam.nandhakumar@gmail.com).
Repository: https://github.com/raamnandhakumar-eng/polecoai
