---
id: E13_triad_feature
type: capability_eval
version: 1.0.0
---

# E13: The Feature Challenge (Product Alignment)

**Obiettivo**: Misurare la capacità dell'agente di implementare una feature rispettando i vincoli di dominio e architetturali.

**Scenario**:
- File di input: `.agent/evals/triad/feature_challenge.py`
- Contenuto: Un servizio API Skeleton `UserService`.
- Task: Implementare il metodo `anonymize_user(user_id)` secondo GDPR.

**Aspettativa**:
1.  Il metodo deve mascherare email e nome.
2.  Deve loggare l'operazione con format JSON strutturato (come da `domain_language.md`).
3.  I test di integrazione (`tests/test_feature.py`) devono passare.

**Comando di validazione**:
`python3 .agent/evals/runner.py --id E13`
