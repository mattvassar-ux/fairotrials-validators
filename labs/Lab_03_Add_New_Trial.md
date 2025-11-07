
# Lab 03 — Add a Trial and Re‑run

## Goal
Modify a sample JSON to add one more trial record and re‑run.

## Steps
1. Open `samples/sample_outcomes.json` in a text editor.
2. Duplicate the last record and change:
   - `trial_id`
   - `registered_primary_outcomes`
   - `published_primary_outcomes`
3. Save the file, then run:
   ```powershell
   py validators/outcome_switching_validator.py --input samples/sample_outcomes.json --output outcome_switching_report.csv
   ```
4. Verify your new `trial_id` appears in the CSV; discuss results.
