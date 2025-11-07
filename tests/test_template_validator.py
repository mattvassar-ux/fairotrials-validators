
import json, os, tempfile, csv
from validators.template_validator import validate_record

def test_validate_record_minimal():
    r = validate_record({"trial_id":"T1"})
    assert r["trial_id"] == "T1"
    assert r["basic_ok"] is True
    assert r["notes"] == ""

def test_validate_record_missing_id():
    r = validate_record({})
    assert r["trial_id"] == ""
    assert r["basic_ok"] is False
    assert "missing_trial_id" in r["notes"]
