PYTHON ?= $(shell if [ -f ../.venv/bin/python3 ]; then echo ../.venv/bin/python3; elif [ -f .venv/bin/python3 ]; then echo .venv/bin/python3; else which python3; fi)
PYTEST ?= $(shell if [ -f ../.venv/bin/pytest ]; then echo ../.venv/bin/pytest; elif [ -f .venv/bin/pytest ]; then echo .venv/bin/pytest; else which pytest; fi)
STREAMLIT ?= $(shell if [ -f ../.venv/bin/streamlit ]; then echo ../.venv/bin/streamlit; elif [ -f .venv/bin/streamlit ]; then echo .venv/bin/streamlit; else which streamlit; fi)

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
	$(PYTEST) -v tests/

demo:
	$(STREAMLIT) run ui/app.py

bench:
	$(PYTHON) -m sqlsage.eval.benchmark

paper:
	cd paper && tectonic sqlsage_architecture_paper.tex

clean:
	rm -rf .pytest_cache logs/ target/
