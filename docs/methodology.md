# Methodology

## Scope

The study measures observed AI use in four SOC major groups: Sales and Related
(41), Office and Administrative Support (43), Food Preparation and Serving
Related (35), and Personal Care and Service (39). Computer and Mathematical
Occupations (15) provide a high-usage comparison group.

## Task-to-occupation mapping

AEI task statements are normalized by lowercasing, trimming whitespace,
collapsing repeated spaces, and removing a terminal period. They are then
matched exactly to O*NET task statements. The verified February 2025 and August
2025 runs both have a 100% match rate over their respective task universes.

When a task statement appears under more than one occupation, the baseline uses
the first unique O*NET match. A separate robustness calculation divides the
task’s usage equally across every occupation listing it.

## Representation index

For occupation group \(g\), the representation index is

\[R_g = s_g^U / s_g^E,\]

where \(s_g^U\) is the group’s share of task-matched conversations and
\(s_g^E\) is its share of national employment. Usage shares are normalized over
matched tasks. Employment shares use May 2023 OEWS values and are held fixed in
the cross-release comparison.

## Taxonomy audit

The administrative-support robustness check excludes four occupations whose
tasks are technical computing work but whose codes fall under SOC 43:
Bioinformatics Technicians, Computer Operators, Statistical Assistants, and
Desktop Publishers. Usage shares are renormalized after exclusion.

## Wage specifications

The paper estimates two occupation-level OLS specifications using the 585
occupations with positive usage and wage observations:

\[\log(s_o^U) = \alpha + \beta\log(w_o) + \gamma Frontline_o + \epsilon_o.\]

The first specification omits the frontline indicator. Standard errors use the
HC1 heteroskedasticity correction.

## Collaboration modes

Directive and feedback-loop conversations are classified as automation-style.
Task iteration, learning, and validation are classified as augmentation-style.
Shares are calculated from the corresponding AEI conversation counts.

## February 2026 exposure

The extension summarizes occupation-level observed exposure within the five
selected groups. Reported group means weight occupations equally. The optional
OEWS routine calculates employment-weighted means when a detailed national
employment file is supplied.

## V2 two-part adoption model

The v2 sample starts from all 756 occupations in Anthropic's February 2026
`job_exposure.csv`. After merging the controls and dropping incomplete rows,
732 occupations remain. The first stage is a logit model for any observed use:

\[Pr(Observed_o > 0) = f(\log Wage_o, Frontline_o, Education_o,
Computer_o, Physical_o).\]

The second stage estimates OLS only among the 333 occupations with positive
observed exposure:

\[\log(Observed_o \mid Observed_o > 0) = \alpha + X_o\beta + \epsilon_o.\]

Continuous predictors are standardized over the complete first-stage sample.
The first-stage table reports both log-odds coefficients and average marginal
effects. Both stages use HC1 standard errors. This is a descriptive two-part
model, not a Heckman selection correction.

## V2 O*NET measures

- `education_index` is the weighted mean of O*NET's 12 required-education
  categories, using the reported occupation percentages as weights.
- `computer_use_score` is the O*NET importance score for Working with
  Computers.
- `physical_presence_index` averages time standing, time walking or running,
  outdoor exposure, and work indoors without environmental controls.
- `customer_facing_index` averages contact with others, face-to-face
  discussions, and dealing with external customers or the public.

The physical-presence and customer-facing frontline definitions select the top
quartile of their respective O*NET index. February 2025 task usage is moved
from the O*NET-SOC 2010 taxonomy to the 2019 taxonomy using the official
crosswalk. When one old occupation maps to multiple new occupations, its usage
is divided equally across the mapped codes. Detailed OEWS employment is
calibrated to the original May 2023 major-group employment shares.

## V2 AI access gap

The v2 benchmark is

\[AccessGap_o = TheoreticalExposure_o - ObservedExposure_o.\]

The theoretical measure is the occupation mean of the GPTs-are-GPTs gamma task
rating. The observed measure is Anthropic's share of tasks with meaningful
observed penetration. The gap regression uses log wage, frontline status,
education, computer use, physical presence, and customer interaction with HC1
standard errors. Because the two exposure measures come from different task
universes and methods, the difference is a potential-versus-use benchmark. It
is not a literal measure of whether an employer denied tool access.

## Interpretation

The analysis is descriptive. It does not identify a causal effect of AI on
employment, wages, skills, or productivity.
