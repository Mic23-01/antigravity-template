# Research Summary: Codebase Quality & Bug Hunt Analysis

> **ID**: AG.research.20260115.bug_hunt_analysis
> **Type**: Technical Audit
> **Scope**: `canary_check.py`, `check_chroma.py`
> **Severity**: HIGH (False Positives in CI/CD)

## 1. Analisi Segnalazioni Utente (Confermate)

### 1.1 Hardcoded Environment Path (`canary_check.py`)
- **Location**: Riga 123
- **Codice**: `brain_dir = Path("/home/ubuntu/.gemini/antigravity/brain")`
- **Problema**: Lega l'esecuzione all'utente `ubuntu` e alla cartella `.gemini`. Se l'agente gira su un container Docker diverso o su Mac, fallisce silenziosamente (`return None`).
- **Impatto**: **Medium/High**. Riduce la portabilità del template.

### 1.2 "Success Masking" Logic Bug (`canary_check.py`)
- **Location**: Riga 333 (Reset)
- **Codice**:
    ```python
    309: success &= check_walkthrough_evidence(...) # Triad/Evidence sets success
    ...
    333: success = True # RESET!
    ```
- **Problema**: La variabile `success` viene sovrascritta a `True` prima di eseguire i check statici finali (Config, Workflow, Script).
- **Impatto**: **CRITICO**.
    - Se la **Triad Eval** fallisce (Riga 301 `success = False`).
    - O se il **Walkthrough Evidence** fallisce (Riga 166-170).
    - La variabile viene resettata a `True` alla riga 333.
    - Il sistema finale riporta `SYSTEM STATUS: 100% OPERATIONAL` (Line 355) anche se la Triad o le Evidence sono fallite (mascherando il fail).

---

## 2. Altri Casi Identificati (Deep Search)

### 2.1 `check_chroma.py`
- **Location**: Riga 14
- **Codice**: `ap.add_argument("--data-dir", default="/home/ubuntu/chroma-data")`
- **Problema**: Hardcoded default path. Se lanciato senza argomenti su un altro environment, fallisce o crea directory spurie.
- **Suggerimento**: Usare variabili d'ambiente o percorsi relativi.

### 2.2 `event_logger.py` (Potenziale)
- **Analisi**: Usa percorsi relativi (`.agent/audit`). È compliant ("Good Design").

---

## 3. Conclusioni
L'analisi conferma che l'attuale impianto di validazione (`canary_check.py`) è inaffidabile per i check dinamici (Eval/Triad/Walkthrough) a causa del reset della variabile `success`. Questo crea un **False Sense of Security**.

### Raccomandazioni (Boss Level)
1.  **Refactoring Immediato di `canary_check.py`**:
    *   Rimuovere il reset `success = True` alla riga 333.
    *   Usare un accumulatore unico (diciamo `compliance_score`) o non resettare `success`.
2.  **Environment Variables**:
    *   Sostituire `/home/ubuntu` con `os.path.expanduser("~")` o `os.environ.get("AG_HOME")`.
