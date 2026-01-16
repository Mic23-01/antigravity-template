#!/usr/bin/env python3
"""
Checkpoint Manager (MemoryEngine Edition)
-----------------------------------------
Robust handler for the Agent's "Hot State" (STATE.md).
Ensures atomic writes, rotation, and structure validation.
Supports sandboxed environments via configurable paths.
"""

import os
import shutil
import datetime
import argparse
import json
import sys
from pathlib import Path


class MemoryEngine:
    """
    Core class for Agent memory persistence.
    Supports both real and sandboxed environments.
    """

    def __init__(self, memory_dir: Path = None):
        """
        Initialize the MemoryEngine.
        
        Args:
            memory_dir: Custom directory for memory storage.
                        Defaults to the directory containing this script.
        """
        if memory_dir is None:
            self.memory_dir = Path(__file__).parent.resolve()
        else:
            self.memory_dir = Path(memory_dir).resolve()
        
        self.state_file = self.memory_dir / "STATE.md"
        self.backup_dir = self.memory_dir / "backups"
        self._ensure_dirs()

    def _ensure_dirs(self):
        """Ensure memory and backup directories exist."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _rotate_backups(self, max_backups: int = 5):
        """Keep last N backups."""
        if not self.state_file.exists():
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = self.backup_dir / f"STATE_{timestamp}.md"
        shutil.copy2(self.state_file, backup_path)

        # Prune old backups
        backups = sorted(self.backup_dir.glob("STATE_*.md"))
        if len(backups) > max_backups:
            for old_backup in backups[:-max_backups]:
                old_backup.unlink()

    def update(self, state: str, context: str, next_step: str) -> dict:
        """
        Atomic write of the state file.
        
        Args:
            state: Current narrative of what is happening.
            context: Compacted history of recent events.
            next_step: The immediate next action.
            
        Returns:
            dict: Status of the update operation.
        """
        self._rotate_backups()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = f"""# Agent Session State
**Last Updated**: {timestamp}

## @STATE (Current Narrative)
{state}

## @CONTEXT (Compacted History)
{context}

## @NEXT (Immediate Step)
{next_step}
"""

        temp_file = self.state_file.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)

        # Atomic move
        shutil.move(temp_file, self.state_file)
        
        return {
            "status": "success",
            "path": str(self.state_file),
            "timestamp": timestamp
        }

    def read(self, as_json: bool = False) -> str | dict:
        """
        Read the current state.
        
        Args:
            as_json: If True, return structured dict instead of raw markdown.
            
        Returns:
            str or dict: Current state content.
        """
        if not self.state_file.exists():
            if as_json:
                return {"status": "no_state", "state": None, "context": None, "next": None}
            return "NO_STATE_FOUND"

        content = self.state_file.read_text(encoding="utf-8")
        
        if as_json:
            # Parse sections
            result = {"status": "ok", "raw": content}
            try:
                if "@STATE" in content:
                    state_section = content.split("## @STATE")[1].split("## @CONTEXT")[0]
                    result["state"] = state_section.strip().replace("(Current Narrative)\n", "")
                if "@CONTEXT" in content:
                    context_section = content.split("## @CONTEXT")[1].split("## @NEXT")[0]
                    result["context"] = context_section.strip().replace("(Compacted History)\n", "")
                if "@NEXT" in content:
                    next_section = content.split("## @NEXT")[1]
                    result["next"] = next_section.strip().replace("(Immediate Step)\n", "")
            except IndexError:
                pass
            return result
        
        return content

    def restore(self, backup_id: str = None) -> dict:
        """
        Restore from a backup.
        
        Args:
            backup_id: Timestamp ID of backup (e.g., '20260116_130529_123456').
                       If None or 'last', restores the most recent backup.
                       
        Returns:
            dict: Status of the restore operation.
        """
        backups = sorted(self.backup_dir.glob("STATE_*.md"))
        
        if not backups:
            return {"status": "error", "message": "No backups available"}
        
        if backup_id is None or backup_id == "last":
            target_backup = backups[-1]
        else:
            target_backup = self.backup_dir / f"STATE_{backup_id}.md"
            if not target_backup.exists():
                return {"status": "error", "message": f"Backup {backup_id} not found"}
        
        # Backup current before restoring
        self._rotate_backups()
        
        shutil.copy2(target_backup, self.state_file)
        
        return {
            "status": "success",
            "restored_from": str(target_backup),
            "current_state": str(self.state_file)
        }

    def list_backups(self) -> list:
        """List available backups."""
        backups = sorted(self.backup_dir.glob("STATE_*.md"))
        return [{"id": b.stem.replace("STATE_", ""), "path": str(b)} for b in backups]


# --- CLI Interface ---

def main():
    parser = argparse.ArgumentParser(description="Manage Agent Checkpoint State")
    subparsers = parser.add_subparsers(dest="command")

    # Update Command
    update_parser = subparsers.add_parser("update", help="Update the state")
    update_parser.add_argument("--state", required=True, help="Current Narrative")
    update_parser.add_argument("--context", required=True, help="Compacted History")
    update_parser.add_argument("--next", required=True, help="Next Action")
    update_parser.add_argument("--memory-dir", default=None, help="Custom memory directory")

    # Read Command
    read_parser = subparsers.add_parser("read", help="Read current state")
    read_parser.add_argument("--json", action="store_true", help="Output as JSON")
    read_parser.add_argument("--memory-dir", default=None, help="Custom memory directory")

    # Restore Command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("--id", default="last", help="Backup ID or 'last'")
    restore_parser.add_argument("--memory-dir", default=None, help="Custom memory directory")

    # List Backups Command
    list_parser = subparsers.add_parser("list-backups", help="List available backups")
    list_parser.add_argument("--memory-dir", default=None, help="Custom memory directory")

    args = parser.parse_args()

    # Determine memory directory
    memory_dir = Path(args.memory_dir) if hasattr(args, 'memory_dir') and args.memory_dir else None
    engine = MemoryEngine(memory_dir)

    if args.command == "update":
        result = engine.update(args.state, args.context, args.next)
        print(f"State updated successfully at {result['path']}")
    elif args.command == "read":
        output = engine.read(as_json=getattr(args, 'json', False))
        if isinstance(output, dict):
            print(json.dumps(output, indent=2))
        else:
            print(output)
    elif args.command == "restore":
        result = engine.restore(args.id)
        if result["status"] == "success":
            print(f"Restored from: {result['restored_from']}")
        else:
            print(f"Error: {result['message']}")
            sys.exit(1)
    elif args.command == "list-backups":
        backups = engine.list_backups()
        if backups:
            for b in backups:
                print(f"  {b['id']}")
        else:
            print("No backups available.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
