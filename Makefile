# Makefile for Music Trends Analysis Project

.PHONY: all setup run-model run-viz test clean

all: setup run-model run-viz test

setup:
	pip install -r requirements.txt

run-model:
	python3 src/data_processing.py
	python3 src/train_model.py

run-viz:
	python3 src/visualization.py

test:
	PYTHONPATH=. python3 tests/test_pipeline.py

clean:
	rm -rf __pycache__
	rm -f data/processed/merged_data.csv
	rm -rf visualizations/*.png visualizations/*.html
