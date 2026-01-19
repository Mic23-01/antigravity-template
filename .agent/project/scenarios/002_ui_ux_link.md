---
name: UI/UX Brain-Link Verification
description: Verifies that the agent actively uses the ui_ux_designer skill for aesthetic decisions.
target_file: docs_custom/brand_identity_guide.md
task: "Define the color palette for a 'Fintech Crypto' product using official data from the skill."
assertions:
  - type: file_exists
    path: docs_custom/brand_identity_guide.md
  - type: file_content_contains
    path: docs_custom/brand_identity_guide.md
    pattern: "#F59E0B" # Specific Hex code for Fintech/Crypto in the database
  - type: file_content_contains
    path: docs_custom/brand_identity_guide.md
    pattern: "#8B5CF6" # Another fintech hex code
---
