# Research Summary: AG_BRAIN_DIR Default Path Presentation

**ID**: AG.research.20260122.brain_dir_defaults  
**Project**: Antigravity  
**Type**: architect_research  
**Status**: validation_complete  

---

## 1. Objective

Verify if `AG_BRAIN_DIR` default path (`~/.gemini/antigravity/brain`) is properly presented as a "recommended default" rather than an opinionated requirement, ensuring cross-platform portability.

## 2. Current Implementation Analysis

### 2.1 README.md Documentation

**Location**: Line 78  
**Presentation**: 
```markdown
> [!TIP]
> **Custom Brain Path**: Set `AG_BRAIN_DIR` environment variable to override 
> the default brain location (`~/.gemini/antigravity/brain`). 
> This is useful for custom deployments or CI environments.
```

**Analysis**:
- ✅ Uses `[!TIP]` alert (not `[!IMPORTANT]` or `[!CAUTION]`)
- ✅ Explicitly says "override the **default**"
- ✅ Provides use cases ("custom deployments or CI")
- ✅ Non-prescriptive tone

### 2.2 canary_check.py Implementation

**Location**: Lines 302-310  
**Strategy**:
```python
# Brain Directory Resolution Strategy:
# 1. Primary: AG_BRAIN_DIR environment variable (explicit override)
# 2. Default: ~/.gemini/antigravity/brain (standard location)
# 3. Fallback: CWD walkthrough.md (for standalone/local testing)

brain_dir_env = os.getenv("AG_BRAIN_DIR")
if brain_dir_env:
    brain_dir = Path(brain_dir_env)
else:
    brain_dir = Path.home() / ".gemini/antigravity/brain"
```

**Analysis**:
- ✅ **Explicit comments** documenting the resolution hierarchy
- ✅ **Three-tier fallback**: env var → default → CWD
- ✅ Uses `Path.home()` (cross-platform Python standard)
- ✅ Default is described as "standard location" (not "required")

## 3. Cross-Platform Portability Check

| OS | `Path.home()` | Default Expansion | Status |
|---|---|---|---|
| **Linux** | `/home/<user>` | `~/.gemini/...` | ✅ Works |
| **macOS** | `/Users/<user>` | `~/.gemini/...` | ✅ Works |
| **Windows** | `C:\Users\<user>` | `~\.gemini\...` | ✅ Works (Python handles `\` conversion) |

**Conclusion**: The use of `Path.home()` + relative subdir is **universally portable**.

## 4. Potential Improvements (Optional)

### 4.1 Enhanced README Clarity

**Current**: "This is useful for custom deployments or CI environments."  
**Suggested Enhancement**:
```markdown
> [!TIP]
> **Custom Brain Path**: Set `AG_BRAIN_DIR` environment variable to override 
> the default brain location (`~/.gemini/antigravity/brain`). 
>
> **Common use cases**:
> - Custom deployments (e.g., `/opt/antigravity/brain`)
> - CI environments (e.g., `$RUNNER_TEMP/brain`)
> - Multi-user servers (e.g., `/srv/antigravity/agents/<user>/brain`)
```

### 4.2 Windows-Specific Example (Optional)

Add a Windows example to make it even more explicit:
```markdown
**Examples**:
- Linux/Mac: `export AG_BRAIN_DIR="$HOME/custom/brain"`
- Windows: `$env:AG_BRAIN_DIR="$HOME\custom\brain"`
```

## 5. Verdict

**CURRENT IMPLEMENTATION: ✅ ALREADY CORRECT**

The template already follows best practices:
1. ✅ Default is presented as **recommended**, not mandatory
2. ✅ Environment variable override is **clearly documented**
3. ✅ Code uses **cross-platform** Python primitives
4. ✅ Fallback strategy is **explicitly commented** in code

**No changes required**. Optional enhancements above are cosmetic improvements only.

## 6. Structural Impact

**Files Analyzed**:
- `README.md` (Line 78)
- `.agent/tools/canary_check.py` (Lines 302-310)

**Recommendation**: MAINTAIN current approach. Optionally enhance README with additional use-case examples.
