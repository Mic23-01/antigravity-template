
#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import json
import shutil
from pathlib import Path

# Mapping ID -> Test File
TRIAD_MAP = {
    "E11": {"spec": "cases/E11_triad_refactor_spec.md", "test": "triad/tests/test_refactor.py", "name": "Refactor Challenge"},
    "E12": {"spec": "cases/E12_triad_bugfix_spec.md", "test": "triad/tests/test_bugfix.py", "name": "Bugfix Challenge"},
    "E13": {"spec": "cases/E13_triad_feature_spec.md", "test": "triad/tests/test_feature.py", "name": "Feature Challenge"},
}

def run_eval(eval_id, eval_def, use_coverage=False):
    # Pre-flight: Check for uv
    if not shutil.which("uv"):
        return {"id": eval_id, "success": False, "error": "uv not found"}

    script_dir = Path(__file__).parent
    test_path = script_dir / eval_def["test"]
    
    if not test_path.exists():
        return {"id": eval_id, "success": False, "error": f"Test file missing: {test_path}"}
        
    # Build Command
    # Use '--with pytest pytest-cov' if coverage requested
    packages = ["pytest"]
    if use_coverage:
        packages.append("pytest-cov")
        
    cmd = ["uv", "run"]
    for p in packages:
        cmd.extend(["--with", p])
    
    cmd.append("pytest")
    cmd.append(str(test_path))
    cmd.append("-v")
    
    if use_coverage:
        # Cover the challenge file implementation (assuming structure)
        # For Triad, the code is often inside the test or imported.
        # This is a best-effort coverage setup.
        cmd.extend(["--cov=.", "--cov-report=term-missing"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = (result.returncode == 0)
        return {
            "id": eval_id,
            "success": success,
            "output": result.stdout + result.stderr,
            "error": None
        }
    except Exception as e:
        return {"id": eval_id, "success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Antigravity Eval Runner")
    parser.add_argument("--id", help="Run specific Eval ID (e.g. E11)")
    parser.add_argument("--all", action="store_true", help="Run all evals")
    parser.add_argument("--coverage", action="store_true", help="Enable pytest-cov")
    parser.add_argument("--json", action="store_true", help="Output JSON result only")
    
    args = parser.parse_args()
    
    results_map = {}
    
    to_run = []
    if args.id:
        if args.id not in TRIAD_MAP:
            if args.json:
                print(json.dumps({"error": f"Unknown ID: {args.id}"}))
                sys.exit(1)
            else:
                print(f"Unknown ID: {args.id}")
                sys.exit(1)
        to_run.append(args.id)
    elif args.all:
        to_run = list(TRIAD_MAP.keys())
    else:
        parser.print_help()
        sys.exit(0)

    # Execution Loop
    for eid in to_run:
        if not args.json:
            print(f"\nrunning {TRIAD_MAP[eid]['name']} ({eid})...")
            
        res = run_eval(eid, TRIAD_MAP[eid], args.coverage)
        results_map[eid] = res
        
        if not args.json:
            status = "✅ PASS" if res["success"] else "❌ FAIL"
            print(f"{status}")
            if not res["success"] and res["error"]:
                print(f"Error: {res['error']}")
            elif not res["success"]:
                print("--- Output ---")
                print(res["output"][-500:]) # Tail of output

    # Scoring Logic
    total = len(to_run)
    passed = sum(1 for r in results_map.values() if r["success"])
    score = int((passed / total) * 100) if total > 0 else 0
    
    final_output = {
        "score": score,
        "total": total,
        "passed": passed,
        "results": results_map
    }

    if args.json:
        print(json.dumps(final_output, indent=2))
    else:
        print("\n=== Eval Scorecard ===")
        print(f"Final Score: {score}/100")
        if score == 100:
            print("🚀 READY FOR DEPLOY")
        else:
            print("⚠️  IMPROVEMENT NEEDED")
            
    sys.exit(0 if score == 100 else 1)

if __name__ == "__main__":
    main()
