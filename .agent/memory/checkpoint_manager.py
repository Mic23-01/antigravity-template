#!/usr/bin/env python3
"""
Checkpoint Manager
------------------
Robust handler for the Agent's "Hot State" (STATE.md).
Ensures atomic writes, rotation, and structure validation.
"""

import os
import shutil
import datetime
import argparse
import sys
from pathlib import Path

# Constants
MEMORY_DIR = Path(__file__).parent.resolve()
STATE_FILE = MEMORY_DIR / "STATE.md"
BACKUP_DIR = MEMORY_DIR / "backups"

def ensure_dirs():
    """Ensure memory and backup directories exist."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def rotate_backups():
    """Keep last 5 backups."""
    if not STATE_FILE.exists():
        return
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = BACKUP_DIR / f"STATE_{timestamp}.md"
    shutil.copy2(STATE_FILE, backup_path)
    
    # Prune old backups
    backups = sorted(BACKUP_DIR.glob("STATE_*.md"))
    if len(backups) > 5:
        for old_backup in backups[:-5]:
            old_backup.unlink()

def write_state(state_text, context_text, next_text):
    """
    Atomic write of the state file.
    Does not use 'w' mode directly on the target to avoid corruption during crash.
    """
    ensure_dirs()
    rotate_backups()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# Agent Session State
**Last Updated**: {timestamp}

## @STATE (Current Narrative)
{state_text}

## @CONTEXT (Compacted History)
{context_text}

## @NEXT (Immediate Step)
{next_text}
"""
    
    temp_file = STATE_FILE.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Atomic move
    shutil.move(temp_file, STATE_FILE)
    print(f"State updated successfully at {STATE_FILE}")

def read_state():
    """Read the current state safely."""
    if not STATE_FILE.exists():
        return "NO_STATE_FOUND"
    return STATE_FILE.read_text(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Manage Agent Checkpoint State")
    subparsers = parser.add_subparsers(dest="command")
    
    # Update Command
    update_parser = subparsers.add_parser("update", help="Update the state")
    update_parser.add_argument("--state", required=True, help="Current Narrative Narrative")
    update_parser.add_argument("--context", required=True, help="Compacted History")
    update_parser.add_argument("--next", required=True, help="Next Action")
    
    # Read Command
    read_parser = subparsers.add_parser("read", help="Read current state")
    
    args = parser.parse_args()
    
    if args.command == "update":
        write_state(args.state, args.context, args.next)
    elif args.command == "read":
        print(read_state())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
