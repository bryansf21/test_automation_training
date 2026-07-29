import argparse
import csv

from testing import ngetest

def load_measurements(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "target": float(row["target"]),
                "measured": float(row["measured"]),
            })
    return rows

def evaluate(rows, tolerance_mm):
    results = []
    for r in rows:
        error = abs(r["measured"] - r["target"])
        results.append({
            "target": r["target"],
            "measured": r["measured"],
            "error": round(error, 3),
            "pass": ngetest(r["measured"], r["target"], tolerance_mm),
        })
    return results

def make_report(results, tolerance_mm):
    n = len(results)
    n_pass = sum(r["pass"] for r in results)
    verdict = "PASS" if n_pass == n else "FAIL"
 
    lines = [
        f"Spec: error <= {tolerance_mm} mm",
        "-" * 46,
        f"{'target':>8} {'measured':>10} {'error':>8}  result",
    ]
    for r in results:
        flag = "ok" if r["pass"] else "FAIL <-"
        lines.append(f"{r['target']:>8.1f} {r['measured']:>10.2f} "
                     f"{r['error']:>8.3f}  {flag}")
    lines.append("-" * 46)
    lines.append(f"{n_pass}/{n} points passed  ->  {verdict}")
    return "\n".join(lines)
 
 
def main():
    parser = argparse.ArgumentParser(description="Evaluate a measurements CSV.")
    parser.add_argument("--file", default="measurements.csv", help="CSV to read")
    parser.add_argument("--tolerance", type=float, default=1.0,
                        help="pass/fail limit in mm (default 1.0)")
    args = parser.parse_args()
 
    rows = load_measurements(args.file)
    results = evaluate(rows, args.tolerance)
    report = make_report(results, args.tolerance)
    print(report)
 
    # exit code: 0 = all passed, 1 = at least one failed
    all_passed = all(r["pass"] for r in results)
    return 0 if all_passed else 1
 
 
if __name__ == "__main__":
    raise SystemExit(main())
 