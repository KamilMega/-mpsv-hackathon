import csv
import json
import chromadb
import argparse
import os

# Připojení k Chroma DB
client = chromadb.PersistentClient(path="chroma_db")
collection_name = "positions"
collection = client.get_collection(name=collection_name)

# Funkce pro export do CSV
def export_to_csv(output_file, data):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "document", "embedding"])  # Hlavičky

        for record in data:
            writer.writerow([record['id'], record['document'], json.dumps(record['embedding'])])

    print(f"Exportováno do CSV: {output_file}")

# Funkce pro export do JSON
def export_to_json(output_file, data):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Exportováno do JSON: {output_file}")

# Funkce pro načtení dat z ChromaDB
def get_data_from_chromadb():
    # Získání všech dat z kolekce
    all_records = collection.get(include=["embeddings", "documents"])
    ids = all_records['ids']
    documents = all_records['documents']
    embeddings = all_records['embeddings']

    data = []
    for i in range(len(ids)):
        record = {
            "id": ids[i],
            "document": documents[i],
            "embedding": embeddings[i].tolist()
        }
        data.append(record)

    return data

# CLI logika
def main():
    parser = argparse.ArgumentParser(description="Export dat z ChromaDB do JSON nebo CSV formátu.")
    parser.add_argument("--output", type=str, required=True, help="Cesta k výstupnímu souboru.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Formát výstupu (json nebo csv).")
    
    args = parser.parse_args()
    output_file = args.output
    output_format = args.format

    # Získání dat z ChromaDB
    data = get_data_from_chromadb()

    # Kontrola, zda je výstupní složka dostupná
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Export do požadovaného formátu
    if output_format == "csv":
        export_to_csv(output_file, data)
    else:
        export_to_json(output_file, data)

if __name__ == "__main__":
    main()
