---
description: "R&D Agent 2026: Deep Research with Recursive Loop (Gemini-Level), Negative Analysis (Skeptical), and Impact Scorecard."
---

1) Context & Deep Mapping (The Network)
- **External Mapping**: Use `context7` to understand target libraries and their modern alternatives.
- **Internal Mapping**: Use `grep_search` or `duckdb` (via `.agent/project/librarian.py --audit`) to map the structural impact on local dependencies.
- **Goal**: Understand not just "what" the technology does, but "where" it will touch the project.

2) Recursive Deep Search Loop (The Gemini-Cycle)
- **Phase A: Query Expansion (Divergence)**
  - Generate 5 parallel research axes:
    1. **Official**: Docs and Changelogs.
    2. **Skeptical**: "Why [X] sucks", "Performance issues", "Alternatives".
    3. **Comparative**: Benchmark vs Competitor Y.
    4. **Migration**: "Migration from [Current] to [X]", "Breaking changes".
    5. **Future**: "Roadmap 2026", "Deprecation warnings".
- **Phase B: Massive Ingestion (Automated)**
  - **Action**: Collect the best 3-5 URLs per axis.
  - **Tool**: Execute `uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE.md`
  - **Read**: Read ONLY `RESEARCH_BUNDLE.md` (Save tokens and time).
- **Phase C: Reflection & Convergence**
  - Use `sequential-thinking` to ask yourself: "Do the sources agree?".
  - If there is conflict or a gap, launch a targeted Recursive Loop.

3) Ephemeral Sandbox (The PoC)
- **Golden Rule**: Use `uv run --with <libs>` to use top-tier libraries without polluting the environment.
- **ANTI-RULE-0005**: 
    - Create scripts in `verifiche_test/RND_<slug>.py`.
    - Execute and capture quantitative output.
    - **DELETE IMMEDIATELY**: `rm verifiche_test/RND_<slug>.py`.
    - **DOUBLE CHECK**: Run `ls` to confirm workspace cleanliness.

4) Impact Analysis (The Scorecard)
- Produce a mandatory impact table for every research task:

| Metric | Rating (1-5) | Impact Description |
| :--- | :--- | :--- |
| **Simplification** | 1-5 | How much code/complexity does it remove? |
| **Performance** | 1-5 | Impact on speed/memory. |
| **Blast Radius** | 1-5 | How many files does it touch? (1=Few, 5=All) |
| **Canon Compliance** | Yes/No | Does it respect project standards? |
| **Depth of Field** | N Sources | Total number of unique sources consulted. |

5) Persistence & Decision
- **Research Summary**: Save to `.agent/research_summaries/` (ID: `<Prefix>.deep_rag.YYYYMMDD.<slug>`).
- **Chroma**: Persist with tag `type=deep_search`.
- **Conditional ADR**: If Simplification > 4 and Risk < 3, propose adoption directly.

6) Final Output
- Explicitly include: "Processed X sources on 5 axes (Recursive Deep Search)".
- Completed Scorecard.
- Link to Summary.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
