include common/Makefile

all: format-black format-isort test

format: format-ruff format-black format-isort

format-black:
	@echo [black] && poetry run black . -v

format-isort:
	@echo [isort] && poetry run isort --profile black --filter-files .

format-ruff:
	@echo [ruff] && poetry run ruff --fix --exclude .venv,working . || true

test:
	@echo [pytest] && poetry run pytest -svx # exit instantly on first error or failed test.

test-report:
	@echo [pytest] && poetry run pytest -svx --cov --cov-report html
