import json
import psycopg2
import os
from dotenv import load_dotenv

# Načtení proměnných prostředí ze souboru .env
load_dotenv()

# Načtení souboru
with open('data/profese.json', encoding='utf-8') as file:
    data = json.load(file)

# Připojení k PostgreSQL databázi
connection = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', ''),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)
cursor = connection.cursor()

# Vytvoření tabulky profese_json
create_table_query = '''
CREATE TABLE IF NOT EXISTS search.profese_json (
    id SERIAL PRIMARY KEY,
    kod VARCHAR(255),
    title VARCHAR(255),
    data_json JSONB
);
'''
cursor.execute(create_table_query)
connection.commit()

# Vložení dat do tabulky
insert_query = '''
INSERT INTO search.profese_json (id, kod, title, data_json) VALUES (%s, %s, %s, %s)
'''

for polozka in data['polozky']:
    id_value = polozka.get('id')
    kod = polozka.get('kod')
    title = polozka.get('title')
    data_json = json.dumps(polozka)
    cursor.execute(insert_query, (id_value, kod, title, data_json))

# Potvrzení transakce
connection.commit()

# Uzavření připojení
cursor.close()
connection.close()

print("Data byla úspěšně uložena do tabulky profese_json.")
