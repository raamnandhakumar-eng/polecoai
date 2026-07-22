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

## Interpretation

The analysis is descriptive. It does not identify a causal effect of AI on
employment, wages, skills, or productivity.
