import requests
from src.config import AZURE_API_KEY, AZURE_ENDPOINT, AZURE_EMBEDDING_DEPLOYMENT_ID, AZURE_GPT_DEPLOYMENT_ID
from src.utils.prompt import query_extraction_system_prompt, query_extraction_user_prompt
from src.utils.extract_utils import extract_skills_and_descriptors
import json

# Funkce pro generování embeddingu pomocí Azure OpenAI API
def generate_vector(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    data = {
        "input": text
    }

    response = requests.post(
        f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_EMBEDDING_DEPLOYMENT_ID}/embeddings?api-version=2023-05-15",
        headers=headers,
        json=data
    )

    if 'data' in response.json():
        embedding = response.json()['data'][0]['embedding']
        return embedding if isinstance(embedding, list) and len(embedding) > 0 else None
    else:
        raise ValueError(f"Odpověď z API neobsahuje klíč 'data' pro '{text}'.")

# Funkce pro získání klíčových slov pomocí GPT-4o-mini
def get_keywords_from_gpt(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Tento model extrahuje klíčová slova z textu."
            },
            {
                "role": "user",
                "content": f"Vypiš klíčová slova pro text: {text}"
            }
        ]
    }

    response = requests.post(
        f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_GPT_DEPLOYMENT_ID}/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        json=data
    )
    try:
        keywords = response.json()['choices'][0]['message']['content']
        return keywords
    except Exception as e:
        # V případě chyby nastavíme klíčová slova na "error"
        print(f"ID: Chyba při získávání klíčových slov: {e}")
        return response.json()['choices'][0]['message']['content']

def get_search_text_keywords_from_gpt(text):
    result = extract_skills_and_descriptors(query_extraction_system_prompt, query_extraction_user_prompt, text, "")
    print(f"{result}")
    return result

def translate_from_hantec_using_gpt(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Tento model překládá přehnaný brněnský hantec do češtiny za účelem vyhledání volného pracovního místa."
            },
            {
                "role": "user",
                "content": f"""
                Níže uvedený text může být v češtině, nebo v přehnaném brněnském hantecu. Pokud by byl v brněnském hantecu, tak jej nejdříve přelož do češtiny.
                Vstupní hantec bude přehnaně vtipný. Budeš ho muset převést tak, aby text byl normální.
                V níže uvedeném textu je uveden popis hledané profese v lidském jazyce.
                Zkus z popisu uhodnout název pozice a dodej 3 klíčová slova, která by název mohl obsahovat.
                Na základě textu vypiš čárkou oddělený tipovaný název profese a klíčová slova, která by nejlépe umožnila vyhledat profesi v databázi profesí podle jejího názvu.
                Text může obsahovat upřesnění požadované mzdy, místa výkonu, pracovního poměru. Ty přidej do výstupu taktéž
                Příklad vstupu: "Tož chtěl bych lidem kókat do hlavy a řešit jejich problémy s madr minimálně za 50000 kaček v brně"
                Příklad výstupu: "psycholog, terapie, traumata, minimálně za 50000 kč v brně"

                Text:
                 {text}
                """
            }
        ]
    }

    response = requests.post(
        f"{AZURE_ENDPOINT}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        json=data
    )

    return response.json()['choices'][0]['message']['content']

def trim_string_array(input_str):
    start_index = input_str.find("[")
    end_index = input_str.rfind("]")

    # Zkontrolujeme, zda znaky "[" a "]" existují v řetězci
    if start_index != -1 and end_index != -1 and end_index > start_index:
        return input_str[start_index:end_index+1]  # Vracíme podřetězec včetně []
    else:
        return []

def translate_to_hantec_using_gpt(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Tento model obohacuje vstupní json o brněnský hantec."
            },
            {
                "role": "user",
                "content": f"""
                    Na vstupu máš JSON, který obsahuje data s volnými pracovními pozicemi a rekvalifikačními kurzy.

                    Proveď překlad JSONu podle následujících instrukcí:
                    - Neměň strukturu JSON, budeš měnit pouze hodnoty atributů pozadovanaProfese a doporuceneKurzy.nazev
                    - Vytvoř vtipný překlad hodnot uvedených atributů do brněnského hantecu a hodnoty nahraď.
                    - Snaž se být co nejvtipnější, klidně i přeháněj. Humor může být nekorektní, pokud to bude vtipné a neformální, jako typický hantec.
                    - Pokud dává smysl, zapoj do názvu související neoblíbené české politiky nebo události z Brna.

                    JSON:
                    {text}
                """
            }
        ]
    }

    response = requests.post(
        f"{AZURE_ENDPOINT}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        json=data
    )

    json_string = trim_string_array(response.json()['choices'][0]['message']['content'])
    print(f"{json_string}")
    return json.loads(json_string)




