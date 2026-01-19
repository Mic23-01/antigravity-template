---
name: Protocol Compliance Check
description: Verifies that the agent knows how to create a valid FixLog when modifying a file.
target_file: math_dummy.py
task: "Add an 'add(a, b)' function to math_dummy.py and follow the protocol."
assertions:
  - type: file_exists
    path: math_dummy.py
  - type: file_contains
    path: math_dummy.py
    pattern: "def add"
  - type: file_glob_exists
    path: ".agent/fix_logs/AG.fix.*.json"
  - type: file_content_contains
    path: ".agent/fix_logs/AG.fix.*.json"
    pattern: '"result": "pass"'
---
