import subprocess
from pathlib import Path

def test_outcome_switching_runs(tmp_path):
    out = tmp_path / "outcome_switching_report.csv"
    cmd = [
        "fairo-outcomes",
        "--input", "samples/sample_outcomes.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
