import subprocess
from pathlib import Path

def test_consort_harms_runs(tmp_path):
    out = tmp_path / "consort_harms_report.csv"
    cmd = [
        "fairo-harms",
        "--input", "samples/sample_harms.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
