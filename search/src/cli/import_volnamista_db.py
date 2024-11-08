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

# Rozdělení hodnot ID a jejich ukládání do číselníků
def split_id(value):
    if value:
        parts = value.split('/')
        if len(parts) == 2:
            return parts[0], parts[1]
    return None, None

# Vkládání dat do číselníků a hlavní tabulky po dávkách (po 1000 záznamech)
batch_size = 1000
batch = []

for item in data.get("polozky", []):
    # Min požadované vzdělání
    vzdelani_typ, vzdelani_id = split_id(item.get("minPozadovaneVzdelani", {}).get("id"))
    if vzdelani_typ and vzdelani_id:
        cursor.execute("INSERT INTO volna_mista.vzdelani (typ, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (vzdelani_typ, vzdelani_id))

    # Směnnost
    smennost_typ, smennost_id = split_id(item.get("smennost", {}).get("id"))
    if smennost_typ and smennost_id:
        cursor.execute("INSERT INTO volna_mista.smennost (typ, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (smennost_typ, smennost_id))

    # Typ mzdy
    mzda_typ, mzda_id = split_id(item.get("typMzdy", {}).get("id"))
    if mzda_typ and mzda_id:
        cursor.execute("INSERT INTO volna_mista.typ_mzdy (typ, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (mzda_typ, mzda_id))

    # Profese Cz Isco
    profese_dokument, profese_id = split_id(item.get("profeseCzIsco", {}).get("id"))
    if profese_dokument and profese_id:
        cursor.execute("INSERT INTO volna_mista.profese (id, dokument) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (profese_id, profese_dokument))

    # Pracovní poměr
    prac_pomer_typ, prac_pomer_id = split_id(item.get("kontaktniPracoviste", {}).get("id"))
    if prac_pomer_typ and prac_pomer_id:
        cursor.execute("INSERT INTO volna_mista.kontaktni_pracoviste (typ, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (prac_pomer_typ, prac_pomer_id))

    # Načtení informací o pracovišti
    pracoviste = item.get("mistoVykonuPrace") and item.get("mistoVykonuPrace").get("pracoviste", [{}])[0] if item.get("mistoVykonuPrace") else {}
    pracoviste_nazev = pracoviste.get("nazev") if pracoviste else None
    pracoviste_adresa = pracoviste.get("adresa", {}).get("dodatekAdresy") if pracoviste and pracoviste.get("adresa") else None
    kod_obce_ruian = pracoviste.get("adresa", {}).get("kodAdresnihoMista") if pracoviste and pracoviste.get("adresa") else None

    # Přidání dat do dávky
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
        vzdelani_id,
        smennost_id,
        mzda_id,
        item.get("mistoVykonuPrace", {}).get("typMistaVykonuPrace", {}).get("id") if item.get("mistoVykonuPrace") and item.get("mistoVykonuPrace").get("typMistaVykonuPrace") else None,
        item.get("zamestnavatel", {}).get("ico") if item.get("zamestnavatel") else None,
        item.get("zamestnavatel", {}).get("nazev") if item.get("zamestnavatel") else None,
        profese_id,
        pracoviste_nazev,
        pracoviste_adresa,
        kod_obce_ruian,
        prac_pomer_id,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("email") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("telefon") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("jmeno") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None,
        item.get("prvniKontaktSeZamestnavatelem", {}).get("komuSeHlasit", {}).get("prijmeni") if item.get("prvniKontaktSeZamestnavatelem") and item.get("prvniKontaktSeZamestnavatelem").get("komuSeHlasit") else None
    )
    batch.append(misto_values)

    # Pokud je dávka plná, vložíme data do databáze
    if len(batch) >= batch_size:
        cursor.executemany("""
        INSERT INTO volna_mista.volna_mista (
            portal_id, id, referencni_cislo, azylant, cizinec_mimo_eu,
            datum_vlozeni, datum_zmeny, mesicni_mzda_do, mesicni_mzda_od,
            modra_karta, pocet_hodin_tydne, pocet_mist, pozadovana_profese,
            statni_sprava_samosprava, termin_ukonceni_pracovniho_pomeru,
            termin_zahajeni_pracovniho_pomeru, souhlas_agentury_agentura,
            souhlas_agentury_uzivatel, upresnujici_informace, zamestnanecka_karta,
            min_pozadovane_vzdelani, smennost, typ_mzdy, misto_vykonu_prace,
            zamestnavatel_ico, zamestnavatel_nazev, profese_cz_isco, pracoviste,
            adresa_pracoviste, kod_obce_ruian, kontaktni_pracoviste, prvni_kontakt_email, prvni_kontakt_telefon,
            prvni_kontakt_jmeno, prvni_kontakt_prijmeni
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        connection.commit()
        batch = []

# Vložení zbylých dat
if batch:
    cursor.executemany("""
    INSERT INTO volna_mista.volna_mista (
        portal_id, id, referencni_cislo, azylant, cizinec_mimo_eu,
        datum_vlozeni, datum_zmeny, mesicni_mzda_do, mesicni_mzda_od,
        modra_karta, pocet_hodin_tydne, pocet_mist, pozadovana_profese,
        statni_sprava_samosprava, termin_ukonceni_pracovniho_pomeru,
        termin_zahajeni_pracovniho_pomeru, souhlas_agentury_agentura,
        souhlas_agentury_uzivatel, upresnujici_informace, zamestnanecka_karta,
        min_pozadovane_vzdelani, smennost, typ_mzdy, misto_vykonu_prace,
        zamestnavatel_ico, zamestnavatel_nazev, profese_cz_isco, pracoviste,
        adresa_pracoviste, kod_obce_ruian, kontaktni_pracoviste, prvni_kontakt_email, prvni_kontakt_telefon,
        prvni_kontakt_jmeno, prvni_kontakt_prijmeni
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, batch)
    connection.commit()

# Potvrzení transakce a zavření spojení
cursor.close()
connection.close()

print("Data byla úšpěšně vložena do databáze.")
