# Reproducibility record

The final local run used Python 3.12. Generated tables and figures were rebuilt
after the repository reorganization and compared with the pre-refactor files.
All eight CSV tables and all six PNG figures have identical SHA-256 hashes.

## Reported-result checks

| Quantity | Reproduced value | Paper value |
|---|---:|---:|
| Frontline usage share | 11.13% | 11.1% |
| Frontline employment share | 31.74% | 31.7% |
| Sales representation index | 0.2576 | 0.26 |
| Administrative index, baseline to strict | 0.645 → 0.338 | 0.645 → 0.338 |
| Wage elasticity, HC1 SE | 0.384 (0.185) | 0.38 (0.19) |
| Wage elasticity with frontline control | 0.408 (0.206) | 0.41 (0.21) |
| Frontline coefficient, HC1 SE | 0.186 (0.190) | 0.19 (0.19) |
| Customer Service Representatives | 0.7011 | 0.70 |

The four frontline indices are unchanged to three decimals under task
splitting. The computer/mathematical index changes from 10.944 to 10.918, as
stated in the paper.

Run the assertions with:

```bash
python tests/test_reported_results.py
```

## Official-source checks

The August 2025 source file has SHA-256:

```text
c8ef9c5eee0c42febc73e358ecc7d2358e0a0ce3b50122c0c15ae8ec569aceff
```

The following occupation values were checked against Anthropic’s public
`labor_market_impacts/job_exposure.csv`: Customer Service Representatives,
Cashiers, Retail Salespersons, Computer Programmers, Software Developers,
Hosts and Hostesses, Concierges, wholesale/manufacturing Sales
Representatives, Travel Agents, Data Entry Keyers, Receptionists and
Information Clerks, Secretaries and Administrative Assistants, and Statistical
Assistants.

## Visual checks

All six generated figures were inspected at full resolution. The paper PDF was
rendered page by page and checked for missing figures, clipped content, and
placeholder text.
