# ==============================================================================
# Makefile - Automated Resume & Skill Gap Analyzer
# ==============================================================================

.PHONY: help install dev run test lint clean format

PYTHON ?= python3
VENV ?= .venv

help:
	@echo "Available Make Commands:"
	@echo "  make install    - Install core dependencies"
	@echo "  make dev        - Install core + development dependencies"
	@echo "  make run        - Launch Streamlit application"
	@echo "  make test       - Run pytest test suite"
	@echo "  make lint       - Run ruff code linter"
	@echo "  make format     - Automatically format code with ruff"
	@echo "  make clean      - Remove build, cache, and bytecode artifacts"

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt

run:
	streamlit run resume_analyzer/app.py

test:
	pytest resume_analyzer/tests -v

lint:
	ruff check .

format:
	ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
