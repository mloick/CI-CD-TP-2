.PHONY: test test-cov lint

test:
	./venv/bin/pytest -v

test-cov:
	./venv/bin/pytest --cov=src --cov-fail-under=80

lint:
	./venv/bin/ruff check .
