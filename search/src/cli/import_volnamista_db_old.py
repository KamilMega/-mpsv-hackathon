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
with open("data/volna_mista.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Vkládání dat do tabulky misto ve schematu volna_mista
for item in data.get("polozky", []):
    misto_insert_query = """
    INSERT INTO volna_mista.volne_mista (
        portal_id, id, referencni_cislo, azylant, cizinec_mimo_eu,
        datum_vlozeni, datum_zmeny, mesicni_mzda_do, mesicni_mzda_od,
        modra_karta, pocet_hodin_tydne, pocet_mist, pozadovana_profese,
        statni_sprava_samosprava, termin_ukonceni_pracovniho_pomeru,
        termin_zahajeni_pracovniho_pomeru, souhlas_agentury_agentura,
        souhlas_agentury_uzivatel, upresnujici_informace, zamestnanecka_karta,
        min_pozadovane_vzdelani, smennost, typ_mzdy, misto_vykonu_prace,
        zamestnavatel_ico, zamestnavatel_nazev, profese_cz_isco, pracoviste,
        kontaktni_pracoviste, prvni_kontakt_email, prvni_kontakt_telefon,
        prvni_kontakt_jmeno, prvni_kontakt_prijmeni
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    misto_values = (
        item.get("portalId"),
        item.get("id"),
        item.get("referencniCislo"),
        item.get("azylant"),
        item.get("cizinecMimoEu"),
        item.get("datumVlozeni"),
        item.get("datumZmeny"),
        item.get("mesicniMzdaDo"),
        item.get("mesicniMzdaOd"),
        item.get("modraKarta"),
        item.get("pocetHodinTydne"),
        item.get("pocetMist"),
        item.get("pozadovanaProfese", {}).get("cs") if item.get("pozadovanaProfese") else None,
        item.get("statniSpravaSamosprava"),
        item.get("terminUkonceniPracovnihoPomeru"),
        item.get("terminZahajeniPracovnihoPomeru"),
        item.get("souhlasAgenturyAgentura"),
        item.get("souhlasAgenturyUzivatel"),
        item.get("upresnujiciInformace", {}).get("cs") if item.get("upresnujiciInformace") else None,
        item.get("zamestnaneckaKarta"),
        item.get("minPozadovaneVzdelani", {}).get("id") if item.get("minPozadovaneVzdelani") else None,
        item.get("smennost", {}).get("id") if item.get("smennost") else None,
        item.get("typMzdy", {}).get("id") if item.get("typMzdy") else None,
        item.get("mistoVykonuPrace", {}).get("typMistaVykonuPrace", {}).get("id") if item.get("mistoVykonuPrace") and item.get("mistoVykonuPrace").get("typMistaVykonuPrace") else None,
        item.get("zamestnavatel", {}).get("ico") if item.get("zamestnavatel") else None,
        item.get("zamestnavatel", {}).get("nazev") if item.get("zamestnavatel") else None,
        item.get("profeseCzIsco", {}).get("id") if item.get("profeseCzIsco") else None,
        item.get("mistoVykonuPrace", {}).get("pracoviste", [{}])[0].get("nazev") if item.get("mistoVykonuPrace") and item.get("mistoVykonuPrace").get("pracoviste") else None,
        item.get("kontaktniPracoviste", {}).get("id") if item.get("kontaktniPracoviste") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("email") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("telefon") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("jmeno") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("prijmeni") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None
    )
    cursor.execute(misto_insert_query, misto_values)

# Potvrzení transakce a zavření spojení
connection.commit()
cursor.close()
connection.close()

print("Data byla úšpěšně vložena do databáze.")

