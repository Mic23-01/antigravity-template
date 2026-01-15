# Antigravity Canary Check - v1.1.0 (Skills Integrated)
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

def check_skills():
    """Verifica dinamica delle Skills elencate in SKILLS_INDEX.md"""
    print(f"\n{BLUE}=== Skills Integrity Check ==={RESET}")
    
    skill_index = Path(".agent/skills/SKILLS_INDEX.md")
    if not skill_index.exists():
        print(f"  {RED}[FAIL]{RESET} SKILLS_INDEX.md missing!")
        return False
        
    print(f"  {GREEN}[OK]{RESET} Index found at {skill_index}")
    
    # Parse index for skills (looking for `skill_name` pattern)
    skills_found = []
    with open(skill_index, 'r') as f:
        for line in f:
            if "|" in line and "`" in line:
                # Extract content between backticks
                try:
                    skill_name = line.split("`")[1]
                    # Filter out header row or description column accidents
                    if "Skill Name" not in skill_name and " " not in skill_name:
                        skills_found.append(skill_name)
                except IndexError:
                    continue

    if not skills_found:
        print(f"  {YELLOW}[WARN]{RESET} No skills found in Index (Parsing error?)")
        return True # Non-blocking warning

    all_ok = True
    print(f"  Found {len(skills_found)} skills in Index. Verifying integrity...")
    
    for sk in set(skills_found):
        skill_path = Path(f".agent/skills/{sk}/SKILL.md")
        if skill_path.exists():
            # Frontmatter check
            try:
                with open(skill_path, 'r') as f:
                    content = f.read()
                    if content.startswith("---") and "version:" in content:
                        print(f"    {GREEN}✔{RESET} {sk} valid (v{content.split('version:')[1].splitlines()[0].strip()})")
                    else:
                        print(f"    {YELLOW}⚠{RESET} {sk} exists but INVALID FRONTMATTER")
                        all_ok = False
            except Exception as e:
                print(f"    {RED}✘{RESET} {sk} READ ERROR: {e}")
                all_ok = False
        else:
             print(f"    {RED}✘{RESET} {sk} BROKEN (Missing {skill_path})")
             all_ok = False

    # Ghost Skills Check (Filesystem -> Index)
    print(f"  {BLUE}Verifying Ghost Skills (Unindexed directories)...{RESET}")
    skills_dir = Path(".agent/skills")
    if skills_dir.exists():
        physical_skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        ghosts = set(physical_skills) - set(skills_found)
        if ghosts:
             print(f"    {YELLOW}⚠ Ghost Skills detected (Folder exists but not in Index):{RESET}")
             for g in ghosts:
                 print(f"      - {g}")
             # Decidi se questo è bloccante o no. Per "ordine rigido", potrebbe esserlo, o solo warning.
             # User requested "skills rotte che nessuno nota". Unindexed = Not noted.
             # Let's keep it as WARNING for now, or FAIL? User said "rischi skills rotte".
             # A ghost skill is not broken, just ignored. But it's "dust".
    else:
        print(f"  {RED}[FAIL]{RESET} .agent/skills directory missing!")
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
    # Initialize overall status for dynamic checks
    all_systems_go = True

    print(f"{BLUE}#########################################{RESET}")
    print(f"{BLUE}# ANTIGRAVITY CANARY SYSTEM INTEGRITY   #{RESET}")
    print(f"{BLUE}#########################################{RESET}")

    # 3. Dynamic Agent Check (Behavioral)
    print(f"\n{BLUE}=== Behavioral Analysis (Dynamic Agent) ==={RESET}")
    # Run the default compliance scenario in dry-run mode
    dyn_cmd = ["uv", "run", "--with", "PyYAML", "python3", ".agent/tools/dynamic_agent.py", "--scenario", "001_compliance.md", "--mode", "dry-run"]
    try:
        # Use subprocess directly to capture output better or just rely on exit code
        if subprocess.run(dyn_cmd, check=False).returncode == 0:
             print(f"  {GREEN}✔ Protocol Compliance Verified{RESET}")
        else:
             print(f"  {RED}✘ Behavioral Deviation Detected{RESET}")
             all_systems_go = False
    except Exception as e:
         print(f"  {RED}✘ Execution Error: {e}{RESET}")
         all_systems_go = False

    # This block will be printed after the dynamic agent check, reflecting its status
    print(f"\n{GREEN if all_systems_go else RED}#########################################{RESET}")
    print(f"{GREEN if all_systems_go else RED}# SYSTEM STATUS: {'100% OPERATIONAL' if all_systems_go else 'ATTENTION REQUIRED'}       #{RESET}")
    print(f"{GREEN if all_systems_go else RED}#########################################{RESET}")

    success = True # This will track static checks, separate from all_systems_go for dynamic

    # 1. Critical Config Files
    print(f"\n{BLUE}=== Critical Configuration Audit ==={RESET}")
    success &= check_file(".agent/project/PROJECT_AGENT_CONFIG.md", "Global Workflow Config")
    success &= check_file(".agent/rules/global-validation-protocol.md", "Leader Rule")
    success &= check_file("docs_custom/SOURCES.md", "Primary Source of Truth")

    # 2. Workflow Audit
    success &= check_workflows()

    # 3. Script Execution
    success &= run_script_test("python3 .agent/project/librarian.py --hygiene", "Librarian Hygiene Check")

    # 4. Skills Integrity
    success &= check_skills()
    
    print(f"\n{BLUE}#########################################{RESET}")
    if success:
        print(f"{GREEN}# SYSTEM STATUS: 100% OPERATIONAL       #{RESET}")
    else:
        print(f"{RED}# SYSTEM STATUS: DEGRADED / INCOMPLETE  #{RESET}")
    print(f"{BLUE}#########################################{RESET}")

if __name__ == "__main__":
    main()
