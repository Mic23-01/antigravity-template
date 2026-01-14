#!/usr/bin/env python3
"""
Antigravity Initialization Engine (Divine Edition).
--------------------------------------------------
Automates the hydration of a new Antigravity project.
Replaces the manual 'sed' playbook with a safe, interactive wizard.

Usage:
    python3 .agent/tools/init_antigravity.py
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Default Template Values (What we look for to replace)
DEFAULT_PROJECT_NAME = "Antigravity"
DEFAULT_PREFIX = "AG"

def input_clean(prompt, default=None):
    """Safe input wrapper."""
    d_fmt = f" [{default}]" if default else ""
    try:
        val = input(f"{BLUE}{prompt}{d_fmt}: {RESET}").strip()
        return val if val else default
    except KeyboardInterrupt:
        print(f"\n{RED}Aborted.{RESET}")
        sys.exit(1)

def run_command(cmd, cwd=None, ignore_errors=False):
    """Runs a shell command."""
    print(f"{YELLOW}Running: {cmd}{RESET}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            print(f"{RED}Error executing command: {e.stderr}{RESET}")
        return False

def replace_in_file(file_path, old_str, new_str):
    """Safely replaces text in a file."""
    p = Path(file_path)
    if not p.exists():
        return False
    
    try:
        content = p.read_text(encoding='utf-8')
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            p.write_text(new_content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"{RED}Failed to read/write {file_path}: {e}{RESET}")
    return False

def main():
    print(f"{GREEN}#########################################{RESET}")
    print(f"{GREEN}# ANTIGRAVITY INITIALIZATION ENGINE     #{RESET}")
    print(f"{GREEN}#########################################{RESET}")

    # 1. Wizard
    print("\nWelcome Architect. Let's configure your new Agent System.")
    
    project_name = input_clean("Project Name", "Solaris")
    prefix = input_clean("Project Prefix (2-4 chars)", "SOL").upper()

    print(f"\n{BLUE}Plan:{RESET}")
    print(f"- Project: {DEFAULT_PROJECT_NAME} -> {GREEN}{project_name}{RESET}")
    print(f"- Prefix:  {DEFAULT_PREFIX}       -> {GREEN}{prefix}{RESET}")
    
    if input_clean("Proceed?", "y").lower() != 'y':
        print("Aborted.")
        sys.exit(0)

    # 2. Hydration (Config Source of Truth)
    # Theoretically, we only need to update PROJECT_AGENT_CONFIG.md
    # because workflows read from there using placeholders.
    # HOWEVER, some files might have hardcoded defaults or we might want to brand the readme.
    
    print(f"\n{BLUE}=== Hydrating Configuration ==={RESET}")
    
    config_path = ".agent/project/PROJECT_AGENT_CONFIG.md"
    if replace_in_file(config_path, f'"{DEFAULT_PROJECT_NAME}"', f'"{project_name}"'):
        print(f"{GREEN}✔ Updated ProjectName in config.{RESET}")
    else:
        print(f"{YELLOW}⚠ Could not update ProjectName (Already changed?){RESET}")

    if replace_in_file(config_path, f'"{DEFAULT_PREFIX}"', f'"{prefix}"'):
        print(f"{GREEN}✔ Updated Prefix in config.{RESET}")
    else:
        print(f"{YELLOW}⚠ Could not update Prefix (Already changed?){RESET}")

    # 3. Environment Setup
    print(f"\n{BLUE}=== Environment Setup ==={RESET}")
    
    # Check uv
    if run_command("uv --version", ignore_errors=True):
        print(f"{GREEN}✔ uv detected.{RESET}")
        # Init venv
        if not Path(".venv").exists():
            print("Creating virtual environment...")
            run_command("uv venv")
    else:
        print(f"{YELLOW}⚠ uv not found. Skipping venv creation.{RESET}")

    # Check git
    if not Path(".git").exists():
        print("Initializing Git repository...")
        run_command("git init")
    else:
        print(f"{GREEN}✔ Git already initialized.{RESET}")

    print(f"\n{GREEN}#########################################{RESET}")
    print(f"{GREEN}# INITIALIZATION COMPLETE               #{RESET}")
    print(f"{GREEN}#########################################{RESET}")
    print(f"\nNext Steps:")
    print(f"1. Run canary check: {YELLOW}python3 .agent/tools/canary_check.py{RESET}")
    print(f"2. Start your first task with task_boundary tool.")

    # 4. Self Destruct Protocol
    print(f"\n{RED}=== Protocollo Autodistruzione ==={RESET}")
    if input_clean("Vuoi rimuovere questo script di init per sicurezza?", "n").lower() == 'y':
        try:
            os.remove(__file__)
            print(f"{GREEN}Script rimosso. Buona fortuna, Architect.{RESET}")
        except Exception as e:
            print(f"{RED}Errore durante la rimozione: {e}{RESET}")
    else:
        print(f"{YELLOW}Script conservato in .agent/tools/.{RESET}")

if __name__ == "__main__":
    main()
