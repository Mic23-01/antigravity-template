# Agentic Setup Playbook (Antigravity) — Project Bootstrap

## Scopo
Installare nel progetto corrente un sistema agentico replicabile:
- Workflows: /tech_rag, /research_rag, /decision_rag (adattivi)
- Evals: checker + canary IDs + runner run_checks.sh
- Chroma: collezioni + metadata standard
- Safety: no .env* leakage + regression gate obbligatorio

## Regole operative (OBBLIGATORIE)
- Non leggere/stampare `.env*`, `mcp_secrets.env`, `~/.ssh` o segreti.
- Cambi piccoli e verificabili.
- Dopo ogni persistenza in Chroma: eseguire subito `check_chroma.py` (Regression Gate).
- Se emerge un nuovo failure class: proporre un nuovo eval case (non scriverlo senza OK).

---

# Step 0 — Parametri progetto (compilare)
Imposta questi valori (es. in un file temporaneo o variabili d'ambiente):
- PROJECT_NAME = "<NOME_PROGETTO>"        (es: DeD)
- PROJECT_PREFIX = "<prefisso>"          (es: ded)
- SMOKE_TEST_CMD = "<comando>"           (es: pytest -q | npm test | pnpm test | ecc.)
- CHROMA_DATA_DIR = "/home/ubuntu/chroma-data"

---

# Step 1 — Copia la baseline da BrainTracker
Da eseguire dalla root del progetto target:

```bash
cp -a /home/ubuntu/Progetti/Progetti_Approvati/BrainTracker/.agent .
```

Verifica:
```bash
ls -la .agent
```

# Step 2 — Adattamento automatico (Prefix & Metadata)

> [!NOTE]
> I workflow di baseline sono ora **dinamici**: usano `<ProjectName>` come placeholder che l'agente risolve leggendo la root del progetto. La sostituzione `sed` serve principalmente per il prefisso dei canary e degli script.

Esegui (assicurati che `PROJECT_NAME` e `PROJECT_PREFIX` siano impostati):

```bash
# Sostituzione prefisso canary (bt. -> prefisso specifico)
find .agent -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" \) -print0 \
| xargs -0 sed -i \
  -e "s/bt\./${PROJECT_PREFIX}./g" \
  -e "s/BT-/${PROJECT_PREFIX^^}-/g"

# Se vuoi 'fissare' il nome progetto (opzionale, consigliato se non c'è un PROJECT_OVERVIEW.md chiaro):
# find .agent -type f -name "*.md" -print0 | xargs -0 sed -i "s/<ProjectName>/${PROJECT_NAME}/g"
```

# Step 3 — Imposta Smoke Test per /tech_rag (progetto-specifico)

Apri:
`.agent/workflows/tech_rag.md`

Aggiorna la sezione "Test Gate" includendo il comando specifico:
`Default Smoke cmd: ${SMOKE_TEST_CMD}`

# Step 4 — Canary IDs (stabili)

Aggiorna `.agent/evals/run_checks.sh` affinché verifichi i nuovi ID:
- collection: `fix_logs`, id: `${PROJECT_PREFIX}.fix.eval.metadata_gate`
- collection: `research_summaries`, id: `${PROJECT_PREFIX}.research.eval.metadata_gate`

# Step 5 — Inizializza canary (1 volta sola)

In Antigravity, esegui:
1. `/tech_rag CANARY micro-run` (es. update README) -> verifica salvataggio auto su ID stabile.
2. `/research_rag CANARY micro-run` -> verifica salvataggio auto su ID stabile.
3. Esegui `./.agent/evals/run_checks.sh`.

# Step 6 — Convenzioni Chroma (OBBLIGATORIE)

Stesse collezioni e metadata standard (project, type, date, ecc.) come nel Playbook originale.

---

## Come lo usi in pratica
1) Copi questo file nel progetto target.
2) In Antigravity scrivi:
> "Esegui AGENT_SETUP_PLAYBOOK.md per questo progetto. Nome: DeD, Prefisso: ded, Smoke: npm test."
