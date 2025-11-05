# FAIROTrials Validators (MVP Bundle)


## Project Context
This repository serves as the prototype for the **FAIROTrials Commons** project,
an NSF POSE Phase 1 initiative led by Dr. Matt Vassar (Oklahoma State University).
It provides seven lightweight, reproducible validators for assessing transparency
and traceability in clinical trial metadata, outcome reporting, and data sharing.
Each validator is independently executable and Docker-ready, providing a working
proof-of-concept for a FAIR and Open Science (FAIRO) clinical trial validation ecosystem.


Seven lightweight validators for clinical trial transparency & traceability.
Each validator is a single Python script with sample JSON and CSV output.

## Validators
1. **FAIR Metadata** — checks core metadata & persistent IDs (`fair_metadata_validator.py`)
2. **FDAAA Timeliness** — flags on-time/late/missing results (`fdaaa_timeliness_validator.py`)
3. **Accessible Links** — basic URL & HTTPS checks (`accessible_link_checker.py`)
4. **Outcome Switching** — compares registered vs published primary outcomes (`outcome_switching_validator.py`)
5. **CONSORT‑Harms Completeness** — key harms reporting elements (`consort_harms_validator.py`)
6. **Trial Linkage** — registry ↔ publication bidirectional links (`linkage_validator.py`)
7. **Data Sharing Transparency** — dataset DOI, code repo, license, access (`data_sharing_validator.py`)

## Quickstart (Windows)
Install Python 3.11+ then open **PowerShell** in this folder:
```
py validators\fair_metadata_validator.py --input samples\sample_fair_trials.json --out_csv fair_metadata_report.csv
py validators\fdaaa_timeliness_validator.py --input samples\sample_fdaaa_trials.json --out_csv fdaaa_timeliness_report.csv
py validators\accessible_link_checker.py --input samples\sample_access_links.json --out_csv accessible_links_report.csv
py validators\outcome_switching_validator.py --input samples\sample_outcomes.json --out_csv outcome_switching_report.csv
py validators\consort_harms_validator.py --input samples\sample_harms.json --out_csv consort_harms_report.csv
py validators\linkage_validator.py --registry samples\sample_registry_linkage.json --pubs samples\sample_publications.json --out_csv linkage_report.csv
py validators\data_sharing_validator.py --pubs samples\sample_data_sharing_pubs.json --out_csv data_sharing_report.csv
```

## One‑click demo (Windows)
Double‑click `run_all.bat` to generate all 7 CSV reports.

## License
Apache‑2.0 (see `LICENSE`)


## Docker (reproducible runs)
Build locally:
```
docker build -t fairotrials-validators:latest .
```

Run a validator (writes CSV to your host working directory):
```
docker run --rm -v "$PWD:/work" -w /app fairotrials-validators:latest   fairo-fdaaa --input samples/sample_fdaaa_trials.json --out_csv /work/fdaaa_timeliness_report.csv
```

CI builds a Docker image on every push (see `.github/workflows/docker.yml`).

## PyPI Release (optional)
This repo includes a workflow to publish to PyPI on **GitHub Releases**.
Before using it:
1. Create a PyPI project name (e.g., `fairotrials-validators`).
2. Add a repository secret **`PYPI_API_TOKEN`** (from PyPI > Account settings > API tokens).
3. Create a GitHub release (tag like `v0.1.0`). The workflow builds and publishes.


## Unified CLI
After installing (`pip install -e .`), you can run everything via **`fairo`**:
```
# Run all validators on bundled samples
fairo run-all-samples

# Or call a specific one
fairo fdaaa --input samples/sample_fdaaa_trials.json --out_csv fdaaa_timeliness_report.csv
```


## Makefile (handy shortcuts)
```
make install       # pip install -e .
make run-all       # run all validators on samples (via CLI)
make docker-build  # build Docker image
make docker-run    # run one validator in Docker and write CSV to host
make package       # build wheel and sdist
```
