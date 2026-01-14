#!/usr/bin/env python3
import csv
import json
import sys
import argparse
from pathlib import Path

# Configurazione Path relativa allo script
BASE_DIR = Path(__file__).parent.parent
# La struttura scaricata è .agent/skills/ui_ux_designer/resources/data/*.csv
RESOURCE_DIR = BASE_DIR / "resources" / "data"

def load_db(filename):
    """Carica un file CSV dal database risorse e lo trasforma in una lista di dict."""
    path = RESOURCE_DIR / filename
    if not path.exists():
        return []
    
    results = []
    try:
        with open(path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
    
    return results

def search(query, db_name="colors.csv"):
    data = load_db(db_name)
    results = []
    query = query.lower()
    
    for item in data:
        # Cerca in tutti i valori del dizionario (riga CSV)
        content = " ".join([str(v).lower() for v in item.values() if v])
        if query in content:
            results.append(item)
    
    return results[:3] # Limita a 3 risultati per non intasare il contesto

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="Cosa stai cercando (es. 'dark mode', 'corporate')")
    parser.add_argument("--type", default="colors", 
                        choices=["colors", "typography", "styles", "products", "ux", "landing", "charts"])
    args = parser.parse_args()

    # Mapping dei file CSV reali trovati nel repo
    db_map = {
        "colors": "colors.csv",
        "typography": "typography.csv",
        "styles": "styles.csv",
        "products": "products.csv",
        "ux": "ux-guidelines.csv",
        "landing": "landing.csv",
        "charts": "charts.csv"
    }

    target_file = db_map.get(args.type, "colors.csv")
    results = search(args.query, target_file)
    
    if results:
        print(json.dumps(results, indent=2))
    else:
        print(f"No results found for '{args.query}' in {target_file}.")

if __name__ == "__main__":
    main()
