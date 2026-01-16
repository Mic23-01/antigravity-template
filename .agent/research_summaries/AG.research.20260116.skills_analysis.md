# Research: Antigravity Skills Deep Analysis
**ID**: AG.research.20260116.skills_analysis
**Status**: Complete
**Type**: Architectural Documentation
**Project**: Antigravity

---

## SKILLS_INDEX.md

### Cosa Fa
Il catalogo centrale di tutte le skill disponibili. Mappa nome, descrizione e workflow trigger per ogni skill.

### Funziona?
**SÌ**. Elenca 6 skill base operative.

### Fondamentale?
**MEDIO**: È documentazione. Non è eseguibile, ma serve come "mappa" per l'Agente per sapere quali skill esistono.

### Callers
- Nessuno (è una reference doc).

### Lancio Manuale?
**NO**: È solo un file markdown da leggere.

### Enhancement
- **Auto-Validation**: Script che verifica che tutte le skill elencate esistano effettivamente come cartelle.
- **Coverage Metrics**: Aggiungere `last_used` timestamp per vedere quali skill sono morte.

---

## 1. fixlog_writer

### Cosa Fa
Standardizza la scrittura dei **FixLog** (memoria delle modifiche). Scrive in **Dual Persistence**:
- Filesystem: `.agent/fix_logs/<ID>.json`
- ChromaDB: Collection `fix_logs`

### Funziona?
**SÌ**. Lo abbiamo appena usato: `AG.fix.20260116.b9b17ed4`.

### Fondamentale?
**CRITICO**. Senza questa skill:
- Il Session Sentinel blocca tutto (Dirty Session).
- Non c'è tracciabilità delle modifiche.
- ChromaDB non può fare semantic search su interventi passati.

### Callers
- **Workflow**: `tech_rag` (Step 6 Persistence), `refactor`.
- **Script**: `.agent/skills/fixlog_writer/scripts/write_log.py`

### Lancio Manuale?
**NO** (orchestrato dai workflow). L'Agente lo chiama automaticamente via `uv run`.

### Best Practice
- **Always Persist**: Non saltare mai questo step.
- **Descriptive**: Usa `--desc` dettagliato (chi legge fra 3 mesi deve capire cosa hai fatto).

### Enhancement
1. **Auto-Enrichment**: Leggere automaticamente `git diff --stat` per popolare `--files`.
2. **LLM Summarization**: Se `--desc` è troppo lungo, compattalo via LLM prima di salvare.
3. **Evidence Link**: Auto-attach screenshot/video path se presente nel workflow.
4. **Batch Mode**: Supportare più FixLog in un singolo comando (utile per refactoring massivi).

---

## 2. regression_gate

### Cosa Fa
Il **Guardiano della Qualità**. Wrapper unificato che esegue:
1. **Chroma Check**: Verifica che il FixLog in ChromaDB sia valido (metadata corretti).
2. **Librarian Audit**: Scansiona `.agent/fix_logs/` per ghost files o duplicati.

### Funziona?
**SÌ**. Canary lo esegue implicitamente.

### Fondamentale?
**CRITICO**. Previene:
- Metadata rotti in Chroma (es. `files` come stringa invece di lista).
- Ghost logs (file nel filesystem ma non in Chroma).
- Regression silenziose (log di "pass" falsi).

### Callers
- **Workflow**: `tech_rag` (Step 7 Post-check), `refactor`.
- **Script**: `.agent/skills/regression_gate/scripts/run_audit.py`

### Lancio Manuale?
**AUTOMATICO** nei workflow. Manuale solo per debug (`python3 .agent/skills/regression_gate/scripts/run_audit.py --collection fix_logs --id <ID>`).

### Best Practice
- **Fail-Fast**: Se fallisce, STOP. Non procedere.
- **Read Examples**: Consulta `.agent/skills/regression_gate/examples/correct_metadata.md`.

### Enhancement
1. **Auto-Fix**: Se rileva metadata rotti, propone un comando di fix automatico.
2. **Diff View**: Mostra cosa è cambiato rispetto all'ultimo audit.
3. **Webhook Notify**: Integrazione Slack/Discord per alert su fallimenti.
4. **Temporal Check**: Verifica che il `date` nel metadata corrisponda al timestamp del file.

---

## 3. resolve_canon_sources

### Cosa Fa
Risolve la **gerarchia delle fonti** (Source of Truth):
- **Custom** (`docs_custom/SOURCES.md`) > **Template** (`.agent/docs/SOURCES.md`).

Determina quale file leggere e se attivare `markdownify` per deep reading.

### Funziona?
**SÌ**. È logica Python (non testata qui, ma usata implicitamente).

### Fondamentale?
**ALTO**. Senza questo:
- L'Agente non sa dove cercare le Gold Sources.
- Potrebbe usare template stantii invece di custom aggiornati.

### Callers
- **Workflow**: `tech_rag` (Step 0), `research_rag` (Step 0), `refactor` (Step 0).

### Lancio Manuale?
**NO**: È una decisione di routing, non uno script standalone.

### Best Practice
- **Hydrate Custom**: Dopo `/custom_project`, verifica sempre che `docs_custom/SOURCES.md` esista.

### Enhancement
1. **Versioning**: Supportare `docs_custom/SOURCES_v2.md` per A/B testing.
2. **Merge Strategy**: Se Custom è parziale, fare merge con Template (non override totale).
3. **Cache**: Dopo la prima risoluzione, cachare il risultato in `STATE.md` per evitare I/O ripetuto.
4. **Visual Diff**: Tool CLI che mostra differenze tra Custom e Template sources.

---

## 4. security_audit

### Cosa Fa
Audit di sicurezza statico:
1. **Secret Scanning**: Cerca pattern Regex (AWS Keys, GitHub Tokens, etc).
2. **Risky Files**: Identifica `.exe`, `.p12`, `.key`, file > 50MB.
3. **Dependency Check**: `uv pip check` per verificare coerenza ambiente Python.

### Funziona?
**NON TESTATO** in questa sessione.

### Fondamentale?
**ALTO** (Security). Previene:
- Leak di credenziali su GitHub.
- Deployment di malware accidentale.
- Dependency hell.

### Callers
- **Workflow**: `tech_rag` (opzionale, Pre-Commit).
- **Manual**: On-demand "Verifica sicurezza".

### Lancio Manuale?
**SÌ**: `python3 .agent/skills/security_audit/scripts/audit_runner.py`.

### Best Practice
- **Pre-Commit Hook**: Integrare in `.git/hooks/pre-commit`.
- **CI/CD**: Eseguire nel pipeline GitHub Actions.

### Enhancement
1. **SAST Integration**: Collegare a Semgrep o Bandit per analisi statica avanzata.
2. **License Check**: Verificare licenze delle dipendenze (GPL vs MIT).
3. **CVE Database**: Query a NVD per vulnerabilità note nelle dipendenze.
4. **Auto-Ignore**: File `.securityignore` per whitelist falsi positivi.
5. **JSON Report**: Output strutturato per SIEM/Dashboarding.

---

## 5. test_gate_bivio

### Cosa Fa
Gestisce l'**interazione di testing** chiedendo all'utente il livello:
- **Easy/Smoke**: `<SmokeTestCmd>` (rapido, es. `ls -la docs_custom/`).
- **Deep**: `<DeepTestCmd>` + negative markers (es. `pytest -m "negative or fuzz"`).
- **Debug**: `<DebugTestCmd>` con `--pdb` per debugging interattivo.

### Funziona?
**SÌ** (logica, non testato interattivamente qui).

### Fondamentale?
**ALTO**. Implementa il **"Zero Silence for Ghost Failures"**:
- Forza l'Agente a chiedere prima di testare.
- Previene test superficiali ("ci gira" != "funziona").

### Callers
- **Workflow**: `tech_rag` (Step 5 Test Gate).

### Lancio Manuale?
**NO** (è un interrupt interattivo).

### Best Practice
- **Config**: Popolare `.agent/project/PROJECT_AGENT_CONFIG.md` con comandi test validi.

### Enhancement
1. **Smart Detection**: Se rileva `pytest.ini`, propone automaticamente "Deep" invece di chiedere.
2. **Parallel Execution**: Eseguire Smoke + Deep in parallelo e mostrare diff dei risultati.
3. **Coverage Integration**: Dopo "Deep", mostrare coverage % e suggerire aree scoperte.
4. **Mutation Testing**: Step "Ultra Deep" con `mutmut` per rilevare test deboli.

---

## 6. ui_ux_designer

### Cosa Fa
**AI Design Lead**. Accesso a database di:
- **Colors**: Palette (Hex codes).
- **Typography**: Font families.
- **Styles**: Layout patterns, Landing page examples.

Previene invenzioni casuali ("Non inventare `#123456`").

### Funziona?
**SÌ** (testato in Canary: vedi scenario `002_ui_ux_link.md`).

### Fondamentale?
**MEDIO-ALTO** (UI Projects). Garantisce:
- Coerenza estetica (Design System).
- Professionalità (no colori casuali).

### Callers
- **Workflow**: `tech_rag` (UI/Frontend context), `custom_project` (Brand Hydration).

### Lancio Manuale?
**SÌ**: `python3 .agent/skills/ui_ux_designer/scripts/search_design.py --query "Fintech Crypto" --type colors`.

### Best Practice
- **Search First**: Sempre cercare nel DB prima di proporre stili.
- **Fallback**: Se DB è vuoto, documentarlo in `brand_identity_guide.md`.

### Enhancement
1. **Generative Palette**: Se la query non trova risultati, generare palette via AI (es. Gemini Flash Vision da immagine di riferimento).
2. **A11y Validation**: Verificare contrasto WCAG AAA prima di proporre colori.
3. **Component Library**: Database di componenti React/Vue preconfigurati (es. "Button Primary").
4. **Figma Integration**: Export automatico da Figma Design Tokens.
5. **Trend Analysis**: Suggerire stili basati su trend 2026 (via web scraping).

---

## Summary Table: Caller Matrix

| Skill | tech_rag | research_rag | refactor | custom_project | Manual |
|-------|----------|--------------|----------|----------------|--------|
| fixlog_writer | ✅ Step 6 | ❌ | ✅ | ❌ | ❌ |
| regression_gate | ✅ Step 7 | ❌ | ✅ | ❌ | ✅ Debug |
| resolve_canon_sources | ✅ Step 0 | ✅ Step 0 | ✅ Step 0 | ❌ | ❌ |
| security_audit | 🟡 Optional | ❌ | 🟡 Optional | ❌ | ✅ Pre-Commit |
| test_gate_bivio | ✅ Step 5 | ❌ | ❌ | ❌ | ❌ |
| ui_ux_designer | 🟡 UI Context | ❌ | ❌ | ✅ Brand | ✅ Design |

---

## Top 3 Cross-Skill Enhancements

### 1. Unified CLI (`antigravity.py`)
Invece di comandi sparsi, un singolo entry point:
```bash
python3 .agent/antigravity.py skill <skill_name> <args>
```

### 2. Skill Chaining
Automatizzare pipeline comuni:
```bash
python3 .agent/antigravity.py chain fixlog regression_gate
```

### 3. Telemetry Integration
Ogni skill emette eventi via `event_logger.py`:
- `SKILL_START`, `SKILL_PASS`, `SKILL_FAIL`.
- Queryable in DuckDB per analytics.

---

**FILESYSTEM UPDATES**:
- NEW: `.agent/research_summaries/AG.research.20260116.skills_analysis.md`
