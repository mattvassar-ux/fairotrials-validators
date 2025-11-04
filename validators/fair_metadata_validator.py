#!/usr/bin/env python3
"""
FAIR Metadata Validator (MVP)
Checks presence/format of key fields for Findable, Accessible, Interoperable, Reusable.
Input: JSON list of trials with keys below.
"""
import argparse, json, csv, re

RE_DOI = re.compile(r'\b10\.\d{4,9}/\S+\b', re.I)

REQUIRED = [
    "trial_id", "title", "registry", "registry_url",
    "sponsor", "phase", "condition", "intervention"
]

def booly(x): return bool(x and str(x).strip())

def has_persistent_ids(rec):
    # Accept NCT pattern or other registry ID; DOIs for pubs optional but recommended
    nct_ok = bool(re.match(r'^(NCT\d{8}|EUCTR|ISRCTN|ANZCTR|ChiCTR|DRKS|JPRN)', str(rec.get("trial_id","")).upper()))
    any_pub_doi = any(RE_DOI.search(d or "") for d in rec.get("publication_dois", []) or [])
    return nct_ok, any_pub_doi

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="fair_metadata_report.csv")
    args = ap.parse_args()

    data = json.load(open(args.input, "r", encoding="utf-8"))
    rows = []
    for rec in data:
        checks = {f"has_{k}": booly(rec.get(k)) for k in REQUIRED}
        nct_ok, pub_doi_ok = has_persistent_ids(rec)
        checks["has_persistent_trial_id"] = nct_ok
        checks["has_publication_doi"] = pub_doi_ok
        total = len(checks)
        passed = sum(1 for v in checks.values() if v)
        pct = round(100.0 * passed/total, 1) if total else 0.0
        rows.append({
            "trial_id": rec.get("trial_id",""),
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
