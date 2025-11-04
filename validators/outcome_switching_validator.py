#!/usr/bin/env python3
"""
Outcome Switching Validator (MVP)
Compares registered primary outcomes vs published primary outcomes.
Input JSON list of records with: nct_id, registered_primary_outcomes[], published_primary_outcomes[]
"""
import argparse, json, csv

def norm(x): return [s.strip().lower() for s in (x or []) if s and str(s).strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="outcome_switching_report.csv")
    args = ap.parse_args()

    data = json.load(open(args.input, "r", encoding="utf-8"))
    rows = []
    for rec in data:
        nct = rec.get("nct_id","")
        reg = set(norm(rec.get("registered_primary_outcomes")))
        pub = set(norm(rec.get("published_primary_outcomes")))
        missing_in_pub = sorted(list(reg - pub))
        added_in_pub = sorted(list(pub - reg))
        switched = bool(missing_in_pub or added_in_pub)
        rows.append({
            "nct_id": nct,
            "registered_primary_outcomes": "; ".join(sorted(reg)),
            "published_primary_outcomes": "; ".join(sorted(pub)),
            "missing_in_publication": "; ".join(missing_in_pub),
            "added_in_publication": "; ".join(added_in_pub),
            "outcome_switching_flag": switched
        })
    hdr = list(rows[0].keys()) if rows else []
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)
    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
