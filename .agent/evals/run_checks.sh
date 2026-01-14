#!/usr/bin/env bash
set -euo pipefail

PY=".venv/bin/python"

echo "== Chroma regression gate (canary IDs) =="

$PY .agent/evals/check_chroma.py --collection fix_logs --id ded.fix.eval.metadata_gate
$PY .agent/evals/check_chroma.py --collection research_summaries --id ded.research.eval.metadata_gate

echo "PASS: regression gate OK"
