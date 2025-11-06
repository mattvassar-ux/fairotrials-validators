import subprocess
from pathlib import Path

def test_fdaaa_timeliness_runs(tmp_path):
    out = tmp_path / "fdaaa_timeliness_report.csv"
    cmd = [
        "fairo-fdaaa",
        "--input", "samples/sample_fdaaa_trials.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
