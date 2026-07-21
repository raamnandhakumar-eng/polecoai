# Verification record

Verified locally on 21 July 2026 with Python 3.12. All generated tables and
figures were rebuilt after replacing the project mirror with the official
Anthropic V3 source file.

## Step-by-step result

| Step | Status | Evidence |
|---|---:|---|
| Install dependencies | ✅ | `pip install -r requirements.txt` completed in `.venv`. |
| Run `src/02_analysis.py` | ✅ | 100.0% task-to-SOC match (3,514 tasks); frontline usage **11.13%**; frontline employment **31.74%**; Sales index **0.2576**, which rounds to **0.26**. |
| Run `src/03_extensions.py` | ✅ | Office/Admin falls **0.645 → 0.338** after excluding the four technical occupations; V3 task-to-SOC match is 100.0% (2,617 tasks). |
| Run `src/05_robustness.py` | ✅ with wording note | All four **frontline** indices are unchanged to three decimals under task splitting. Computer/Math moves slightly, **10.944 → 10.918**, so “all indices” is accurate only when it means all frontline indices. The paper states this precisely. |
| Run `src/04_latest_exposure.py` | ✅ | Customer Service Representatives are **0.7011** (reported as **0.70**); 44 of 112 frontline occupations (39%) have zero exposure. |
| Inspect all six charts | ✅ | Every chart is readable and interpretable; descriptions are below. |
| Run official-data downloader | ✅ after recovery | Hugging Face CLI timed out. The exact official V3 file was then downloaded through the public dataset page, checked against the official SHA-256, and the downloader was rerun successfully from that source. |
| Re-run scripts 02 and 03 on official V3 data | ✅ | The requested values are unchanged. |
| Verify `job_exposure.csv` rows | ✅ for all requested checks | The three requested occupations and ten additional rows match the official rendered CSV exactly. The environment blocked saving the full raw CSV URL, so the checked 133-row subset remains in `data/labor_market_impacts_2026/`. |
| Compare the paper with generated results | ✅ | Headline, robustness, temporal, automation, and 2026 exposure claims agree with the result tables. The task-splitting sentence correctly distinguishes the four unchanged frontline indices from the small Computer/Math change. |
| Rebuild and inspect the paper PDF | ✅ | `writeup/paper.pdf` rebuilt as a 12-page PDF; every page was rendered and visually inspected. Placeholder author text and unsupported convergence claims were removed. |
| Publish to GitHub | ❌ blocked by repository permission | `raamnandhakumar-eng/polecoai` exists and is publicly readable, but creating the publication branch returned GitHub API `403 Resource not accessible by integration`. The GitHub app needs write access to this repository. |

## Requested headline checks

| Check | Script/table | Reproduced | Paper | Match |
|---|---|---:|---:|:---:|
| Frontline usage total | `02_analysis.py` | 11.13% | 11.1% | ✅ |
| Frontline employment total | `02_analysis.py` | 31.74% | 31.7% | ✅ |
| Sales representation index | `02_analysis.py` | 0.2576 (0.26) | 0.26 | ✅ |
| Admin strict-classification index | `03_extensions.py` | 0.645 → 0.338 | 0.645 → 0.338 | ✅ |
| Wage elasticity, HC1 SE | `02_analysis.py` | 0.384 (0.185) | 0.38 (0.19) | ✅ |
| Wage elasticity with frontline control | `02_analysis.py` | 0.408 (0.206) | 0.41 (0.21) | ✅ |
| Frontline coefficient, HC1 SE | `02_analysis.py` | 0.186 (0.190) | 0.19 (0.19) | ✅ |
| Shared-task robustness | `05_robustness.py` | Four frontline indices unchanged to 3 decimals | Same, with Computer/Math 10.944 → 10.918 noted | ✅ |
| Customer Service Representatives | `04_latest_exposure.py` | 0.7011 (0.70) | 0.70 | ✅ |

The automated assertions are in `src/07_verify_results.py`; its final output
is `ALL REQUESTED NUMERIC CHECKS PASSED`.

## Official-source checks

The V3 source is Anthropic's
[`aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv`](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/release_2025_09_15/data/intermediate/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv).
The local file is 18,894,517 bytes and its SHA-256 is:

```text
c8ef9c5eee0c42febc73e358ecc7d2358e0a0ce3b50122c0c15ae8ec569aceff
```

The occupation checks were read from Anthropic's official rendered
[`labor_market_impacts/job_exposure.csv`](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/labor_market_impacts/job_exposure.csv).

| SOC | Occupation | Official | Local subset | Match |
|---|---|---:|---:|:---:|
| 43-4051 | Customer Service Representatives | 0.7011 | 0.7011 | ✅ |
| 41-2011 | Cashiers | 0.0846 | 0.0846 | ✅ |
| 41-2031 | Retail Salespersons | 0.3222 | 0.3222 | ✅ |
| 15-1251 | Computer Programmers | 0.7451 | 0.7451 | ✅ |
| 15-1252 | Software Developers | 0.2880 | 0.2880 | ✅ |
| 35-9031 | Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop | 0.0734 | 0.0734 | ✅ |
| 39-6012 | Concierges | 0.1875 | 0.1875 | ✅ |
| 41-4012 | Wholesale/Manufacturing Sales Representatives, except technical/scientific | 0.6279 | 0.6279 | ✅ |
| 41-3041 | Travel Agents | 0.4054 | 0.4054 | ✅ |
| 43-9021 | Data Entry Keyers | 0.6707 | 0.6707 | ✅ |
| 43-4171 | Receptionists and Information Clerks | 0.4338 | 0.4338 | ✅ |
| 43-6014 | Secretaries/Admin Assistants, except legal/medical/executive | 0.4528 | 0.4528 | ✅ |
| 43-9111 | Statistical Assistants | 0.5099 | 0.5099 | ✅ |

## What each chart shows

1. **Figure 1 — representation.** Gray/orange bars show Claude usage share
   and black dots show employment share. Computer/Math is massively
   overrepresented, while every orange frontline group is underrepresented;
   the widest absolute gaps are Admin, Sales, and Food Service.
2. **Figure 2 — frontline tasks.** The top task-coded frontline usage is
   dominated by technical work filed inside SOC 43, followed by information
   tasks such as correspondence, reports, event planning, and policy Q&A.
   This is the visual reason for the strict-classification robustness check.
3. **Figure 3 — wage gradient.** On a log usage axis, frontline occupations
   cluster mainly in the low-wage/low-usage region. Usage tends to rise with
   wages, though the relationship is dispersed and has prominent outliers.
4. **Figure 4 — February versus August 2025.** Admin, Personal Care, and Sales
   rise modestly; Food Service falls; Computer/Math remains around eleven
   times parity. The gap does not broadly converge.
5. **Figure 5 — automation style.** Conditional on being used, AI is most
   automation-style in frontline Admin (62.7%), above Computer/Math (58.1%).
   Food Service and Personal Care are at or above 50%; Sales is 48%, compared
   with 43% for all other occupations.
6. **Figure 6 — 2026 observed exposure.** Computer/Math has the highest group
   mean, while Sales and Admin are highly polarized: many occupations remain
   near zero but a few have very high exposure. Food Service and Personal Care
   remain concentrated close to zero.

All six charts could be interpreted; none requires author clarification.

## Errors encountered and resolution

1. The first `03_extensions.py` run stopped with `FileNotFoundError` because
   `data/v3_2025_08/global_task_data.csv` did not yet exist.
2. The first `01_download_data.py` attempt exhausted five Hugging Face HEAD
   retries and ended in a read timeout. The exact official V3 object was
   recovered from the public dataset page, its hash matched, and the script
   then completed successfully.
3. The original smoke test wrote synthetic fixtures into the real data path.
   During QA its isolated replacement first exposed duplicate fixture rows and
   a missing temporary output directory. Both were fixed; the final smoke test
   passes and cannot alter official inputs.
4. Matplotlib printed a read-only cache warning in this container and used a
   temporary cache. This did not affect any output or exit status.
5. The official raw `job_exposure.csv` download URL was blocked by the hosted
   browser's URL-safety policy. The official web-rendered CSV remained
   accessible and was sufficient to verify all 13 requested spot-check rows.

## Most surprising number

**0.7011 for Customer Service Representatives** surprised me most because it
is almost nine times the Cashiers value (0.0846), even though both jobs sit at
the customer boundary; the contrast makes the paper's real divide look like
information-mediated versus physically co-present service work, not simply
professional versus frontline work.
