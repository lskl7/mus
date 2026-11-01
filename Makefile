PYTHON := .venv/bin/python
SRC := src
export PYTHONPATH := src/music
export MYPYPATH := src/music

.PHONY: install lint typecheck check run

install:
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m flake8 $(SRC)

typecheck:
	$(PYTHON) -m mypy --strict --explicit-package-bases $(SRC)/music

check: lint typecheck

run:
	PYTHONPATH=src/music .venv/bin/python src/music/__main__.py
