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
import json
import shutil
from pathlib import Path

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Default Template Values
DEFAULT_PROJECT_NAME = "Antigravity"
DEFAULT_PREFIX = "AG"

# Paths
LIBRARIAN_DB = Path(".agent/memory/librarian.db")
DOCS_SOURCE = Path(".agent/docs")
DOCS_TARGET = Path("docs_custom")
CONFIG_PATH = Path(".agent/project/PROJECT_AGENT_CONFIG.md")

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

def check_guardrails(force=False):
    """Checks if the project is already initialized."""
    if LIBRARIAN_DB.exists() and not force:
        print(f"{RED}[!] FATAL: Project appears to be already initialized (Librarian DB found).{RESET}")
        print(f"{YELLOW}    Use --force to override this safety check.{RESET}")
        return False
    return True

def populate_docs(manifest_docs=None):
    """Copies templates to docs_custom and optionally hydrates them."""
    print(f"\n{BLUE}=== Template Population ==={RESET}")
    if not DOCS_TARGET.exists():
        DOCS_TARGET.mkdir(parents=True)
        print(f"{GREEN}✔ Created {DOCS_TARGET}{RESET}")

    if not DOCS_SOURCE.exists():
        print(f"{RED}⚠ Source docs {DOCS_SOURCE} not found. Skipping population.{RESET}")
        return

    # Map of template -> target
    templates = {
        "brand_identity_guide.md": "brand_identity_guide.md",
        "architecture.md": "architecture.md",
        "domain_language.md": "domain_language.md",
        "product_strategy.md": "product_strategy.md",
        "SOURCES.md": "SOURCES.md"
    }

    for src_name, target_name in templates.items():
        src = DOCS_SOURCE / src_name
        dst = DOCS_TARGET / target_name
        
        if dst.exists():
            print(f"{YELLOW}  - {target_name} exists, skipping.{RESET}")
            continue

        if src.exists():
            shutil.copy2(src, dst)
            print(f"{GREEN}  + Cloned {target_name}{RESET}")
        else:
            print(f"{YELLOW}  ⚠ Template {src_name} missing.{RESET}")

def hydrate_config(project_name, prefix):
    """Updates the main configuration file."""
    print(f"\n{BLUE}=== Hydrating Configuration ==={RESET}")
    
    if replace_in_file(CONFIG_PATH, f'"{DEFAULT_PROJECT_NAME}"', f'"{project_name}"'):
        print(f"{GREEN}✔ Updated ProjectName in config.{RESET}")
    else:
        print(f"{YELLOW}⚠ Could not update ProjectName (Already matched?).{RESET}")

    if replace_in_file(CONFIG_PATH, f'"{DEFAULT_PREFIX}"', f'"{prefix}"'):
        print(f"{GREEN}✔ Updated Prefix in config.{RESET}")
    else:
        print(f"{YELLOW}⚠ Could not update Prefix (Already matched?).{RESET}")

def init_env():
    """Initializes git environment."""
    print(f"\n{BLUE}=== Environment Setup ==={RESET}")
    
    # Check uv
    if run_command("uv --version", ignore_errors=True):
        print(f"{GREEN}✔ uv detected.{RESET}")
        print("Note: Using Zero-Venv architecture. Persistence managed via uv cache.")
    else:
        print(f"{YELLOW}⚠ uv not found. Tool performance may be degraded.{RESET}")

    # Check git
    if not Path(".git").exists():
        print("Initializing Git repository...")
        run_command("git init")
    else:
        print(f"{GREEN}✔ Git already initialized.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Initialization Engine")
    parser.add_argument("--manifest", help="Path to JSON manifest for non-interactive mode")
    parser.add_argument("--force", action="store_true", help="Ignore guardrails (e.g. existing DB)")
    parser.add_argument("--flavor", choices=["Architect", "Dev"], default="Architect", help="Initialization flavor")
    args = parser.parse_args()

    print(f"{GREEN}#########################################{RESET}")
    print(f"{GREEN}# ANTIGRAVITY INITIALIZATION ENGINE     #{RESET}")
    print(f"{GREEN}#########################################{RESET}")

    # 1. Guardrails
    if not check_guardrails(args.force):
        sys.exit(1)

    # 2. Configuration Strategy
    project_name = DEFAULT_PROJECT_NAME
    prefix = DEFAULT_PREFIX
    
    if args.manifest:
        print(f"{BLUE}Loading Manifest: {args.manifest}{RESET}")
        try:
            with open(args.manifest, 'r') as f:
                data = json.load(f)
                project_name = data.get("project_name", project_name)
                prefix = data.get("prefix", prefix)
        except Exception as e:
            print(f"{RED}Failed to load manifest: {e}{RESET}")
            sys.exit(1)
    else:
        # Interactive Wizard
        print("\nWelcome Architect. Let's configure your new Agent System.")
        project_name = input_clean("Project Name", "Solaris")
        prefix = input_clean("Project Prefix (2-4 chars)", "SOL").upper()

        print(f"\n{BLUE}Plan:{RESET}")
        print(f"- Project: {DEFAULT_PROJECT_NAME} -> {GREEN}{project_name}{RESET}")
        print(f"- Prefix:  {DEFAULT_PREFIX}       -> {GREEN}{prefix}{RESET}")
        
        if input_clean("Proceed?", "y").lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # 3. Execution
    hydrate_config(project_name, prefix)
    populate_docs()
    init_env()

    print(f"\n{GREEN}#########################################{RESET}")
    print(f"{GREEN}# INITIALIZATION COMPLETE               #{RESET}")
    print(f"{GREEN}#########################################{RESET}")
    print(f"\nNext Steps:")
    print(f"1. Run canary check: {YELLOW}python3 .agent/tools/canary_check.py{RESET}")

if __name__ == "__main__":
    main()
