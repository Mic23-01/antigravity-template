#!/usr/bin/env python3
"""
Antigravity Canary Check: System Integrity & Protocol Verification Tool.
Verifies that all components (Rules, Workflows, Scripts) are 100% operational.
"""

import os
import sys
import subprocess
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

def check_file(path, description):
    p = Path(path)
    if p.exists():
        print(f"  {GREEN}[OK]{RESET} {description} found at {path}")
        return True
    else:
        print(f"  {RED}[ERROR]{RESET} {description} MISSING at {path}")
        return False

def check_workflows():
    print(f"\n{BLUE}=== Workflow Consistency Check ==={RESET}")
    workflows = [
        "tech_rag.md", "research_rag.md", "librarian.md", 
        "custom_project.md", "refactor.md"
    ]
    all_ok = True
    for w in workflows:
        path = f".agent/workflows/{w}"
        if check_file(path, f"Workflow {w}"):
            # Check for placeholder consistency (Simple Grep)
            with open(path, 'r') as f:
                content = f.read()
                if "docs_custom/" in content:
                    print(f"    {GREEN}Cascade Awareness: PASS{RESET}")
                else:
                    print(f"    {YELLOW}Cascade Awareness: WARNING (No docs_custom ref){RESET}")
        else:
            all_ok = False
    return all_ok

def run_script_test(cmd, description):
    print(f"\n{BLUE}=== Testing Script: {description} ==={RESET}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  {GREEN}[PASS]{RESET} {description} executed successfully.")
            return True
        else:
            print(f"  {RED}[FAIL]{RESET} {description} failed (Code {result.returncode}).")
            print(f"  Error: {result.stderr or result.stdout}")
            return False
    except Exception as e:
        print(f"  {RED}[FATAL]{RESET} {description} crashed: {str(e)}")
        return False

def main():
    print(f"{BLUE}#########################################{RESET}")
    print(f"{BLUE}# ANTIGRAVITY CANARY SYSTEM INTEGRITY   #{RESET}")
    print(f"{BLUE}#########################################{RESET}")

    success = True

    # 1. Critical Config Files
    print(f"\n{BLUE}=== Critical Configuration Audit ==={RESET}")
    success &= check_file(".agent/project/PROJECT_AGENT_CONFIG.md", "Global Workflow Config")
    success &= check_file(".agent/rules/global-validation-protocol.md", "Leader Rule")
    success &= check_file("docs_custom/SOURCES.md", "Primary Source of Truth")

    # 2. Workflow Audit
    success &= check_workflows()

    # 3. Script Execution
    success &= run_script_test("python3 .agent/project/librarian.py --hygiene", "Librarian Hygiene Check")

    print(f"\n{BLUE}#########################################{RESET}")
    if success:
        print(f"{GREEN}# SYSTEM STATUS: 100% OPERATIONAL       #{RESET}")
    else:
        print(f"{RED}# SYSTEM STATUS: DEGRADED / INCOMPLETE  #{RESET}")
    print(f"{BLUE}#########################################{RESET}")

if __name__ == "__main__":
    main()
