# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

**Sriramkrishnan Nandhakumar**  
Boston University Questrom School of Business, MBA 2026  
Working paper, revised July 2026

[Read the paper (PDF)](paper/paper.pdf) · [Read in Markdown](paper/paper.md) · [Methodology](docs/methodology.md) · [Reproducibility record](docs/reproducibility.md)

![AI usage and employment shares across U.S. occupation groups](figures/fig1_representation.png)

## Abstract

Generative AI may raise productivity where it is deployed, but those gains will not be broadly shared if adoption bypasses large parts of the workforce. This paper measures **realized AI adoption** in frontline service occupations using the Anthropic Economic Index, which maps millions of Claude conversations to O*NET task statements, combined with U.S. employment and wage data.

Frontline occupations in sales, office and administrative support, food preparation and serving, and personal care and service account for **31.7% of U.S. employment but only 11.1% of task-matched AI usage**. The gap is larger than the raw occupational classification suggests. Removing four technical occupations historically classified under administrative-support codes lowers that group's representation index from **0.65 to 0.34**, while a separate task-splitting robustness check leaves the estimates essentially unchanged.

The February and August 2025 releases provide suggestive evidence that underrepresentation persisted rather than closed. Conditional on reaching frontline tasks, AI use is also more likely to take an automation-style form. Automation accounts for **62.7%** of classified frontline administrative-support conversations, compared with **43.0%** in other occupations. Occupation-level regressions indicate that the gap is not primarily a wage gradient: the estimated wage elasticity of usage is **0.38** with an HC1 robust standard error of **0.19**, while the frontline coefficient is statistically indistinguishable from zero.

The February 2026 exposure data reveal a second divide within frontline work. Screen-mediated occupations such as customer service and data entry show high exposure, while physically co-present occupations such as food service and personal care remain close to zero. The evidence is consistent with a gap shaped by task medium, worker access, workflow design, and organizational investment, rather than technical capability alone.

## Main findings

### 1. Nearly one-third of workers receive only one-ninth of observed AI usage

The four frontline groups jointly account for **31.7% of employment and 11.1% of task-matched usage**.

| Occupation group | Raw representation index | Corrected index |
|---|---:|---:|
| Office and administrative support | 0.64 | **0.34** |
| Sales and related | 0.26 | 0.26 |
| Personal care and service | 0.23 | 0.23 |
| Food preparation and serving | 0.06 | 0.06 |
| Computer and mathematical | 10.94 | 10.94 |

A representation index of 1 means that an occupation group's usage share equals its employment share. Retail sales appears in the usage data at roughly **one-fortieth the per-worker rate of software work**. Food service appears at roughly **one-hundred-eightieth the rate**.

### 2. Occupational classification makes the gap look smaller

The raw administrative-support category includes Bioinformatics Technicians, Computer Operators, Statistical Assistants, and Desktop Publishers. Removing these technical occupations lowers the administrative-support index from **0.645 to 0.338**. The estimates for the other frontline groups move by no more than 0.01.

This is not a cosmetic adjustment. It shows how a classification artifact can overstate AI adoption among frontline workers.

### 3. The gap is not mainly explained by wages

The occupation-level regression uses 585 occupations with positive observed usage and wage data.

- Wage elasticity of usage: **0.38** (HC1 robust SE **0.19**)
- Wage elasticity with frontline control: **0.41** (SE **0.21**)
- Frontline coefficient: **0.19** (SE **0.19**)
- R-squared: **0.03**

Wages explain little of the cross-occupation variation in usage, and the frontline coefficient is not statistically different from zero. The evidence is more consistent with usage failing to scale with the number of frontline workers than with a simple low-wage penalty.

### 4. The gap remained large across the 2025 releases

Between February and August 2025, the representation indices changed only modestly:

- Office and administrative support: 0.65 to 0.73
- Sales: 0.26 to 0.30
- Personal care: 0.23 to 0.34
- Food service: 0.061 to 0.045
- Computer and mathematical: 10.94 to 11.48

No frontline group approached parity. Because the releases use different classification pipelines and task universes, this is **suggestive evidence of persistence**, not a formal trend estimate.

![Representation indices in February and August 2025](figures/fig4_temporal.png)

### 5. Frontline AI use is more likely to involve delegation

Conditional on observed use, automation-style interactions account for:

- **62.7%** of frontline office and administrative-support use
- **56.2%** of food-service use
- **50.9%** of personal-care use
- **48.0%** of sales use
- **43.0%** of use across other occupations

Automation-style use combines directive and feedback-loop conversations. Augmentation-style use includes iteration, learning, and validation. This distinction matters because experimental evidence associates full delegation during skill acquisition with weaker learning outcomes. The paper treats this comparison cautiously, but it raises a real human-capital concern: frontline workers may receive both less AI access and a less skill-building form of access.

![Automation-style share of classified conversations](figures/fig5_automation_share.png)

### 6. The important divide is screen-mediated versus physically co-present work

The February 2026 cross-section shows sharp polarization within frontline occupations.

| Occupation | Observed exposure |
|---|---:|
| Customer Service Representatives | **0.70** |
| Data Entry Keyers | **0.67** |
| Retail Salespersons | **0.32** |
| Cashiers | **0.08** |

Customer Service Representatives score above Software Developers at 0.29 and close to Computer Programmers at 0.75. At the same time, **44 of 112 frontline occupations**, including all cook categories, waiters, and bartenders, register zero observed exposure.

The dividing line is not simply wage or occupational prestige. It is whether the task can be mediated through a screen.

![Observed AI exposure by occupation in February 2026](figures/fig6_exposure_2026.png)

## Why I studied this

While operating Krishna Foods and Energy, I saw the divide between back-office work and the production and retail floor. Demand forecasts, supplier comparisons, pricing analyses, customer correspondence, and management reports could be digitized and supported by AI. Packing, stocking, serving customers, supervising production, and resolving real-time quality problems remained physical, time-sensitive, and difficult to mediate through a chat interface.

The task-level data reproduce that practical divide. AI appears first in the information-processing tasks embedded within frontline occupations, while the in-person core of the work remains largely absent.

## Why the findings matter

Productivity studies often measure what happens after workers receive an AI tool. Those studies can find large gains, especially for less-experienced workers. But gains conditional on deployment do not answer who receives access in the first place.

If adoption remains concentrated in technical and screen-based work, AI may reduce performance gaps within exposed occupations while widening the divide between workers who receive useful access and workers who do not.

The paper points to two practical questions:

1. **Access and workflow design:** Are frontline workers receiving employer-provided devices, tools, training, and redesigned workflows at the point of work?
2. **Human-capital design:** Does AI help workers reason through tasks and build skill, or does it mainly encourage delegation?

## Data and method

The analysis combines:

- Anthropic Economic Index task-level usage data from February 2025
- the V3 release covering an August 2025 usage window
- O*NET task statements, occupation codes, and wage data
- BLS Occupational Employment and Wage Statistics for May 2023
- Anthropic's February 2026 occupation-level observed-exposure measure

The study is descriptive. It reports usage shares, employment shares, representation indices, interaction-mode composition, and occupation-level regressions with HC1 heteroskedasticity-robust standard errors.

The measurement audit addresses occupational misclassification, tasks attached to multiple occupations, small interaction-mode cells, and selection into Claude rather than other AI platforms.

## Important limitations

- The data capture Claude usage, not all generative AI use.
- User occupation is inferred from task content rather than directly observed.
- Conversation share is not equivalent to work-time share or productivity.
- Employer-deployed systems may be underrepresented in consumer usage data.
- The February and August 2025 releases do not form a methodologically consistent panel.
- The February 2026 exposure measure is complementary and not directly comparable with the 2025 usage-share series.

The paper makes no causal claim about AI's effect on employment or wages.

## Reproduce the analysis

```bash
git clone https://github.com/raamnandhakumar-eng/polecoai.git
cd polecoai
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
make reproduce
```

Generated tables and figures are committed so the results can be inspected without rerunning the full pipeline.

## Repository structure

```text
src/polecoai/    reusable analysis, data, regression, and plotting functions
scripts/         executable analysis and paper-build commands
data/            provenance records and ignored raw/processed data
results/tables/  generated CSV tables reported in the paper
figures/         generated publication figures
paper/           current paper source and PDF
docs/            methodology, data dictionary, and reproducibility record
tests/           smoke tests and reported-result assertions
```

## Citation

> Nandhakumar, S. (2026). *The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data*. Working paper. https://github.com/raamnandhakumar-eng/polecoai

Code is released under the [MIT License](LICENSE). Source datasets retain their original licenses. Anthropic Economic Index data are distributed under CC BY 4.0.
