
import argparse
import sys
from .fair_metadata_validator import main as fair_meta_main
from .fdaaa_timeliness_validator import main as fdaaa_main
from .accessible_link_checker import main as accessible_main
from .outcome_switching_validator import main as outcomes_main
from .consort_harms_validator import main as harms_main
from .data_sharing_validator import main as data_sharing_main

# linkages might not exist if user didn't copy; guard import
def _linkage_main():
    try:
        from .linkage_validator import main as linkage_main
        return linkage_main
    except Exception:
        def missing():
            print("[error] linkage validator not present in this build.", file=sys.stderr)
            sys.exit(1)
        return missing

def main():
    parser = argparse.ArgumentParser(
        prog="fairo",
        description="FAIROTrials multi-validator CLI (MVP)."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # simple pass-through subcommands to each validator
    sub.add_parser("fair-meta", help="Run FAIR metadata validator").add_argument("--input", required=True)
    sub.add_parser("fdaaa", help="Run FDAAA timeliness validator").add_argument("--input", required=True)
    sub.add_parser("accessible", help="Run Accessible Links validator").add_argument("--input", required=True)
    sub.add_parser("outcomes", help="Run Outcome Switching validator").add_argument("--input", required=True)
    sub.add_parser("harms", help="Run CONSORT-Harms validator").add_argument("--input", required=True)
    lk = sub.add_parser("linkage", help="Run Registry–Publication Linkage validator")
    lk.add_argument("--registry", required=True)
    lk.add_argument("--pubs", required=True)
    ds = sub.add_parser("data-sharing", help="Run Data Sharing Transparency validator")
    ds.add_argument("--pubs", required=True)

    # global-ish output override
    for name in ["fair-meta","fdaaa","accessible","outcomes","harms","linkage","data-sharing"]:
        sp = next(s for s in sub.choices.values() if s.prog.endswith(name))
        if name == "linkage":
            sp.add_argument("--out_csv", default="linkage_report.csv")
        elif name == "data-sharing":
            sp.add_argument("--out_csv", default="data_sharing_report.csv")
        elif name == "fdaaa":
            sp.add_argument("--out_csv", default="fdaaa_timeliness_report.csv")
        elif name == "accessible":
            sp.add_argument("--out_csv", default="accessible_links_report.csv")
        elif name == "outcomes":
            sp.add_argument("--out_csv", default="outcome_switching_report.csv")
        elif name == "harms":
            sp.add_argument("--out_csv", default="consort_harms_report.csv")
        else:
            sp.add_argument("--out_csv", default="fair_metadata_report.csv")

    # convenience: run-all-samples (uses repo paths)
    runall = sub.add_parser("run-all-samples", help="Run all validators against bundled sample JSON")
    runall.add_argument("--prefix", default="", help="Optional prefix for output files")

    args, extra = parser.parse_known_args()

    # dispatch
    if args.cmd == "fair-meta":
        sys.argv = ["fair_metadata_validator.py", "--input", args.input, "--out_csv", args.out_csv] + extra
        fair_meta_main()
    elif args.cmd == "fdaaa":
        sys.argv = ["fdaaa_timeliness_validator.py", "--input", args.input, "--out_csv", args.out_csv] + extra
        fdaaa_main()
    elif args.cmd == "accessible":
        sys.argv = ["accessible_link_checker.py", "--input", args.input, "--out_csv", args.out_csv] + extra
        accessible_main()
    elif args.cmd == "outcomes":
        sys.argv = ["outcome_switching_validator.py", "--input", args.input, "--out_csv", args.out_csv] + extra
        outcomes_main()
    elif args.cmd == "harms":
        sys.argv = ["consort_harms_validator.py", "--input", args.input, "--out_csv", args.out_csv] + extra
        harms_main()
    elif args.cmd == "linkage":
        sys.argv = ["linkage_validator.py", "--registry", args.registry, "--pubs", args.pubs, "--out_csv", args.out_csv] + extra
        _linkage_main()()
    elif args.cmd == "data-sharing":
        sys.argv = ["data_sharing_validator.py", "--pubs", args.pubs, "--out_csv", args.out_csv] + extra
        data_sharing_main()
    elif args.cmd == "run-all-samples":
        cmds = [
            ["fair-meta", "--input", "samples/sample_fair_trials.json", "--out_csv", f"{args.prefix}fair_metadata_report.csv"],
            ["fdaaa", "--input", "samples/sample_fdaaa_trials.json", "--out_csv", f"{args.prefix}fdaaa_timeliness_report.csv"],
            ["accessible", "--input", "samples/sample_access_links.json", "--out_csv", f"{args.prefix}accessible_links_report.csv"],
            ["outcomes", "--input", "samples/sample_outcomes.json", "--out_csv", f"{args.prefix}outcome_switching_report.csv"],
            ["harms", "--input", "samples/sample_harms.json", "--out_csv", f"{args.prefix}consort_harms_report.csv"],
            ["linkage", "--registry", "samples/sample_registry_linkage.json", "--pubs", "samples/sample_publications.json", "--out_csv", f"{args.prefix}linkage_report.csv"],
            ["data-sharing", "--pubs", "samples/sample_data_sharing_pubs.json", "--out_csv", f"{args.prefix}data_sharing_report.csv"]
        ]
        code = 0
        for c in cmds:
            try:
                sys.argv = ["fairo"] + c
                main()  # recursive call for each subcommand; simple and DRY
            except SystemExit as e:
                if e.code not in (0, None):
                    code = e.code
        sys.exit(code)
    else:
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()
