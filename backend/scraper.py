from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import urllib.parse
import base64
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_cache = {
    "data": None,
    "timestamp": 0
}


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()

    # 🟢 CLAVE: headless moderno
    options.add_argument("--headless=new")

    # 🟢 estabilidad en servidores
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # 🟢 importante para páginas pesadas
    options.add_argument("--window-size=1920,1080")

    # 🟢 evitar detección básica
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 🟢 user agent (a veces necesario)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    return driver


def limpiar_canales(canales):
    limpios = {}

    for c in canales:
        nombre = c["nombre"]
        url = c["url"]

        # limpiar nombre
        nombre = nombre.replace("Movil", "").replace("| Móvil", "").strip()

        # usar nombre como clave para evitar duplicados
        limpios[nombre] = {
            "nombre": nombre,
            "url": url
        }

    return list(limpios.values())


def parse_matches_with_channels(html):
    soup = BeautifulSoup(html, "html.parser")

    resultados = []

    for bloque in soup.find_all("li"):
        texto = bloque.get_text(" ", strip=True)

        # 🔥 versión SIMPLE (la que “sí funcionaba”)
        if "vs" not in texto.lower():
            continue

        if len(texto) < 10:
            continue

        hora = None
        for t in bloque.stripped_strings:
            if re.match(r"^\d{2}:\d{2}$", t):
                hora = t
                break

        canales = []

        for a in bloque.find_all("a", href=True):
            nombre = a.get_text(strip=True)
            href = a["href"]

            if "embed/eventos" in href:
                parsed = urllib.parse.urlparse(href)
                params = urllib.parse.parse_qs(parsed.query)

                if "r" in params:
                    encoded = params["r"][0]
                    real_url = decode_url(encoded)

                    canales.append({
                        "nombre": nombre,
                        "url": real_url
                    })

        canales = limpiar_canales(canales)
        texto=limpiar_canales_texto(texto)
        print(texto)
        resultados.append({
            "hora": hora,
            "partido": texto,
            "canales": canales
        })

    return resultados

import re
import re

def limpiar_canales_texto(texto):
    basura = [
        "TyC Sports", "TyC Sports Movil",
        "ESPN", "ESPN2", "ESPN3", "ESPN5",
        "ESPN Movil", "ESPN3 Movil",
        "Disney", "Disney+", "Disney+ Movil",
        "Fox Sports", "Fox Sports 2",
        "DSports", "DSports Movil",
        "beIN Sports", "beIN Sports Ñ",
        "Movil", "Móvil", "FOX", "Deportes", "Universo" 
    ]

    texto_lower = texto.lower()

    # 🔥 buscar primera aparición de cualquier canal
    cut_index = None

    for b in basura:
        idx = texto_lower.find(b.lower())
        if idx != -1:
            if cut_index is None or idx < cut_index:
                cut_index = idx

    # ✂️ cortar todo lo que viene después
    if cut_index is not None:
        texto = texto[:cut_index]

    # limpiar espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto









def decode_url(encoded):
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        return decoded
    except:
        return None

def extraer_get_url(url):
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)

    if "get" in params:
        return params["get"][0]
    
    return url

def limpiar_url(url):
    return extraer_get_url(url)

def limpiar_nombre(nombre):
    nombre = nombre.replace("Movil", "")
    nombre = nombre.replace("| Móvil", "")
    nombre = nombre.replace("|", "")
    nombre = nombre.strip()
    return nombre

def limpiar_data(data):
    resultado = []

    for item in data:
        canales_limpios = {}
        
        for c in item["canales"]:
            nombre = limpiar_nombre(c["nombre"])
            url = limpiar_url(c["url"])

            if nombre:  # evita vacíos
                canales_limpios[nombre] = {
                    "nombre": nombre,
                    "url": url
                }

        resultado.append({
            "hora": item["hora"],
            "partido": item["partido"].strip(),
            "canales": list(canales_limpios.values())
        })

    return resultado


def obtener_partidos():
    global _cache

    # ⏱ cache por 60 segundos
    if _cache["data"] and (time.time() - _cache["timestamp"] < 60):
        print("⚡ usando cache")
        return _cache["data"]

    print("🕸 scrapeando...")

    driver = get_driver()

    try:
        url = "https://futbollibres.com/"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "vs")
        )
        time.sleep(3)  # deja renderizar JS

        html = driver.page_source

        data = parse_matches_with_channels(html)
        data = limpiar_data(data)
        if not data:
            print("ℹ️ No hay partidos en este momento")
            return []
        # 💾 guardar cache
        _cache["data"] = data
        _cache["timestamp"] = time.time()

        return data

    finally:
        driver.quit()





import requests
from bs4 import BeautifulSoup

def get_html_without_selenium():
    url = "https://futbollibres.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    return response.text
