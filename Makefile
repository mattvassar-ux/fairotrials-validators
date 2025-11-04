
SHELL := /bin/bash

.PHONY: help install dev run-all test docker-build docker-run lint package clean

help:
	@echo "Targets:"
	@echo "  install      - pip install the package (editable)"
	@echo "  dev          - install dev deps (build, wheel)"
	@echo "  run-all      - run all validators on samples via CLI"
	@echo "  test         - CI-like sample run"
	@echo "  docker-build - build Docker image"
	@echo "  docker-run   - run FDAAA validator in Docker (writes CSV to host)"
	@echo "  lint         - (placeholder)"
	@echo "  package      - build wheel and sdist"
	@echo "  clean        - remove build artifacts and CSVs"

install:
	python -m pip install --upgrade pip
	pip install -e .

dev:
	pip install build

run-all:
	fairo run-all-samples

test:
	fairo run-all-samples --prefix test_
	@ls -1 *_report.csv | sed -n '1,7p'

docker-build:
	docker build -t fairotrials-validators:latest .

docker-run:
	docker run --rm -v "$$PWD:/work" -w /app fairotrials-validators:latest \
	  fairo fdaaa --input samples/sample_fdaaa_trials.json --out_csv /work/fdaaa_timeliness_report.csv

lint:
	@echo "No linters configured (keep MVP light)."

package:
	python -m build

clean:
	rm -rf build dist *.egg-info *_report.csv
