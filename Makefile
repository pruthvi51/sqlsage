.PHONY: help setup test demo bench paper clean

help:
	@echo "SQLSage NL-to-SQL Platform Commands:"
	@echo "  make setup     Install dependencies with uv"
	@echo "  make test      Run unit and integration test suite"
	@echo "  make demo      Launch Streamlit interactive NL-to-SQL workbench"
	@echo "  make bench     Run CareLake-QA execution accuracy benchmark"
	@echo "  make paper     Compile LaTeX research technical report with tectonic"

setup:
	uv pip install -e ".[dev]"

test:
	pytest -v tests/

demo:
	streamlit run ui/app.py

bench:
	python3 -m sqlsage.eval.benchmark

paper:
	cd paper && tectonic sqlsage_architecture_paper.tex

clean:
	rm -rf .pytest_cache logs/ target/
