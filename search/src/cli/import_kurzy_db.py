import json
import psycopg2
import sys
import subprocess

# Zkontrolovat, zda je modul psycopg2 nainstalován, pokud ne, nainstalovat jej
try:
    import psycopg2
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

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
with open("data/kurzy.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Vkládání dat do tabulky kurz ve schematu volna_mista
for item in data.get("list", []):
    kurz_insert_query = """
    INSERT INTO volna_mista.kurz (
        id, kod, nazev, popis_rekvalifikace, rekvalifikacni_zarizeni_id,
        stav_kurzu_id, forma_vyuky_id, doklad_k_akreditaci_uuid, jazyk_vyuky_id,
        osoba_id, osoba_nazev, osoba_ico, adresa_sidl_id, voleny_kurz_id, typ_rekvalifikace_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    kurz_values = (
        item.get("id"),
        item.get("kod"),
        item.get("nazev"),
        item.get("popisRekvalifikace"),
        item.get("rekvalifikacniZarizeniId"),
        item.get("stavKurzuId"),
        item.get("formaVyukyId"),
        item.get("dokladKAkreditaciUuid"),
        item.get("jazykVyukyId"),
        item.get("osoba", {}).get("id"),
        item.get("osoba", {}).get("nazev"),
        item.get("osoba", {}).get("ico"),
        item.get("adresaSidla", {}).get("id") if item.get("adresaSidla") else None,
        item.get("volenyRekvalifikacniKurz", {}).get("id") if item.get("volenyRekvalifikacniKurz") else None,
        item.get("typRekvalifikaceId")
    )
    cursor.execute(kurz_insert_query, kurz_values)

    # Vkládání dat do tabulky aktualni_terminy ve schematu volna_mista
    aktualni_terminy = item.get("aktualniTerminy")
    if aktualni_terminy:
        for termin in aktualni_terminy:
            termin_insert_query = """
            INSERT INTO volna_mista.aktualni_terminy (
                kurz_id, datum_od, datum_do, cena, hrazena_cena, spolu_ucast, kapacita,
                zruseny, uzavreny
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            termin_values = (
                item.get("id"),
                termin.get("datumOd"),
                termin.get("datumDo"),
                termin.get("cena"),
                termin.get("hrazenaCena"),
                termin.get("spoluUcast"),
                termin.get("kapacita"),
                termin.get("zruseny"),
                termin.get("uzavreny")
            )
            cursor.execute(termin_insert_query, termin_values)

# Potvrzení transakce a zavření spojení
connection.commit()
cursor.close()
connection.close()

print("Data byla úspěšně vložena do databáze.")