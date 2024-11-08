-- DDL skript pro vytvoření tabulky profese ve schematu volna_mista
CREATE SCHEMA IF NOT EXISTS volna_mista;

drop table volna_mista.profese;
CREATE TABLE volna_mista.profese_vektor (
    id SERIAL PRIMARY KEY,
    document VARCHAR(255) NOT NULL,
    embedding FLOAT8[] -- Použití typu FLOAT8[] kvůli různým velikostem vektorů
--    embedding VECTOR(768) -- nebo jiná vhodná dimenze v závislosti na délce vektoru
);
