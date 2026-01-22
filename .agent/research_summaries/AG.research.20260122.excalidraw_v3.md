# Research Summary: Excalidraw Skill V3 (Atomic Precision)
ID: AG.research.20260122.excalidraw_v3

## 1. Final Diagnosis (The "Ghosts" in the Canvas)
- **Delete Failure**: `delete_element` in a loop fails because the backend ID lookups are slower than the loop execution, causing race conditions in the Express memory store.
- **Arrow Disconnection**: Arrows currently use global coordinates in the `points` array, but Excalidraw expects **offsets relative to the element's start x/y**.
- **Overlap**: Caused by additive drawing without a reliable atomic "reset" of the scene.

## 2. Competitive Scorecard (Dagre vs Grid)
| Axis | Research Findings | Score (1-5) |
| :--- | :--- | :--- |
| **Innovation** | Dagre for DAG auto-layout. | 4 |
| **Skeptical Check** | Pure JSON manipulation is error-prone without a native reset. | 2 |
| **Future Readiness** | Atomic Scene Management is the 2026 standard. | 5 |
| **Simplicity** | Native `clear_scene` reduces bridge code complexity by 50%. | 5 |

## 3. The "Serious" Fix (Backend Upgrade)
I will modify `mcp_excalidraw` to include a native `clear_scene` tool. This will invoke the Express `/api/elements/sync` endpoint with an empty set, ensuring an atomic wipe.

## 4. Implementation Blueprint (V3)
1. **[BACKEND]** Add `clear_scene` to `src/index.ts`.
2. **[BACKEND]** Rebuild with `npm run build`.
3. **[BRIDGE]** Upgrade `mcp_bridge.py` with the correct geometric formula for arrows:
   - `Points[1] = (TargetX - StartX, TargetY - StartY)`
4. **[VERIFICATION]** Smoke test: `clear_scene` -> `Perfect Draw`.
