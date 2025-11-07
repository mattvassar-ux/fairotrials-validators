
# Lab 01 — Run the Validators (Windows)

## Goal
Generate CSV reports locally using the sample JSON files.

## Steps
1. Install Python 3.11+
2. Download the repository ZIP from GitHub and extract it.
3. Open the folder in Explorer, click the **path bar**, type `powershell`, press **Enter**.
4. Run one validator:
   ```powershell
   py validators/fair_metadata_validator.py --input samples/sample_fair_trials.json --output fair_metadata_report.csv
   ```
5. Confirm `fair_metadata_report.csv` appears in the same folder; open it with Notepad.
6. (Optional) Run all on Windows with:
   ```powershell
   run_all.bat
   ```
