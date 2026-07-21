# The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data

**Sriramkrishnan Nandhakumar** · raam.nandhakumar@gmail.com · Working paper, July 2026
Code and data: https://github.com/raamnandhakumar-eng/polecoai
*JEL codes: J23, J24, O33*

## Abstract

This paper measures realized AI adoption in frontline service occupations using the Anthropic Economic Index, which maps millions of AI conversations to O*NET task statements. Frontline occupations — sales, administrative support, food service, and personal care — account for 31.7 percent of US employment but 11.1 percent of task-matched AI usage. Three facts characterize the gap. First, it is understated by occupational classification: excluding technical occupations misfiled under clerical codes reduces the administrative-support representation index from 0.65 to 0.34, while a task-splitting exercise leaves all four frontline estimates unchanged to three decimal places. Second, comparing February and August 2025 releases provides suggestive evidence of persistence rather than convergence. Third, conditional on reaching frontline tasks, usage skews toward full-delegation interaction modes (62.7 percent, versus 43.0 percent elsewhere) — the interaction style experimental evidence associates with the weakest skill formation. Occupation-level regressions indicate the gap is not a wage gradient: usage is only weakly wage-elastic (0.38, robust SE 0.19), and a frontline indicator is statistically indistinguishable from zero, implying the deficit operates through usage per worker rather than usage per occupation. February 2026 exposure scores show within-frontline polarization between screen-mediated and physically co-present service work. I discuss demand, access, and measurement mechanisms and their distributional implications.

## 1. Introduction

In my experience building and operating a food company, the processes most
amenable to digital tools were the information-heavy edges of the business:
pricing, procurement, inventory planning, reporting, and retail coordination.
Production-floor work, stocking, and face-to-face service still required
physical presence. That contrast motivated the paper's focus on whether AI is
reaching frontline occupations themselves or primarily the back-office tasks
embedded inside them.

This paper asks where AI adoption actually stands in frontline service work — the occupations employing nearly one-third of American workers — and what characterizes the adoption that does occur.

The question bears on the distribution of gains from generative AI. Where the technology has been deployed, estimated productivity effects are large and often largest for less-experienced workers: Brynjolfsson, Li, and Raymond (2025) document a 14 percent average increase in issues resolved per hour among customer-support agents given an AI assistant, and Noy and Zhang (2023) find comparable effects in professional writing tasks. These estimates are, however, conditional on deployment. If adoption systematically bypasses the occupations in which most low- and middle-wage workers are employed, within-task equalization can coexist with a widening between-occupation divide. Adoption inequality is documented directly in Danish linked survey-register data: Humlum and Vestergaard (2025) find chatbot take-up concentrated among younger, higher-earning workers, with women 16 percentage points less likely to adopt.

The paper's measurement contribution is to observe adoption rather than predict it. Prospective exposure indices score occupations by whether their tasks could, in principle, be performed by AI (Felten, Raj, and Seamans 2021; Eloundou et al. 2024). The Anthropic Economic Index (AEI; Handa et al. 2025) instead classifies millions of actual Claude conversations to O*NET task statements, permitting a distinction that turns out to be substantive: frontline occupations score as moderately *exposed* in prospective indices, but are barely *reached* in observed usage — and the interaction mode where they are reached differs systematically from the settings the productivity literature has studied.

I document five results. (i) Frontline occupation groups hold 31.7 percent of employment and 11.1 percent of task-matched usage; representation indices range from 0.64 (administrative support) to 0.06 (food service), against 10.9 for computer and mathematical occupations. (ii) The gap is larger than raw aggregates suggest: a taxonomy audit shows the administrative-support figure is inflated by technical occupations historically filed under clerical codes. (iii) Between February and August 2025, representation indices moved little and did not converge; food service declined. (iv) Conditional on reaching frontline tasks, usage is disproportionately automation-style. (v) By February 2026, observed exposure had polarized within frontline work: screen-mediated service occupations rank among the most exposed in the economy while in-person service occupations remain near zero.

The analysis is descriptive; I make no causal claims and, accordingly, present no identification strategy in the causal sense. The empirical discipline lies instead in measurement validity: each headline estimate is subjected to robustness exercises (taxonomy correction, task-splitting, cell-size disclosure, platform-selection bounds) designed to establish that the documented patterns are features of adoption rather than artifacts of classification or sample composition.

## 2. Conceptual Framework

A task-based framework organizes the empirics (Acemoglu and Autor 2011; Acemoglu and Restrepo 2019). An occupation *o* is a bundle of tasks; AI enters at the task level. For a task to appear in usage data, three conditions must jointly hold: technical feasibility (the task can be performed or assisted through a language-model interface), worker access (a device, time, and permission at the point of work), and expected value to the user. Prospective exposure indices measure only the first condition; observed usage reflects the product of all three. The wedge between exposure and usage is therefore informative about access and value frictions.

Define the representation index for occupation group *g* as

  R_g = s_g^U / s_g^E,

where s_g^U is group *g*'s share of task-matched usage and s_g^E its share of employment. R_g = 1 indicates usage proportional to employment. Because s_g^U aggregates over occupations while s_g^E aggregates over workers, R_g < 1 can arise through two distinct channels: fewer of the group's occupations appearing in usage at all (an extensive margin across occupations), or usage failing to scale with the number of workers per occupation (an intensive, per-worker margin). Section 5.3 uses occupation-level regressions to separate these channels.

The framework also distinguishes interaction modes. Following Handa et al. (2025), directive and feedback-loop conversations delegate the task (automation-style); iteration, learning, and validation conversations work through it (augmentation-style). In the displacement–reinstatement language of Acemoglu and Restrepo (2019), automation-style usage substitutes for worker task performance, while augmentation-style usage complements it; experimentally, the delegation mode is associated with markedly weaker skill formation (Shen and Tamkin 2026). The mode composition of frontline usage is therefore an object of interest in its own right.

## 3. Data

**Usage.** The AEI initial release (February 2025) reports, for 3,514 O*NET task statements, the share of a large sample of Claude.ai conversations classified to each task by Clio, a privacy-preserving pipeline (Tamkin et al. 2024; Handa et al. 2025). The V3 release (September 2025) reports analogous shares for an August 4–11, 2025 window (2,617 matched tasks) and classifies each task's conversations into the five collaboration modes above. Task statements match O*NET-SOC occupation codes exactly (100 percent match) after text normalization.

**Employment and wages.** Employment is from BLS Occupational Employment and Wage Statistics (May 2023), aggregated to SOC major groups; occupation median wages are from O*NET.

**Observed exposure, February 2026.** The AEI labor-market-impacts release provides an observed-exposure score for 756 occupations (Massenkoff and McCrory 2026), combining O*NET task data, task-level feasibility ratings (Eloundou et al. 2024), and observed usage through February 2026; it measures the employment-relevant share of an occupation's tasks with observed AI coverage. As a coverage measure it is not commensurable with usage shares and is treated as a complementary cross-section.

**Definitions and conventions.** Frontline occupations are SOC major groups 41 (Sales), 43 (Office and Administrative Support), 35 (Food Preparation and Serving), and 39 (Personal Care and Service). Usage shares are renormalized over task-matched conversations (excluding the V3 "none" bucket, 5.7 percent); employment shares are fixed at May 2023 values, so movements in R_g reflect usage dynamics only.

**Known limitations.** The data observe Claude usage, not all AI usage; conversations are classified by content, so user occupation is inferred, not observed; and usage share is not work-time share. Section 6 assesses each threat and its likely direction.

## 4. Empirical Approach

The design is descriptive. The estimands are population shares, ratios of shares, and conditional means in observed usage data; no counterfactual is constructed and no causal parameter is identified. The role usually played by an identification section is played here by threats to measurement validity, of which four are material: (i) occupational misclassification within the SOC taxonomy; (ii) many-to-many task–occupation mappings; (iii) small cells in mode-composition estimates; and (iv) platform selection into Claude usage. Sections 5 and 6 address each with, respectively, an exclusion audit, a fractional-assignment exercise, cell-size disclosure, and a bounding argument supported by within-platform contrasts and external survey evidence. Where language below is causal-adjacent ("enters," "absorbs"), it should be read as descriptive of observed patterns.

## 5. Results

### 5.1 Descriptive statistics

Frontline groups jointly hold 31.7 percent of US employment and 11.1 percent of task-matched usage. Representation indices (results/representation_by_group.csv; Figure 1): administrative support 0.64, sales 0.26, personal care 0.23, food service 0.06; computer and mathematical occupations 10.9 (37.3 percent of usage on 3.4 percent of employment). In per-worker terms, retail sales work appears in the usage data at roughly one-fortieth the rate of software work, and food service at roughly one one-hundred-eightieth. Within frontline groups, the highest-usage genuinely-frontline tasks (Figure 2) are information tasks embedded in service jobs: composing responses to customer correspondence (Correspondence Clerks), answering procedural and policy questions (Cashiers), event planning (Restaurant Hosts), document reformatting (Word Processors), and supervisory problem-resolution. The in-person core of the occupations — selling, serving, caring — is essentially absent.

### 5.2 The taxonomy audit

The administrative-support figure is inflated by construction. Its top-usage tasks belong disproportionately to technical occupations filed under SOC 43's historical clerical categories: Bioinformatics Technicians (43-9111.01), Computer Operators (43-9011), Statistical Assistants (43-9111), and Desktop Publishers (43-9031). Excluding these four occupations reduces the administrative-support index from 0.645 to 0.338 (results/robustness_misclassification.csv); the remaining frontline indices move by at most 0.01, consistent with a surgical rather than mechanical correction. The corrected estimates place all four frontline groups between 0.06 and 0.34.

### 5.3 Wages, and the margin of the gap

Occupation-level regressions separate the channels behind R_g < 1. Using the 585 occupations with positive usage and wage data, I estimate by OLS

  ln(s_o^U) = α + β ln(w_o) + γ·Frontline_o + ε_o,

with heteroskedasticity-robust (HC1) standard errors (results/regression_usage_wage.csv; Figure 3). The estimated wage elasticity is 0.38 (SE 0.19) without the frontline indicator and 0.41 (SE 0.21) with it; R² is 0.03 in both specifications, so wages explain almost none of the cross-occupation variance in usage. The frontline coefficient is 0.19 (SE 0.19): I cannot reject the null that frontline occupations have the same per-occupation usage as observably similar occupations, and the point estimate is, if anything, positive.

This null is informative. Frontline occupations are not missing from the usage data occupation-by-occupation; conditional on wages, an average frontline occupation's usage share resembles anyone else's. The representation gap arises because usage fails to scale with *employment*: frontline occupations are enormous (Retail Salespersons, Cashiers, and Customer Service Representatives each employ millions), so proportionate per-occupation usage translates into deeply disproportionate per-worker usage. The gap is an intensive-margin, usage-per-worker phenomenon — a fact any mechanism proposed in Section 7 must accommodate.

### 5.4 Dynamics, February–August 2025

Between the two releases (results/temporal_feb_vs_aug_2025.csv; Figure 4), indices moved modestly: computer/mathematical 10.94 to 11.48, administrative support 0.65 to 0.73, sales 0.26 to 0.30, personal care 0.23 to 0.34, food service 0.061 to 0.045. No frontline group converged toward parity, and food service declined. Because the releases use different classification pipelines and task universes (3,514 versus 2,617 tasks), levels are not strictly commensurable; I therefore interpret this as suggestive evidence of persistence rather than a measured trend. Constructing a methodologically consistent panel is feasible with the monthly aggregates introduced in the June 2026 AEI release (Massenkoff et al. 2026), whose data publication is in progress at this writing; Section 8 outlines the design.

### 5.5 Interaction modes

Conditional on reaching frontline tasks, usage skews toward delegation (results/automation_share_by_bucket.csv; Figure 5). Automation-style shares: frontline administrative 62.7 percent (73,038 classified conversations), computer/mathematical 58.1 percent (336,486), food service 56.2 percent (2,948), personal care 50.9 percent (4,439), sales 48.0 percent, all other occupations 43.0 percent. Cell sizes differ by two orders of magnitude; the estimate for administrative tasks is well powered, and the smaller frontline cells should be read as directionally consistent only. The pattern is notable against the experimental evidence: in a randomized trial, Shen and Tamkin (2026) find AI assistance during skill acquisition reduced mastery scores by 17 percentage points, with the deficit concentrated in delegation-style interaction patterns that correspond behaviorally to the AEI's directive and feedback-loop modes, while comprehension-seeking patterns (the AEI's learning and validation modes) preserved mastery. The results suggest frontline tasks receive not only less AI usage but a mode composition associated with weaker human-capital accumulation per interaction.

### 5.6 Observed exposure, February 2026

The most recent cross-section (results/exposure_2026_by_group.csv; Figure 6) is consistent with persistence and adds a within-group fact. Unweighted group means of observed exposure: computer/mathematical 0.38, sales 0.24, administrative support 0.19, personal care 0.02, food service 0.01; 44 of 112 frontline occupations (39 percent) — including all cook categories, waiters, and bartenders — register zero. Within frontline work, however, exposure is sharply bimodal. Customer Service Representatives score 0.70, above Software Developers (0.29) and comparable to Computer Programmers (0.75); Data Entry Keyers score 0.67; and within the same storefront, Retail Salespersons (0.32) score four times Cashiers (0.08). The dividing characteristic is not occupational prestige but task medium — whether the work is conducted through a screen or in a room with another person: screen-mediated service tasks show high observed coverage, physically co-present tasks show approximately none. This is consistent with the Section 5.1 finding that embedded information tasks are the entry margin, now visible at occupation scale.

## 6. Robustness and Threats to Validity

**Task-splitting.** 272 of 18,428 task statements (1.5 percent) appear under multiple occupations; the baseline assigns each to one. Splitting shared tasks' usage equally across all listing occupations leaves every frontline index unchanged to three decimal places and moves computer/mathematical from 10.944 to 10.918 (results/robustness_task_split.csv). The misfiled technical occupations of Section 5.2 hold their tasks uniquely, so exclusion — not fractional assignment — is the appropriate correction, and the two data issues are independent.

**Platform selection.** Claude's user base skews technical, mechanically inflating computer/mathematical shares relative to an all-platforms measure; recent work formalizes the resulting bias in single-platform exposure estimates ("Who Uses AI?," arXiv 2605.21743). Three observations bound its reach here. The within-frontline polarization of Section 5.6 arises among occupations facing an identical platform environment, so user composition cannot generate it. The mode-composition result is conditional on use: selection determines who appears, not how appearers interact. And the 2026 exposure scores incorporate first-party API traffic alongside consumer usage. Selection therefore plausibly inflates the level of the headline gap but is a poor candidate for its structure, persistence, or mode composition; platform-free Danish evidence (Humlum and Vestergaard 2025) exhibits the same occupational unevenness.

**Weighting.** The Section 5.6 means weight occupations equally. Because the highest-exposure frontline occupations are among the largest employers, employment weighting would likely raise frontline means and sharpen, not attenuate, the polarization contrast; the replication code accepts a detailed OEWS file and reports both.

**Remaining threats.** Conversation-to-task classification error is unobserved; the 100 percent statement-level match rate governs the join, not the upstream classification. Occupation of the user is inferred from task content, so managerial performance of frontline-classified tasks cannot be excluded — a decomposition proposed in Section 8. Employer-deployed AI is invisible to consumer usage data; note, however, that this omission implies frontline workers encounter AI primarily as employer-directed systems rather than worker-directed tools, which restates rather than overturns the mode-composition finding.

## 7. Mechanisms

Three mechanisms could generate the observed configuration — a per-worker usage deficit, persistent over 2025, automation-tilted in mode, and polarized by task medium.

**Demand.** The in-person core of frontline work — stocking, serving, de-escalating, caring — is not feasibly performed through a chat interface; this accounts for the near-zero coverage of food service and personal care, and for the medium-based polarization. It cannot alone explain the per-worker deficit in occupations rich in information tasks, which Sections 5.1 and 5.6 show are feasible and increasingly covered.

**Access.** Frontline work is performed on the clock, frequently without a workstation and under device policies; the discretionary experimentation margin that plausibly drove early white-collar adoption is largely absent at the point of frontline work. Access frictions map naturally onto the intensive-margin result of Section 5.3: they suppress usage per worker without eliminating occupations from the data.

My operating experience is consistent with this access mechanism but does not
identify it causally. Office-side planning and reporting happened at a computer
and could be digitized; production and customer-facing work happened at the
point of service, where attention, devices, and permission were constrained.
Some frontline information tasks were nevertheless suitable for automation,
which is why the access explanation complements rather than replaces the
demand-side boundary described above.

**Measurement.** Consumer usage data omit employer-embedded deployment. The direction of this omission is informative rather than exculpatory, as argued in Section 6, and the taxonomy audit demonstrates that correcting the measurable component of mismeasurement enlarges rather than shrinks the gap.

On balance, the evidence suggests the *level* of the gap reflects demand and access jointly, while its *composition* — automation-tilted, entering through embedded information tasks, absorbing screen-mediated occupations first — is a robust feature of how AI is meeting frontline work across all three measurement systems examined.

## 8. Conclusion and Policy Implications

Frontline service occupations account for roughly one-third of US employment and one-ninth of observed AI usage. The deficit operates through usage per worker rather than per occupation, survives taxonomy and join corrections that reverse the apparent ranking of frontline groups, shows no sign of convergence over 2025, and — conditional on arrival — takes the interaction form associated experimentally with the weakest skill formation. By February 2026, coverage had polarized within frontline work along the screen/in-person task boundary, with customer service among the most exposed occupations in the economy.

Two implications follow for policy and practice, stated with appropriate caution. First, to the extent productivity gains accrue where adoption occurs, current adoption patterns route them toward already-intensive occupations, while a large share of the workforce encounters AI chiefly as employer-directed automation; distributional analyses of AI centered on professional occupations describe the exposed minority. Second, the mode composition is plausibly a deployment default rather than a technological necessity: the one experimental setting with large frontline-adjacent gains involved employer-provisioned augmentation (Brynjolfsson, Li, and Raymond 2025), and the experimental learning evidence (Shen and Tamkin 2026) implies product and policy choices over interaction modes carry human-capital consequences.

Future research follows directly. A methodologically consistent adoption panel — reclassifying a fixed task universe across AEI releases, now feasible with the monthly aggregates of the June 2026 release — would convert the persistence result into a measured trajectory. A supervisory decomposition, crossing task assignments with first-line-supervisor SOC codes, would test whether frontline adoption is in practice managerial adoption. Both are implementable with public data and the replication code accompanying this paper.

## References

Acemoglu, D., and D. Autor. 2011. "Skills, Tasks and Technologies: Implications for Employment and Earnings." *Handbook of Labor Economics* 4B.

Acemoglu, D., and P. Restrepo. 2019. "Automation and New Tasks: How Technology Displaces and Reinstates Labor." *Journal of Economic Perspectives* 33(2).

Brynjolfsson, E., D. Li, and L. Raymond. 2025. "Generative AI at Work." *Quarterly Journal of Economics* 140(2). (NBER WP 31161, 2023.)

Eloundou, T., S. Manning, P. Mishkin, and D. Rock. 2024. "GPTs are GPTs: Labor Market Impact Potential of LLMs." *Science* 384.

Felten, E., M. Raj, and R. Seamans. 2021. "Occupational, Industry, and Geographic Exposure to Artificial Intelligence." *Strategic Management Journal* 42(12).

Handa, K., A. Tamkin, M. McCain, et al. 2025. "Which Economic Tasks are Performed with AI? Evidence from Millions of Claude Conversations." arXiv:2503.04761.

Humlum, A., and E. Vestergaard. 2025. "The Unequal Adoption of ChatGPT Exacerbates Existing Inequalities among Workers." *Proceedings of the National Academy of Sciences* 122(1).

Massenkoff, M., and P. McCrory. 2026. "Labor Market Impacts of AI: A New Measure and Early Evidence." Anthropic, March 5, 2026.

Massenkoff, M., E. Lyubich, S. Sacher, Z. Hitzig, S. Zhang, R. Heller, and P. McCrory. 2026. "Anthropic Economic Index Report: Cadences." Anthropic, June 26, 2026.

Noy, S., and W. Zhang. 2023. "Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence." *Science* 381.

Shen, J. H., and A. Tamkin. 2026. "How AI Impacts Skill Formation." arXiv:2601.20245.

Tamkin, A., M. McCain, et al. 2024. "Clio: Privacy-Preserving Insights into Real-World AI Use." arXiv:2412.13678.

US Bureau of Labor Statistics. 2023. Occupational Employment and Wage Statistics, May 2023. US Department of Labor, O*NET Database.

"Who Uses AI? Platform Selection and the Measurement of Occupational AI Exposure." 2026. arXiv:2605.21743.
