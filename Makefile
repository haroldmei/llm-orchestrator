.PHONY: install test lint format clean run

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf logs/*.log
	rm -rf specs/*.md

run:
	python main.py --data-spec data/data_spec_example.md

