#!/usr/bin/env python3
"""
Event Logger Module (Antigravity Telemetry Backbone)
----------------------------------------------------
A robust, singleton-based logger for operational telemetry.
Implementing Dual Layer Audit:
- Layer 1: Machine (JSONL) - Full Traceability
- Layer 2: Human (Markdown) - Readable Summary (Critical Events Only)
"""
import json
import datetime
import os
import sys
from pathlib import Path
from enum import Enum, auto

# Paths
AGENT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = AGENT_ROOT / "audit"
JSONL_PATH = AUDIT_DIR / "agent_events.jsonl"
MARKDOWN_PATH = AUDIT_DIR / "audit_summary.md"

class EventType(Enum):
    """Standardized Event Types"""
    FIX_LOG = "FIX_LOG"
    CANARY_START = "CANARY_START" 
    CANARY_PASS = "CANARY_PASS"
    CANARY_FAIL = "CANARY_FAIL"
    TOOL_ERROR = "TOOL_ERROR"
    DECISION_MADE = "DECISION_MADE"
    EVAL_COMPLETE = "EVAL_COMPLETE"
    GENERIC = "GENERIC"

class Telemetry:
    _instance = None
    _context = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Telemetry, cls).__new__(cls)
            cls._instance._ensure_audit_dir()
        return cls._instance

    def _ensure_audit_dir(self):
        if not AUDIT_DIR.exists():
            AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    def set_context(self, **kwargs):
        """Sets global context for all subsequent logs (e.g. project name)."""
        self._context.update(kwargs)

    def log(self, event_type: str, payload: dict):
        """
        Logs an event to both JSONL and Markdown.
        """
        self._ensure_audit_dir()
        
        timestamp = datetime.datetime.now().isoformat()
        
        # Merge payload with global context
        final_payload = {**self._context, **payload}
        
        # --- Layer 1: Machine (JSONL) ---
        event_record = {
            "timestamp": timestamp,
            "type": event_type,
            "payload": final_payload
        }
        
        try:
            with open(JSONL_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_record) + "\n")
        except Exception as e:
            # Failsafe: print to stderr if logging fails
            print(f"\033[91m[TELEMETRY FAILURE] Could not write to JSONL: {e}\033[0m", file=sys.stderr)

        # --- Layer 2: Human (Markdown) ---
        # Only Log significant events to Markdown
        critical_events = [
            EventType.FIX_LOG.value, 
            EventType.EVAL_COMPLETE.value, 
            EventType.DECISION_MADE.value,
            EventType.CANARY_FAIL.value
        ]
        
        if event_type in critical_events:
            self._update_markdown_index(timestamp, event_type, final_payload)

    def _update_markdown_index(self, timestamp, event_type, payload):
        """
        Updates the human-readable Markdown table.
        """
        header = "| Date | Type | Description | Result | Evidence |\n| :--- | :--- | :--- | :--- | :--- |\n"
        
        if not MARKDOWN_PATH.exists():
            with open(MARKDOWN_PATH, "w", encoding="utf-8") as f:
                f.write(f"# 🛡️ Antigravity Audit Summary\n\n> **Human Layer**: Summary of critical events. For full traces see `agent_events.jsonl`.\n\n{header}")
        
        # Extract details safely
        desc = payload.get("description") or payload.get("document") or "N/A"
        result = payload.get("result") or payload.get("score") or "INFO"
        
        # Evidence handling
        evidence = "N/A"
        if "evidence_path" in payload:
            evidence = f"[Link]({payload['evidence_path']})"
        elif "files" in payload:
            evidence = f"`{len(payload['files'])} files`"
        elif "id" in payload:
             evidence = f"`{payload['id']}`"

        dt_short = timestamp.split("T")[0]
        
        row = f"| {dt_short} | **{event_type}** | {desc} | {result} | {evidence} |\n"
        
        try:
            with open(MARKDOWN_PATH, "a", encoding="utf-8") as f:
                f.write(row)
        except Exception as e:
            print(f"\033[91m[TELEMETRY FAILURE] Could not write to Markdown: {e}\033[0m", file=sys.stderr)

# Singleton Export
logger = Telemetry()

# CLI Self-Test
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run self-test")
    args = parser.parse_args()

    if args.test:
        print("Running Telemetry Self-Test...")
        logger.set_context(project="Antigravity", user="Canary")
        logger.log(EventType.GENERIC.value, {"message": "Test Event"})
        print("✔ JSONL Logged")
        logger.log(EventType.FIX_LOG.value, {"description": "Telemetry Upgrade", "result": "SUCCESS", "id": "TEST-123"})
        print("✔ Markdown Logged")
        print("Done.")
