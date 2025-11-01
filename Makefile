.PHONY: help install dev format lint test security clean run build

help:  ## Show this help
	@echo "5GH'z Cleaner - Makefile Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

dev:  ## Install dev dependencies
	pip install -r requirements.txt[dev]

format:  ## Format code (Black + isort)
	black src/ tests/ --line-length 120
	isort src/ tests/ --profile black

lint:  ## Lint code (Pylint + Flake8)
	pylint src/ --exit-zero
	flake8 src/

test:  ## Run tests
	pytest tests/ -v --cov=src --cov-report=term-missing

security:  ## Security checks (Bandit + Safety)
	bandit -r src/ -ll
	safety check

clean:  ## Clean cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true

run:  ## Run application
	python main.py

build:  ## Build application
	python scripts/build.py

all: format lint test security  ## Run all checks

.DEFAULT_GOAL := help
