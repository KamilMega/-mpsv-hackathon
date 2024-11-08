import psycopg2
import os
from dotenv import load_dotenv
from src.utils.extract_utils import extract_skills_and_jobdesc_from_job_description, extract_skills_and_descriptors
from src.utils.prompt import course_system_prompt, course_user_prompt


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

# Načtení záznamů ze sloupců pozadovana_profese a upresnujici_informace
select_query = '''
select id, nazev, popis_rekvalifikace  
from kurzy_json kj 
WHERE klicova_slova IS NULL
LIMIT 1000;
'''
cursor.execute(select_query)
records = cursor.fetchall()

# Zpracování záznamů
for record in records:
    record_id, nazev_kurzu, popis_rekvalifikace = record
    if nazev_kurzu or popis_rekvalifikace:
        # Vytvoření textu z požadované profese a upřesňujících informací
        #combined_text = f"{pozadovana_profese}\n{upresnujici_informace}" if upresnujici_informace else pozadovana_profese

        try:
            # Zavolání funkce get_keywords_skils_from_gpt a získání klíčových slov a dovedností
            result = extract_skills_and_descriptors(course_system_prompt, course_user_prompt, nazev_kurzu, popis_rekvalifikace)
            keywords_list = result.get("course_descriptors", [])
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
        UPDATE search.kurzy_json
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
