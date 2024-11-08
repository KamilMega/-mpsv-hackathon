CREATE SCHEMA IF NOT EXISTS search;

CREATE TABLE IF NOT EXISTS search.volna_mista_json (
                                                            id SERIAL PRIMARY KEY,
                                                            portal_id VARCHAR(255),
    data_json JSONB
    );

ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS klicova_slova TEXT;

ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS dovednosti TEXT;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS pozadovana_profese VARCHAR(255);

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS profese_cz_isco INTEGER;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS obec INTEGER;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS okres INTEGER;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS kraj INTEGER;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS kod_adresniho_mista INTEGER;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS upresnujici_informace TEXT;

ALTER TABLE search.volna_mista_json
    ADD COLUMN IF NOT EXISTS nazev_pracoviste VARCHAR(255);

-- Přidání požadovaných sloupečků
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS mesicni_mzda_od INTEGER;
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS mesicni_mzda_do INTEGER;
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS zamestnavatel_nazev VARCHAR(255);
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS zamestnavatel_ico VARCHAR(255);
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS min_pozadovane_vzdelani VARCHAR(255);
ALTER TABLE search.volna_mista_json ADD COLUMN IF NOT EXISTS pracovne_pravni_vztah VARCHAR(255);


UPDATE search.volna_mista_json
SET pozadovana_profese = (data_json->'pozadovanaProfese')->>'cs';

UPDATE search.volna_mista_json
SET profese_cz_isco = CAST(REGEXP_REPLACE((data_json->'profeseCzIsco')->>'id', '^CzIsco/', '') AS INTEGER);

UPDATE search.volna_mista_json
SET obec = CAST(REGEXP_REPLACE((data_json->'mistoVykonuPrace'->'pracoviste'->0->'adresa'->'obec'->>'id'), '^Obec/', '') AS INTEGER);


-- obec:
UPDATE search.volna_mista_json
SET obec = CAST(REGEXP_REPLACE((data_json->'mistoVykonuPrace'->'obec'->>'id'), '^Obec/', '') AS INTEGER)
where obec is null;

UPDATE search.volna_mista_json
SET okres = CAST(REGEXP_REPLACE((data_json->'mistoVykonuPrace'->'pracoviste'->0->'adresa'->'okres'->>'id'), '^Okres/', '') AS INTEGER);

UPDATE search.volna_mista_json
SET kraj = CAST(REGEXP_REPLACE((data_json->'mistoVykonuPrace'->'pracoviste'->0->'adresa'->'kraj'->>'id'), '^Kraj/', '') AS INTEGER);

UPDATE search.volna_mista_json
SET kod_adresniho_mista = CAST((data_json->'mistoVykonuPrace'->'pracoviste'->0->'adresa'->>'kodAdresnihoMista') AS INTEGER);

UPDATE search.volna_mista_json
SET upresnujici_informace = (data_json->'upresnujiciInformace')->>'cs';

UPDATE search.volna_mista_json
SET nazev_pracoviste = (data_json->'mistoVykonuPrace'->'pracoviste'->0->>'nazev');

update volna_mista_json vm set okres = (select ob.okres from ruian.rn_obec ob where ob.kod = vm.obec )
where okres is null;

update volna_mista_json vm set kraj = (select ok.vusc from ruian.rn_okres ok where ok.kod = vm.okres )
where kraj is null;


- mesicni_mzda_od
- mesicni_mzda_do
- zamestnavatel_nazev
- zamestnavatel_ico
- min_pozadovane_vzdelani
- pracovne_pravni_vztah (první)

-- Aktualizace mesicni_mzda_od
UPDATE search.volna_mista_json
SET mesicni_mzda_od = (data_json->>'mesicniMzdaOd')::INTEGER;

-- Aktualizace mesicni_mzda_do
UPDATE search.volna_mista_json
SET mesicni_mzda_do = (data_json->>'mesicniMzdaDo')::INTEGER;

-- Aktualizace zamestnavatel_nazev
UPDATE search.volna_mista_json
SET zamestnavatel_nazev = (data_json->'zamestnavatel'->>'nazev');

-- Aktualizace zamestnavatel_ico
UPDATE search.volna_mista_json
SET zamestnavatel_ico = (data_json->'zamestnavatel'->>'ico');

-- Aktualizace min_pozadovane_vzdelani
UPDATE search.volna_mista_json
SET min_pozadovane_vzdelani = REGEXP_REPLACE((data_json->'minPozadovaneVzdelani'->>'id'), '^VzdelaniDetailniKategorie/', '');

-- Aktualizace pracovne_pravni_vztah
UPDATE search.volna_mista_json
SET pracovne_pravni_vztah = (data_json->'pracovnePravniVztahy'->0->>'id');
