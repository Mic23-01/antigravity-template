# Research Summary: Portability & Hardcoded Paths Policy

**ID**: AG.research.20260122.portability_policy  
**Project**: Antigravity  
**Type**: architect_research  
**Status**: gap_identified  

---

## 1. Objective

Verify if Antigravity template has an explicit policy against hardcoded paths (OS/user-specific) to ensure portability across different environments.

## 2. Findings

### 2.1 Current State

| Location | Hardcoded/Portability Mentions | Status |
|----------|-------------------------------|--------|
| **Rules** (5 files) | 1 indirect (Docker volume mapping) | ❌ No dedicated policy |
| **Workflows** (5+ files) | 0 mentions | ❌ No enforcement |
| **Skills** (7 skills) | 1 (security_audit detects secrets) | ⚠️ Partial |

### 2.2 Gap Identified

**CRITICAL GAP**: No explicit rule forbids or warns against:
- Hardcoded `/home/username/` paths
- OS-specific paths (`C:\Users\`, `/Users/`)
- Absolute paths in code/docs (except Docker context)
- User-specific environment assumptions

### 2.3 Recent Evidence

Today's work exposed this exact issue:
- `mcp_bridge.py` had: `/home/ubuntu/Progetti/IDE_Sviluppo/mcp_excalidraw/dist/index.js`
- `SKILL.md` had: `file:///home/ubuntu/...` links
- **Both needed manual fixes** to use env vars or relative paths

## 3. Proposed Solution

### New Rule: `portability-enforcement.md`

```markdown
---
trigger: always_on
description: Portability Enforcement (Anti-Hardcoded Paths)
---

# Portability Enforcement (ALWAYS ON)

## Purpose
Ensure the Antigravity template remains portable across different OS/users.

## PROHIBITED Patterns
The Agent **MUST NEVER** commit code/docs containing:
- Absolute user paths: `/home/<user>/`, `/Users/<user>/`, `C:\Users\<user>\`
- OS-specific hardcoded directories without env var fallback
- IDE/editor-specific absolute paths in examples

## REQUIRED Actions
1. **Use Environment Variables** for paths:
   ```python
   path = os.environ.get("VAR_NAME", os.path.expanduser("~/default"))
   ```
2. **Use Relative Paths** in documentation
3. **Use `~` or `$HOME`** when documenting setup

## Enforcement
- Security audit tool should flag patterns: `/home/`, `/Users/`, `C:\`
- Pre-commit check: grep for absolute paths in staged files
```

## 4. Structural Impact

### Files to Create
- **NEW**: `.agent/rules/portability-enforcement.md`

### Files to Modify
- `.agent/skills/security_audit/scripts/audit_runner.py` - Add hardcoded path detection

## 5. Implementation Blueprint

```bash
# Step 1: Create new rule
cat > .agent/rules/portability-enforcement.md << 'EOF'
[... content from above ...]
EOF

# Step 2: Enhance security_audit
# Add regex: r'(?:/home/|/Users/|C:\\Users\\)[\w/\\]+'

# Step 3: Verify with grep
grep -rn "/home/" .agent/ --exclude-dir=.git
```

## 6. Recommendation

**PROCEED** with creating dedicated portability rule to prevent future hardcoded path issues in template code.
