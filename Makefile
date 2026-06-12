NAME = src
EXEC = python
DEBUGER = pdb

install:
	uv init
	uv add numpy
	uv add pydantic
	uv add flake8
	uv add mypy
	uv add torch
	uv add transformers

run:
	uv run $(EXEC) -m $(NAME)

debug:
	uv run $(EXEC) -m $(DEBUGER) $(NAME)

lint:
	uv run flake8 . --exclude=llm_sdk/llm_sdk/__init__.py,.venv
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude="\.venv" \
        --exclude="llm_sdk/llm_sdk/__init__\.py"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf .venv .python-version main.py

.PHONY: install run debug lint clean