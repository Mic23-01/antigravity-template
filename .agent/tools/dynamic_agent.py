#!/usr/bin/env python3
"""
Dynamic Agent Runner (Divine Edition)
-------------------------------------
Executes behavioral scenarios in a sandboxed environment.
Validates that the Agent follows the Antigravity Protocol (FixLogs, Code Integrity).
"""

import os
import sys
import shutil
import yaml
import glob
import re
import argparse
from pathlib import Path

# Config
SANDBOX_ROOT = Path("/tmp/ag_dynamic_sandbox")
SCENARIO_ROOT = Path(".agent/project/scenarios")

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def setup_sandbox(project_root: Path):
    """Mirror the essential project structure to sandbox."""
    if SANDBOX_ROOT.exists():
        shutil.rmtree(SANDBOX_ROOT)
    SANDBOX_ROOT.mkdir(parents=True)
    
    # Copy essential dirs
    for item in ['.agent', 'docs_custom']:
        src = project_root / item
        if src.exists():
            shutil.copytree(src, SANDBOX_ROOT / item)
    
    # Copy root config files
    for f in project_root.glob("*.md"):
        shutil.copy2(f, SANDBOX_ROOT)
        
    print(f"{BLUE}[Sandbox] Initialized at {SANDBOX_ROOT}{RESET}")

def load_scenario(scenario_path: Path):
    """Load scenario definition from Markdown frontmatter/content."""
    content = scenario_path.read_text()
    if content.startswith("---"):
        try:
            # Extract frontmatter
            fm = content.split("---")[1]
            return yaml.safe_load(fm)
        except Exception as e:
            print(f"{RED}Error parsing YAML frontmatter: {e}{RESET}")
            return None
    return None

def execute_agent_simulation(scenario, mode="dry-run"):
    """
    Simulates the agent execution.
    In 'real' mode, this would call the LLM API.
    In 'dry-run' mode, we simulate the 'correct' behavior manually to verify the checker logic.
    """
    print(f"{YELLOW}[Agent] Simulating Task: {scenario['task']} ({mode}){RESET}")
    
    if mode == "dry-run":
        if scenario['name'] == "UI/UX Brain-Link Verification":
             print(f"  [Sim] Analisi prompt: {scenario['task']}")
             print(f"  [Sim] Ricerca in database UI/UX per 'Fintech Crypto'...")
             # Simula il recupero dei dati dalla skill
             hex_primary = "#F59E0B"
             hex_accent = "#8B5CF6"
             target = SANDBOX_ROOT / scenario['target_file']
             target.parent.mkdir(parents=True, exist_ok=True)
             target.write_text(f"# Brand Identity\nPalette: {hex_primary}, {hex_accent}\nSource: ui_ux_designer skill")
             print(f"  [Sim] File {target} creato con successo.")
        else:
             # Default behavior (Scenario 001)
             target = SANDBOX_ROOT / scenario['target_file']
             target.parent.mkdir(parents=True, exist_ok=True)
             target.write_text("def add(a, b):\n    return a + b\n")
        
        # Simulate FixLog creation via fixlog_writer
        import uuid
        from datetime import datetime
        log_id = f"AG.fix.{datetime.now().strftime('%Y%m%d')}.{uuid.uuid4().hex[:8]}"
        log_path = SANDBOX_ROOT / f".agent/fix_logs/{log_id}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text('{"id": "'+log_id+'", "result": "pass", "task": "'+scenario['name']+'"}')
        print(f"{GREEN}[Agent] Simulation complete.{RESET}")
        return True
    
    # Future: Implement real `run_command("antigravity run ...")`
    return False

def verify_assertions(scenario):
    """Check if the sandbox state matches expectations."""
    print(f"{BLUE}[Audit] Verifying Assertions...{RESET}")
    all_pass = True
    
    for assertion in scenario.get('assertions', []):
        atype = assertion['type']
        
        if atype == 'file_exists':
            path = SANDBOX_ROOT / assertion['path']
            if path.exists():
                print(f"  ✔ file_exists: {assertion['path']}")
            else:
                print(f"  ❌ file_exists: {assertion['path']}")
                all_pass = False
                
        elif atype == 'file_contains':
            path = SANDBOX_ROOT / assertion['path']
            if path.exists() and assertion['pattern'] in path.read_text():
                 print(f"  ✔ file_contains: {assertion['pattern']}")
            else:
                 print(f"  ❌ file_contains: {assertion['pattern']}")
                 all_pass = False
        
        elif atype == 'file_glob_exists':
            matches = list(SANDBOX_ROOT.glob(assertion['path']))
            if matches:
                print(f"  ✔ file_glob_exists: {assertion['path']} (Found {len(matches)})")
            else:
                print(f"  ❌ file_glob_exists: {assertion['path']}")
                all_pass = False

        elif atype == 'file_content_contains':
            # Check content in glob matches
            pattern = assertion['path']
            matches = list(SANDBOX_ROOT.glob(pattern))
            found_content = False
            for m in matches:
                if assertion['pattern'] in m.read_text():
                    found_content = True
                    break
            if found_content:
                print(f"  ✔ file_content_contains: {assertion['pattern']}")
            else:
                print(f"  ❌ file_content_contains: {assertion['pattern']}")
                all_pass = False
                
    return all_pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="001_compliance.md")
    parser.add_argument("--mode", default="dry-run", choices=["dry-run", "real"])
    args = parser.parse_args()
    
    scenario_file = SCENARIO_ROOT / args.scenario
    if not scenario_file.exists():
        print(f"{RED}Scenario not found: {scenario_file}{RESET}")
        sys.exit(1)
        
    scenario = load_scenario(scenario_file)
    if not scenario:
        sys.exit(1)
        
    print(f"{GREEN}=== DYNAMIC AGENT: {scenario['name']} ==={RESET}")
    
    # 1. Setup
    setup_sandbox(Path("."))
    
    # 2. Execute
    execute_agent_simulation(scenario, args.mode)
    
    # 3. Audit
    if verify_assertions(scenario):
        print(f"\n{GREEN}Outcome: PASS (Behavior Verified){RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}Outcome: FAIL (Protocol Violation){RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
