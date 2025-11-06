import subprocess
from pathlib import Path

def test_fair_metadata_runs(tmp_path):
    out = tmp_path / "fair_metadata_report.csv"
    cmd = [
        "fairo-fair-meta",
        "--input", "samples/sample_fair_trials.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
