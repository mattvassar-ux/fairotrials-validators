#!/usr/bin/env python3
"""
CONSORT‑Harms Completeness Validator (MVP)
Checks presence of key harms reporting elements.
Input JSON list of trial harm summaries:
{ nct_id, arms: ["Drug X","Placebo"], ae_definition, collection_timeframe, solicited_vs_unsolicited, denominators_reported, by_severity, by_seriousness, by_body_system }
"""
import argparse, json, csv

FIELDS = [
  "ae_definition","collection_timeframe","solicited_vs_unsolicited",
  "denominators_reported","by_severity","by_seriousness","by_body_system"
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="consort_harms_report.csv")
    args = ap.parse_args()

    data = json.load(open(args.input, "r", encoding="utf-8"))
    rows = []
    for rec in data:
        checks = {f"has_{k}": bool(rec.get(k)) for k in FIELDS}
        total = len(checks)
        passed = sum(1 for v in checks.values() if v)
        pct = round(100.0 * passed/total, 1) if total else 0.0
        rows.append({
            "nct_id": rec.get("nct_id",""),
            **checks,
            "checks_passed": passed,
            "total_checks": total,
            "percent_complete": pct
        })

    hdr = list(rows[0].keys()) if rows else []
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)
    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
