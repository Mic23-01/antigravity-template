---
name: UI/UX Brain-Link Verification
description: Verifica che l'agente usi attivamente la skill ui_ux_designer per decisioni estetiche.
target_file: docs_custom/brand_identity_guide.md
task: "Definisci la palette colori per un prodotto 'Fintech Crypto' usando i dati ufficiali della skill."
assertions:
  - type: file_exists
    path: docs_custom/brand_identity_guide.md
  - type: file_content_contains
    path: docs_custom/brand_identity_guide.md
    pattern: "#F59E0B" # Hex code specifico per Fintech/Crypto nel database
  - type: file_content_contains
    path: docs_custom/brand_identity_guide.md
    pattern: "#8B5CF6" # Altro hex code fintech
---
