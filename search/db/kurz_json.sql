CREATE SCHEMA IF NOT EXISTS search;

CREATE TABLE "search".kurzy_json (
                                           id serial4 NOT NULL,
                                           kurz_id varchar(255) NULL,
                                           data_json jsonb NULL,
                                           CONSTRAINT kurzy_json_pkey PRIMARY KEY (id)
);


ALTER TABLE search.kurzy_json ADD COLUMN IF NOT EXISTS klicova_slova TEXT;

ALTER TABLE search.kurzy_json ADD COLUMN IF NOT EXISTS dovednosti TEXT;

ALTER TABLE "search".kurzy_json
ADD COLUMN nazev VARCHAR(255),
ADD COLUMN popis_rekvalifikace TEXT;

UPDATE "search".kurzy_json
SET
    nazev = data_json->>'nazev',
    popis_rekvalifikace = data_json->>'popisRekvalifikace';