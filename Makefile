INPUT = data/input/function_calling_tests.json
OUTPUT = data/output/function_calling_results.json

install:
	uv sync

sync:
	uv sync

run:
	uv run python3 -m src --input $(INPUT) --output $(OUTPUT)

debug:

clean: rm -rf $(FILES_TO_DELETE)

lint:
	uv run python -m flake8 src
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run python -m flake8 src
	mypy . --strict