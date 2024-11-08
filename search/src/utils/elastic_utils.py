import requests
import json

# Nastavení Elasticsearch endpointu
ES_HOST = "https://cms.po-dev-ace.com/elastic/"
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
        
# Funkce pro vyhledávání v Elasticsearch
def search(query_vector,n_results):
    search_url = f"{ES_HOST}{ES_INDEX}/_search"
    query_body = {
        "_source": ["document"],
        "size": n_results,
        "query": {
            "bool": {
                "must": [
                    {
                        "script_score": {
                            "query": {
                                # "term": {
                                #     "employment_type": "HPP"  # Filtrování na základě typu úvazku
                                # }
                                "match_all": {}
                            },
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {
                                    "query_vector": query_vector  # Převod vektoru na seznam
                                }
                            }
                        }
                    }
                ]
            }
        }
    }
    response = requests.post(search_url, headers=HEADERS, data=json.dumps(query_body), verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error searching in elastic {search_text}")