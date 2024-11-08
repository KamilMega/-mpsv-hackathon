CREATE SCHEMA IF NOT EXISTS volna_mista;

CREATE TABLE IF NOT EXISTS volna_mista.vzdelani (
                                                    id TEXT PRIMARY KEY,
                                                    typ TEXT
);

CREATE TABLE IF NOT EXISTS volna_mista.smennost (
                                                    id TEXT PRIMARY KEY,
                                                    typ TEXT
);

CREATE TABLE IF NOT EXISTS volna_mista.typ_mzdy (
                                                    id TEXT PRIMARY KEY,
                                                    typ TEXT
);

CREATE TABLE IF NOT EXISTS volna_mista.profese (
                                                   id INTEGER PRIMARY KEY,
                                                   dokument TEXT
);

CREATE TABLE IF NOT EXISTS volna_mista.kontaktni_pracoviste (
                                                                id TEXT PRIMARY KEY,
                                                                typ TEXT
);

CREATE TABLE IF NOT EXISTS volna_mista.volne_mista (
                                                       portal_id BIGINT PRIMARY KEY,
                                                       id TEXT,
                                                       referencni_cislo TEXT,
                                                       azylant BOOLEAN,
                                                       cizinec_mimo_eu BOOLEAN,
                                                       datum_vlozeni TIMESTAMP,
                                                       datum_zmeny TIMESTAMP,
                                                       mesicni_mzda_do INTEGER,
                                                       mesicni_mzda_od INTEGER,
                                                       modra_karta BOOLEAN,
                                                       pocet_hodin_tydne INTEGER,
                                                       pocet_mist INTEGER,
                                                       pozadovana_profese TEXT,
                                                       statni_sprava_samosprava BOOLEAN,
                                                       termin_ukonceni_pracovniho_pomeru DATE,
                                                       termin_zahajeni_pracovniho_pomeru DATE,
                                                       souhlas_agentury_agentura BOOLEAN,
                                                       souhlas_agentury_uzivatel BOOLEAN,
                                                       upresnujici_informace TEXT,
                                                       zamestnanecka_karta BOOLEAN,
                                                       min_pozadovane_vzdelani TEXT REFERENCES volna_mista.vzdelani(id),
    smennost TEXT REFERENCES volna_mista.smennost(id),
    typ_mzdy TEXT REFERENCES volna_mista.typ_mzdy(id),
    misto_vykonu_prace TEXT,
    zamestnavatel_ico TEXT,
    zamestnavatel_nazev TEXT,
    profese_cz_isco INTEGER REFERENCES volna_mista.profese(id),
    pracoviste TEXT,
    adresa_pracoviste TEXT,
    kod_obce_ruian TEXT,
    kontaktni_pracoviste TEXT REFERENCES volna_mista.kontaktni_pracoviste(id),
    prvni_kontakt_email TEXT,
    prvni_kontakt_telefon TEXT,
    prvni_kontakt_jmeno TEXT,
    prvni_kontakt_prijmeni TEXT
    );
