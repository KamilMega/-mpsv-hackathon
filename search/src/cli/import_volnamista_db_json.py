import json
import psycopg2

# Načtení souboru
with open('Data/volna_mista.json', encoding='utf-8') as file:
    data = json.load(file)

# Připojení k PostgreSQL databázi
connection = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)
cursor = connection.cursor()

# Vytvoření tabulky volna_mista_json
create_table_query = '''
CREATE TABLE IF NOT EXISTS volna_mista.volna_mista_json (
    id SERIAL PRIMARY KEY,
    portal_id VARCHAR(255),
    data_json JSONB
);
'''
cursor.execute(create_table_query)
connection.commit()

# Vložení dat do tabulky
insert_query = '''
INSERT INTO volna_mista_json (portal_id, data_json) VALUES (%s, %s)
'''

for polozka in data['polozky']:
    portal_id = polozka.get('portalId')
    data_json = json.dumps(polozka)
    cursor.execute(insert_query, (portal_id, data_json))

# Potvrzení transakce
connection.commit()

# Uzavření připojení
cursor.close()
connection.close()

print("Data byla úspěšně uložena do tabulky volna_mista_json.")
