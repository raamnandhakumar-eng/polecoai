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

Percent fields use percentage points rather than proportions unless the column
name or paper text states otherwise. `observed_exposure` is a proportion from 0
to 1.
