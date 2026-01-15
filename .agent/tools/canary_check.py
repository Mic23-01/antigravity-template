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

def find_latest_walkthrough():
    """Finds the most recent walkthrough.md in the brain directory."""
    brain_dir = Path("/home/ubuntu/.gemini/antigravity/brain")
    if not brain_dir.exists():
        return None
    
    # Get all walkthrough.md files
    walkthroughs = list(brain_dir.glob("*/walkthrough.md"))
    if not walkthroughs:
        return None
        
    # Sort by modification time
    latest = max(walkthroughs, key=lambda p: p.stat().st_mtime)
    return latest

def check_walkthrough_evidence(path):
    """
    Smart Gate: Checks if walkthrough.md contains valid evidence.
    Rule: Must have [Image] OR [CodeBlock] OR [Diff].
    """
    try:
        with open(path, 'r') as f:
            content = f.read()
            
        # Check 1: Empty file
        if len(content.strip()) < 100:
            print(f"  {RED}[FAIL]{RESET} Walkthrough at {path.name} is too short (<100 chars). EVIDENCE MISSING.")
            return False
            
        import re
        # Check 2: Image markdown ![alt](url)
        has_image = bool(re.search(r'!\[.*?\]\(.*?\)', content))
        
        # Check 3: Code block ``` (triple backticks)
        has_code = "```" in content
        
        if has_image:
            print(f"  {GREEN}[PASS]{RESET} Evidence found in {path.name} (Image detected).")
            return True
        elif has_code:
            print(f"  {GREEN}[PASS]{RESET} Evidence found in {path.name} (Code/Diff block detected).")
            return True
        else:
            print(f"  {RED}[FAIL]{RESET} Walkthrough at {path.name} lacks visual or code evidence.")
            print(f"         {YELLOW}Hint: Add a screenshot ( ![desc](path) ) or a log block ( ``` ).{RESET}")
            return False
            
    except Exception as e:
        print(f"  {RED}[ERROR]{RESET} Could not read walkthrough: {e}")
        return False

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

    except Exception as e:
        print(f"  {RED}[FATAL]{RESET} {description} crashed: {str(e)}")
        return False


def check_session_integrity():
    """
    ZERO STEP: Verifies that the previous session was properly persisted.
    If 'dirty files' are detected (modified > last fixlog), it BLOCKS execution.
    """
    print(f"\n{BLUE}=== Session Integrity Check (The Sentinel) ==={RESET}")
    sentinel_path = ".agent/tools/session_sentinel.py"
    if not os.path.exists(sentinel_path):
        print(f"  {YELLOW}[SKIP]{RESET} Sentinel tool not found (Bootstrapping phase?)")
        return True

    try:
        # We run the sentinel. If it exits with 1 -> DIRTY.
        res = subprocess.run(["python3", sentinel_path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  {GREEN}[PASS]{RESET} Session is CLEAN. Persistence verified.")
            return True
        else:
            print(f"  {RED}[BLOCK]{RESET} DIRTY SESSION DETECTED!")
            print(f"  {RED}FATAL: You have modified files without a subsequent FixLog.{RESET}")
            print(f"  {YELLOW}Action Required: Run 'fixlog_writer' to sanitize the memory before proceeding.{RESET}")
            # Print the Sentinel's evidence
            print("  Evidence:")
            for line in res.stdout.splitlines():
                print(f"    {line}")
            return False
            
    except Exception as e:
        print(f"  {RED}[ERROR]{RESET} Sentinel execution failed: {e}")
        return False

def main():
    # Initialize overall status for dynamic checks
    all_systems_go = True
    
    # -1. Session Integrity (Hard Gate)
    if not check_session_integrity():
        print(f"\n{RED}#########################################{RESET}")
        print(f"{RED}# SYSTEM LOCKED: PERSISTENCE REQUIRED   #{RESET}")
        print(f"{RED}#########################################{RESET}")
        sys.exit(1)

    print(f"{BLUE}#########################################{RESET}")
    print(f"{BLUE}# ANTIGRAVITY CANARY SYSTEM INTEGRITY   #{RESET}")
    print(f"{BLUE}#########################################{RESET}")

    # 0. Artifact Evidence Check (Smart Gate)
    print(f"\n{BLUE}=== Artifact Evidence Enforcement ==={RESET}")
    # Defines path convention based on Brain/Task context. 
    # Since this script runs in the root, we look for a generic walkthrough or rely on an env var.
    # ideally, we should check the LATEST interaction or a specific path provided.
    # For this implementation, we will check a standard location or skip if not found (Warn only).
    
    # In a real Agentic run, the artifacts are in: <appDataDir>/brain/<conversation-id>/walkthrough.md
    # But canary_check doesn't know the conversation ID easily without input.
    # Strategy: Scan the most recent brain directory or just check if a 'walkthrough.md' exists in CWD (for local testing).
    
    # For now, we'll check a placeholder path or rely on the user to point it out.
    # To make it robust as a generally usable tool, we'll search for the newest walkthrough in .gemini/antigravity/brain/
    # If not found, we skip (SOFT GATE).
    
    # 0.5 Eval Triad (Optional - Flag Based)
    if "--triad" in sys.argv:
        print(f"\n{BLUE}=== Capability Eval Triad (Deep Evaluation) ==={RESET}")
        runner_path = ".agent/evals/runner.py"
        if os.path.exists(runner_path):
            print(f"  {BLUE}Running Full Eval Suite (Refactor/Bugfix/Feature)...{RESET}")
            # We run it as a subprocess to keep isolation
            triad_res = subprocess.run(["python3", runner_path, "--all"], capture_output=False) # Let it print to stdout
            if triad_res.returncode == 0:
                print(f"  {GREEN}[PASS]{RESET} Application Capability Verified (Triad Score: 100%)")
            else:
                print(f"  {RED}[FAIL]{RESET} Capability Eval Failed. Check outputs above.")
                success = False
        else:
             print(f"  {RED}[ERROR]{RESET} Eval Runner missing at {runner_path}")
    
    latest_walkthrough = find_latest_walkthrough()
    if latest_walkthrough:
        # Initialize success before its first use here
        success = True # This will track static checks, separate from all_systems_go for dynamic
        success &= check_walkthrough_evidence(latest_walkthrough)
    else:
        print(f"  {YELLOW}[SKIP]{RESET} No recent walkthrough.md found to verify.")

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
