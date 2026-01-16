# Agentic Setup Playbook (Antigravity) — Project Bootstrap

## Purpose
Install a replicable agentic system in the current project:
- Workflows: /tech_rag, /research_rag, /decision_rag (adaptive)
- Evals: checker + canary IDs + runner run_checks.sh
- Chroma: collections + standard metadata
- Safety: no .env* leakage + mandatory regression gate

## Operational Rules (MANDATORY)
- Do not read/print `.env*`, `mcp_secrets.env`, `~/.ssh` or secrets.
- Small, verifiable changes.
- After each Chroma persistence: immediately run `check_chroma.py` (Regression Gate).
- If a new failure class emerges: propose a new eval case (do not write without approval).

---

# Step 0 — Project Parameters (Fill in)
Set these values (e.g., in a temporary file or environment variables):
- PROJECT_NAME = "<PROJECT_NAME>"        (e.g., DeD)
- PROJECT_PREFIX = "<prefix>"          (e.g., ded)
- SMOKE_TEST_CMD = "<command>"           (e.g., pytest -q | npm test | pnpm test | etc.)
- CHROMA_DATA_DIR = "$HOME/chroma-data"

---

# Step 1 — Copy Baseline from Template
Execute from the root of the target project:

```bash
cp -a <template_path>/.agent .
```

Verify:
```bash
ls -la .agent
```

# Step 2 — Automatic Adaptation (Prefix & Metadata)

> [!NOTE]
> Baseline workflows are now **dynamic**: they use `<ProjectName>` as a placeholder that the agent resolves by reading the project root. The `sed` substitution is mainly for canary prefix and scripts.

Execute (ensure `PROJECT_NAME` and `PROJECT_PREFIX` are set):

```bash
# Canary prefix substitution (bt. -> specific prefix)
find .agent -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" \) -print0 \
| xargs -0 sed -i \
  -e "s/bt\./${PROJECT_PREFIX}./g" \
  -e "s/BT-/${PROJECT_PREFIX^^}-/g"

# If you want to 'lock' the project name (optional, recommended if there's no clear PROJECT_OVERVIEW.md):
# find .agent -type f -name "*.md" -print0 | xargs -0 sed -i "s/<ProjectName>/${PROJECT_NAME}/g"
```

# Step 3 — Set Smoke Test for /tech_rag (project-specific)

Open:
`.agent/workflows/tech_rag.md`

Update the "Test Gate" section including the specific command:
`Default Smoke cmd: ${SMOKE_TEST_CMD}`

# Step 4 — Canary IDs (stable)

Update `.agent/evals/run_checks.sh` to verify new IDs:
- collection: `fix_logs`, id: `${PROJECT_PREFIX}.fix.eval.metadata_gate`
- collection: `research_summaries`, id: `${PROJECT_PREFIX}.research.eval.metadata_gate`

# Step 5 — Initialize Canary (one-time only)

In Antigravity, execute:
1. `/tech_rag CANARY micro-run` (e.g., update README) -> verify auto-save on stable ID.
2. `/research_rag CANARY micro-run` -> verify auto-save on stable ID.
3. Run `./.agent/evals/run_checks.sh`.

# Step 6 — Chroma Conventions (MANDATORY)

Same collections and standard metadata (project, type, date, etc.) as in the original Playbook.

---

## How to Use in Practice
1) Copy this file to the target project.
2) In Antigravity write:
> "Execute AGENT_SETUP_PLAYBOOK.md for this project. Name: DeD, Prefix: ded, Smoke: npm test."

---

## Project Hydration: Template → Custom

**Question**: When I copy `.agent/` to a new project, how do I transform it from a generic template to a **project-specific** system?

**Answer**: Use the **`/custom_project` workflow**:

1. **Automatic Discovery**: The agent reads your `package.json`, `pyproject.toml`, repo structure, and deduces:
   - Stack (React/Next/Django/etc)
   - Project name
   - Existing color palette (if `tailwind.config.js` or CSS variables exist)

2. **Gap Analysis**: The agent compares template placeholders in `.agent/docs/` against what it found and asks you targeted questions:
   - "What is the 12-month Vision?"
   - "Define the term 'Player' in your domain language"
   - "What are your Gold Sources (official docs URLs)?"

3. **Hydration Engine**: Once you answer, the agent generates a `manifest.json` and executes:
   ```bash
   python3 .agent/tools/init_antigravity.py --manifest manifest.json
   ```
   This populates `docs_custom/` with:
   - `architecture.md`
   - `brand_identity_guide.md`
   - `domain_language.md`
   - `product_strategy.md`
   - `SOURCES.md`

4. **Binding**: After review/approval, these files become your **Custom Source of Truth**. The agent now uses `docs_custom/` (via `resolve_canon_sources` skill) instead of `.agent/docs/` templates.

---

## Key Mechanism: Custom > Template Hierarchy

- **Before Hydration**: Agent reads `.agent/docs/` (generic templates).
- **After Hydration**: Agent reads `docs_custom/` (your project-specific docs).
- **Enforcement**: The `resolve_canon_sources` skill ensures this priority automatically.

**Next Steps After Copy**:
```bash
# Option A: Fully Automated
/custom_project

# Option B: Manual (if you prefer control)
1. Manually edit PROJECT_AGENT_CONFIG.md (set ProjectName, Prefix)
2. Manually create docs_custom/ files
3. Run canary to verify
```
