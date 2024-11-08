import sys

import psycopg2
import os
from dotenv import load_dotenv
from src.utils.extract_utils import extract_skills_and_jobdesc_from_job_description, extract_skills_and_descriptors
from src.utils.prompt import job_ad_system_prompt, job_ad_user_prompt

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
ALTER TABLE search.volna_mista_json
ADD COLUMN IF NOT EXISTS klicova_slova TEXT,
ADD COLUMN IF NOT EXISTS dovednosti TEXT;
'''
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
limit = 1000
select_query = '''
SELECT vmj.id, pj.title || ' - ' || vmj.pozadovana_profese as pozadovana_profese, vmj.upresnujici_informace
FROM search.volna_mista_json vmj
JOIN search.profese_json pj ON pj.kod = vmj.profese_cz_isco::text
WHERE klicova_slova IS NULL
OFFSET %s LIMIT %s;
'''
cursor.execute(select_query,(offset, limit))
records = cursor.fetchall()

# Zpracování záznamů
for record in records:
    record_id, pozadovana_profese, upresnujici_informace = record
    if pozadovana_profese or upresnujici_informace:
        # Vytvoření textu z požadované profese a upřesňujících informací
        #combined_text = f"{pozadovana_profese}\n{upresnujici_informace}" if upresnujici_informace else pozadovana_profese

        try:
            # Zavolání funkce get_keywords_skils_from_gpt a získání klíčových slov a dovedností
            result = extract_skills_and_descriptors(job_ad_system_prompt,job_ad_user_prompt, upresnujici_informace, pozadovana_profese)
            keywords_list = result.get("job_descriptors", [])
            skills_list = result.get("skills", [])

            # Převod seznamů na řetězce bez závorek a uvozovek, oddělené čárkami
            keywords = ", ".join(keywords_list)
            skills = ", ".join(skills_list)

            print(f"ID: {record_id}, Klíčová slova: {keywords}, Dovednosti: {skills}")
        except Exception as e:
            # V případě chyby nastavíme klíčová slova a dovednosti na "error"
            keywords = "error"
            skills = "error"
            print(f"ID: {record_id}, Chyba při získávání klíčových slov a dovedností: {e}")

        # Uložení klíčových slov a dovedností do příslušných sloupců
        update_query = '''
        UPDATE search.volna_mista_json
        SET klicova_slova = %s, dovednosti = %s
        WHERE id = %s;
        '''
        cursor.execute(update_query, (keywords, skills, record_id))

        # Potvrzení každé transakce po aktualizaci
        connection.commit()

# Uzavření připojení
cursor.close()
connection.close()

print("Zpracování prvních 50 záznamů bylo dokončeno.")
