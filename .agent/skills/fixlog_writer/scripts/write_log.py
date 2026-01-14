#!/usr/bin/env python3
"""
FixLog Writer Script.
Standardizes the creation of FixLog entries for ChromaDB.
"""
import argparse
import sys
import datetime
import json
import uuid

# ANSI Colors
GREEN = '\033[92m'
RESET = '\033[0m'
BLUE = '\033[94m'

def get_date_slug():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")

def main():
    parser = argparse.ArgumentParser(description="Generate and save FixLog entry.")
    parser.add_argument("--project", required=True, help="Project Name")
    parser.add_argument("--prefix", default="AG", help="Project Prefix")
    parser.add_argument("--desc", required=True, help="Description of the fix (Document content)")
    parser.add_argument("--files", required=True, help="Comma separated list of modified files")
    parser.add_argument("--test", required=True, help="Test results summary")
    parser.add_argument("--result", required=True, choices=["pass", "fail"], help="Outcome")
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument("--dry-run", action="store_true", help="Print JSON without saving to Chroma")

    args = parser.parse_args()

    # ID Generation Logic
    # Format: <Prefix>.fix.<YYYYMMDD>.<short_uuid>
    slug = str(uuid.uuid4())[:8]
    date_str = get_date_slug()
    log_id = f"{args.prefix}.fix.{date_str}.{slug}"
    
    # ISO Date for metadata
    iso_date = datetime.date.today().isoformat()

    # Construct Payload
    payload = {
        "id": log_id,
        "document": args.desc,
        "metadatas": {
            "project": args.project,
            "type": "fix_log",
            "date": iso_date,
            "files": args.files,
            "tests": args.test,
            "result": args.result,
            "notes": args.notes
        }
    }

    if args.dry_run:
        print(f"{BLUE}=== DRY RUN: Generated Payload ==={RESET}")
        print(json.dumps(payload, indent=2))
        return

    # Chroma Injection (simulated via update_tool call structure output for Agent usage)
    # real persistence handles via 'uv run --with chromadb ...' if we implemented the full db write here.
    # For now, to keep it simple and aligned with existing tools: 
    # we emit the JSON that the Agent should pass to `chroma_add_documents` or `chroma_update_documents`.
    
    print(f"{GREEN}=== Generated FixLog Payload ==={RESET}")
    print(json.dumps(payload, indent=2))
    print(f"\n{BLUE}To save, use the chroma_add_documents tool with this data.{RESET}")

if __name__ == "__main__":
    main()
