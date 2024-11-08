create table r_volnamista_kurz
as
WITH vazba_vm_kurz AS (
    select
        vmj.id as id_volnemisto,
        --	vmj.pozadovana_profese,
        kj.id as id_kurz ,
        -- 	kj.nazev,
        (vmj.emb_dovednosti <-> kj.emb_dovednosti ) AS weighted_distance,
        ROW_NUMBER() OVER (PARTITION BY vmj.portal_id ORDER BY (vmj.emb_dovednosti <-> kj.emb_dovednosti )  ) as relevance
    from volna_mista_json vmj, kurzy_json kj
    where (vmj.emb_dovednosti <-> kj.emb_dovednosti ) <0.7
      and vmj.emb_dovednosti  is not null
      and kj.emb_dovednosti  is not null
)
SELECT *
FROM vazba_vm_kurz
WHERE relevance <= 10
order by id_volnemisto, relevance;


ALTER TABLE "search".r_volnamista_kurz ADD "valid" int DEFAULT 1 NULL;

