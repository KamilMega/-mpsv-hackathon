CREATE OR REPLACE FUNCTION vytvorit_vazbu_volna_mista_kurzy()
RETURNS VOID AS $$
DECLARE
rec RECORD;
    pocet INT := 0;
    kurzor_vazba CURSOR FOR
        WITH vazba_vm_kurz AS (
            SELECT
                vmj.id AS id_volnemisto,
                kj.id AS id_kurz,
                (vmj.emb_dovednosti <-> kj.emb_dovednosti) AS weighted_distance,
                ROW_NUMBER() OVER (PARTITION BY vmj.portal_id ORDER BY (vmj.emb_dovednosti <-> kj.emb_dovednosti)) AS relevance
            FROM volna_mista_json vmj, kurzy_json kj
            WHERE (vmj.emb_dovednosti <-> kj.emb_dovednosti) < 0.8
                AND vmj.emb_dovednosti IS NOT NULL
                AND kj.emb_dovednosti IS NOT NULL
        )
SELECT *
FROM vazba_vm_kurz
WHERE relevance <= 10
ORDER BY id_volnemisto, relevance;

BEGIN
    -- Vytvoření tabulky, pokud ještě neexistuje
CREATE TABLE IF NOT EXISTS r_volnamista_kurz (
                                                 id_volnemisto INTEGER,
                                                 id_kurz INTEGER,
                                                 weighted_distance FLOAT,
                                                 relevance INTEGER
);

-- Otevření kurzoru
OPEN kurzor_vazba;

-- Průchod záznamy kurzorem
LOOP
FETCH kurzor_vazba INTO rec;
        EXIT WHEN NOT FOUND;

        -- Vložení záznamu do tabulky
INSERT INTO r_volnamista_kurz (id_volnemisto, id_kurz, weighted_distance, relevance)
VALUES (rec.id_volnemisto, rec.id_kurz, rec.weighted_distance, rec.relevance);

-- Počítání záznamů a commit po každých 100 záznamech
pocet := pocet + 1;
        IF pocet % 100 = 0 THEN
            -- Commit po každých 100 záznamech
            COMMIT;
            RAISE NOTICE 'Uložených 100 záznamů';
            -- Nová transakce začíná automaticky po commitu
END IF;
END LOOP;

    -- Zavření kurzoru
CLOSE kurzor_vazba;

-- Konečný commit pro zbývající záznamy
COMMIT;
RAISE NOTICE 'Zpracování dokončeno, poslední commit proveden';
END;
$$ LANGUAGE plpgsql;
