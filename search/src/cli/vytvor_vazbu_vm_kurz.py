import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# Načtení proměnných prostředí ze souboru .env
load_dotenv()

# Připojení k databázi
connection = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)
cursor = connection.cursor()

# Vytvoření tabulky, pokud neexistuje
cursor.execute("""
    CREATE TABLE IF NOT EXISTS search.r_volnamista_kurz_1 (
        id_volnemisto INTEGER,
        id_kurz INTEGER,
        weighted_distance FLOAT,
        relevance INTEGER
    )
""")
connection.commit()

# Nastavení parametrů
pocet = 0

try:
    # Iterace přes všechna volná místa
    cursor.execute("SELECT id FROM search.volna_mista_json WHERE  emb_dovednosti IS NOT NULL")
    volnamista_records = cursor.fetchall()

    for volnemisto in volnamista_records:
        volnemisto_id = volnemisto[0]

        # Načtení vazby mezi volným místem a kurzy pro dané volné místo
        cursor.execute("""
            WITH vazba_vm_kurz AS (
                SELECT 
                    vmj.id AS id_volnemisto, 
                    kj.id AS id_kurz,
                    (vmj.emb_dovednosti <-> kj.emb_dovednosti) AS weighted_distance,
                    ROW_NUMBER() OVER (PARTITION BY vmj.portal_id ORDER BY (vmj.emb_dovednosti <-> kj.emb_dovednosti)) AS relevance
                FROM search.volna_mista_json vmj, search.kurzy_json kj 
                WHERE (vmj.emb_dovednosti <-> kj.emb_dovednosti) < 1
                    AND vmj.emb_dovednosti IS NOT NULL
                    AND kj.emb_dovednosti IS NOT NULL
                    AND vmj.id = %s
            )
            SELECT *
            FROM vazba_vm_kurz
            WHERE relevance <= 20
            ORDER BY id_volnemisto, relevance
        """, (volnemisto_id,))

        results = cursor.fetchall()
        if not results:
            continue  # Pokud nejsou žádné záznamy, pokračujte na další volné místo

        # Vkládání výsledků do cílové tabulky
        insert_query = """
            INSERT INTO search.r_volnamista_kurz_1 (id_volnemisto, id_kurz, weighted_distance, relevance)
            VALUES %s
        """
        execute_values(cursor, insert_query, results)
        pocet += len(results)

        # Commit po každých 100 záznamů
        if pocet % 100 == 0:
            connection.commit()
            print(f'Uložených {pocet} záznamů')

    # Konečný commit pro zbývající záznamy
    connection.commit()
    print('Zpracování dokončeno, poslední commit proveden')

except Exception as e:
    connection.rollback()
    print("Došlo k chybě:", e)
finally:
    cursor.close()
    connection.close()
