.PHONY: setup lint format test clean coverage

setup:
	uv pip install -e ".[dev]"

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

test:
	pytest tests/ -v

coverage:
	pytest --cov=xllm6 tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 