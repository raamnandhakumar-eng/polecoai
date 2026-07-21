# Headline findings (real AEI data, release 2025-02-10)

**The gap.** Frontline occupation groups (Sales; Office & Admin Support; Food
Prep & Serving; Personal Care & Service) account for **31.7% of US employment
but only 11.1% of Claude usage** — a ~3x underrepresentation. The gradient
within frontline work is steep:

| Group | Usage % | Employment % | Representation index |
|---|---|---|---|
| Office & Admin Support | 7.87 | 12.20 | 0.64 |
| Sales and Related | 2.27 | 8.81 | 0.26 |
| Personal Care & Service | 0.46 | 2.00 | 0.23 |
| Food Prep & Serving | 0.53 | 8.72 | **0.06** |

For contrast: Computer & Mathematical occupations are at index **10.94**
(37.3% of usage on 3.4% of employment) — a ~180x gap versus food service.

**The exceptions.** The frontline tasks that DO appear are the *information*
tasks embedded in frontline jobs, not the interpersonal/physical core:
composing customer correspondence (damage claims, billing disputes),
cashiers' "answer customers' questions on procedures or policies,"
restaurant hosts planning events, supervisors drafting reports. This supports
a task-content story: AI enters frontline work through its back-office edges.

**Measurement caveat (own it in the paper).** Several top "Office & Admin"
tasks belong to Bioinformatics Technicians and Computer Operators — technical
occupations that SOC classifies under admin support. Excluding them makes the
true frontline gap *larger*. Flagging this is a feature: it shows you read
the taxonomy critically instead of taking the join at face value.

**Null-ish result to report honestly.** Food service and building/grounds
occupations show near-zero usage (0.03-0.06 index). Discuss mechanisms:
physical task content, no device access at the point of work, and consumer
chat data not capturing employer-side tools.

---

# Extension results (src/03_extensions.py)

## A. Robustness: the gap is bigger than it looks
Excluding technical occupations misfiled under SOC 43 (Bioinformatics
Technicians, Computer Operators, Statistical Assistants, Desktop Publishers)
cuts the Office & Admin representation index from **0.645 to 0.338** — the
apparent "least underrepresented" frontline group was ~half technical work in
disguise. The true frontline gap is substantially larger than the baseline
estimate. (Other frontline groups barely move: a clean placebo.)

## B. Temporal (Feb 2025 vs Aug 2025 AEI V3): the gap is NOT closing
| Group | Index Feb | Index Aug | Direction |
|---|---|---|---|
| Computer & Math | 10.94 | 11.48 | up |
| Office/Admin | 0.65 | 0.73 | up slightly |
| Sales | 0.26 | 0.30 | up slightly |
| Personal Care | 0.23 | 0.34 | up |
| Food Service | 0.061 | **0.045** | DOWN |

Six months of rapid adoption left relative frontline representation roughly
flat; food service *fell*. Adoption deepened where it was already deep.
Caveat to state plainly: V1 and V3 use different classification pipelines and
task universes (3,514 vs 2,617 matched tasks), so treat this as indicative,
not a measured trend. Proposing how to measure it properly = discussion gold.

## C. Automation vs augmentation: when AI reaches frontline work, it automates
Share of automation-style usage (directive + feedback loop):
- Frontline Office/Admin: **62.7%**
- Computer & Math: 58.1%
- Frontline Food Service: 56.2%
- All other occupations: 43.0%

Frontline admin tasks are used in automation mode MORE than software tasks.
Combined headline: **AI rarely touches frontline work, but when it does, it
delegates rather than teaches.** Distributional implication: the workers with
the least AI exposure are also getting the least skill-building (augmentation)
value when exposure arrives.
