.PHONY: lint-boundaries test

lint-boundaries:
	venv/bin/lint-imports

test:
	FLASK_ENV=testing venv/bin/python -m pytest tests/ -v

lint: lint-boundaries
