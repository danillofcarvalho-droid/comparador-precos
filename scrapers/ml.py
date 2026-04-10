import requests
from bs4 import BeautifulSoup

def coletar_preco_ml(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Esta é a forma mais estável: buscar a meta tag de preço
        meta_preco = soup.find("meta", itemprop="price")
        if meta_preco:
            return float(meta_preco["content"])
            
        # Plano B se a meta tag falhar
        preco_frac = soup.find("span", class_="andes-money-amount__fraction")
        if preco_frac:
            return float(preco_frac.get_text().replace(".", ""))
            
        return None
    except:
        return None