import json
from src.utils.api_utils import generate_vector
import chromadb
from src.config import CHROMA_DB_PATH

# Připojení k Chroma DB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Smazání kolekce, pokud již existuje
collection_name = "positions"
existing_collections = client.list_collections()

if any(c.name == collection_name for c in existing_collections):
    client.delete_collection(name=collection_name)
    print(f"Kolekce '{collection_name}' byla smazána.")

# Vytvoření nové kolekce
collection = client.create_collection(name=collection_name)

# Načtení dat z JSON souboru s obalovým elementem "polozky"
with open('data/profese.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

positions = data['polozky']

for position in positions:
    vector = generate_vector(position['title'])

    if vector:
        print(f"Ukládám embedding pro pozici: {position['title']}")

        try:
            collection.add(
                documents=[position['title']],
                embeddings=[vector],
                ids=[str(position['id'])]
            )
            print(f"Naindexováno: {position['title']} (ID: {position['id']})")
        except Exception as e:
            print(f"Chyba při vkládání do Chroma DB: {e}")
    else:
        print(f"Embedding pro {position['title']} nebyl vygenerován.")
