
#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import json
from pathlib import Path

# Mapping ID -> Test File
TRIAD_MAP = {
    "E11": {"spec": "cases/E11_triad_refactor_spec.md", "test": "triad/tests/test_refactor.py", "name": "Refactor Challenge"},
    "E12": {"spec": "cases/E12_triad_bugfix_spec.md", "test": "triad/tests/test_bugfix.py", "name": "Bugfix Challenge"},
    "E13": {"spec": "cases/E13_triad_feature_spec.md", "test": "triad/tests/test_feature.py", "name": "Feature Challenge"},
}

import shutil

def run_eval(eval_id, eval_def):
    print(f"\nrunning {eval_def['name']} ({eval_id})...")
    
    # Pre-flight: Check for uv
    if not shutil.which("uv"):
        print("❌ CRITICAL: 'uv' not found in PATH.")
        print("   Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

    # We look for the test file relative to this script
    script_dir = Path(__file__).parent
    test_path = script_dir / eval_def["test"]
    
    if not test_path.exists():
        print(f"FAIL: Test file missing at {test_path}")
        return False
        
    # ROBUSTNESS: Use '--with pytest' to ensure the test runner exists ephemerally
    # This prevents "command not found" errors if pytest isn't in pyproject.toml
    cmd = ["uv", "run", "--with", "pytest", "pytest", str(test_path), "-v"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {eval_def['name']} PASSED")
            return True
        else:
            print(f"❌ {eval_def['name']} FAILED")
            print("--- Output ---")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print(f"❌ EXECUTION FLAKINESS: Could not spawn process (is 'uv' executable?)")
        return False
    except Exception as e:
        print(f"❌ EXECUTION ERROR: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Antigravity Eval Runner")
    parser.add_argument("--id", help="Run specific Eval ID (e.g. E11)")
    parser.add_argument("--all", action="store_true", help="Run all evals")
    
    args = parser.parse_args()
    
    results = {}
    
    if args.id:
        if args.id not in TRIAD_MAP:
            print(f"Unknown ID: {args.id}")
            sys.exit(1)
        success = run_eval(args.id, TRIAD_MAP[args.id])
        results[args.id] = success
    elif args.all:
        for eid, edef in TRIAD_MAP.items():
            success = run_eval(eid, edef)
            results[eid] = success
    else:
        parser.print_help()
        sys.exit(0)
        
    # Final Report
    print("\n=== Eval Scorecard ===")
    all_pass = True
    for k, v in results.items():
        status = "PASS" if v else "FAIL"
        if not v: all_pass = False
        print(f"{k}: {status}")
        
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
