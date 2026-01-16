---
description: "The Tech Explorer: Deep Discovery, Multi-Axis R&D (Gemini-Level), and Unbiased Benchmarking."
---

1) The Divergence Gate (Frontier R&D)
- **Goal**: Research technologies or strategies that are NOT yet in the project.
- **Strategic Pivot**: Consult `docs_custom/product_strategy.md` (Roadmap) to identify the next big hurdle.
- **Objective**: Discovery, Competitive Analysis, or Future-Proofing.

2) Recursive Deep Search Loop (The Gemini-Cycle)
- **Phase A: Query Expansion (Divergence)**
  - Generate 5 parallel research axes (MANDATORY):
    1. **Official**: Docs and Changelogs (The "How").
    2. **Skeptical**: "Why [X] sucks", "Major issues", "Silent failures" (The "Antidote").
    3. **Comparative**: Benchmark against 3 modern competitors (The "Market").
    4. **Legacy/Migration**: Difficulty of integration vs current stack (The "Cost").
    5. **Future (2026+)**: Roadmap and "The Next Big Thing" (The "Vision").
- **Phase B: Massive Ingestion (Automated)**
  - **Tool**: Execute `uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE_DIVERGENT.md`

3) Ephemeral Sandbox (The "Burner" Proof of Concept)
- **Action**: Test the technology in total isolation.
- **Rule**: Create scripts ONLY in `verifiche_test/RND_<slug>.py`.
- **Constraint**: Do not access the main project logic (mock it if needed).
- **Cleanup**: Delete the Sandbox script immediately after capturing the log.

4) Competitive Scorecard (The Impact-Discovery Matrix)
Produce a mandatory comparison for the new discovery:

| Axis | Research Findings | Score (1-5) |
| :--- | :--- | :--- |
| **Innovation** | How disruptive is it? | 1-5 |
| **Skeptical Check** | How many "Red Flags" found? | 1-5 |
| **Future Readiness** | Is it still the standard in 2026? | 1-5 |
| **Simplicity** | Does it reduce code by > 30%? | 1-5 |

5) Persistence & Strategic ID
- **Research Summary**: Save to `.agent/research_summaries/` (ID: `<Prefix>.deep_rag.YYYYMMDD.<slug>`).
- **Metadata**: `project=<ProjectName>, type=tech_discovery, status=frontier_scout`.

6) Final Output (The Discovery Pitch)
- Discovery Synthesis + Multi-Axis Scorecard.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
