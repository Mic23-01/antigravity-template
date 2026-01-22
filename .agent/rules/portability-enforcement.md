---
trigger: always_on
description: Portability Enforcement (Anti-Hardcoded Paths)
---

# Portability Enforcement (ALWAYS ON)

**SUPREME DIRECTIVE**: The Antigravity template is designed for **universal portability**. Hardcoded paths tied to specific users or OS configurations are **strictly prohibited**.

## Purpose
Ensure code, skills, and documentation remain portable across different:
- Operating Systems (Linux, macOS, Windows)
- User accounts (`ubuntu`, `john`, etc.)
- Deployment environments (local, Docker, CI/CD)

## PROHIBITED Patterns

The Agent **MUST NEVER** commit or propose:

### 1. Absolute User Paths
- ❌ `/home/ubuntu/Projects/...`
- ❌ `/Users/john/Documents/...`
- ❌ `C:\Users\Admin\Desktop\...`

### 2. Hardcoded OS Directories
- ❌ `/usr/local/bin/myapp` (without env var fallback)
- ❌ `C:\Program Files\App\...`

### 3. IDE/Editor-Specific Paths in Examples
- ❌ `file:///home/ubuntu/Progetti/...` (in documentation)
- ❌ Absolute workspace paths in JSON/YAML configs

## REQUIRED Actions

### For Code (Python/Node/etc.)
```python
# ✅ CORRECT: Use environment variables with sensible defaults
import os
path = os.environ.get("MY_VAR", os.path.expanduser("~/default_dir"))

# ❌ WRONG:
path = "/home/ubuntu/my_project"
```

### For Documentation
```markdown
# ✅ CORRECT: Use relative or home-based paths
Clone to: `~/projects/antigravity`

# ❌ WRONG:
Clone to: `/home/ubuntu/Progetti/antigravity`
```

### For Examples/Configs
```bash
# ✅ CORRECT: Use environment variables or placeholders
export MY_PATH="$HOME/custom_path"

# ❌ WRONG:
MY_PATH=/home/ubuntu/custom_path
```

## Enforcement Strategy

### 1. Pre-Commit Detection
Run security audit before committing:
```bash
uv run .agent/skills/security_audit/scripts/audit_runner.py
```

### 2. Manual Review Checklist
Before creating Pull Requests or releases:
- [ ] No `/home/<user>/` patterns in code
- [ ] All paths use env vars or `~` expansion
- [ ] Documentation uses generic examples

### 3. CI/CD Gate
The `canary_check` should include portability validation in future versions.

## Exceptions

**ONLY** permitted in:
- User-specific `.env.local` files (never committed)
- Private configuration examples (explicitly marked as "EXAMPLE - CUSTOMIZE")
- Git-ignored files (`.gitignore` protected)

---

> [!IMPORTANT]
> **Portability = Accessibility**. Every hardcoded path is a barrier to entry for new contributors and users. The template must work seamlessly for everyone, everywhere.
