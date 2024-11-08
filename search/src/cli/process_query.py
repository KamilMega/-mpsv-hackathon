import json
import argparse
from src.utils.api_utils import generate_vector

# Nastavení argumentů
parser = argparse.ArgumentParser(description="Vygeneruj vektor na základě query a ulož do souboru.")
parser.add_argument("query", type=str, help="Dotaz, na základě kterého se vektor vygeneruje.")
parser.add_argument("output_file", type=str, help="Cesta k souboru, do kterého se uloží výsledný vektor.")

args = parser.parse_args()

# Vygenerování vektoru
vector = generate_vector(args.query)

# Uložení vektoru do souboru
with open(args.output_file, "w") as f:
    json.dump(vector, f)

print(f"Vektor byl úspěšně uložen do souboru {args.output_file}")