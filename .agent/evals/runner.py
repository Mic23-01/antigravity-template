#!/usr/bin/env python3
# /// script
# dependencies = ["chromadb"]
# ///
"""
Antigravity Eval Runner (v2.0 - Unified)
=========================================
Replaces legacy .sh scripts with a single Python entry point.

Usage:
    uv run .agent/evals/runner.py --all             # Run Triad coding challenges
    uv run .agent/evals/runner.py --protocol        # Run Protocol checks (Chroma metadata)
    uv run .agent/evals/runner.py --id E11          # Run single challenge
    uv run .agent/evals/runner.py --difficulty hard # Difficulty scaling (coming soon)
"""

import sys
import os
import argparse
import subprocess
import json
import shutil
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# --- Triad Challenges ---
TRIAD_MAP = {
    "E11": {"spec": "cases/E11_triad_refactor_spec.md", "test": "triad/tests/test_refactor.py", "name": "Refactor Challenge"},
    "E12": {"spec": "cases/E12_triad_bugfix_spec.md", "test": "triad/tests/test_bugfix.py", "name": "Bugfix Challenge"},
    "E13": {"spec": "cases/E13_triad_feature_spec.md", "test": "triad/tests/test_feature.py", "name": "Feature Challenge"},
}

# --- Protocol Checks (Canary IDs) ---
PROTOCOL_CHECKS = [
    {"collection": "fix_logs", "id": "AG.fix.eval.metadata_gate", "name": "FixLog Canary"},
    {"collection": "research_summaries", "id": "AG.research.eval.metadata_gate", "name": "Research Canary"},
]

# Required metadata fields per collection
REQUIRED_METADATA = {
    "fix_logs": ["project", "type", "date", "files", "tests", "result"],
    "research_summaries": ["project", "type", "date", "topic", "tags", "sources"],
    "decisions": ["project", "type", "date", "decision_id", "status", "topic", "tags"]
}


def run_triad_eval(eval_id, eval_def, use_coverage=False):
    """Runs a single Triad coding challenge via pytest."""
    if not shutil.which("uv"):
        return {"id": eval_id, "success": False, "error": "uv not found"}

    script_dir = Path(__file__).parent
    test_path = script_dir / eval_def["test"]

    if not test_path.exists():
        return {"id": eval_id, "success": False, "error": f"Test file missing: {test_path}"}

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


def run_protocol_check(check_def, data_dir=None):
    """Runs a Chroma metadata validation check."""
    try:
        import chromadb
    except ImportError:
        return {"name": check_def["name"], "success": False, "error": "chromadb not installed. Use: uv run --with chromadb ..."}

    if data_dir is None:
        data_dir = os.path.join(os.path.expanduser("~"), "chroma-data")

    try:
        client = chromadb.PersistentClient(path=data_dir)
        col = client.get_collection(check_def["collection"])
        got = col.get(ids=[check_def["id"]], include=["metadatas"])

        if not got["ids"]:
            return {"name": check_def["name"], "success": False, "error": f"ID '{check_def['id']}' not found"}

        md = got["metadatas"][0] if got["metadatas"] else None

        if md is None:
            return {"name": check_def["name"], "success": False, "error": "metadata is null"}

        missing = [k for k in REQUIRED_METADATA.get(check_def["collection"], []) if k not in md]
        if missing:
            return {"name": check_def["name"], "success": False, "error": f"missing keys: {missing}"}

        return {"name": check_def["name"], "success": True, "error": None}
    except Exception as e:
        return {"name": check_def["name"], "success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Antigravity Eval Runner (v2.0)")
    parser.add_argument("--id", help="Run specific Triad Eval ID (e.g. E11)")
    parser.add_argument("--all", action="store_true", help="Run all Triad evals")
    parser.add_argument("--protocol", action="store_true", help="Run protocol checks (Chroma metadata)")
    parser.add_argument("--coverage", action="store_true", help="Enable pytest-cov for Triad")
    parser.add_argument("--json", action="store_true", help="Output JSON result only")
    parser.add_argument("--difficulty", choices=["easy", "hard"], default="easy", help="Difficulty level (future use)")
    parser.add_argument("--data-dir", default=None, help="Chroma data directory (default: ~/chroma-data)")

    args = parser.parse_args()

    results = []
    total = 0
    passed = 0

    # --- Protocol Checks Mode ---
    if args.protocol:
        if not args.json:
            print(f"\n{BLUE}=== Protocol Checks (Chroma Metadata) ==={RESET}")

        for check in PROTOCOL_CHECKS:
            res = run_protocol_check(check, args.data_dir)
            results.append(res)
            total += 1
            if res["success"]:
                passed += 1
                if not args.json:
                    print(f"  {GREEN}✅ {res['name']}{RESET}")
            else:
                if not args.json:
                    print(f"  {RED}❌ {res['name']}: {res['error']}{RESET}")

    # --- Triad Challenges Mode ---
    triad_to_run = []
    if args.id:
        if args.id not in TRIAD_MAP:
            if args.json:
                print(json.dumps({"error": f"Unknown ID: {args.id}"}))
            else:
                print(f"{RED}Unknown ID: {args.id}{RESET}")
            sys.exit(1)
        triad_to_run.append(args.id)
    elif args.all:
        triad_to_run = list(TRIAD_MAP.keys())

    if triad_to_run:
        if not args.json:
            print(f"\n{BLUE}=== Triad Coding Challenges ==={RESET}")

        for eid in triad_to_run:
            if not args.json:
                print(f"\n  Running {TRIAD_MAP[eid]['name']} ({eid})...")

            res = run_triad_eval(eid, TRIAD_MAP[eid], args.coverage)
            results.append(res)
            total += 1
            if res["success"]:
                passed += 1
                if not args.json:
                    print(f"  {GREEN}✅ PASS{RESET}")
            else:
                if not args.json:
                    print(f"  {RED}❌ FAIL{RESET}")
                    if res["error"]:
                        print(f"  Error: {res['error']}")
                    else:
                        # Show tail of output
                        print(f"  --- Output (tail) ---")
                        print(res["output"][-500:])

    # --- Final Output ---
    if total == 0:
        parser.print_help()
        sys.exit(0)

    score = int((passed / total) * 100) if total > 0 else 0

    final_output = {
        "score": score,
        "total": total,
        "passed": passed,
        "results": results
    }

    if args.json:
        print(json.dumps(final_output, indent=2))
    else:
        print(f"\n{BLUE}=== Eval Scorecard ==={RESET}")
        print(f"  Final Score: {passed}/{total} ({score}%)")
        if score == 100:
            print(f"  {GREEN}🚀 READY FOR DEPLOY{RESET}")
        else:
            print(f"  {YELLOW}⚠️  IMPROVEMENT NEEDED{RESET}")

    sys.exit(0 if score == 100 else 1)


if __name__ == "__main__":
    main()
