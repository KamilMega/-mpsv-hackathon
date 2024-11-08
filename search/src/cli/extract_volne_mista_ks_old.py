import psycopg2
import os
from dotenv import load_dotenv
from src.utils.api_utils import get_keywords_from_gpt
from src.utils.api_utils import get_keywords_skils_from_gpt

# Načtení proměnných prostředí ze souboru .env
load_dotenv()

# Připojení k PostgreSQL databázi
connection = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)
cursor = connection.cursor()

# Přidání sloupce klicova_slova do tabulky volna_mista.volna_mista_json
add_column_query = '''
ALTER TABLE search.volna_mista_json
ADD COLUMN IF NOT EXISTS klicova_slova TEXT;
'''
cursor.execute(add_column_query)
connection.commit()

# Načtení záznamů ze sloupce pozadovana_profese, které nemají klicova_slova
select_query = '''
SELECT id, pozadovana_profese FROM search.volna_mista_json WHERE klicova_slova ='error' or klicova_slova is null LIMIT 50;
'''
cursor.execute(select_query)
records = cursor.fetchall()

# Zpracování záznamů
for record in records:
    record_id, pozadovana_profese = record
    if pozadovana_profese:
        try:
            # Zavolání funkce get_keywords_from_gpt
            keywords = get_keywords_skils_from_gpt(pozadovana_profese)
            print(f"ID: {record_id}, Klíčová slova: {keywords}")
        except Exception as e:
            # V případě chyby nastavíme klíčová slova na "error"
            keywords = "error"
            print(f"ID: {record_id}, Chyba při získávání klíčových slov: {e}")

        # Uložení klíčových slov do sloupce klicova_slova
        update_query = '''
        UPDATE search.volna_mista_json
        SET klicova_slova = %s
        WHERE id = %s;
        '''
        cursor.execute(update_query, (keywords, record_id))

        # Potvrzení každé transakce po aktualizaci
        connection.commit()

# Uzavření připojení
cursor.close()
connection.close()

print("Zpracování prvních 50 záznamů bylo dokončeno.")
