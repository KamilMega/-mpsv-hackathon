from flask import Flask, request, jsonify
import json
from src.utils.api_utils import generate_vector, get_search_text_keywords_from_gpt, translate_to_hantec_using_gpt, translate_from_hantec_using_gpt
from src.utils.postgre_utils import search_volna_mista, get_volne_misto, get_relevantni_kurzy
from src.utils.string_utils import trim_string_array
from src.utils.rest_utils import convert_extracted_search_filter
import logging
import traceback
import time

# Inicializace Flask aplikace
app = Flask(__name__)

# Nastavení logovací úrovně
app.logger.setLevel(logging.INFO)
# app.logger.info(f"Test 123")

# Nastavení loggeru pro Flask
handler = logging.StreamHandler()
app.logger.addHandler(handler)

@app.errorhandler(Exception)
def handle_exception(e):
    # Zaloguj celý traceback do logu Flasku
    app.logger.error(f"Exception occurred: {str(e)}", exc_info=True)

    # Vrátit uživateli standardní odpověď s chybou
    return jsonify({"error": "An internal error occurred."}), 500


@app.route('/search', methods=['GET'])
def api_search():
    search_text = request.args.get('query')
    page = request.args.get('page', default=0, type=int)
    pageSize = request.args.get('pageSize', default=50, type=int)
    
    # pracovnepravni_vztah = request.args.get('pracovnepravniVztah')
    # minimalni_stupen_vzdelani = request.args.get('minimalniStupenVzdelani')
    # mzda_castka = request.args.get('mzdaCastka')
    # lokace_nazev = request.args.get('lokaceNazev')
    # lokace_typ = request.args.get('lokaceTyp')

    if not search_text:
        return jsonify({"error": "search_text is required"}), 400
    
    hantec = "brn" in search_text
    
    if hantec:
        search_text = translate_from_hantec_using_gpt(search_text)

    try:
        extractedPrompt = get_search_text_keywords_from_gpt(search_text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    descriptor = ",".join(extractedPrompt["descriptors"])
    vector = generate_vector(descriptor)

    if vector is None:
        return jsonify({"error": "Unable to generate vector from keywords"}), 500

    # search_filter = {}
    # if extractedPrompt["searchFilters"]["pracovnepravni_vztah"]:
    #     search_filter["pracovnepravni_vztah"] = extractedPrompt["searchFilters"]["pracovnepravni_vztah"]
    # if pracovnepravni_vztah:
    #     search_filter["pracovnepravni_vztah"] = pracovnepravni_vztah
    
    # if extractedPrompt["searchFilters"]["minimalni_stupen_vzdelani"]:
    #     search_filter["minimalni_stupen_vzdelani"] = extractedPrompt["searchFilters"]["minimalni_stupen_vzdelani"]   
    # if minimalni_stupen_vzdelani:
    #     search_filter["minimalni_stupen_vzdelani"] = minimalni_stupen_vzdelani
    
    # if extractedPrompt["searchFilters"]["mzda"]
    #     search_filter["mzda"] = []
    #     search_filter["mzda"]["castka"] = mzda_castka
    #     search_filter["minimalni_stupen_vzdelani"] = extractedPrompt["searchFilters"]["minimalni_stupen_vzdelani"]  
    # search_filter["mzda"] = {}
    # if mzda_castka:
    #     search_filter["mzda"]["castka"] = mzda_castka
    
    # search_filter["lokace"] = {}
    # if lokace_nazev:
    #     search_filter["lokace"]["nazev"] = lokace_nazev
    #     search_filter["lokace"]["typ"] = lokace_typ

    results, totalCount = search_volna_mista(vector, page, pageSize, extractedPrompt["search_filters"])

    for result in results:
        result["doporuceneKurzy"] = get_relevantni_kurzy(result["id"], 3)

    if hantec:
        small_results = []

        # Zpracování pole `results`
        for result in results:
            # Zkopírujeme hodnotu `pozadovanaProfese`
            pozadovana_profese = result.get("pozadovanaProfese", "")
            
            # Zkopírujeme názvy kurzů z `doporuceneKurzy`
            doporucene_kurzy = [{"nazev": kurz.get("nazev", "")} for kurz in result.get("doporuceneKurzy", [])]
            
            # Přidáme do `small_results` s požadovanou strukturou
            small_results.append({
                "pozadovanaProfese": pozadovana_profese,
                "doporuceneKurzy": doporucene_kurzy
            })
        
        small_results = translate_to_hantec_using_gpt(small_results)
        
        for i, result in enumerate(results):
            if i < len(small_results):
                # Překopírování hodnoty `pozadovanaProfese`
                result["pozadovanaProfese"] = small_results[i].get("pozadovanaProfese", "")
                
                # Aktualizace pouze hodnoty `nazev` v každém kurzu
                for j, kurz in enumerate(result.get("doporuceneKurzy", [])):
                    if j < len(small_results[i]["doporuceneKurzy"]):
                        kurz["nazev"] = small_results[i]["doporuceneKurzy"][j].get("nazev", "")

    return jsonify({
        "totalCount": totalCount,
        "results": results,
        "searchFilters": extractedPrompt["search_filters"],
        "searchText": search_text,
        "searchDescriptors": extractedPrompt["descriptors"],
        "hantec": hantec
        })

@app.route('/volna-mista/<int:id>', methods=['GET'])
def api_get_volne_misto(id):
    result = get_volne_misto(id)
    
    if result:
        result["doporuceneKurzy"] = get_relevantni_kurzy(result["id"], 10)
    
    return jsonify(result)


# Spuštění Flask aplikace
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    