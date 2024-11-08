-- DDL skript pro vytvoření tabulky kurz
CREATE TABLE kurz (
                      id SERIAL PRIMARY KEY,
                      kod BIGINT NOT NULL,
                      nazev VARCHAR(255) NOT NULL,
                      popis_rekvalifikace TEXT,
                      rekvalifikacni_zarizeni_id INT,
                      stav_kurzu_id INT,
                      forma_vyuky_id INT,
                      doklad_k_akreditaci_uuid UUID,
                      jazyk_vyuky_id INT,
                      osoba_id INT,
                      osoba_nazev VARCHAR(255),
                      osoba_ico VARCHAR(20),
                      adresa_sidl_id INT,
                      voleny_kurz_id INT,
                      typ_rekvalifikace_id INT
);

-- DDL skript pro vytvoření tabulky aktualni_terminy
CREATE TABLE aktualni_terminy (
                                  id SERIAL PRIMARY KEY,
                                  kurz_id INT REFERENCES kurz(id),
                                  datum_od DATE,
                                  datum_do DATE,
                                  cena NUMERIC,
                                  hrazena_cena NUMERIC,
                                  spolu_ucast NUMERIC,
                                  kapacita INT,
                                  zruseny BOOLEAN,
                                  uzavreny BOOLEAN
);