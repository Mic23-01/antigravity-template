# Research Summary: Excalidraw Skill Refinement
ID: AG.research.20260122.excalidraw_v2

## 1. Problem Diagnosis
- **Persistence Error**: PM2 failed because the target `dist/index.js` was missing in the `Progetti` path. The actual build is in `~/mcp_excalidraw/dist`.
- **Drawing Quality**: 
    - Remnants: No "Clear Canvas" tool exists in the MCP server.
    - Layout: Hardcoded coordinates lead to overlaps (Z-axis and Spatial).
    - Refresh: Excalidraw's state is additive; refresh doesn't clear the server-side memory.

## 2. Capability Audit (mcp-excalidraw)
- **Get Scene**: `get_resource('elements')` works and returns IDs.
- **Cleanup**: Sequential `delete_element` calls are required since no batch delete is implemented.
- **Conversion**: `create_from_mermaid` works but the layout is handled by the frontend.

## 3. Proposed Improvements
A) **PM2 Systemd Fix**: Provide the correct absolute path and the `sudo pm2 startup` confirmation.
B) **Bridge Upgrade**: Add `clear_canvas()` and `smart_batch_create()` to `mcp_bridge.py`.
C) **Layout Logic**: Implement a "Flow Layout" algorithm in the bridge to automatically offset elements based on their width/height.

## 4. Implementation Blueprint
1. **Fix PM2**: Redirect user to `~/mcp_excalidraw`.
2. **Upgrade Bridge**: Add scene inspection and automated cleanup.
3. **Template Examples**: Add a "Clean Scene" pattern to the skill.

## 5. Persistence Metadata
- **Project**: Antigravity
- **Type**: architecture_fix
- **Status**: ready_to_implement
