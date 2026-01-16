import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Try importing duckdb, handle if missing
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

# Config
IGNORE_DIRS = {
    ".git", ".pytest_cache", "__pycache__", "node_modules", "venv", 
    ".agent/fix_logs", ".agent/research_summaries", ".agent/brain", ".agent/memory", "memory"
}
IGNORE_FILES = {
    ".DS_Store", "uv.lock", "package-lock.json"
}
TOLERANCE_SECONDS = 2.0
DB_PATH = Path(".agent/memory/librarian.db")

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

def get_last_source_modification(root_path):
    max_mtime = 0.0
    last_file = None
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
            
            full_path = Path(root) / file
            try:
                stat = full_path.stat()
                if stat.st_mtime > max_mtime:
                    max_mtime = stat.st_mtime
                    last_file = full_path
            except Exception:
                continue
                
    return max_mtime, last_file

def get_last_fixlog_timestamp(logs_path):
    if not logs_path.exists():
        return 0.0, None
        
    max_log_time = 0.0
    last_log = None
    
    for log_file in logs_path.glob("*.json"):
        try:
            stat = log_file.stat()
            if stat.st_mtime > max_log_time:
                max_log_time = stat.st_mtime
                last_log = log_file
        except:
            continue
            
    return max_log_time, last_log

def get_semantic_diff():
    """Returns a concise summary of changes using git diff --stat."""
    try:
        # Check if it's a git repo
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True)
        res = subprocess.run(["git", "diff", "--stat"], capture_output=True, text=True)
        if res.stdout.strip():
            return res.stdout.strip()
        
        # If no indexed changes, check cached/unstaged
        res = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
        return res.stdout.strip() or "No detectable semantic diff (files changed but content identical?)"
    except:
        return "Semantic diff unavailable (Not a git repository or git missing)."

def check_duckdb_consistency(last_log_time):
    """
    Dual Check: Queries DuckDB to find files modified since the last log.
    Returns (is_dirty, details)
    """
    if not HAS_DUCKDB or not DB_PATH.exists():
        return False, "DuckDB check skipped (Missing library or DB file)."
    
    try:
        conn = duckdb.connect(str(DB_PATH))
        # Find files where mtime > last_log_time
        res = conn.execute("SELECT path, mtime FROM files WHERE mtime > ?", [last_log_time]).fetchall()
        conn.close()
        
        if res:
            details = "\n".join([f"  - {row[0]} (DB mtime: {row[1]})" for row in res])
            return True, details
        return False, "Clean"
    except Exception as e:
        return False, f"DuckDB check error: {e}"

def main():
    root_dir = Path(".")
    logs_dir = root_dir / ".agent/fix_logs"
    
    last_src_time, last_src_file = get_last_source_modification(root_dir)
    last_log_time, last_log_file = get_last_fixlog_timestamp(logs_dir)
    
    # Debug info (can be captured by caller)
    # print(f"DEBUG: Last Source: {last_src_time} ({last_src_file})")
    # print(f"DEBUG: Last Log:    {last_log_time} ({last_log_file})")

    is_dirty_walk = last_src_time > (last_log_time + TOLERANCE_SECONDS)
    is_dirty_db, db_details = check_duckdb_consistency(last_log_time)
    
    if is_dirty_walk or is_dirty_db:
        print(f"{RED}#########################################{RESET}")
        print(f"{RED}# DIRTY SESSION DETECTED (Sentinel v2)  #{RESET}")
        print(f"{RED}#########################################{RESET}")
        
        print(f"\n{YELLOW}[1] Filesystem Layer (os.walk):{RESET}")
        if is_dirty_walk:
            print(f"  {RED}✘ DIRTY{RESET}")
            print(f"  Last modified file: {last_src_file}")
            print(f"  Timestamp: {last_src_time}")
        else:
            print(f"  {GREEN}✔ CLEAN{RESET}")

        print(f"\n{YELLOW}[2] Structural Layer (DuckDB):{RESET}")
        if is_dirty_db:
            print(f"  {RED}✘ DIRTY{RESET}")
            print(db_details)
        else:
            print(f"  {GREEN}✔ CLEAN{RESET}")
            
        print(f"\n{BLUE}=== Semantic Diff (Git Stat) ==={RESET}")
        print(get_semantic_diff())
        
        print(f"\n{RED}FATAL: Discrepancy detected between memory and reality.{RESET}")
        print(f"{YELLOW}Action: Sync FixLogs before proceeding.{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}✔ SESSION CLEAN (Dual Layer Verification Passed){RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
