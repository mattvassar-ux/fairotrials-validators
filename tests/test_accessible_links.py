import subprocess
from pathlib import Path

def test_accessible_links_runs(tmp_path):
    out = tmp_path / "accessible_links_report.csv"
    cmd = [
        "fairo-accessible",
        "--input", "samples/sample_access_links.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
