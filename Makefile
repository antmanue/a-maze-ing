all: venv install run

venv: ## 1. Creates virtual environment to isolate dependencies
	python3 -m venv venv
	@echo "Activate with: source venv/bin/activate"

install: ## 1.1 DONT FORGET TO ACTIVATE "VENV" IT FIRST. Install linters
	pip install mypy
	pip install flake8
	pip install mlx-2.2-py3-none-any.whl
	python3 -c "from mlx import Mlx; print('[OK] MLX')"

package: ## 1.2 Install files from build
	pip install mlx-2.2-py3-none-any.whl
	pip install build
	python3 -m build
	mv dist/mazegen-1.0.0-py3-none-any.whl .
	pip install mazegen-1.0.0-py3-none-any.whl

run: ## 3. Run
	python3 a_maze_ing.py config.txt
	
clean: ## 4. Delete all bytecode (.pyc) that is stored inside __pycache__ and remove virtual env
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf venv
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm mazegen-*.whl
	rm maze.txt

debug: ## Run the python built in debugger(with comands s-step, n-next, c-continue, q-quit)
	python3 -m pdb a_maze_ing.py config.txt
	
lint: ## Make all style and typehints verifcations
	flake8 . --exclude=venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=venv
	mypy . --strict
