install: ## Install linters
	pip install mypy
	pip install flake8

venv: ## Creates virtual environment to isolate dependencies
	python3 -m venv venv
	@echo "Activate with: source venv/bin/activate"

run:

debug:

clean: ## Delete all bytecode (.pyc) that is stored inside __pycache__ and remove virtual env
	rm maze.txt
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf venv

lint:
	flake8 . --exclude=venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=venv
	mypy . --strict
