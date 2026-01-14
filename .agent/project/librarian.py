#!/usr/bin/env python3
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

def run_duckdb_audit():
    """Esegue l'analisi strutturale usando DuckDB."""
    if not HAS_DUCKDB:
        print(f"{RED}[!] DuckDB not installed. Run with `uv run --with duckdb ...` to enable audit.{RESET}")
        return

    print(f"\n{BLUE}=== 🦆 Librarian: Deep Structural Analysis (DuckDB) ==={RESET}")
    metadata = get_file_metadata()
    
    # In-Memory DB for analysis (Could be persisted if needed)
    conn = duckdb.connect(':memory:')
    
    # Crea tabella e carica dati
    conn.execute("CREATE TABLE files (path VARCHAR, size_kb DOUBLE, age_days DOUBLE, extension VARCHAR)")
    
    # Bulk insert is faster but simple loop is fine for this scale
    # Prepare data for executemany
    data_to_insert = [(f['path'], f['size_kb'], f['age_days'], f['extension']) for f in metadata]
    conn.executemany("INSERT INTO files VALUES (?, ?, ?, ?)", data_to_insert)
    
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

def main():
    parser = argparse.ArgumentParser(description="The Librarian: Project Hygiene Tool")
    parser.add_argument('--audit', action='store_true', help='Run DuckDB structural audit')
    parser.add_argument('--hygiene', action='store_true', help='Run standard hygiene checks')
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
        
    if args.audit or args.all:
        run_duckdb_audit()

    print(f"\n{GREEN}=== Checks Complete ==={RESET}")

if __name__ == "__main__":
    main()
