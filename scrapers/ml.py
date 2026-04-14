import requests
from bs4 import BeautifulSoup

def coletar_preco_ml(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        sopa = BeautifulSoup(res.text, 'html.parser')
        
        # O ML usa uma meta tag específica que é infalível
        meta_preco = sopa.find("meta", itemprop="price")
        if meta_preco:
            return float(meta_preco["content"])
            
        return None
    except:
        return None