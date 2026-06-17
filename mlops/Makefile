SHELL := /bin/bash
VENV  := .venv
PY    := $(VENV)/bin/python
PIP   := $(VENV)/bin/pip
export DYLD_LIBRARY_PATH := /opt/homebrew/opt/expat/lib

.PHONY: help setup install fetch train eval export pipeline test lint clean dvc-init mlflow-ui

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install the package + dev deps
	@test -d $(VENV) || python3.12 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"

install: ## Reinstall the package after pyproject.toml change
	$(PIP) install -e ".[dev]"

fetch: ## Download dataset(s) into data/raw/
	$(PY) scripts/fetch_data.py

train: ## Train anomaly model on the configured category
	$(PY) scripts/train.py

eval: ## Run eval harness against latest checkpoint
	$(PY) scripts/evaluate.py

export: ## Export trained model(s) to ONNX for cloud GPU serving
	$(PY) scripts/export.py

pipeline: ## Run full DVC pipeline
	$(VENV)/bin/dvc repro

test: ## Run pytest
	$(VENV)/bin/pytest -q

lint: ## Lint with ruff
	$(VENV)/bin/ruff check src scripts tests

dvc-init: ## One-time DVC init (run once at the start of the project)
	$(VENV)/bin/dvc init --subdir

mlflow-ui: ## Browse experiment runs at http://127.0.0.1:5000
	$(VENV)/bin/mlflow ui --backend-store-uri file:./mlruns

clean: ## Remove caches and build artifacts (keeps venv and raw data)
	rm -rf build dist *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
