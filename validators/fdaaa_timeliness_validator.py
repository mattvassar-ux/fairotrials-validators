#!/usr/bin/env python3
"""
FDAAA Timeliness Validator (MVP)
Computes lateness of results posting vs statutory deadline (simplified).
Input records need: nct_id, primary_completion_date (YYYY-MM-DD),
results_first_posted_date (YYYY-MM-DD or ""), is_applicable (bool).
"""
import argparse, json, csv
from datetime import date, timedelta

def parse(d):
    try:
        y,m,d = map(int, d.split("-"))
        return date(y,m,d)
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="fdaaa_timeliness_report.csv")
    args = ap.parse_args()

    data = json.load(open(args.input, "r", encoding="utf-8"))
    rows = []
    for rec in data:
        nct = rec.get("nct_id","")
        applicable = bool(rec.get("is_applicable", True))
        pcd = parse(rec.get("primary_completion_date","") or "")
        posted = parse(rec.get("results_first_posted_date","") or "")
        deadline = pcd + timedelta(days=365) if pcd else None
        status = "not_applicable"
        days_late = ""
        if applicable and pcd:
            if posted:
                if deadline and posted <= deadline:
                    status = "on_time"
                    days_late = 0
                else:
                    status = "late"
                    days_late = (posted - deadline).days if deadline else ""
            else:
                status = "missing"
                days_late = ""
        rows.append({
            "nct_id": nct,
            "primary_completion_date": rec.get("primary_completion_date",""),
            "results_first_posted_date": rec.get("results_first_posted_date",""),
            "deadline_1yr_after_pcd": str(deadline) if deadline else "",
            "status": status,
            "days_late": days_late
        })

    hdr = list(rows[0].keys()) if rows else []
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)
    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
