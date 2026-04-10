import requests
from bs4 import BeautifulSoup

def coletar_preco_amazon(url):
    # Headers mais completos para simular um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # A Amazon muda as IDs de preço frequentemente. Vamos tentar as 3 mais comuns:
        preco_tag = soup.find("span", class_="a-price-whole") or \
                    soup.find("span", id="priceblock_ourprice") or \
                    soup.find("span", id="priceblock_dealprice")
        
        if preco_tag:
            # Remove pontos de milhar e converte para float
            preco_texto = preco_tag.get_text().replace(".", "").replace(",", ".")
            return float(preco_texto)
        return None
    except:
        return None