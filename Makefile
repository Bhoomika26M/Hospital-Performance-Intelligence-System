.PHONY: all setup data pipeline kpis storyboard workbook test clean

PYTHON = .venv/bin/python
PIP = .venv/bin/pip
PYTEST = .venv/bin/pytest

all: data pipeline kpis storyboard workbook test

setup:
	@echo "Creating virtual environment and installing dependencies..."
	python3.11 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

data:
	@echo "Acquiring raw hospital clinical encounter data..."
	$(PYTHON) scripts/data_collection.py

pipeline:
	@echo "Executing end-to-end deterministic data processing pipeline..."
	$(PYTHON) scripts/run_pipeline.py

kpis:
	@echo "Computing headline operational scorecards..."
	$(PYTHON) scripts/generate_hospital_kpis.py

storyboard:
	@echo "Generating programmatic 8-page storyboard PDF..."
	$(PYTHON) scripts/generate_storyboard.py

workbook:
	@echo "Building Tableau Packaged Workbook (Aegis.dv.twbx)..."
	$(PYTHON) scripts/build_tableau_workbook.py

test:
	@echo "Running automated test suite..."
	$(PYTEST) -v tests/

clean:
	@echo "Cleaning temporary Python bytecode and test caches..."
	rm -rf __pycache__ .pytest_cache tests/__pycache__ src/*/__pycache__

