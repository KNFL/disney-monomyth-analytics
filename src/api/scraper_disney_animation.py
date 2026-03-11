# STEP 1 request films page
# STEP 2 parse html
# STEP 3 find film containers
# STEP 4 extract title and year
# STEP 5 build list of dictionaries
# STEP 6 return dataset

import requests
from bs4 import BeautifulSoup
import json
import os
from dateutil import parser
import unicodedata
import re

URL = "https://disneyanimation.com/films/"

def clean_date(date_text):
    """Convertir fechas a formato ISO: YYYY-MM-DD"""
    try:
        dt = parser.parse(date_text)
        return dt.date().isoformat()
    except:
        return ""

def normalize_title(title):
    """Normalizar título para evitar errores de texto"""
    title = unicodedata.normalize("NFKC", title)
    return " ".join(title.strip().split())

def create_film_id(title, year):
    """Crear ID único para cada película"""

    # normalizar texto
    title = unicodedata.normalize("NFKD", title)

    # minúsculas
    title = title.lower()

    # reemplazar caracteres no alfanuméricos
    title = re.sub(r"[^a-z0-9]+", "_", title)

    # quitar underscores al inicio o final
    title = title.strip("_")

    film_id = f"disney_animation_{title}_{year}"

    return film_id

def get_films_page():
    """Download the films page"""
    
    response = requests.get(URL)
    
    if response.status_code != 200:
        raise Exception("Failed to load page")
    
    return response.text


def parse_films(html):
    """Parse films from html"""
    
    soup = BeautifulSoup(html, "html.parser")
    
    films = []
    
    BASE_URL = "https://disneyanimation.com"
    
    film_cards = soup.find_all("figcaption")
    
    for card in film_cards:

        title_tag = card.find("h4")
        year_tag = card.find("p")
        link_tag = card.find("a")

        if not title_tag or not year_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        year = year_tag.get_text(strip=True)
        link = BASE_URL + link_tag["href"]

        film = {
            "title": title,
            "year": year,
            "url": link
        }

        films.append(film)
    
    return films

def scrape_film_details(film):

    url = film["url"]
    response = requests.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    # normalizar título
    film["title"] = normalize_title(film["title"])

    # extraer sinopsis
    synopsis_tag = soup.select_one("div.col-md-7 p")

    if synopsis_tag:
        film["synopsis"] = synopsis_tag.get_text(strip=True)
    else:
        film["synopsis"] = ""

    # extraer release date
    release_label = soup.find("strong", string=lambda s: s and "Release Date" in s)

    if release_label:

        container = release_label.find_parent("div")
        date_tag = container.find("p")

        if date_tag:
            raw_date = date_tag.get_text(strip=True)
            film["release_date"] = clean_date(raw_date)   # ← limpieza
        else:
            film["release_date"] = ""

    else:
        film["release_date"] = ""

    return film
def save_films(films):

    with open("data_raw/disney_animation_films.json", "w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=4)
        
def load_existing_films():

    path = "data_raw/disney_animation_films.json"

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_date(txt):
    try:
        dt = parser.parse(txt, dayfirst=False)  # acepta muchos formatos
        return dt.date().isoformat()  # 'YYYY-MM-DD'
    except Exception:
        return None

def normalize_title(t):
    t = t.strip()
    t = unicodedata.normalize("NFKC", t)
    return " ".join(t.split())  # quita espacios extra

def main():

    # 1 descargar página de Disney Animation
    html = get_films_page()

    # 2 extraer lista básica de películas
    films = parse_films(html)

    # 3 cargar dataset existente
    existing_films = load_existing_films()

    # 4 crear conjunto de URLs ya procesadas
    existing_urls = {film["url"] for film in existing_films}

    new_films = []

    # 5 procesar solo películas nuevas
    for film in films:
        
        film["title"] = normalize_title(film["title"])
        
        # crear ID único
        film["film_id"] = create_film_id(film["title"], film["year"])

        if film["url"] in existing_urls:
            continue

        print(f"Scraping new film: {film['title']}")

        film = scrape_film_details(film)

        new_films.append(film)

    # 6 combinar datasets
    updated_dataset = existing_films + new_films

    # 7 guardar dataset actualizado
    save_films(updated_dataset)

    print(f"New films added: {len(new_films)}")
    print(f"Total films in dataset: {len(updated_dataset)}")



if __name__ == "__main__":
    main()