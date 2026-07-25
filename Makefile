.PHONY: install data analysis extensions robustness exposure verify paper reproduce smoke

install:
	python -m pip install -e ".[dev]"

data:
	python scripts/download_data.py

analysis:
	python scripts/run_analysis.py

extensions:
	python scripts/run_extensions.py

robustness:
	python scripts/run_robustness.py

exposure:
	python scripts/run_latest_exposure.py

verify:
	python tests/test_reported_results.py

paper:
	python scripts/build_paper.py

smoke:
	python tests/test_smoke.py

reproduce: data analysis extensions robustness exposure verify paper
