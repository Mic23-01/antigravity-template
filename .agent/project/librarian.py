#!/usr/bin/env python3
# /// script
# dependencies = ["duckdb"]
# ///
"""
The Librarian: Automated Hygiene & Structural Analysis Tool.
Integrates filesystem heuristics and DuckDB-based code analysis.

Usage:
  uv run --with duckdb .agent/project/librarian.py [options]
  
Options:
  --audit       Run deep structural analysis using DuckDB (The SQL Eye)
  --hygiene     Run standard file hygiene checks (Ghost files, Configs)
  --all         Run all checks (Default)
"""

import os
import json
import glob
import sys
import time
import argparse
import re
from pathlib import Path

# Try importing duckdb, handle if missing
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

def get_file_metadata(root_dir="."):
    """Raccoglie i metadati reali del filesystem per DuckDB."""
    metadata = []
    # Ignore node_modules, .git, .venv to speed up and reduce noise
    exclude_dirs = {'node_modules', '.git', '.venv', '__pycache__', 'dist', 'coverage'}
    
    for path in Path(root_dir).rglob('*'):
        # Check if any parent part is in exclude list
        if any(part in exclude_dirs for part in path.parts):
            continue
            
        if path.is_file():
            try:
                stat = path.stat()
                metadata.append({
                    "path": str(path),
                    "size_kb": stat.st_size / 1024,
                    "age_days": (time.time() - stat.st_mtime) / (24 * 3600),
                    "extension": path.suffix
                })
            except Exception:
                continue
    return metadata

def run_duckdb_audit(db_path=":memory:"):
    """Esegue l'analisi strutturale usando DuckDB."""
    if not HAS_DUCKDB:
        print(f"{RED}[!] DuckDB not installed. Run with `uv run --with duckdb ...` to enable audit.{RESET}")
        return

    print(f"\n{BLUE}=== 🦆 Librarian: Deep Structural Analysis (DuckDB) ==={RESET}")
    metadata = get_file_metadata()
    
    # In-Memory or Persistent DB
    if db_path != ":memory:":
        print(f"  {BLUE}Persisting to {db_path}...{RESET}")
        
    conn = duckdb.connect(db_path)
    
    # Crea tabella e carica dati (Drop if exists to refresh state)
    conn.execute("DROP TABLE IF EXISTS files")
    conn.execute("CREATE TABLE files (path VARCHAR, size_kb DOUBLE, age_days DOUBLE, extension VARCHAR, mtime DOUBLE)")
    
    # Prepare data for executemany
    data_to_insert = [(f['path'], f['size_kb'], f['age_days'], f['extension'], Path(f['path']).stat().st_mtime) for f in metadata]
    conn.executemany("INSERT INTO files VALUES (?, ?, ?, ?, ?)", data_to_insert)
    
    # 1. Rilevamento potenziale codice morto / File vecchi mai toccati
    print(f"\n{YELLOW}[!] Stale Files (> 30 days inactive):{RESET}")
    stale_files = conn.execute("""
        SELECT path, age_days 
        FROM files 
        WHERE age_days > 30 
          AND extension IN ('.py', '.ts', '.tsx', '.md') 
          AND path NOT LIKE '%.agent%' 
        ORDER BY age_days DESC 
        LIMIT 10
    """).fetchall()
    
    if stale_files:
        for row in stale_files:
            print(f"  - {row[0]} ({int(row[1])} days)")
    else:
        print(f"  {GREEN}None found.{RESET}")

    # 2. Analisi Complessità/Dimensione
    print(f"\n{YELLOW}[!] Large Files (> 50KB) - Refactor Candidates:{RESET}")
    big_files = conn.execute("SELECT path, size_kb FROM files WHERE size_kb > 50 ORDER BY size_kb DESC LIMIT 10").fetchall()
    if big_files:
        for row in big_files:
            print(f"  - {row[0]} ({int(row[1])} KB)")
    else:
        print(f"  {GREEN}None found.{RESET}")

    # 3. Distribuzione Componenti
    print(f"\n{YELLOW}[!] File Type Distribution:{RESET}")
    stats = conn.execute("SELECT extension, count(*) as count FROM files GROUP BY extension HAVING count > 1 ORDER BY count DESC").fetchall()
    for row in stats:
        print(f"  - {row[0]}: {row[1]} files")

def check_ghost_files():
    """Finds files that might be dead/ghosts (Simple Heuristic)."""
    print(f"\n{YELLOW}[*] Ghost File Hunt (Heuristic)...{RESET}")
    ghosts = []
    # Using glob strictly excluding common noise
    for ext in ['**/*.ts', '**/*.tsx', '**/*.py', '**/*.js']:
        for f in glob.glob(ext, recursive=True):
            if any(x in f for x in ['node_modules', '.agent', 'dist', 'coverage', '.git']):
                continue
            lower = f.lower()
            if '_backup' in lower or '_old' in lower or 'tmp_' in lower:
                ghosts.append(f)
    
    if ghosts:
        print(f"{RED}Found {len(ghosts)} potential ghost files:{RESET}")
        for g in ghosts:
            print(f"  - {g}")
    else:
        print(f"{GREEN}No obvious ghost files found.{RESET}")

def check_config_schema():
    """Validates backend config against expected structure."""
    print(f"\n{YELLOW}[*] Config Schema Check...{RESET}")
    config_path = 'backend/characters_config.json'
    if not os.path.exists(config_path):
        # Silent fail if project structure implies it might not exist yet
        return

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict):
             print(f"{RED}Config root is not a dict{RESET}")
             return
        print(f"{GREEN}Config JSON is valid.{RESET}")
    except json.JSONDecodeError:
        print(f"{RED}Config JSON is malformed!{RESET}")

def check_component_duplication():
    """Checks for duplicate component names in large files."""
    print(f"\n{YELLOW}[*] Component Duplication Check...{RESET}")
    files_to_check = ['App.tsx', 'src/features/master-dashboard/MasterDashboardRoot.tsx']
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Very simple check for duplicate JSX tags
        import re
        modals = ['SpellsModal', 'InventoryModal', 'CantripsModal', 'FeaturesModal']
        for modal in modals:
            matches = re.findall(rf'<{modal}\s', content)
            if len(matches) > 1:
                print(f"{RED}DANGER: Duplicate <{modal}> found in {file_path}!{RESET}")
                return False
    
    print(f"{GREEN}No duplicate critical components found.{RESET}")
    return True

def check_docs_custom():
    """Verifica la presenza e l'integrità della documentazione custom."""
    print(f"\n{YELLOW}[*] Docs Custom Check...{RESET}")
    docs_dir = Path("docs_custom")
    required_files = [
        "architecture.md",
        "brand_identity_guide.md",
        "domain_language.md",
        "product_strategy.md",
        "SOURCES.md"
    ]
    
    if not docs_dir.exists():
        print(f"{RED}[!] docs_custom/ directory MISSING! Project not hydrated.{RESET}")
        return

    missing = []
    for f in required_files:
        if not (docs_dir / f).exists():
            missing.append(f)
            
    if missing:
        print(f"{RED}[!] Missing Critical Docs in docs_custom/:{RESET}")
        for m in missing:
            print(f"  - {m}")
    else:
        print(f"{GREEN}All Critical Docs present in docs_custom/.{RESET}")

def check_dependency_sync():
    """Verifies if requirements.txt and pyproject.toml are in sync (basic check)."""
    print(f"\n{YELLOW}[*] Dependency Sync Check...{RESET}")
    req_path = Path("requirements.txt")
    toml_path = Path("pyproject.toml")
    
    if not req_path.exists() or not toml_path.exists():
        print(f"  {YELLOW}[SKIP]{RESET} One or both config files (requirements.txt, pyproject.toml) are missing.")
        return

    try:
        req_content = req_path.read_text()
        toml_content = toml_path.read_text()
        
        # Very naive check: search for names of dependencies in each other
        # This is a heuristic to catch obvious omissions
        import re
        # Find everything that looks like a package name in requirements.txt (e.g. "package==" or "package>=")
        req_packages = re.findall(r'^([a-zA-Z0-9_\-]+)', req_content, re.MULTILINE)
        
        missing_in_toml = []
        for pkg in req_packages:
            if pkg.lower() not in toml_content.lower():
                missing_in_toml.append(pkg)
                
        if missing_in_toml:
            print(f"{RED}[!] Discrepancy Found:{RESET}")
            for m in missing_in_toml:
                print(f"  - '{m}' found in requirements.txt but missing in pyproject.toml")
        else:
            print(f"{GREEN}Dependencies seem vertically synced.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Failed to sync dependencies: {e}")

def check_readme_structure():
    """Verifies if the directory structure in README.md matches actual reality."""
    print(f"\n{YELLOW}[*] README Structure Alignment...{RESET}")
    readme_path = Path("README.md")
    if not readme_path.exists():
        return

    try:
        content = readme_path.read_text()
        lines = content.splitlines()
        
        missing_paths = []
        path_stack = [] # list of (indent_level, name)
        
        for line in lines:
            # Look for tree nodes: │   ├── .agent/  or └── memory/
            match = re.search(r'^([│\s\s\s]*)[├└]──\s*([a-zA-Z0-9_\-\./]+)', line)
            if match:
                indent = len(match.group(1))
                name = match.group(2).strip().rstrip('/')
                
                # Pop from stack until we find the parent (lower indent)
                while path_stack and path_stack[-1][0] >= indent:
                    path_stack.pop()
                
                # Construct path
                if path_stack:
                    full_path = os.path.join(path_stack[-1][1], name)
                else:
                    full_path = name
                
                # If it's a directory, we push it to stack for children
                # (Assuming dirs end with / or are known dirs)
                if line.strip().endswith('/') or '/' in name or os.path.isdir(full_path):
                     path_stack.append((indent, full_path))
                
                if not os.path.exists(full_path):
                    # Fallback: maybe it's just a file in the root mentioned with a name?
                    if not os.path.exists(name):
                        missing_paths.append(full_path)
                
        if missing_paths:
            print(f"{RED}[!] Documentation Drift Detected in README.md:{RESET}")
            for m in missing_paths:
                print(f"  - Reference '{m}' does not exist on disk.")
        else:
            print(f"{GREEN}README structure is aligned with filesystem.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} README check failed: {e}")

def check_project_config():
    """Validates if the core agent configuration exists and is readable."""
    print(f"\n{YELLOW}[*] Project Agent Config Check...{RESET}")
    config_path = Path(".agent/project/PROJECT_AGENT_CONFIG.md")
    if not config_path.exists():
        print(f"{RED}[!] PROJECT_AGENT_CONFIG.md is MISSING!{RESET}")
    else:
        print(f"{GREEN}Core config found.{RESET}")

def check_dead_code():
    """Heuristic search for functions/classes defined but never used."""
    print(f"\n{YELLOW}[*] Dead Code Hunt (AST Heuristic)...{RESET}")
    py_files = list(Path(".").rglob("*.py"))
    py_files = [f for f in py_files if not any(x in str(f) for x in ['.agent', '.venv', 'tests', '__pycache__'])]
    
    import re
    definitions = {} # name -> file
    
    # 1. Collect definitions
    for f in py_files:
        try:
            content = f.read_text()
            # def name( or class name( or class name:
            found = re.findall(r'(?:def|class)\s+([a-zA-Z0-9_]+)\s*[\(\:]', content)
            for name in found:
                if name.startswith('_') or name == 'main': # Removed 'or name == 'Task'' as per instruction context
                    continue
                definitions[name] = str(f)
        except Exception:
            continue
            
    # 2. Search for usages
    all_content = ""
    for f in py_files:
        try:
            all_content += f.read_text()
        except:
            continue
            
    dead_candidates = []
    for name, source_file in definitions.items():
        # Count occurrences. If 1, it's just the definition.
        # This is a very rough estimate but good for a "Librarian" warning.
        if all_content.count(name) <= 1:
            dead_candidates.append(f"{name} ({source_file})")
            
    if dead_candidates:
        print(f"{YELLOW}[!] Potential Dead Code (1 usage only):{RESET}")
        for d in dead_candidates:
            print(f"  - {d}")
    else:
        print(f"{GREEN}No obvious dead code detected.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="The Librarian: Project Hygiene Tool")
    parser.add_argument('--audit', action='store_true', help='Run DuckDB structural audit')
    parser.add_argument('--hygiene', action='store_true', help='Run standard hygiene checks')
    parser.add_argument('--persist', action='store_true', help='Persists results to .agent/memory/librarian.db')
    parser.add_argument('--all', action='store_true', help='Run all checks')
    
    # Default to all if no args
    if len(sys.argv) == 1:
        args = parser.parse_args(['--all'])
    else:
        args = parser.parse_args()

    print(f"{GREEN}=== The Librarian: Automated Hygiene Check ==={RESET}")
    
    if args.hygiene or args.all:
        check_ghost_files()
        check_config_schema()
        check_component_duplication()
        check_docs_custom()
        check_dependency_sync()
        check_readme_structure()
        check_project_config()
        check_dead_code()
        
    if args.audit or args.all or args.persist:
        # Use persistent DB if --persist or --all is set
        db_path = ":memory:"
        if args.all or args.persist:
             db_path = str(Path(".agent/memory/librarian.db"))
             # Ensure directory exists
             Path(".agent/memory").mkdir(parents=True, exist_ok=True)
             
        run_duckdb_audit(db_path)

    print(f"\n{GREEN}=== Checks Complete ==={RESET}")

if __name__ == "__main__":
    main()
