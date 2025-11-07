
# Developer Guide — FAIROTrials Validators (Education-Ready)

This guide explains the repo structure and how to extend it safely for teaching and POSE Phase 1 demos.

## Repository Layout (additions)
```
docs/
  developer_guide.md      # this file
educational_modules/      # lecture-ready content
labs/                     # step-by-step student labs
tests/                    # unit tests for new validators
validators/               # production validators + template
```

## Local Setup (Windows/macOS/Linux)
1. Install Python 3.11+
2. Clone the repo: `git clone https://github.com/mattvassar-ux/fairotrials-validators`
3. `cd fairotrials-validators`
4. (Optional) Create a virtual env
5. Install package in editable mode: `pip install -e .`

## Quick Run
- Run all: `py run_all.bat` (Windows) or `python -m validators.fair_metadata_validator --help` etc.
- Example:  
  `py validators/fair_metadata_validator.py --input samples/sample_fair_trials.json --output fair_metadata_report.csv`

## Adding a New Validator (10‑minute path)
1. Copy `validators/template_validator.py` → `validators/<your_name>_validator.py`
2. Edit `REQUIRED_FIELDS` and `validate_record()` to implement your checks.
3. Place a **sample JSON** in `samples/` and run:
   ```bash
   py validators/<your_name>_validator.py --input samples/<your_sample>.json --output <your_report>.csv
   ```
4. Add a minimal unit test in `tests/test_<your_name>_validator.py` (see template).
5. Open a Pull Request.

## CSV Output Contract
All validators should write a CSV with:
- `trial_id`
- one or more boolean/score columns
- `notes` (semicolon‑separated reasons/flags)

## Code Style & Linting
- Keep scripts single‑file, dependency‑light.
- OK to import: `json, csv, argparse, datetime, re, urllib.request`.
- Avoid network calls for classroom runs unless behind `--allow-network`.

## Releasing
- Tag releases (e.g., `v0.1.1`) after labs are updated.
- Keep `docs/` and `labs/` in sync with CLI examples.
