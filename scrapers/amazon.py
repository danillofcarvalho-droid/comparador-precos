import requests
from bs4 import BeautifulSoup

def coletar_preco_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tentativa 1: Preço padrão
        preco = soup.find("span", class_="a-price-whole")
        
        # Tentativa 2: Preço em oferta ou mobile
        if not preco:
            preco = soup.select_one(".a-price .a-offscreen") or \
                    soup.select_one("#price_inside_buybox")
        
        if preco:
            # Limpeza robusta: tira R$, pontos, espaços e vírgulas
            texto = preco.get_text().replace("R$", "").replace(".", "").replace(",", ".").strip()
            return float(texto)
        return None
    except:
        return None