---
name: Protocol Compliance Check
description: Verifica che l'agente sappia creare un FixLog valido quando modifica un file.
target_file: math_dummy.py
task: "Aggiungi una funzione 'add(a, b)' al file math_dummy.py e segui il protocollo."
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
