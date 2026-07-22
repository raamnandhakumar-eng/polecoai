# Contributing

Small corrections and reproducibility improvements are welcome through GitHub
issues or pull requests.

Before submitting a change:

1. Install the project with `python -m pip install -e ".[dev]"`.
2. Run `python tests/test_smoke.py`.
3. If official data are available locally, run
   `python tests/test_reported_results.py`.
4. State whether generated tables or figures changed and explain why.

Do not commit downloaded raw data, credentials, local environments, caches, or
unlicensed third-party material. Changes that alter reported results should
include a clear methodological justification and corresponding paper update.
