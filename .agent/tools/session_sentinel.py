#!/usr/bin/env python3
"""
Session Sentinel: The Guardian of Persistence.
Checks if there are modified files in the project that have NOT been covered by a subsequent FixLog.
Returns:
  0: CLEAN (All work logged)
  1: DIRTY (Unsaved work detected)
"""

import os
import sys
import json
import time
from pathlib import Path

# Config
IGNORE_DIRS = {
    ".git", ".pytest_cache", "__pycache__", "node_modules", "venv", 
    ".agent/fix_logs", ".agent/research_summaries", ".agent/brain"
}
IGNORE_FILES = {
    ".DS_Store", "uv.lock", "package-lock.json"
}
# Tolleranza in secondi (il log potrebbe esser scritto 1 secondo prima del flush su disco)
TOLERANCE_SECONDS = 2.0

def get_last_source_modification(root_path):
    max_mtime = 0.0
    last_file = None
    
    for root, dirs, files in os.walk(root_path):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
            
            # Skip artifacts (md files in brain are not "source code" in this context, usually)
            # Actually, we want to track EVERYTHING. If I change task.md, I should log it? 
            # Protocol says "Tech Tasks". Updating task.md is admin. 
            # Let's keep it strict: Code and Docs matter.
            
            full_path = Path(root) / file
            stat = full_path.stat()
            if stat.st_mtime > max_mtime:
                max_mtime = stat.st_mtime
                last_file = full_path
                
    return max_mtime, last_file

def get_last_fixlog_timestamp(logs_path):
    if not logs_path.exists():
        return 0.0, None
        
    max_log_time = 0.0
    last_log = None
    
    for log_file in logs_path.glob("*.json"):
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
                # We expect 'metadatas' -> 'date'. But date is just YYYY-MM-DD.
                # Use file creation time (st_mtime) of the JSON log itself as the "Seal of Quality".
                # The file mtime represents WHEN the agent committed the memory.
                stat = log_file.stat()
                if stat.st_mtime > max_log_time:
                    max_log_time = stat.st_mtime
                    last_log = log_file
        except:
            continue
            
    return max_log_time, last_log

def main():
    root_dir = Path(".")
    logs_dir = root_dir / ".agent/fix_logs"
    
    last_src_time, last_src_file = get_last_source_modification(root_dir)
    last_log_time, last_log_file = get_last_fixlog_timestamp(logs_dir)
    
    # Debug info (can be captured by caller)
    # print(f"DEBUG: Source {last_src_time} ({last_src_file}) vs Log {last_log_time} ({last_log_file})")
    
    if last_src_time > (last_log_time + TOLERANCE_SECONDS):
        print(f"DIRTY_SESSION_DETECTED")
        print(f"Last modified file: {last_src_file}")
        print(f"Timestamp: {last_src_time}")
        print(f"Last FixLog: {last_log_file}")
        print(f"Timestamp: {last_log_time}")
        sys.exit(1)
    else:
        # print("CLEAN_SESSION")
        sys.exit(0)

if __name__ == "__main__":
    main()
