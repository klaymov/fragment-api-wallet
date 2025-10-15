ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif


.PHONY: pull
pull:
	git pull origin master
	git submodule update --init --recursive

.PHONY: lint
lint:
	echo "Running ruff..."
	uv run ruff check --config pyproject.toml --diff

.PHONY: format
format:
	echo "Running ruff check with --fix..."
	uv run ruff check --config pyproject.toml --fix --unsafe-fixes

	echo "Running ruff..."
	uv run ruff format --config pyproject.toml

	echo "Running isort..."
	uv run isort --settings-file pyproject.toml

.PHONY: mypy
mypy:
	echo "Running MyPy..."
	uv run mypy --config-file pyproject.toml --explicit-package-bases/

.PHONY: outdated
outdated:
	uv tree --outdated --universal

.PHONY: sync
sync:
	uv sync --extra lint
