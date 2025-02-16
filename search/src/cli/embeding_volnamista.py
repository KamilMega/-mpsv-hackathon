import sys
import psycopg2
import os
from dotenv import load_dotenv
from src.utils.api_utils import generate_vector

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

# Načtení argumentu segmentu
try:
    segment = int(sys.argv[1])
    if segment < 1 or segment > 75:
        raise ValueError("Segment musí být v rozmezí 1 až 75.")
except ValueError as e:
    print(f"Chyba: {e}")
    sys.exit(1)

# Výpočet offsetu a limitu
offset = (segment - 1) * 1000
limit = 1000  # Zpracování po 1000 záznamech

# Načtení záznamů, kde jsou vyplněna klíčová slova a emb_klicova_slova je null
select_query = '''
SELECT id, klicova_slova, dovednosti
FROM search.volna_mista_json
WHERE klicova_slova IS NOT NULL AND emb_klicova_slova IS NULL
OFFSET %s LIMIT %s;
'''
cursor.execute(select_query, (offset, limit))
records = cursor.fetchall()

# Zpracování záznamů
for record in records:
    record_id, klicova_slova, dovednosti = record

    try:
        # Vygenerování vektoru pro klíčová slova a dovednosti
        emb_klicova_slova = generate_vector(klicova_slova)
        emb_dovednosti = generate_vector(dovednosti)

        # Uložení vektorů do příslušných sloupců
        update_query = '''
        UPDATE search.volna_mista_json
        SET emb_klicova_slova = %s, emb_dovednosti = %s
        WHERE id = %s;
        '''
        cursor.execute(update_query, (emb_klicova_slova, emb_dovednosti, record_id))

        # Potvrzení transakce po každé aktualizaci
        connection.commit()

        print(f"ID: {record_id}, Vektory úspěšně uloženy.")
    except Exception as e:
        # V případě chyby vypíšeme chybovou zprávu a pokračujeme s dalším záznamem
        print(f"ID: {record_id}, Chyba při generování vektoru: {e}")
        connection.rollback()  # Vrácení změn v případě chyby

# Uzavření připojení
cursor.close()
connection.close()

print("Zpracování segmentu bylo dokončeno.")
