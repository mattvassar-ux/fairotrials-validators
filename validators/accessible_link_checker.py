#!/usr/bin/env python3
"""
Accessible Link Checker (MVP)
Offline-friendly: validates URL format and HTTPS scheme; flags obvious problems.
Input: JSON list of records with any of these keys: registry_url, publication_urls, dataset_urls
"""
import argparse, json, csv, re

URL_RE = re.compile(r'^(https?)://[^\s/$.?#].[^\s]*$', re.I)

def ok_url(u):
    if not u: return False, "empty"
    if not URL_RE.match(u): return False, "invalid_format"
    if not u.lower().startswith("https://"): return False, "not_https"
    return True, ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="accessible_links_report.csv")
    args = ap.parse_args()

    data = json.load(open(args.input, "r", encoding="utf-8"))
    rows = []
    for rec in data:
        trial = rec.get("trial_id","")
        urls = []
        if rec.get("registry_url"): urls.append(("registry_url", rec["registry_url"]))
        for u in rec.get("publication_urls",[]) or []: urls.append(("publication_url", u))
        for u in rec.get("dataset_urls",[]) or []: urls.append(("dataset_url", u))

        if not urls:
            rows.append({"trial_id": trial, "url_type":"", "url":"", "ok":False, "issue":"no_urls_provided"})
            continue

        for typ, u in urls:
            ok, issue = ok_url(u)
            rows.append({"trial_id": trial, "url_type": typ, "url": u, "ok": ok, "issue": issue})
    hdr = list(rows[0].keys()) if rows else []
    import csv
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)
    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
