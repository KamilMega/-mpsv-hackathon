import psycopg2
import numpy as np

def search(query_vector, n_results):
    # Připojení k PostgreSQL databázi
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Vyhledávací dotaz pro nalezení nejpodobnějších profesí pomocí kosinusové podobnosti
    search_query = f"""
    SELECT id, document, embedding,
           (1 - (embedding <#> %s::vector)) AS similarity
    FROM volna_mista.profese
    ORDER BY similarity DESC
    LIMIT %s;
    """

    # Vypsání SQL dotazu před odesláním
    print(f"Vykonávám SQL dotaz: {search_query}")

    # Převedení vektoru na správný formát pro SQL dotaz
    query_vector_sql = np.array(query_vector, dtype=np.float64).tolist()

    cursor.execute(search_query, (query_vector_sql, n_results))
    results = cursor.fetchall()

    # Uzavření kurzoru a spojení
    cursor.close()
    connection.close()

    return results


def search_volna_mista(query_vector, page, pageSize, searchFilters):
    # Připojení k PostgreSQL databázi
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Vyhledávací dotaz pro nalezení nejpodobnějších profesí pomocí kosinusové podobnosti
    search_query = f"""
    SELECT
        vm.id,
        vm.pozadovana_profese, 
        vm.profese_cz_isco, 
        ob.nazev AS obec_nazev, 
        ok.nazev AS okres_nazev, 
        kr.nazev AS kraj_nazev,
        vm.nazev_pracoviste, 
        vm.mesicni_mzda_od, 
        vm.mesicni_mzda_do, 
        vm.zamestnavatel_nazev, 
        vm.zamestnavatel_ico, 
        vm.upresnujici_informace, 
        cpv.nazev as pracovne_pravni_vztah_nazev, 
        cvdk.nazev as min_pozadovane_vzdelani_nazev,
        vm.klicova_slova,
        vm.dovednosti,
        (0.5 * (vm.emb_klicova_slova <=> '{query_vector}') + 0.5 * (vm.emb_dovednosti <=> '{query_vector}')) AS weighted_distance,
        COUNT(*) OVER() AS total_count
    FROM 
        search.volna_mista_json AS vm
    LEFT JOIN 
        ruian.rn_obec AS ob ON vm.obec = ob.kod
    LEFT JOIN 
        ruian.rn_okres AS ok ON vm.okres = ok.kod
    LEFT JOIN 
        ruian.rn_vusc AS kr ON vm.kraj = kr.kod
    LEFT JOIN 
        search.cl_pracovnepravni_vztah AS cpv ON vm.pracovne_pravni_vztah = cpv.id
    LEFT JOIN 
        search.cl_vzdelani_detailni_kategorie AS cvdk ON vm.min_pozadovane_vzdelani = cvdk.id
    {get_search_filter_query(searchFilters)}
    ORDER BY weighted_distance
    LIMIT {pageSize}
    OFFSET {page * pageSize};
    """
    
    print(f"Vykonávám SQL dotaz: {search_query}")

    cursor.execute(search_query, (query_vector, pageSize))
    results = cursor.fetchall()
    
    if not results:
        return [], 0
    
    totalCount = results[0][8]
    results = [
        {          
            "id": item[0],
            "pozadovanaProfese": item[1],
            "profeseCzIsco": item[2],
            "obecNazev": item[3],
            "okresNazev": item[4],
            "krajNazev": item[5],
            "nazevPracoviste": item[6],
            "mesicniMzdaOd": item[7],
            "mesicniMzdaDo": item[8],
            "zamestnavatelNazev": item[9],
            "zamestnavatelIco": item[10],
            "upresnujiciInformace": item[11],
            "pracovnePravniVztahNazev": item[12],
            "minPozadovaneVzdelaniNazev": item[13],
            "klicovaSlova": item[14],
            "dovednosti": item[15],
            "distance": item[16]
        }
        for item in results
    ]

    # Uzavření kurzoru a spojení
    cursor.close()
    connection.close()

    return results, totalCount

def get_volne_misto(id):
    # Připojení k PostgreSQL databázi
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Vyhledávací dotaz pro nalezení nejpodobnějších profesí pomocí kosinusové podobnosti
    search_query = f"""
    SELECT
        vm.id,
        vm.pozadovana_profese, 
        vm.profese_cz_isco, 
        ob.nazev AS obec_nazev, 
        ok.nazev AS okres_nazev, 
        kr.nazev AS kraj_nazev,
        vm.nazev_pracoviste, 
        vm.mesicni_mzda_od, 
        vm.mesicni_mzda_do, 
        vm.zamestnavatel_nazev, 
        vm.zamestnavatel_ico, 
        vm.upresnujici_informace, 
        cpv.nazev as pracovne_pravni_vztah_nazev, 
        cvdk.nazev as min_pozadovane_vzdelani_nazev,
        vm.klicova_slova,
        vm.dovednosti
    FROM 
        search.volna_mista_json AS vm
    LEFT JOIN 
        ruian.rn_obec AS ob ON vm.obec = ob.kod
    LEFT JOIN 
        ruian.rn_okres AS ok ON vm.okres = ok.kod
    LEFT JOIN 
        ruian.rn_vusc AS kr ON vm.kraj = kr.kod
    LEFT JOIN 
        search.cl_pracovnepravni_vztah AS cpv ON vm.pracovne_pravni_vztah = cpv.id
    LEFT JOIN 
        search.cl_vzdelani_detailni_kategorie AS cvdk ON vm.min_pozadovane_vzdelani = cvdk.id
    WHERE vm.id = {id};
    """

    cursor.execute(search_query)
    result = cursor.fetchone()
    
    result = {                   
        "id": result[0],
        "pozadovanaProfese": result[1],
        "profeseCzIsco": result[2],
        "obecNazev": result[3],
        "okresNazev": result[4],
        "krajNazev": result[5],
        "nazevPracoviste": result[6],
        "mesicniMzdaOd": result[7],
        "mesicniMzdaDo": result[8],
        "zamestnavatelNazev": result[9],
        "zamestnavatelIco": result[10],
        "upresnujiciInformace": result[11],
        "pracovnePravniVztahNazev": result[12],
        "minPozadovaneVzdelaniNazev": result[13],
        "klicovaSlova": result[14],
        "dovednosti": result[15]
    }

    # Uzavření kurzoru a spojení
    cursor.close()
    connection.close()

    return result

def get_relevantni_kurzy(volne_misto_id, count):
    # Připojení k PostgreSQL databázi
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Vyhledávací dotaz pro nalezení nejpodobnějších profesí pomocí kosinusové podobnosti
    search_query = f"""
        select
            kj.id,
            kj.klicova_slova,
            kj.nazev,
            kj.popis_rekvalifikace,
            kj.dovednosti,
            rvmk.relevance
        from r_volnamista_kurz rvmk
        join volna_mista_json vmj on vmj.id  = rvmk.id_volnemisto
        join kurzy_json kj on kj.id  = rvmk.id_kurz
        where vmj.id = {volne_misto_id}
        order by rvmk.relevance
        LIMIT {count}
    """

    cursor.execute(search_query)
    results = cursor.fetchall()
    
    if not results:
        return []
    
    results = [
        {
            "id": item[0],
            "klicovaSlova": item[1],
            "nazev": item[2],
            "popis": item[3],
            "dovednosti": item[4],
            "relevance": item[5]
        }
        for item in results
    ]

    # Uzavření kurzoru a spojení
    cursor.close()
    connection.close()

    return results

def get_search_filter_query(search_filter):
    # Zavolejte jednotlivé funkce a uložte jejich výsledky
    lokace_query = get_lokace_query(search_filter["lokace"])
    mzda_query = get_mzda_query(search_filter["mzda"])
    vztah_query = get_pracovnepravni_vztah_query(search_filter["pracovnepravni_vztah"])
    vzdelani_query = get_minimalni_stupen_vzdelani_query(search_filter["minimalni_stupen_vzdelani"])
    
    # Filtruje pouze neprázdné výsledky
    query_parts = [query for query in [lokace_query, mzda_query, vztah_query, vzdelani_query] if query]

    # Pokud všechny výsledky jsou prázdné, vrátí prázdný string
    if not query_parts:
        return ""
    
    # Spojuje výsledky pomocí "AND" a přidá "WHERE" na začátek
    return "WHERE " + " AND ".join(query_parts)

def get_lokace_query(search_filter_lokace):
    if not search_filter_lokace:
        return None
    if search_filter_lokace["typ"] == "obec":
        return f"""ob.nazev ILIKE '{search_filter_lokace["nazev"]}' """
    elif search_filter_lokace["typ"] == "okres":
        return f"""ok.nazev ILIKE '{search_filter_lokace["nazev"]}' """
    elif search_filter_lokace["typ"] == "kraj":
        return f"""kr.nazev ILIKE '{search_filter_lokace["nazev"]}' """
    else:
        return None
    
def get_mzda_query(search_filter_mzda):
    if not search_filter_mzda or not search_filter_mzda["castka"]:
        return None
    return f"""vm.mesicni_mzda_od >= {search_filter_mzda["castka"]}"""

def get_pracovnepravni_vztah_query(search_filter_pracovnepravni_vztah):
    if not search_filter_pracovnepravni_vztah:
        return None
    return f"""cpv.nazev ILIKE '{search_filter_pracovnepravni_vztah}' """

def get_minimalni_stupen_vzdelani_query(search_filter_minimalni_stupen_vzdelani):
    if not search_filter_minimalni_stupen_vzdelani:
        return None
    return f"""cvdk.nazev ILIKE '{search_filter_minimalni_stupen_vzdelani}' """