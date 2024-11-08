import sys

import psycopg2
import os
from dotenv import load_dotenv
from src.utils.extract_utils import extract_skills_and_jobdesc_from_job_description, extract_skills_and_descriptors
from src.utils.prompt import job_ad_system_prompt, job_ad_user_prompt, compare_system_prompt, compare_user_prompt

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

# Přidání sloupců pro klíčová slova a dovednosti do tabulky volna_mista.volna_mista_json
add_columns_query = '''
ALTER TABLE r_volnamista_kurz
    ADD COLUMN IF NOT EXISTS porovnani TEXT'''
cursor.execute(add_columns_query)
connection.commit()

# Získání segmentu z argumentů příkazové řádky
if len(sys.argv) != 2:
    print("Použití: python script.py <segment>")
    sys.exit(1)

try:
    segment = int(sys.argv[1])
    if segment < 1 or segment > 75:
        raise ValueError("Segment musí být v rozmezí 1 až 75.")
except ValueError as e:
    print(f"Chyba: {e}")
    sys.exit(1)
# Načtení záznamů ze sloupců pozadovana_profese a upresnujici_informace

offset = (segment - 1) * 1000
limit = 100
select_query = '''
            SELECT vmj.id,
                   vmj.pozadovana_profese,
                   kj.id,
                   kj.nazev
            FROM r_volnamista_kurz rvmk
            JOIN volna_mista_json vmj ON vmj.id = rvmk.id_volnemisto
            JOIN kurzy_json kj ON kj.id = rvmk.id_kurz
            WHERE porovnani IS NULL
OFFSET %s LIMIT %s;
'''
cursor.execute(select_query,(offset, limit))
records = cursor.fetchall()

# Zpracování záznamů
for record in records:
    vm_id, pozadovana_profese, kurz_id, nazev = record
    if pozadovana_profese or nazev:
        try:
            # Zavolání funkce get_keywords_skils_from_gpt a získání klíčových slov a dovedností
            result = extract_skills_and_descriptors(compare_system_prompt,compare_user_prompt, pozadovana_profese, nazev)
            porovnani = result.get("compare", [])

            # Převod seznamů na řetězce bez závorek a uvozovek, oddělené čárkami
            porovnani = ", ".join(porovnani)


            print(f"VM ID: {vm_id},KURZ ID: {kurz_id}, Porovnani: {porovnani}")
        except Exception as e:
            # V případě chyby nastavíme klíčová slova a dovednosti na "error"
            keywords = "error"
            skills = "error"
            print(f"VM ID: {vm_id},KURZ ID: {kurz_id}, Chyba při získávání porovnani: {e}")

        # Uložení klíčových slov a dovedností do příslušných sloupců
        update_query = '''
        UPDATE search.r_volnamista_kurz
        SET porovnani = %s
        WHERE id_volnemisto = %s and id_kurz = %s;
        '''
        cursor.execute(update_query, (porovnani, vm_id, kurz_id))

        # Potvrzení každé transakce po aktualizaci
        connection.commit()

# Uzavření připojení
cursor.close()
connection.close()

print("Zpracování prvních 50 záznamů bylo dokončeno.")
