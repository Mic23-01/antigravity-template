# Domain Language (Ubiquitous Language): <PROJECT_NAME>

> **AI Instruction**: 
> 1. **Analyze**: Scan `src/types`, `models/`, and DB schema to identify core Entities (e.g., `User`, `Cart`, `Spell`).
> 2. **Draft**: Fill the "Technical Definition" column based on code usage.
> 3. **Ask**: Request the User to provide the "Business Definition" and "Constraints".
> *Goal*: Create a binding glossary to prevent semantic hallucinations.

## 1. Core Entities (Nouns)
| Term | Business Definition (User) | Technical Definition (AI) | Constraints / Invariants |
| :--- | :--- | :--- | :--- |
| **<ENTITY_NAME>** | <BUSINESS_MEANING> | `Models.<CLASS_NAME>` | <RULES> (e.g., must have email) |
| ... | ... | ... | ... |

## 2. Key Processes (Verbs)
| Action | Input | Output | Important Side Effects |
| :--- | :--- | :--- | :--- |
| **<ACTION_NAME>** | <DATA_IN> | <DATA_OUT> | <DATABASE_CHANGES>, <NOTIFICATIONS> |
| ... | ... | ... | ... |

## 3. Ambiguities & Anti-patterns
> Terms we should NOT use or that create confusion.
- **"<AMBIGUOUS_TERM>"**: Do not use. Use **"<PREFERRED_TERM>"** instead.
