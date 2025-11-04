#!/usr/bin/env python3
"""
Data Sharing Transparency Validator (MVP)
-----------------------------------------
Assesses whether a publication provides an auditable, open data/code trail,
aligned with ICMJE/CONSORT/TOP-style expectations.

Inputs (JSON)
-------------
--pubs : list of publication records like:
[{
  "doi": "10.1056/NEJM123456",
  "title": "...",
  "abstract": "...",
  "fulltext_text": "optional, plain text of paper",
  "data_availability_section": "optional extracted section text",
  "dataset_dois": ["10.5281/zenodo.12345", "10.5061/dryad.abc123"],
  "code_urls": ["https://github.com/org/repo"],
  "license": "CC-BY-4.0",
  "access_model": "open|restricted|on_request",
  "embargo_end": "2026-01-31"
}]

Output (CSV)
------------
One row per publication with flags and a % completeness score:

doi, has_data_statement, has_dataset_doi, has_code_repo, has_license,
license_is_open, access_is_open, embargo_active, checks_passed,
total_checks, percent_complete, notes
"""
import argparse, csv, json, re, sys
from datetime import datetime

DATA_STMT_HINTS = [
    r"data (are|is) available",
    r"data availability",
    r"availability of data",
    r"deposited (in|at)",
    r"data (repository|repositories)",
    r"upon reasonable request",
    r"accession|dataset doi|zenodo|dryad|figshare|osf\.io|nda\.nih\.gov"
]

OPEN_LICENSE_HINTS = [
    r"\bcc-?by\b",
    r"\bcc-?0\b",
    r"\bmit\b",
    r"\bbsd\b",
    r"\bapache\b",
    r"\bgpl\b",
]

REPO_HINTS = [
    r"github\.com/",
    r"gitlab\.com/",
    r"bitbucket\.org/",
]

DOI_PATTERN = re.compile(r'\b10\.\d{4,9}/\S+\b', re.I)

def truthy(x):
    if x is None: return False
    if isinstance(x, bool): return x
    if isinstance(x, (int, float)): return x != 0
    if isinstance(x, str): return x.strip() != ""
    if isinstance(x, (list, dict, set, tuple)): return len(x) > 0
    return True

def find_any(patterns, text):
    t = (text or "").lower()
    for pat in patterns:
        if re.search(pat, t, flags=re.I):
            return True
    return False

def has_dataset_doi(pub):
    # Either in structured field or detectable via text
    if truthy(pub.get("dataset_dois")):
        return True
    blob = " ".join([
        pub.get("data_availability_section","") or "",
        pub.get("fulltext_text","") or "",
        pub.get("abstract","") or "",
        pub.get("title","") or "",
    ])
    if re.search(r'zenodo|dryad|figshare|osf\.io|nda\.nih\.gov', blob, flags=re.I):
        return True
    if DOI_PATTERN.search(blob):
        # crude: count as dataset DOI if it appears near typical repo words
        ctx = blob.lower()
        return any(k in ctx for k in ["zenodo","dryad","figshare","osf.io","nda.nih.gov","dataverse","pdb","ebi"])
    return False

def has_code_repo(pub):
    if truthy(pub.get("code_urls")):
        return True
    blob = " ".join([pub.get("data_availability_section","") or "", pub.get("fulltext_text","") or "", pub.get("abstract","") or "", pub.get("title","") or ""])
    return find_any(REPO_HINTS, blob)

def has_open_license(pub):
    lic = (pub.get("license") or "").lower()
    if lic and find_any(OPEN_LICENSE_HINTS, lic):
        return True
    # Also scan text for license markers
    blob = " ".join([pub.get("data_availability_section","") or "", pub.get("fulltext_text","") or ""])
    return find_any(OPEN_LICENSE_HINTS, blob)

def has_data_statement(pub):
    blob = " ".join([
        pub.get("data_availability_section","") or "",
        pub.get("fulltext_text","") or "",
        pub.get("abstract","") or "",
        pub.get("title","") or "",
    ])
    return find_any(DATA_STMT_HINTS, blob)

def access_is_open(pub):
    mode = (pub.get("access_model") or "").strip().lower()
    if mode in ("open","public","open access","public access"):
        return True
    # fallback: infer from phrases
    blob = " ".join([pub.get("data_availability_section","") or "", pub.get("fulltext_text","") or ""]).lower()
    if "available without restriction" in blob or "publicly available" in blob or "openly available" in blob:
        return True
    return False

def embargo_active(pub, today=None):
    today = today or datetime.utcnow().date()
    raw = pub.get("embargo_end")
    if not raw:
        return False
    try:
        d = datetime.fromisoformat(raw).date()
        return d > today
    except Exception:
        return False

def score(pub):
    checks = {
        "has_data_statement": has_data_statement(pub),
        "has_dataset_doi": has_dataset_doi(pub),
        "has_code_repo": has_code_repo(pub),
        "has_license": truthy(pub.get("license")) or has_open_license(pub),
        "license_is_open": has_open_license(pub),
        "access_is_open": access_is_open(pub),
        "embargo_active": embargo_active(pub),  # This is informative, not required
    }
    # Total checks count: treat embargo_active as informative and NOT counted against completeness
    required_keys = ["has_data_statement","has_dataset_doi","has_code_repo","has_license","license_is_open","access_is_open"]
    checks_passed = sum(1 for k in required_keys if checks[k])
    total_checks = len(required_keys)
    percent = round(100.0 * checks_passed / total_checks, 1) if total_checks else 0.0
    return checks, checks_passed, total_checks, percent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pubs", required=True, help="JSON: publications with data/code info")
    ap.add_argument("--out_csv", default="data_sharing_report.csv")
    args = ap.parse_args()

    try:
        pubs = json.load(open(args.pubs, "r", encoding="utf-8"))
    except Exception as e:
        print(f"[error] Could not read JSON: {e}", file=sys.stderr)
        sys.exit(2)

    rows = []
    for p in pubs:
        doi = (p.get("doi") or "").lower()
        checks, passed, total, pct = score(p)
        rows.append({
            "doi": doi,
            **checks,
            "checks_passed": passed,
            "total_checks": total,
            "percent_complete": pct,
            "notes": ""
        })

    if not rows:
        print("[warn] No rows; check input.", file=sys.stderr)
        sys.exit(0)

    headers = list(rows[0].keys())
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader(); w.writerows(rows)

    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
