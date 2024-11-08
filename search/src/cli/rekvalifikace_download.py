import requests
import json

# URL endpoint pro POST požadavek
url = "https://www.uradprace.cz/api/rekvalifikace/rest/kurz/query-ex"

# Tělo POST požadavku (JSON data)
post_data = {
    "optKurzIds": False,
    "optDruhKurzu": False,
    "optNazevKurzu": False,
    "optKodKurzu": False,
    "optStavKurzu": False,
    "optStavZajmu": False,
    "optNazevVzdelavatele": False,
    "optIcoVzdelavatele": False,
    "optKategorie": False,
    "optAkreditace": False,
    "pagination": {
        "start": 0,
        "count": 2000,
        "order": [
            "-id"
        ]
    },
    "optFormaVzdelavaniIds": False,
    "optTermin": False,
    "optCena": False,
    "optJazykIds": False,
    "optMistoKonani": False,
    "optTypKurzuIds": False
}

# Hlavičky požadavku
headers = {
    "Content-Type": "application/json"
}

# Odeslání POST požadavku
response = requests.post(url, headers=headers, json=post_data)

# Kontrola, zda byl požadavek úspěšný
if response.status_code == 200:
    # Převést odpověď na JSON
    data = response.json()

    # Uložit data do souboru ve formátu JSON
    with open("Data/kurzy.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Data byla úspěšně uložena do souboru 'kurzy.json'.")
else:
    print(f"Chyba při stahování dat: {response.status_code}")
