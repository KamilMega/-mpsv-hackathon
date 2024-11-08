import requests
import json

# Nastavení Elasticsearch endpointu
#ES_HOST = "https://cms.po-dev-ace.com/elastic/"
ES_HOST = "http://localhost:9200/"
ES_INDEX = "professions"

# Headers pro HTTP požadavky
HEADERS = {
    "Content-Type": "application/json"
}

# Funkce pro vložení dokumentů do Elasticsearch
def insert_document(doc_id, document, embedding):
    doc_url = f"{ES_HOST}{ES_INDEX}/_doc/{doc_id}"
    document_body = {
        "id": doc_id,
        "document": document,
        "embedding": embedding
    }
    response = requests.post(doc_url, headers=HEADERS, data=json.dumps(document_body), verify=False)

    if response.status_code == 201:
        print(f"Document {doc_id} inserted successfully.")
    else:
        print(f"Error inserting document {doc_id}: {response.text}")

# Načtení dat z JSON souboru a import do Elasticsearch
def import_data_to_es(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for record in data:
            doc_id = record["id"]
            document = record["document"]
            embedding = record["embedding"]
            insert_document(doc_id, document, embedding)

# Hlavní logika
if __name__ == "__main__":
    import_data_to_es("export/profese_embeddings.json")  # Import dat z JSON do Elasticsearch
