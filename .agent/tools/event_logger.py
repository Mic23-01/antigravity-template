#!/usr/bin/env python3
"""
Event Logger Module (Antigravity Dual Layer Audit)
Layer 1: Machine (JSONL) - Full Traceability
Layer 2: Human (Markdown) - Readable Summary
"""
import json
import datetime
import os
from pathlib import Path

# Paths
AUDIT_DIR = Path(".agent/audit")
JSONL_PATH = AUDIT_DIR / "agent_events.jsonl"
MARKDOWN_PATH = AUDIT_DIR / "audit_summary.md"

def ensure_audit_dir():
    if not AUDIT_DIR.exists():
        AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def log_event(event_type, payload, project_name="Unknown"):
    """
    Logs an event to both JSONL and Markdown.
    """
    ensure_audit_dir()
    
    timestamp = datetime.datetime.now().isoformat()
    
    # --- Layer 1: Machine (JSONL) ---
    event_record = {
        "timestamp": timestamp,
        "type": event_type,
        "project": project_name,
        "payload": payload
    }
    
    try:
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_record) + "\n")
    except Exception as e:
        print(f"Error writing to JSONL: {e}")

    # --- Layer 2: Human (Markdown) ---
    # Only Log significant events to Markdown (Fixes, Evals, Decisions)
    if event_type in ["FIX_LOG", "EVAL_COMPLETE", "DECISION_MADE"]:
        update_markdown_index(timestamp, event_type, payload)

def update_markdown_index(timestamp, event_type, payload):
    """
    Updates the human-readable Markdown table.
    """
    # Header check
    header = "| Date | Type | Description | Result | Evidence |\n| :--- | :--- | :--- | :--- | :--- |\n"
    
    if not MARKDOWN_PATH.exists():
        with open(MARKDOWN_PATH, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Antigravity Audit Summary\n\n> **Human Layer**: Summary of critical events. For full traces see `agent_events.jsonl`.\n\n{header}")
    
    # Format Row
    # Extract details safely
    desc = payload.get("description") or payload.get("document") or "N/A"
    result = payload.get("result") or payload.get("score") or "INFO"
    
    # Evidence handling
    evidence = "N/A"
    if "evidence_path" in payload:
        evidence = f"[Link]({payload['evidence_path']})"
    elif "files" in payload:
        evidence = f"`{len(payload['files'])} files`"

    dt_short = timestamp.split("T")[0]
    
    row = f"| {dt_short} | **{event_type}** | {desc} | {result} | {evidence} |\n"
    
    try:
        with open(MARKDOWN_PATH, "a", encoding="utf-8") as f:
            f.write(row)
    except Exception as e:
        print(f"Error writing to Markdown: {e}")

# Self-test when run directly
if __name__ == "__main__":
    log_event("TEST_EVENT", {"description": "Logger Initialized", "result": "PASS"}, "Antigravity")
