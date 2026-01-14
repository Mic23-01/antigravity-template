#!/bin/bash
# .agent/evals/check_metadata.sh
# Wrapper per garantire che la validazione metadata Chroma funzioni sempre
# usando le dipendenze isolate tramite uv.

if ! command -v uv &> /dev/null
then
    echo "Errore: 'uv' non è installato. Installalo per procedere o usa pip install chromadb."
    exit 1
fi

uv run --with chromadb python3 .agent/evals/check_chroma.py "$@"
