import requests
from bs4 import BeautifulSoup

def coletar_preco_ml(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        sopa = BeautifulSoup(res.text, 'html.parser')
        
        # O "Pulo do Gato": buscar na tag <meta> que é padrão de SEO
        meta_preco = sopa.find("meta", itemprop="price")
        if meta_preco:
            return float(meta_preco["content"])
            
        # Backup caso a meta tag falhe (seletor comum)
        preco_tag = sopa.select_one('.ui-pdp-price__second-line .andes-money-amount__fraction')
        if preco_tag:
            return float(preco_tag.get_text().replace(".", ""))
            
        return None
    except:
        return None