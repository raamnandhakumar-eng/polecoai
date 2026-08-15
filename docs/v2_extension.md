# PolecoAI v2: potential, observed use, and diffusion frictions

## Research question

Who has the potential to benefit from AI, who actually uses it, and what
occupational features explain the gap?

This extension does not replace the working paper. It preserves the original
31.7% employment versus 11.1% task-usage result and adds three occupation-level
tests.

## 1. Extensive and intensive margins

The first stage asks whether an occupation has any observed AI exposure. The
second asks how much exposure it has, conditional on exposure being positive.
All continuous predictors are standardized, and both models use HC1 standard
errors.

| Predictor | Any use, average marginal effect | Log exposure, if positive |
|---|---:|---:|
| Log annual mean wage | -0.008 | 0.046 |
| Current frontline SOC group | 0.129 | 0.449 |
| Required education | 0.014 | -0.016 |
| Computer use | **0.167** | **0.181** |
| Physical presence | **-0.104** | **-0.544** |

The first stage uses 732 occupations. The second uses 333 positive-exposure
occupations. Computer use is positively associated with both the probability
and intensity of observed use. Physical presence is negatively associated with
both. Wage and education are not statistically distinguishable from zero in
these specifications.

The positive coefficient on the current SOC frontline indicator should not be
read as a reversal of the headline gap. The regression is conditional on
computer use, physical presence, education, and wage. The headline is an
unconditional comparison of task-usage and employment shares.

## 2. Alternative frontline definitions

The current definition uses Sales, Office and Administrative Support, Food
Service, and Personal Care. The alternatives select the top quartile of the
O*NET physical-presence and customer-facing indices.

| Definition | Task-usage share | Employment share | Representation index |
|---|---:|---:|---:|
| Current four SOC groups | 11.13% | 31.74% | **0.351** |
| High physical presence | 2.10% | 20.17% | **0.104** |
| High customer-facing | 13.39% | 38.45% | **0.348** |

The underrepresentation result persists across all three definitions. The two
O*NET definitions cover 98.96% of mapped task usage and 90.57% of calibrated
employment because some occupation records lack the required context scores.

## 3. Potential versus observed AI use

The AI access gap is defined as theoretical task exposure minus observed
Anthropic exposure. In the descriptive gap regression, a one-standard-deviation
increase in computer use is associated with a 0.135 larger gap. Customer-facing
work is associated with a 0.030 larger gap. Physical presence is associated with
a 0.061 smaller gap because physically intensive occupations also tend to have
lower theoretical exposure.

This is best read as a diffusion-friction screen. It identifies occupations
where modeled capability is high relative to observed use. It does not prove
that employers denied access or that closing the measured gap would produce a
specific productivity gain.

## Narrow policy implication

If productivity gains require workers to reach useful AI tools, unequal
workplace access could widen productivity and wage differences. The findings
support testing focused interventions rather than assuming that general-purpose
AI will diffuse evenly:

- employer-provided access at the point of work;
- role-specific training;
- workflow redesign around augmentation, not only automation;
- adequate devices and digital infrastructure.

Future work should evaluate these interventions with employer or worker-level
data. The current analysis remains occupation-level and descriptive.

## Main limitations

- Observed exposure reflects Anthropic usage, not all AI products.
- The theoretical and observed measures use different task universes and methods.
- One-to-many taxonomy matches divide task usage equally across mapped codes.
- The top-quartile thresholds are transparent but still researcher choices.
- Occupation-level associations do not identify individual access or causal effects.
