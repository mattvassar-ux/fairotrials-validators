import subprocess
from pathlib import Path

def test_linkage_runs(tmp_path):
    out = tmp_path / "linkage_report.csv"
    cmd = [
        "fairo-linkage",
        "--registry", "samples/sample_registry_linkage.json",
        "--pubs", "samples/sample_publications.json",
        "--out_csv", str(out)
    ]
    subprocess.run(cmd, check=True)
    assert out.exists() and out.stat().st_size > 0
