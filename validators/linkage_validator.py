#!/usr/bin/env python3
import argparse, csv, json, re, sys
from typing import List, Dict

NCT_PATTERN = re.compile(r'\bNCT\d{8}\b', flags=re.I)

def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def mentions_nct_in_text(pub: dict, nct_id: str) -> bool:
    nct = (nct_id or "").strip().upper()
    if not nct:
        return False
    blob = " ".join([
        str(pub.get("title","")),
        str(pub.get("abstract","")),
        str(pub.get("nct_id_hint",""))
    ]).upper()
    found = set(re.findall(r'\bNCT\d{8}\b', blob))
    return nct in found

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--pubs", required=True)
    ap.add_argument("--out_csv", default="linkage_report.csv")
    args = ap.parse_args()

    try:
        reg = read_json(args.registry)
        pubs = read_json(args.pubs)
    except Exception as e:
        print(f"[error] Could not read JSON: {e}", file=sys.stderr)
        sys.exit(2)

    pubs_by_doi: Dict[str, dict] = {}
    pubs_by_pmid: Dict[str, dict] = {}
    pubs_by_nct: Dict[str, List[dict]] = {}

    for p in pubs:
        doi = (p.get("doi") or "").strip().lower()
        pmid = (p.get("pmid") or "").strip()
        if doi:
            pubs_by_doi[doi] = p
        if pmid:
            pubs_by_pmid[pmid] = p
        text = " ".join([str(p.get("title","")), str(p.get("abstract","")), str(p.get("nct_id_hint",""))]).upper()
        for found in set(re.findall(r'\bNCT\d{8}\b', text)):
            pubs_by_nct.setdefault(found, []).append(p)

    rows = []

    for trial in reg:
        nct = (trial.get("nct_id") or trial.get("trial_id") or "").strip().upper()
        reg_dois = set([ (d or "").strip().lower() for d in (trial.get("publication_dois") or []) if d ])
        reg_pmids = set([ (p or "").strip() for p in (trial.get("publication_pmids") or []) if p ])

        explicit_pubs = []
        for d in reg_dois:
            if d in pubs_by_doi:
                explicit_pubs.append(pubs_by_doi[d])
        for p in reg_pmids:
            if p in pubs_by_pmid:
                explicit_pubs.append(pubs_by_pmid[p])

        text_linked_pubs = pubs_by_nct.get(nct, [])

        seen_any = False

        def emit_row(pub: dict):
            nonlocal seen_any
            seen_any = True
            doi = (pub.get("doi") or "").strip().lower()
            pmid = (pub.get("pmid") or "").strip()
            pub_mentions = mentions_nct_in_text(pub, nct)
            registry_lists_pub = (doi in reg_dois) or (pmid in reg_pmids)
            bidirectional = pub_mentions and registry_lists_pub

            if bidirectional:
                status = "bidirectional_complete"
            elif registry_lists_pub and not pub_mentions:
                status = "registry_only"
            elif pub_mentions and not registry_lists_pub:
                status = "publication_only"
            else:
                status = "missing_both"

            rows.append({
                "nct_id": nct,
                "publication_doi": doi,
                "publication_pmid": pmid,
                "publication_mentions_nctid": pub_mentions,
                "registry_lists_publication": registry_lists_pub,
                "bidirectional_link": bidirectional,
                "link_status": status,
                "notes": ""
            })

        seen_ids = set()
        for p in explicit_pubs + text_linked_pubs:
            key = (p.get("doi") or "").lower(), (p.get("pmid") or "")
            if key in seen_ids:
                continue
            seen_ids.add(key)
            emit_row(p)

        if not seen_any:
            rows.append({
                "nct_id": nct,
                "publication_doi": "",
                "publication_pmid": "",
                "publication_mentions_nctid": False,
                "registry_lists_publication": False,
                "bidirectional_link": False,
                "link_status": "no_publications_indexed",
                "notes": ""
            })

    if not rows:
        print("[warn] No rows produced; check inputs.", file=sys.stderr)
        sys.exit(0)

    headers = list(rows[0].keys())
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader(); w.writerows(rows)

    print(f"[ok] Wrote {len(rows)} rows to {args.out_csv}")

if __name__ == "__main__":
    main()
