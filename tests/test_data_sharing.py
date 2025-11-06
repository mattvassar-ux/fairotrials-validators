import subprocess
from pathlib import Path

def test_data_sharing_runs(tmp_path):
    out = tmp_path / "data_sharing_report.csv"
    cmd = [
        "fairo-data-sharing",
        "--pubs", "samples/sample_data_sharing_pubs.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
