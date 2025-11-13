#!/usr/bin/env python3
"""
FAIR Metadata Validator (ClinicalTrials.gov compatible)
Extracts and validates key fields (Findable, Accessible, Interoperable, Reusable)
and outputs results to an Excel spreadsheet.
"""

import argparse, json, re, os
import pandas as pd

RE_DOI = re.compile(r'\b10\.\d{4,9}/\S+\b')

REQUIRED = [
    "trial_id", "title", "registry", "registry_url",
    "sponsor", "phase", "condition", "intervention", "publication_dois"
]

def extract_from_clinicaltrials(raw):
    """Extracts key fields from a ClinicalTrials.gov JSON file."""
    p = raw.get("protocolSection", {})

    return {
        "trial_id": p.get("identificationModule", {}).get("nctId", ""),
        "title": p.get("identificationModule", {}).get("briefTitle", ""),
        "registry": "ClinicalTrials.gov",
        "registry_url": f"https://clinicaltrials.gov/study/{p.get('identificationModule', {}).get('nctId', '')}",
        "sponsor": p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", ""),
        "phase": ", ".join(p.get("designModule", {}).get("phases", [])) or "",
        "condition": ", ".join(p.get("conditionsModule", {}).get("conditions", [])) or "",
        "intervention": ", ".join(
            [i.get("name", "") for i in p.get("armsInterventionsModule", {}).get("interventions", [])]
        ),
        "publication_dois": []  # Not available in ClinicalTrials.gov exports
    }

def booly(val):
    """Treat non-empty strings/lists as True."""
    if val is None:
        return False
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return bool(str(val).strip())

def validate_trial(rec):
    """Return FAIR validation dictionary for one record."""
    checks = {f"has_{k}": booly(rec.get(k)) for k in REQUIRED}
    checks["trial_id"] = rec.get("trial_id", "")
    return checks

def main():
    parser = argparse.ArgumentParser(description="FAIR Metadata Validator (ClinicalTrials.gov compatible)")
    parser.add_argument("--input", required=True, help="Input JSON file (flat or ClinicalTrials.gov format)")
    parser.add_argument("--output", default="validation_results.xlsx", help="Output Excel filename")
    args = parser.parse_args()

    # Load JSON
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize input into a list of records
    if isinstance(data, dict):
        if "protocolSection" in data:
            records = [extract_from_clinicaltrials(data)]
        else:
            records = [data]
    elif isinstance(data, list):
        records = []
        for item in data:
            if "protocolSection" in item:
                records.append(extract_from_clinicaltrials(item))
            else:
                records.append(item)
    else:
        raise ValueError("Unrecognized JSON format")

    # Validate all records
    results = [validate_trial(rec) for rec in records]

    # Convert to Excel
    df = pd.DataFrame(results)
    output_path = os.path.join(os.getcwd(), args.output)
    df.to_excel(output_path, index=False)

    print(f"✅ Validation complete. Results saved to: {output_path}")

if __name__ == "__main__":
    main()
