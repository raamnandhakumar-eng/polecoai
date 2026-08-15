# Data dictionary

## Source inputs

| File | Principal fields | Use |
|---|---|---|
| `onet_task_mappings.csv` | `task_name`, `pct` | February 2025 task usage shares |
| `onet_task_statements.csv` | `O*NET-SOC Code`, `Title`, `Task` | Task-to-occupation mapping |
| `SOC_Structure.csv` | `Major Group`, occupational title | SOC major-group hierarchy |
| `bls_employment_may_2023.csv` | occupational title, `bls_distribution` | Employment shares |
| `wage_data.csv` | `SOCcode`, `MedianSalary` | Occupation median wages |
| `global_task_data.csv` | `facet`, `variable`, `cluster_name`, `value` | August 2025 usage and collaboration modes |
| `job_exposure_frontline_subset.csv` | `occ_code`, `title`, `observed_exposure` | February 2026 occupation exposure |
| `job_exposure.csv` | `occ_code`, `title`, `observed_exposure` | Full February 2026 occupation exposure for v2 |
| `occ_level.csv` | task-capability ratings by O*NET-SOC | Theoretical exposure benchmark |
| `db_30_2_text.zip` | O*NET work activity, context, and education tables | V2 occupation controls and definitions |
| `oesm23nat.zip` | May 2023 detailed OEWS employment and wages | V2 wages and calibrated employment weights |
| `onet_2010_to_2019_crosswalk.csv` | old and new O*NET-SOC codes | Maps original task usage to current occupation measures |

## Generated tables

| Table | Key columns | Description |
|---|---|---|
| `representation_by_group.csv` | `usage_pct`, `employment_pct`, `representation_index` | Usage and employment comparison by SOC group |
| `frontline_tasks.csv` | `task_name`, `soc_code`, `occupation`, `pct` | Highest-share frontline task mappings |
| `regression_usage_wage.csv` | `model`, `term`, `coefficient`, `se_hc1`, `r_squared`, `n` | Wage regression estimates |
| `robustness_misclassification.csv` | baseline and strict usage/index fields | SOC 43 exclusion audit |
| `robustness_task_split.csv` | first-match and split usage/index fields | Shared-task mapping check |
| `temporal_feb_vs_aug_2025.csv` | February/August usage and indices | Cross-release comparison |
| `automation_share_by_bucket.csv` | `automation_share`, `conversations` | Collaboration-mode summary |
| `exposure_2026_by_group.csv` | `mean`, `median`, `zero_share`, `max`, `n` | February 2026 group summary |
| `v2_occupation_analysis.csv` | observed/theoretical exposure, O*NET controls, definitions | Merged v2 occupation dataset |
| `v2_two_part_models.csv` | stage, estimate type, term, estimate, HC1 SE | Extensive- and intensive-margin models |
| `v2_frontline_definitions.csv` | usage share, employment share, representation index | Three frontline definitions |
| `v2_access_gap_regression.csv` | coefficient, HC1 SE, confidence interval | Potential-minus-observed gap model |

Percent fields use percentage points rather than proportions unless the column
name or paper text states otherwise. `observed_exposure` is a proportion from 0
to 1.
