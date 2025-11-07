
#!/usr/bin/env python3
"""Template Validator

Usage:
  py validators/template_validator.py --input samples/sample_template.json --output template_report.csv

This template shows the minimal structure to implement a new rule set.
Keep it dependency-light and CSV-oriented to be classroom-friendly.
"""
import argparse, csv, json, sys
from typing import Dict, List, Any

REQUIRED_FIELDS = ["trial_id"]

def validate_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dictionary of columns for one record.
    Always include 'trial_id' and 'notes'.
    """
    notes: List[str] = []
    row = {"trial_id": rec.get("trial_id", "")}

    # Example check: record contains all REQUIRED_FIELDS
    for f in REQUIRED_FIELDS:
        if not rec.get(f):
            notes.append(f"missing_{f}")

    # Example boolean column
    row["basic_ok"] = (len(notes) == 0)

    row["notes"] = ";".join(notes) if notes else ""
    return row

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to JSON file with a list of trial dicts")
    p.add_argument("--output", required=True, help="CSV output filename")
    args = p.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[error] Input file not found: {args.input}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, list):
        print("[error] Input JSON must be a list of records", file=sys.stderr)
        sys.exit(2)

    out_rows = []
    for rec in data:
        out_rows.append(validate_record(rec))

    cols = list(out_rows[0].keys()) if out_rows else ["trial_id","basic_ok","notes"]
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"[ok] wrote {len(out_rows)} rows to {args.output}")

if __name__ == "__main__":
    main()
