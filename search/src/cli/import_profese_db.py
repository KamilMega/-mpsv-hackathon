
import json
import psycopg2
import sys
import subprocess


# Připojení k PostgreSQL databázi
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Načtení JSON dat ze souboru
with open("data/profese_vektor.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Vkládání dat do tabulky profese ve schematu volna_mista
for item in data:
    profese_insert_query = """
    INSERT INTO volna_mista.profese_vektor (
        id, document, embedding
    ) VALUES (%s, %s, %s)
    """
    profese_values = (
        item.get("id"),
        item.get("document"),
        item.get("embedding")
    )
    cursor.execute(profese_insert_query, profese_values)

# Potvrzení transakce a zavření spojení
connection.commit()
cursor.close()
connection.close()

print("Data byla úspěšně vložena do databáze.")
