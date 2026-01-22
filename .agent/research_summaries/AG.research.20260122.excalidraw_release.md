# Research Summary: Antigravity Excalidraw Release Strategy

**ID**: AG.research.20260122.excalidraw_release  
**Project**: Antigravity  
**Type**: architect_research  
**Status**: ready_to_implement  

---

## 1. Objective

Analyze feasibility of creating a new Antigravity release with the `excalidraw_canvas` skill as an "opt-in" enhancement.

## 2. Findings

### 2.1 Current State

| Artifact | Status | Location |
|----------|--------|----------|
| Excalidraw Skill | Complete (v1.0.0) | `.agent/skills/excalidraw_canvas/` |
| MCP Bridge | Working, hardcoded path | `scripts/mcp_bridge.py` |
| MCP Server | External dependency | `/home/ubuntu/Progetti/IDE_Sviluppo/mcp_excalidraw/` |
| Visual Calibration | Empirically validated | Zenith V5, strokeWidth=2 |
| Fix Logs | 10 uncommitted | `.agent/fix_logs/AG.fix.20260122.*` |

### 2.2 Critical Dependency

The `mcp_bridge.py` script contains:
```python
mcp_path = "/home/ubuntu/Progetti/IDE_Sviluppo/mcp_excalidraw/dist/index.js"
```

This **must** be made configurable via `EXCALIDRAW_MCP_PATH` environment variable for end-user portability.

### 2.3 User Setup Requirements

For v3.0.0 users who want Excalidraw:
1. Clone `mcp_excalidraw` repository
2. Run `npm install && npm run build`
3. Set `EXCALIDRAW_MCP_PATH` environment variable
4. Start Express Canvas server on Port 3000

## 3. Structural Impact

### Files to Modify
- `mcp_bridge.py` → Add env var support
- `SKILL.md` → Document prerequisites
- `README.md` → Add Excalidraw section

### Integration Points
- No impact on existing skills/workflows
- Excalidraw is isolated in its own skill folder
- MCP server is completely external (not bundled)

## 4. Recommendation

**PROCEED** with dual-release strategy:
- Tag current `main` as `v2.0.1` (stable, no Excalidraw in skill docs)
- Commit all pending work + portability fix
- Tag as `v3.0.0-beta` (with Excalidraw experimental)

This preserves backward compatibility while offering cutting-edge visual capabilities for power users.
