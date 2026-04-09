import requests
from bs4 import BeautifulSoup

def coletar_preco_ml(url_ml):
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        resposta = requests.get(url_ml, headers=cabecalho, timeout=10)
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # O Mercado Livre costuma usar a classe 'andes-money-amount__fraction'
        elemento_preco = sopa.find("span", class_="andes-money-amount__fraction")

        if elemento_preco:
            # Remove pontos de milhar para não quebrar o float
            preco_texto = elemento_preco.text.replace('.', '').strip()
            return float(preco_texto)
        
        return None

    except Exception as e:
        print(f"❌ Erro no Mercado Livre: {e}")
        return None